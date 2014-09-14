from __future__ import absolute_import

import logging

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.translation import ugettext_lazy as _

from acls.models import AccessEntry
from acls.utils import apply_default_acls
from acls.views import acl_list_for
from common.utils import encapsulate
from common.views import SingleObjectListView
from documents.permissions import PERMISSION_DOCUMENT_VIEW
from documents.models import Document
from documents.views import DocumentListView
from permissions.models import Permission

from .forms import FolderForm, FolderListForm
from .models import Folder
from .permissions import (PERMISSION_FOLDER_CREATE,
    PERMISSION_FOLDER_EDIT, PERMISSION_FOLDER_DELETE,
    PERMISSION_FOLDER_REMOVE_DOCUMENT, PERMISSION_FOLDER_VIEW,
    PERMISSION_FOLDER_ADD_DOCUMENT)

logger = logging.getLogger(__name__)


class FolderListView(SingleObjectListView):
    model =  Folder
    object_permission = PERMISSION_FOLDER_VIEW

    def get_extra_context(self):
        return {
            'title': _(u'folders'),
            'multi_select_as_buttons': True,
            'extra_columns': [
                {'name': _(u'Created'), 'attribute': 'datetime_created'},
                {'name': _(u'Documents'), 'attribute': encapsulate(lambda x: x.documents.count())}
            ],
            'hide_link': True,
        }


def folder_create(request):
    Permission.objects.check_permissions(request.user, [PERMISSION_FOLDER_CREATE])

    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder, created = Folder.objects.get_or_create(user=request.user, title=form.cleaned_data['title'])
            if created:
                apply_default_acls(folder, request.user)
                messages.success(request, _(u'Folder created successfully'))
                return HttpResponseRedirect(reverse('folders:folder_list'))
            else:
                messages.error(request, _(u'A folder named: %s, already exists.') % form.cleaned_data['title'])
    else:
        form = FolderForm()

    return render_to_response('main/generic_form.html', {
        'title': _(u'create folder'),
        'form': form,
    },
    context_instance=RequestContext(request))


def folder_edit(request, folder_id):
    folder = get_object_or_404(Folder, pk=folder_id)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_FOLDER_EDIT])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_FOLDER_EDIT, request.user, folder)

    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder.title = form.cleaned_data['title']
            try:
                folder.save()
                messages.success(request, _(u'Folder edited successfully'))
                return HttpResponseRedirect(reverse('folders:folder_list'))
            except Exception as exception:
                messages.error(request, _(u'Error editing folder; %s') % exception)
    else:
        form = FolderForm(instance=folder)

    return render_to_response('main/generic_form.html', {
        'title': _(u'edit folder: %s') % folder,
        'form': form,
        'object': folder,
        'object_name': _(u'folder'),
    },
    context_instance=RequestContext(request))


def folder_delete(request, folder_id):
    folder = get_object_or_404(Folder, pk=folder_id)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_FOLDER_DELETE])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_FOLDER_DELETE, request.user, folder)

    post_action_redirect = reverse('folders:folder_list')

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        try:
            folder.delete()
            messages.success(request, _(u'Folder: %s deleted successfully.') % folder)
        except Exception as exception:
            messages.error(request, _(u'Folder: %(folder)s delete error: %(error)s') % {
                'folder': folder, 'error': exception})

        return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'folder'),
        'delete_view': True,
        'previous': previous,
        'next': next,
        'object': folder,
        'title': _(u'Are you sure you with to delete the folder: %s?') % folder,
        'form_icon': u'folder_delete.png',
    }

    return render_to_response('main/generic_confirm.html', context,
        context_instance=RequestContext(request))


class FolderDetailView(DocumentListView):
    def get_folder(self):
        folder = get_object_or_404(Folder, pk=self.kwargs['pk'])

        try:
            Permission.objects.check_permissions(self.request.user, [PERMISSION_FOLDER_VIEW])
        except PermissionDenied:
            AccessEntry.objects.check_access(PERMISSION_FOLDER_VIEW, self.request.user, folder)

        return folder

    def get_queryset(self):
        return self.get_folder().documents

    def get_extra_context(self):
        return {
            'title': _(u'Documents in folder: %s') % self.get_folder(),
            'hide_links': True,
            'multi_select_as_buttons': True,
            'object': self.get_folder(),
            'object_name': _(u'folder'),
        }


def folder_add_document(request, document_id=None, document_id_list=None):

    if document_id:
        documents = [get_object_or_404(Document, pk=document_id)]
    elif document_id_list:
        documents = [get_object_or_404(Document, pk=document_id) for document_id in document_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_FOLDER_ADD_DOCUMENT])
    except PermissionDenied:
        documents = AccessEntry.objects.filter_objects_by_access(PERMISSION_FOLDER_ADD_DOCUMENT, request.user, documents)

    post_action_redirect = None
    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        form = FolderListForm(request.POST, user=request.user)
        if form.is_valid():
            folder = form.cleaned_data['folder']
            for document in documents:
                if folder.add_document(document):
                    messages.success(request, _(u'Document: %(document)s added to folder: %(folder)s successfully.') % {
                        'document': document, 'folder': folder})
                else:
                    messages.warning(request, _(u'Document: %(document)s is already in folder: %(folder)s.') % {
                        'document': document, 'folder': folder})

            return HttpResponseRedirect(next)
    else:
        form = FolderListForm(user=request.user)

    context = {
        'object_name': _(u'document'),
        'form': form,
        'previous': previous,
        'next': next,
    }

    if len(documents) == 1:
        context['object'] = documents[0]
        context['title'] = _(u'Add document: %s to folder.') % documents[0]
    elif len(documents) > 1:
        context['title'] = _(u'Add documents: %s to folder.') % ', '.join([unicode(d) for d in documents])

    return render_to_response('main/generic_form.html', context,
        context_instance=RequestContext(request))


def document_folder_list(request, document_id):
    document = get_object_or_404(Document, pk=document_id)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_DOCUMENT_VIEW])
    except PermissionDenied:
        AccessEntry.objects.check_access(PERMISSION_DOCUMENT_VIEW, request.user, document)

    context = {
        'title': _(u'Folders containing: %s') % document,
        'object': document,
        'multi_select_as_buttons': True,
        'extra_columns': [
            {'name': _(u'Created'), 'attribute': 'datetime_created'},
            {'name': _(u'Documents'), 'attribute': encapsulate(lambda x: x.documents.count())}
        ],
        'hide_link': True,
        }

    queryset=Folder.objects.filter(folderdocument__document=document)

    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_FOLDER_VIEW])
    except PermissionDenied:
        queryset = AccessEntry.objects.filter_objects_by_access(PERMISSION_FOLDER_VIEW, request.user, queryset)

    context['object_list'] = queryset

    return render_to_response('main/generic_list.html', context,
        context_instance=RequestContext(request))


def folder_document_remove(request, folder_id, document_id=None, document_id_list=None):
    post_action_redirect = None

    folder = get_object_or_404(Folder, pk=folder_id)

    if document_id:
        folder_documents = [get_object_or_404(Document, pk=document_id)]
    elif document_id_list:
        folder_documents = [get_object_or_404(Document, pk=document_id) for document_id in document_id_list.split(',')]
    else:
        messages.error(request, _(u'Must provide at least one folder document.'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    logger.debug('folder_documents (pre permission check): %s' % folder_documents)
    try:
        Permission.objects.check_permissions(request.user, [PERMISSION_FOLDER_REMOVE_DOCUMENT])
    except PermissionDenied:
        folder_documents = AccessEntry.objects.filter_objects_by_access(PERMISSION_FOLDER_REMOVE_DOCUMENT, request.user, folder_documents, exception_on_empty=True)

    logger.debug('folder_documents (post permission check): %s' % folder_documents)

    previous = request.POST.get('previous', request.GET.get('previous', request.META.get('HTTP_REFERER', '/')))
    next = request.POST.get('next', request.GET.get('next', post_action_redirect if post_action_redirect else request.META.get('HTTP_REFERER', '/')))

    if request.method == 'POST':
        for folder_document in folder_documents:
            try:
                folder.remove_document(folder_document)
                messages.success(request, _(u'Document: %s removed successfully.') % folder_document)
            except Exception as exception:
                messages.error(request, _(u'Document: %(document)s delete error: %(error)s') % {
                    'document': folder_document, 'error': exception})

        return HttpResponseRedirect(next)

    context = {
        'object_name': _(u'folder document'),
        'previous': previous,
        'next': next,
        'form_icon': u'delete.png',
        'object': folder
    }
    if len(folder_documents) == 1:
        context['object'] = folder_documents[0]
        context['title'] = _(u'Are you sure you wish to remove the document: %(document)s from the folder "%(folder)s"?') % {
            'document': ', '.join([unicode(d) for d in folder_documents]), 'folder': folder}
    elif len(folder_documents) > 1:
        context['title'] = _(u'Are you sure you wish to remove the documents: %(documents)s from the folder "%(folder)s"?') % {
            'documents': ', '.join([unicode(d) for d in folder_documents]), 'folder': folder}

    return render_to_response('main/generic_confirm.html', context,
        context_instance=RequestContext(request))


def folder_document_multiple_remove(request, folder_id):
    return folder_document_remove(request, folder_id, document_id_list=request.GET.get('id_list', []))


def folder_acl_list(request, folder_pk):
    folder = get_object_or_404(Folder, pk=folder_pk)
    logger.debug('folder: %s' % folder)

    return acl_list_for(
        request,
        folder,
        extra_context={
            'object': folder,
        }
    )


def folder_add_multiple_documents(request):
    return folder_add_document(
        request, document_id_list=request.GET.get('id_list', [])
    )
