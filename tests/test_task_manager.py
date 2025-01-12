import pytest
from app.task_manager import TaskManager


@pytest.fixture
def task_manager():
    """
    Создает экземпляр класса TaskManager
    """
    return TaskManager()


def test_add_task_and_set_priority(task_manager):
    """
    Тестирует функцию добавления задачи в Task Manager c выставлением приоритета
    """
    added_task = task_manager.add_task(name="Task_1", priority="low")
    assert added_task["name"] == "Task_1"
    assert added_task["priority"] == "low"
    assert added_task["completed"] is False
    assert len(task_manager.tasks) == 1


def test_add_task_without_priority(task_manager):
    """
    Тестирует функцию добавления задачи в Task Manager без указания приоритета
    """
    added_task = task_manager.add_task(name="Task_2")
    assert added_task["name"] == "Task_2"
    assert added_task["priority"] == "normal"
    assert added_task["completed"] is False
    assert len(task_manager.tasks) == 1


def test_add_task_with_incorrect_priority(task_manager):
    """
    Тестирует функцию добавления задачи в Task Manager
    с указанием приоритета не из списка
    """
    with pytest.raises(ValueError):
        task_manager.add_task(name="Task_3", priority="TEST")


def test_list_tasks(task_manager):
    """
    Тестирует возвращение списка всех задач
    """
    task_manager.add_task(name="Task_1")
    task_manager.add_task(name="Task_2", priority="high")
    assert isinstance(task_manager.list_tasks(), list)
    assert len(task_manager.list_tasks()) == 2
    assert task_manager.list_tasks() == [{"completed": False,
                                          "name": "Task_1",
                                          "priority": "normal"
                                          },
                                         {"completed": False,
                                          "name": "Task_2",
                                          "priority": "high"
                                          }
                                         ]


def test_mark_task_completed(task_manager):
    """
    Тестирует функцию перевода статуса задачи в выполненную
    """
    task_manager.add_task(name="task to complete", priority="high")
    completed_task = task_manager.mark_task_completed("task to complete")
    assert completed_task["completed"] is True


def test_mark_task_completed_not_found(task_manager):
    """
    Тестирует случай появления исключения,
    когда задача для перевода в выполненную не найдена
    """
    task_manager.add_task(name="task to complete", priority="high")
    with pytest.raises(ValueError):
        task_manager.mark_task_completed("non-existing task")


def test_remove_task(task_manager):
    """
    Тестирует функцию удаления задачи
    """
    task_manager.add_task(name="task to remove", priority="low")
    task_manager.remove_task("task to remove")
    assert len(task_manager.tasks) == 0


def test_remove_task_not_found(task_manager):
    """
    Тестирует случай появления исключения,
    когда задача для удаления не была найдена
    """
    task_manager.add_task(name="task to remove", priority="low")
    with pytest.raises(ValueError):
        task_manager.remove_task("non-existing task")
