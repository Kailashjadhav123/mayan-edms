from ..classes import Worker, CeleryQueue

from .literals import TEST_QUEUE_LABEL, TEST_QUEUE_NAME, TEST_WORKER_NAME


class TaskManagerTestMixin:
    def setUp(self):
        super().setUp()
        self._test_queue_list = []
        self._test_worker_list = []

    def tearDown(self):
        for test_queue in self._test_queue_list:
            test_queue.remove()

    def _create_test_queue(self, label=None, name=None):
        total_test_queue_list = len(self._test_queue_list)
        label = label or '{}_{}'.format(
            TEST_QUEUE_LABEL, total_test_queue_list
        )
        name = name or '{}_{}'.format(TEST_QUEUE_NAME, total_test_queue_list)

        self._test_queue = CeleryQueue(
            label=label, name=name, worker=self._test_worker
        )
        self._test_queue_list.append(self._test_queue)

    def _create_test_worker(self):
        self._test_worker = Worker(name=TEST_WORKER_NAME)
        self._test_worker_list.append(self._test_worker)


class TaskManagerViewTestMixin:
    def _request_queue_list(self):
        return self.get(
            viewname='task_manager:queue_list', follow=True
        )
