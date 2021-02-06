import logging

import azure.functions as func
from ..models import ToDos


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    id = req.route_params.get("id")
    todo = ToDos.get_todo_by_id(id)
    if todo:
        if req.method == "DELETE":
            ToDos.delete_todo(todo)
            return func.HttpResponse()
        if req.method == "PUT":
            req_json = req.get_json()
            if req_json.get("completed"):
                todo.completed = req_json.get("completed")
            if req_json.get("description"):
                todo.description = req_json.get("description")
            ToDos.update_todo(todo)
        return func.HttpResponse(fr"Todo\n{todo}")
    return func.HttpResponse(f"There is no todo with id {id}")
