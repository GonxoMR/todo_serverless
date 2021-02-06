import azure.functions as func
import logging

from ..models import Todo, ToDos


def main(req: func.HttpRequest) -> func.HttpResponse:
    if req.method == "POST":
        logging.info("Creating a new todo list item")
        todo = Todo(req.get_json().get("description"))
        ToDos.add_entity(todo)

        return func.HttpResponse(f"{todo}")
models
    logging.info("Getting all todo list items")
    todos = "\n".join(ToDos.get_all_todos())
    return func.HttpResponse(f"Todo:\n{todos}")