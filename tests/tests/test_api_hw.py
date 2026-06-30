rom uuid import uuid4

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
    """Создаёт папку для тестов с повторным созданием и удаляет после теста."""
    folder_path = f"disk:/{temp_folder}"
    response = requests.put(BASE_URL, headers=headers, params={"path": folder_path})
    assert response.status_code == 201, f"Не удалось создать папку: {response.text}"
    yield temp_folder
    requests.delete(BASE_URL, headers=headers, params={"path": folder_path, "permanently": "true"})


# ---------- ПОЛОЖИТЕЛЬНЫЕ ТЕСТЫ ----------

def test_create_folder_success(headers, temp_folder):
    folder_path = f"disk:/{temp_folder}"

    response = requests.put(BASE_URL, headers=headers, params={"path": folder_path})
    assert response.status_code == 201, f"Ожидался код 201 при создании папки: {response.text}"

    list_response = requests.get(BASE_URL, headers=headers, params={"path": "disk:/"})
    assert list_response.status_code == 200, "Не удалось получить список файлов"
    items = list_response.json().get("_embedded", {}).get("items", [])
    folder_names = [item["name"] for item in items]
    assert temp_folder in folder_names, f"Папка '{temp_folder}' не найдена в списке файлов"

    requests.delete(BASE_URL, headers=headers, params={"path": folder_path, "permanently": "true"})


def test_create_folder_success_with_subpath(headers, temp_folder):
    parent = temp_folder
    child = f"{parent}/subfolder"
    parent_path = f"disk:/{parent}"
    child_path = f"disk:/{child}"

    resp_parent = requests.put(BASE_URL, headers=headers, params={"path": parent_path})
    assert resp_parent.status_code == 201, f"Не удалось создать родительскую папку: {resp_parent.text}"

    resp_child = requests.put(BASE_URL, headers=headers, params={"path": child_path})
    assert resp_child.status_code == 201, f"Не удалось создать дочернюю папку: {resp_child.text}"

    list_response = requests.get(BASE_URL, headers=headers, params={"path": parent_path})
    assert list_response.status_code == 200, "Не удалось получить список родительской папки"
    items = list_response.json().get("_embedded", {}).get("items", [])
    child_names = [item["name"] for item in items]
    assert "subfolder" in child_names, "Дочерняя папка не найдена в списке родительской папки"

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
