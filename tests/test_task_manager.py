import pytest
from app.task_manager import TaskManager


@pytest.fixture
def task_manager():
    """
    Создает экземпляр класса TaskManager
    """
    return TaskManager()


@pytest.fixture
def task_manager_with_tasks():
    """
    Создает экземпляр класса TaskManager c задачами
    """
    task_manager = TaskManager()
    task_manager.add_task(name="Task_1")
    task_manager.add_task(name="Task_2", priority="high")
    return task_manager


@pytest.mark.parametrize(
    "name, priority, expected",
    [
        ("Task_1", "low", [{"completed": False,
                            "name": "Task_1",
                            "priority": "low"
                            }]),
        ("Task_2", "high", [{"completed": False,
                             "name": "Task_2",
                             "priority": "high"
                             }]),
        ("Task_3", None, [{"completed": False,
                           "name": "Task_3",
                           "priority": "normal"
                           }])
    ]
)
def test_add_task(task_manager, name, priority, expected):
    """
    Тестирует функцию добавления задачи в Task Manager
    """

    if priority is None:
        task_manager.add_task(name)
    else:
        task_manager.add_task(name, priority)
    assert task_manager.tasks == expected


@pytest.mark.parametrize(
    "name, priority",
    [
        ("Task_1", "TEST"),
        ("Task_2", 123),
        ("Task_4", "lowest")
    ]
)
def test_add_task_with_incorrect_priority(task_manager, name, priority):
    """
    Тестирует функцию добавления задачи в Task Manager
    с указанием приоритета не из списка
    """
    with pytest.raises(ValueError):
        task_manager.add_task(name, priority)


def test_list_tasks(task_manager_with_tasks):
    """
    Тестирует возвращение списка всех задач
    """
    assert task_manager_with_tasks.list_tasks() == [{"completed": False,
                                                     "name": "Task_1",
                                                     "priority": "normal"
                                                     },
                                                    {"completed": False,
                                                     "name": "Task_2",
                                                     "priority": "high"
                                                     }
                                                    ]


def test_mark_task_completed(task_manager_with_tasks):
    """
    Тестирует функцию перевода статуса задачи в выполненную
    """
    completed_task = task_manager_with_tasks.mark_task_completed("Task_1")
    assert completed_task["completed"] is True


def test_mark_task_completed_not_found(task_manager_with_tasks):
    """
    Тестирует случай появления исключения,
    когда задача для перевода в выполненную не найдена
    """
    with pytest.raises(ValueError):
        task_manager_with_tasks.mark_task_completed("non-existing task")


def test_remove_task(task_manager_with_tasks):
    """
    Тестирует функцию удаления задачи
    """
    task_manager_with_tasks.remove_task("Task_2")
    assert any("Task_2" not in task["name"] for task in task_manager_with_tasks.tasks)


def test_remove_task_not_found(task_manager_with_tasks):
    """
    Тестирует случай появления исключения,
    когда задача для удаления не была найдена
    """
    with pytest.raises(ValueError):
        task_manager_with_tasks.remove_task("non-existing task")
