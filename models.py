import datetime
from uuid import uuid4

from azure.data.tables import TableClient

table_client = TableClient.from_connection_string(conn_str="AzureWebJobsStorage", table_name="todos")

class ToDo:
    def __init__(
        self,
        description: str,
        completed: bool = False,
        id: uuid4 = None,
        created_time: datetime = None,
    ) -> None:
        self.id = id if id else uuid4()
        self.created_time = created_time if created_time else datetime.datetime.now()
        self._description = description
        self._completed = completed

    def __str__(self):
        return f"Task({self.description}, {self.completed})"

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @property
    def completed(self) -> bool:
        return self._completed

    @completed.setter
    def completed(self, value: bool) -> None:
        self._completed = value

    @classmethod
    def from_entity(cls, entitiy):
        return cls(
            description=entitiy["Description"],
            completed=entitiy["Completed"],
            id=entitiy["RowKey"],
            created_time=entitiy["CreatedTime"],
        )
    
    def to_table_entity(self):
        todo_ent = {
            "PartitionKey": "todo",
            "RowKey": self.id,
            "Description": self.description,
            "Completed": self.completed,
            "CreatedTime": self.created_time,
        }
        return todo_ent


class ToDos:
    @classmethod
    def add_todo(cls, todo: ToDo):
        table_client.create_entity(entity=todo.to_table_entity())

    @classmethod
    def get_all_todos(cls):
        table_client.query_entities("todos")

    @classmethod
    def get_todo_by_id(cls, id) -> ToDo:
        my_filter = f"RowKey eq {id}"
        todo_ent = table_client.query_entities(my_filter)
        # todo = [todo for todo in todos if todo.id == id]
        # return todo[0] if todo else None
        return ToDo.from_entity(todo_ent)

    @classmethod
    def update_todo(cls, todo: ToDo):
        # Todo - check what is the correct method
        table_client.update_entity(todo.to_table_entity())

    @classmethod
    def delete_todo(cls, todo):
        table_client.delete_entity(partition_key="todo", row_key=todo.id)
