import datetime
import json
import logging

from django.apps import apps
from django.conf import settings
from django.utils.timezone import now

from mayan.apps.acls.models import AccessControlList

from ..permissions import permission_workflow_instance_transition

logger = logging.getLogger(name=__name__)


class WorkflowInstanceBusinessLogicMixin:
    def check_escalation(self):
        current_state = self.get_current_state()

        for escalation in current_state.escalations.filter(enabled=True):
            timedelta = datetime.timedelta(
                **{
                    escalation.unit: escalation.amount
                }
            )

            if now() > self.get_last_log_entry_datetime() + timedelta:
                condition_context = {'workflow_instance': self}

                if escalation.evaluate_condition(context=condition_context):
                    self.do_transition(
                        transition=escalation.transition,
                        comment=escalation.get_comment()
                    )

    def do_transition(
        self, transition, comment=None, extra_data=None, user=None
    ):
        WorkflowInstanceLogEntry = apps.get_model(
            app_label='document_states', model_name='WorkflowInstanceLogEntry'
        )

        try:
            if transition in self.get_transition_choices(user=user).all():
                if extra_data:
                    context = self.loads()
                    context.update(extra_data)
                    self.dumps(context=context)

                workflow_instance_log_entry = WorkflowInstanceLogEntry(
                    comment=comment or '',
                    extra_data=json.dumps(
                        obj=extra_data or {}
                    ),
                    transition=transition, user=user,
                    workflow_instance=self
                )
                workflow_instance_log_entry._event_actor = user
                workflow_instance_log_entry.save()
                return workflow_instance_log_entry
        except AttributeError:
            # No initial state has been set for this workflow.
            if settings.DEBUG:
                raise

    def dumps(self, context):
        """
        Serialize the context data.
        """
        self.context = json.dumps(obj=context)
        self.save()

    def get_context(self):
        # Keep the document instance in the workflow instance fresh when
        # there are cascade state actions, where a second state action is
        # triggered by the events generated by a first state action.
        self.document.refresh_from_db()
        context = {
            'workflow_instance': self
        }
        context['workflow_instance_context'] = self.loads()
        return context

    def get_current_state(self):
        """
        Actual State - The current state of the workflow. If there are
        multiple states available, for example: registered, approved,
        archived; this field will tell at the current state where the
        document is right now.
        """
        last_transition = self.get_last_transition()
        if last_transition:
            return last_transition.destination_state
        else:
            return self.workflow.get_initial_state()

    def get_last_log_entry(self):
        return self.log_entries.order_by('datetime').last()

    def get_last_log_entry_datetime(self):
        last_log_entry = self.get_last_log_entry()
        if last_log_entry:
            return last_log_entry.datetime
        else:
            return self.datetime

    def get_last_transition(self):
        """
        Last Transition - The last transition used by the last user to put
        the document in the actual state.
        """
        last_log_entry = self.get_last_log_entry()
        if last_log_entry:
            return last_log_entry.transition

    def get_runtime_context(self):
        """
        Alias of self.load() to get just the runtime context of the instance
        for ease of use in the condition template.
        """
        return self.loads()

    def get_transition_choices(self, user=None):
        WorkflowTransition = apps.get_model(
            app_label='document_states', model_name='WorkflowTransition'
        )

        current_state = self.get_current_state()

        if current_state:
            queryset = current_state.origin_transitions.all()

            if user:
                queryset = AccessControlList.objects.restrict_queryset(
                    permission=permission_workflow_instance_transition,
                    queryset=queryset, user=user
                )

            # Remove the transitions with a false return value.
            for entry in queryset:
                if not entry.evaluate_condition(workflow_instance=self):
                    queryset = queryset.exclude(id=entry.pk)

            return queryset
        else:
            """
            This happens when a workflow has no initial state and a document
            whose document type has this workflow is created. We return an
            empty transition queryset.
            """
            return WorkflowTransition.objects.none()

    def loads(self):
        """
        Deserialize the context data.
        """
        return json.loads(s=self.context or '{}')


class WorkflowInstanceLogEntryBusinessLogicMixin:
    def get_extra_data(self):
        WorkflowTransitionField = apps.get_model(
            app_label='document_states', model_name='WorkflowTransitionField'
        )

        result = {}
        for key, value in self.loads().items():
            try:
                field = self.transition.fields.get(name=key)
            except WorkflowTransitionField.DoesNotExist:
                """
                There is a reference for a field that does not exist or
                has been deleted.
                """
            else:
                result[field.label] = value

        return result

    def loads(self):
        """
        Deserialize the context data.
        """
        return json.loads(s=self.extra_data or '{}')
