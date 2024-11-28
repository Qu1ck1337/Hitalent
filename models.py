import json
import os
from typing import List, Optional

DATA_FILE = "./data/tasks.json"


class Task:
    def __init__(self, id: int, title: str, description: str, category: str, due_date: str, priority: str, status: str = "Не выполнена"):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data):
        return Task(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            category=data["category"],
            due_date=data["due_date"],
            priority=data["priority"],
            status=data["status"],
        )


class TaskManager:
    def __init__(self, data_file=DATA_FILE):
        self.data_file = data_file
        self.tasks: List[Task] = self.load_tasks()

    def load_tasks(self) -> List[Task]:
        if not os.path.exists(self.data_file):
            return []
        with open(self.data_file, "r", encoding="utf-8") as file:
            return [Task.from_dict(task) for task in json.load(file)]

    def save_tasks(self):
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in self.tasks], file, ensure_ascii=False, indent=4)

    def add_task(self, title: str, description: str, category: str, due_date: str, priority: str):
        task_id = max((task.id for task in self.tasks), default=0) + 1
        self.tasks.append(Task(task_id, title, description, category, due_date, priority))
        self.save_tasks()

    def view_tasks(self, category: Optional[str] = None):
        tasks = self.tasks if category is None else [task for task in self.tasks if task.category == category]
        return tasks

    def edit_task(self, task_id: int, **kwargs):
        for task in self.tasks:
            if task.id == task_id:
                for key, value in kwargs.items():
                    if not value:
                        continue
                    if hasattr(task, key):
                        setattr(task, key, value)
                self.save_tasks()
                return
        raise ValueError("Задача не найдена")

    def delete_task(self, task_id: Optional[int] = None, category: Optional[str] = None):
        if task_id:
            self.tasks = [task for task in self.tasks if task.id != task_id]
        elif category:
            self.tasks = [task for task in self.tasks if task.category != category]
        else:
            raise ValueError("id задачи или категория не предоставлены")
        self.save_tasks()

    def search_tasks(self, keyword: Optional[str] = None, category: Optional[str] = None, status: Optional[str] = None):
        result = self.tasks
        if keyword:
            result = [task for task in result if keyword.lower() in task.title.lower() or keyword.lower() in task.description.lower()]
        if category:
            result = [task for task in result if task.category == category]
        if status:
            result = [task for task in result if task.status == status]
        return result