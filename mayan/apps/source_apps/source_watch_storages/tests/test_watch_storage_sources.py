from pathlib import Path
import shutil

from mayan.apps.documents.models import Document
from mayan.apps.documents.tests.base import GenericDocumentTestCase
from mayan.apps.documents.tests.literals import (
    TEST_FILE_NON_ASCII_FILENAME,
    TEST_FILE_NON_ASCII_COMPRESSED_PATH, TEST_DOCUMENT_SMALL_CHECKSUM,
    TEST_FILE_SMALL_PATH
)
from mayan.apps.source_apps.sources.source_backends.literals import SOURCE_UNCOMPRESS_CHOICE_ALWAYS

from .mixins import WatchStorageSourceTestMixin


class WatchStorageSourceBackendTestCase(
    WatchStorageSourceTestMixin, GenericDocumentTestCase
):
    auto_create_test_source = False
    auto_upload_test_document = False

    def test_exclude_regular_expression(self):
        path = Path(TEST_FILE_SMALL_PATH)

        self._create_test_watch_storage(
            extra_data={'exclude_regex': path.name}
        )

        document_count = Document.objects.count()

        shutil.copy(
            src=TEST_FILE_SMALL_PATH,
            dst=self._test_source._test_temporary_folder
        )

        self._test_source.get_backend_instance().process_documents()

        self.assertEqual(Document.objects.count(), document_count)

        backend_data = self._test_source.get_backend_data()
        backend_data['exclude_regex'] = ''
        self._test_source.set_backend_data(obj=backend_data)

        self._test_source.get_backend_instance().process_documents()

        self.assertEqual(Document.objects.count(), document_count + 1)

    def test_include_regular_expression(self):
        path = Path(TEST_FILE_SMALL_PATH)

        self._create_test_watch_storage(
            extra_data={'include_regex': '_____.*'}
        )

        document_count = Document.objects.count()

        shutil.copy(
            src=TEST_FILE_SMALL_PATH,
            dst=self._test_source._test_temporary_folder
        )

        self._test_source.get_backend_instance().process_documents()

        self.assertEqual(Document.objects.count(), document_count)

        backend_data = self._test_source.get_backend_data()
        backend_data['include_regex'] = path.name
        self._test_source.set_backend_data(obj=backend_data)

        self._test_source.get_backend_instance().process_documents()

        self.assertEqual(Document.objects.count(), document_count + 1)

    def test_upload_simple_file(self):
        self._create_test_watch_storage()

        document_count = Document.objects.count()

        shutil.copy(
            src=TEST_FILE_SMALL_PATH,
            dst=self._test_source._test_temporary_folder
        )

        self._test_source.get_backend_instance().process_documents()

        self.assertEqual(Document.objects.count(), document_count + 1)
        self.assertEqual(
            Document.objects.first().file_latest.checksum,
            TEST_DOCUMENT_SMALL_CHECKSUM
        )

    def test_non_ascii_file_in_non_ascii_compressed_file(self):
        """
        Test Non-ASCII named documents inside Non-ASCII named compressed
        file. GitHub issue #163.
        """
        self._create_test_watch_storage(
            extra_data={'uncompress': SOURCE_UNCOMPRESS_CHOICE_ALWAYS}
        )

        shutil.copy(
            src=TEST_FILE_NON_ASCII_COMPRESSED_PATH,
            dst=self._test_source._test_temporary_folder
        )

        document_count = Document.objects.count()

        self._test_source.get_backend_instance().process_documents()

        self.assertEqual(Document.objects.count(), document_count + 1)

        document = Document.objects.first()

        self.assertEqual(document.label, TEST_FILE_NON_ASCII_FILENAME)
        self.assertEqual(document.file_latest.exists(), True)
        self.assertEqual(document.file_latest.size, 17436)
        self.assertEqual(document.file_latest.mimetype, 'image/png')
        self.assertEqual(document.file_latest.encoding, 'binary')
