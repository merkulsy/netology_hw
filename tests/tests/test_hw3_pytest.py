import pytest
from hw3 import get_name, get_directory, add, documents, directories


class TestHw3:
    # Параметризованные тесты для get_name
    @pytest.mark.parametrize(
        "doc_number, expected",
        [
            ("10006", "Аристарх Павлов"),
            ("11-2", "Геннадий Покемонов"),
            ("101", "Документ не найден"),
            ("5455 028765", "Василий Иванов"),
        ]
    )
    def test_get_name(self, doc_number, expected):
        assert get_name(doc_number) == expected

    # Параметризованные тесты для get_directory
    @pytest.mark.parametrize(
        "doc_number, expected",
        [
            ("11-2", "1"),
            ("10006", "2"),
            ("311 020204", "Полки с таким документом не найдено"),
            ("5455 028765", "1"),
        ]
    )
    def test_get_directory(self, doc_number, expected):
        assert get_directory(doc_number) == expected

    # Тесты для add (с восстановлением состояния)
    def test_add_new_document_to_existing_shelf(self):
        old_docs = documents.copy()
        old_dirs = {k: v.copy() for k, v in directories.items()}
        try:
            add('passport', '123', 'Test', '1')
            assert any(d['number'] == '123' for d in documents)
            assert '123' in directories['1']
        finally:
            documents.clear()
            documents.extend(old_docs)
            directories.clear()
            directories.update(old_dirs)

    def test_add_new_document_to_new_shelf(self):
        old_docs = documents.copy()
        old_dirs = {k: v.copy() for k, v in directories.items()}
        try:
            add('passport', '456', 'Test2', '5')
            assert any(d['number'] == '456' for d in documents)
            assert '5' in directories
            assert '456' in directories['5']
        finally:
            documents.clear()
            documents.extend(old_docs)
            directories.clear()
            directories.update(old_dirs)

    def test_add_duplicate_number_on_same_shelf(self):
        old_docs = documents.copy()
        old_dirs = {k: v.copy() for k, v in directories.items()}
        try:
            initial_count = len(documents)
            add('invoice', '11-2', 'Duplicate', '1')
            assert len(documents) == initial_count
            assert '11-2' in directories['1']
        finally:
            documents.clear()
            documents.extend(old_docs)
            directories.clear()
            directories.update(old_dirs)

    def test_add_document_with_number_present_on_other_shelf(self):
        old_docs = documents.copy()
        old_dirs = {k: v.copy() for k, v in directories.items()}
        try:
            add('insurance', '10006', 'Test', '1')
            assert '10006' in directories['1']
            assert any(d['number'] == '10006' and d['name'] == 'Test' for d in documents)
        finally:
            documents.clear()
            documents.extend(old_docs)
            directories.clear()
            directories.update(old_dirs)