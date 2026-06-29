from uuid import uuid4

import pytest
import requests

from settings import yd_token

YANDEX_TOKEN = yd_token
BASE_URL = "https://cloud-api.yandex.net/v1/disk/resources"


@pytest.fixture
def token():
    if not YANDEX_TOKEN:
        pytest.fail("YANDEX_TOKEN не установлен")
    return YANDEX_TOKEN


@pytest.fixture
def headers(token):
    return {"Authorization": f"OAuth {token}"}


@pytest.fixture
def temp_folder():
    return f"test-folder-{uuid4()}"


@pytest.fixture
def create_and_cleanup_folder(headers, temp_folder):
    """
    Создаёт папку (без проверки статуса ответа) и удаляет её после теста.
    Возвращает имя папки.
    """
    folder_path = f"disk:/{temp_folder}"
    # Выполняем создание, но не проверяем статус – успешность проверяется в тесте через GET
    requests.put(BASE_URL, headers=headers, params={"path": folder_path})
    yield temp_folder
    # Удаление после теста
    requests.delete(BASE_URL, headers=headers, params={"path": folder_path, "permanently": "true"})


# ---------- ПОЛОЖИТЕЛЬНЫЕ ТЕСТЫ ----------

def test_create_folder_success(headers, create_and_cleanup_folder):
    """
    Проверяет, что папка успешно создана:
    - появляется в списке файлов корневой директории (код 200)
    - GET-запрос к папке возвращает 200 и имя совпадает
    """
    folder = create_and_cleanup_folder
    folder_path = f"disk:/{folder}"

    # 1. Проверка появления в списке корня
    list_response = requests.get(BASE_URL, headers=headers, params={"path": "disk:/"})
    assert list_response.status_code == 200, "Не удалось получить список файлов"
    items = list_response.json().get("_embedded", {}).get("items", [])
    folder_names = [item["name"] for item in items]
    assert folder in folder_names, f"Папка '{folder}' не найдена в списке файлов"

    # 2. Проверка, что GET на папку возвращает 200 (существует)
    meta_response = requests.get(BASE_URL, headers=headers, params={"path": folder_path})
    assert meta_response.status_code == 200, "Папка не существует"
    data = meta_response.json()
    assert data.get("name") == folder, "Имя папки не совпадает"


def test_create_folder_success_with_subpath(headers, temp_folder):
    """
    Создание вложенной папки (родительская + дочерняя).
    Проверяет появление дочерней папки в списке родительской (код 200).
    """
    parent = temp_folder
    child = f"{parent}/subfolder"
    parent_path = f"disk:/{parent}"
    child_path = f"disk:/{child}"

    # Создаём родительскую (без проверки статуса)
    requests.put(BASE_URL, headers=headers, params={"path": parent_path})
    # Создаём дочернюю (без проверки статуса)
    requests.put(BASE_URL, headers=headers, params={"path": child_path})

    # Проверяем, что дочерняя папка появилась в списке родительской
    list_response = requests.get(BASE_URL, headers=headers, params={"path": parent_path})
    assert list_response.status_code == 200, "Не удалось получить список родительской папки"
    items = list_response.json().get("_embedded", {}).get("items", [])
    child_names = [item["name"] for item in items]
    assert "subfolder" in child_names, "Дочерняя папка не найдена в списке родительской папки"

    # Дополнительная проверка: GET на дочернюю папку возвращает 200
    meta_response = requests.get(BASE_URL, headers=headers, params={"path": child_path})
    assert meta_response.status_code == 200, "Дочерняя папка не существует"

    # Очистка: удаляем родительскую папку рекурсивно
    requests.delete(BASE_URL, headers=headers, params={"path": parent_path, "permanently": "true"})


# ---------- ОТРИЦАТЕЛЬНЫЕ ТЕСТЫ ----------

def test_create_existing_folder(headers, create_and_cleanup_folder):
    """
    Попытка создать уже существующую папку → 409 Conflict.
    """
    folder = create_and_cleanup_folder
    folder_path = f"disk:/{folder}"
    response = requests.put(BASE_URL, headers=headers, params={"path": folder_path})
    assert response.status_code == 409, "При создании существующей папки код ответа должен быть 409"


def test_create_folder_invalid_path(headers):
    """
    Невалидный путь → 404.
    """
    response = requests.put(BASE_URL, headers=headers, params={"path": "disk://///invalid"})
    assert response.status_code == 404


def test_create_folder_unauthorized(temp_folder):
    """
    Отсутствие токена → 401.
    """
    headers_no_auth = {}
    folder_path = f"disk:/{temp_folder}"
    response = requests.put(BASE_URL, headers=headers_no_auth, params={"path": folder_path})
    assert response.status_code == 401, "Ожидается 401 при отсутствии авторизации"


def test_create_folder_with_wrong_token(temp_folder):
    """
    Неверный токен → 401.
    """
    wrong_headers = {"Authorization": "OAuth wrong_token"}
    folder_path = f"disk:/{temp_folder}"
    response = requests.put(BASE_URL, headers=wrong_headers, params={"path": folder_path})
    assert response.status_code == 401, "Ожидается 401 при неверном токене"