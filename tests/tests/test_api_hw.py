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
    folder_path = f"disk:/{temp_folder}"
    response = requests.put(BASE_URL, headers=headers, params={"path": folder_path})
    assert response.status_code in (201, 409), f"Не удалось создать папку: {response.text}"
    yield temp_folder
    requests.delete(BASE_URL, headers=headers, params={"path": folder_path, "permanently": "true"})


# ---------- ПОЛОЖИТЕЛЬНЫЕ ТЕСТЫ ----------

def test_create_folder_success(headers, create_and_cleanup_folder):
    folder = create_and_cleanup_folder
    folder_path = f"disk:/{folder}"
    meta_response = requests.get(BASE_URL, headers=headers, params={"path": folder_path})
    assert meta_response.status_code == 200, "Папка не найдена после создания"
    data = meta_response.json()
    assert data.get("name") == folder, "Имя папки не совпадает"


def test_create_folder_success_with_subpath(headers, temp_folder):
    parent = temp_folder
    child = f"{parent}/subfolder"
    parent_path = f"disk:/{parent}"
    child_path = f"disk:/{child}"

    # Создаём родительскую папку
    resp_parent = requests.put(BASE_URL, headers=headers, params={"path": parent_path})
    assert resp_parent.status_code == 201, f"Не удалось создать родительскую папку: {resp_parent.text}"

    # Создаём дочернюю папку
    resp_child = requests.put(BASE_URL, headers=headers, params={"path": child_path})
    assert resp_child.status_code == 201, f"Не удалось создать дочернюю папку: {resp_child.text}"

    # Проверяем существование дочерней папки
    meta_response = requests.get(BASE_URL, headers=headers, params={"path": child_path})
    assert meta_response.status_code == 200, "Дочерняя папка не найдена"

    # Очистка: удаляем родительскую папку рекурсивно
    requests.delete(BASE_URL, headers=headers, params={"path": parent_path, "permanently": "true"})


# ---------- ОТРИЦАТЕЛЬНЫЕ ТЕСТЫ ----------

def test_create_existing_folder(headers, create_and_cleanup_folder):
    folder = create_and_cleanup_folder
    folder_path = f"disk:/{folder}"
    response = requests.put(BASE_URL, headers=headers, params={"path": folder_path})
    assert response.status_code == 409, "При создании существующей папки код ответа должен быть 409"


def test_create_folder_invalid_path(headers):
    response = requests.put(BASE_URL, headers=headers, params={"path": "disk://///invalid"})
    assert response.status_code == 404


def test_create_folder_unauthorized(temp_folder):
    headers_no_auth = {}
    folder_path = f"disk:/{temp_folder}"
    response = requests.put(BASE_URL, headers=headers_no_auth, params={"path": folder_path})
    assert response.status_code == 401, "Ожидается 401 при отсутствии авторизации"


def test_create_folder_with_wrong_token(temp_folder):
    wrong_headers = {"Authorization": "OAuth wrong_token"}
    folder_path = f"disk:/{temp_folder}"
    response = requests.put(BASE_URL, headers=wrong_headers, params={"path": folder_path})
    assert response.status_code == 401, "Ожидается 401 при неверном токене"