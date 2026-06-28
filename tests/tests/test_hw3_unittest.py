import unittest
from hw3 import get_name, get_directory, add, documents, directories


class TestHw3(unittest.TestCase):
    def setUp(self):
        self.original_documents = [doc.copy() for doc in documents]
        self.original_directories = {k: v.copy() for k, v in directories.items()}

    def tearDown(self):
        documents.clear()
        documents.extend(self.original_documents)
        directories.clear()
        directories.update(self.original_directories)

    def test_get_name(self):
        params = (
            ("10006", "Аристарх Павлов"),
            ("11-2", "Геннадий Покемонов"),
            ("101", "Документ не найден"),
            ("5455 028765", "Василий Иванов"),
        )
        for doc_number, expected in params:
            with self.subTest(doc_number=doc_number):
                self.assertEqual(get_name(doc_number), expected)

    def test_get_directory(self):
        params = (
            ("11-2", "1"),
            ("10006", "2"),
            ("311 020204", "Полки с таким документом не найдено"),
            ("5455 028765", "1"),
        )
        for doc_number, expected in params:
            with self.subTest(doc_number=doc_number):
                self.assertEqual(get_directory(doc_number), expected)

    def test_add_new_document_to_existing_shelf(self):
        add('passport', '123', 'Test', '1')
        self.assertTrue(any(d['number'] == '123' for d in documents))
        self.assertIn('123', directories['1'])

    def test_add_new_document_to_new_shelf(self):
        add('passport', '456', 'Test2', '5')
        self.assertTrue(any(d['number'] == '456' for d in documents))
        self.assertIn('5', directories)
        self.assertIn('456', directories['5'])

    def test_add_duplicate_number_on_same_shelf(self):
        initial_count = len(documents)
        add('invoice', '11-2', 'Duplicate', '1')
        self.assertEqual(len(documents), initial_count)
        self.assertIn('11-2', directories['1'])

    def test_add_document_with_number_present_on_other_shelf(self):
        add('insurance', '10006', 'Test', '1')
        self.assertIn('10006', directories['1'])
        self.assertTrue(any(d['number'] == '10006' and d['name'] == 'Test' for d in documents))