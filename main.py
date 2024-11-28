from models import TaskManager
from validators import validate_non_empty, validate_date, validate_priority, ValidationError


def main():
    manager = TaskManager()

    while True:
        try:
            print("\nМенеджер задач:")
            print("1. Просмотр задач")
            print("2. Добавление задачи")
            print("3. Изменение задачи")
            print("4. Удаление задачи")
            print("5. Поиск задач")
            print("6. Выход")
            choice = input("Выберите действие: ")

            if choice == "1":
                category = input("Введите категорию (нажмите Enter, чтобы посмотреть все): ")
                tasks = manager.view_tasks(category if category else None)
                if not tasks:
                    print("Задач не найдено.")
                for task in tasks:
                    print(task.to_dict())

            elif choice == "2":
                title = input("Название задачи: ")
                validate_non_empty(title, "Название задачи")
                description = input("Описание: ")
                category = input("Категория: ")
                due_date = input("Срок выполнения (YYYY-MM-DD): ")
                validate_date(due_date)
                priority = input("Приоритет (низкий, средний, высокий): ")
                validate_priority(priority)

                manager.add_task(title, description, category, due_date, priority)
                print("Задача добавлена!")

            elif choice == "3":
                task_id = int(input("Введите ID задачи для изменения: "))
                task = next((t for t in manager.tasks if t.id == task_id), None)
                if not task:
                    raise ValidationError("Задача с таким ID не найдена.")

                print("Введите новые значения (нажмите Enter, чтобы оставить без изменений):")
                title = input("Новое название: ")
                description = input("Новое описание: ")
                category = input("Новая категория: ")
                due_date = input("Новый срок выполнения (YYYY-MM-DD): ")
                if due_date:
                    validate_date(due_date)
                priority = input("Новый приоритет: ")
                if priority:
                    validate_priority(priority)
                status = input("Новый статус (выполнена/не выполнена): ")

                manager.edit_task(task_id, title=title or None, description=description or None,
                                  category=category or None, due_date=due_date or None,
                                  priority=priority or None, status=status or None)
                print("Задача изменена!")

            elif choice == "4":
                task_id = input("Введите ID задачи для удаления (или нажмите Enter, чтобы удалить по категории): ")
                if task_id:
                    if not task_id.isdigit():
                        raise ValidationError("ID задачи должен быть числом.")
                    manager.delete_task(task_id=int(task_id))
                else:
                    category = input("Введите категорию: ")
                    validate_non_empty(category, "Категория")
                    manager.delete_task(category=category)
                print("Задача удалена!")

            elif choice == "5":
                keyword = input("Введите ключевое слово: ")
                category = input("Введите категорию: ")
                status = input("Введите статус (выполнена/не выполнена): ")
                tasks = manager.search_tasks(keyword or None, category or None, status or None)
                if not tasks:
                    print("Задач не найдено.")
                for task in tasks:
                    print(task.to_dict())

            elif choice == "6":
                break

            else:
                print("Неверный выбор, попробуйте снова.")

        except ValidationError as e:
            print(f"Ошибка: {e}")
        except ValueError as e:
            print(f"Ошибка ввода: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")


if __name__ == "__main__":
    main()