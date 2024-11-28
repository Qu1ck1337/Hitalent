import os

import pytest
from models import TaskManager

TEST_FILE_PATH = "./data/test_tasks.json"

@pytest.fixture
def manager():
    if os.path.exists(TEST_FILE_PATH):
        os.remove(TEST_FILE_PATH)
    return TaskManager(data_file=TEST_FILE_PATH)


def test_add_task(manager):
    manager.add_task("Добавочная задача", "", "", "2024-11-30", "высокий")
    assert len(manager.tasks) == 1

def test_view_tasks(manager):
    manager.add_task("Просмотр задачи", "Описание", "Работа", "2024-11-30", "средний")
    tasks = manager.view_tasks()
    assert len(tasks) == 1


def test_edit_task(manager):
    manager.add_task("Изменение задачи", "Описание", "Работа", "2024-11-30", "низкий")
    manager.edit_task(1, title="Новое название")
    assert manager.tasks[0].title == "Новое название"


def test_delete_task(manager):
    manager.add_task("Удаление задачи", "", "", "2024-11-30", "высокий")
    manager.delete_task(1)
    assert len(manager.tasks) == 0


def test_search_tasks(manager):
    manager.add_task("Поиск задачи", "Описание", "", "2024-11-30", "низкий")
    manager.add_task("Задача 1", "Описание", "", "2024-11-30", "низкий")
    manager.add_task("Задача 2", "Описание", "", "2024-11-30", "низкий")
    tasks = manager.search_tasks(keyword="поиск")
    assert len(tasks) == 1