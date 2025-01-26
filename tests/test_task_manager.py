import pytest
import allure
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


@allure.feature("Добавление задачи в Task Manager")
@allure.story("Успешное добавление задачи")
@allure.severity(allure.severity_level.BLOCKER)
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
        with allure.step("Добавить задачу без указания приоритета"):
            task_manager.add_task(name)
    else:
        with allure.step("Добавить задачу c указанием приоритета"):
            task_manager.add_task(name, priority)
    with allure.step("Проверить, что задача была добавлена"):
        assert task_manager.tasks == expected


@allure.feature("Добавление задачи в Task Manager")
@allure.story("Добавление задачи с указанием некорректного приоритета")
@allure.severity(allure.severity_level.CRITICAL)
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
    with allure.step("Добавить задачу с некорректным приоритетом"):
        with pytest.raises(ValueError):
            task_manager.add_task(name, priority)


@allure.feature("Отображение списка всех задач в Task Manager")
@allure.story("Успешное отображение списка всех задач")
@allure.severity(allure.severity_level.CRITICAL)
def test_list_tasks(task_manager_with_tasks):
    """
    Тестирует возвращение списка всех задач
    """
    with allure.step("Проверить отображение всех задач"):
        assert task_manager_with_tasks.list_tasks() == [{"completed": False,
                                                         "name": "Task_1",
                                                         "priority": "normal"
                                                         },
                                                        {"completed": False,
                                                         "name": "Task_2",
                                                         "priority": "high"
                                                         }
                                                        ]


@allure.feature('Перевод задачи в статус "completed" в Task Manager')
@allure.story('Успешный перевод статуса задачи в "completed"')
@allure.severity(allure.severity_level.CRITICAL)
def test_mark_task_completed(task_manager_with_tasks):
    """
    Тестирует функцию перевода статуса задачи в выполненную
    """
    with allure.step('Перевести статус задачи в "completed"'):
        completed_task = task_manager_with_tasks.mark_task_completed("Task_1")
    with allure.step('Проверить, что задача изменила статус на "completed"'):
        assert completed_task["completed"] is True


@allure.feature('Перевод задачи в статус "completed" в Task Manager')
@allure.story('Перевод несуществующей задачи в статус "completed"')
@allure.severity(allure.severity_level.NORMAL)
def test_mark_task_completed_not_found(task_manager_with_tasks):
    """
    Тестирует случай появления исключения,
    когда задача для перевода в выполненную не найдена
    """
    with allure.step("Проверить появление ошибки " +
                     "при попытке изменения статуса для несуществующей задачи"
                     ):
        with pytest.raises(ValueError):
            task_manager_with_tasks.mark_task_completed("non-existing task")


@allure.feature("Удаление задачи из Task Manager")
@allure.story("Успешное удаление задачи")
@allure.severity(allure.severity_level.CRITICAL)
def test_remove_task(task_manager_with_tasks):
    """
    Тестирует функцию удаления задачи
    """
    with allure.step("Удалить задачу"):
        task_manager_with_tasks.remove_task("Task_2")
    with allure.step("Проверить, что задача была удалена"):
        assert any("Task_2" not in task["name"] for task in task_manager_with_tasks.tasks)


@allure.feature("Удаление задачи из Task Manager")
@allure.story("Удаление несуществующей задачи")
@allure.severity(allure.severity_level.NORMAL)
def test_remove_task_not_found(task_manager_with_tasks):
    """
    Тестирует случай появления исключения,
    когда задача для удаления не была найдена
    """
    with allure.step("Проверить появление ошибки " +
                     "при попытке удаления несуществующей задачи"
                     ):
        with pytest.raises(ValueError):
            task_manager_with_tasks.remove_task("non-existing task")
