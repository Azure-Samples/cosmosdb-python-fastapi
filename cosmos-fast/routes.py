from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List


from models import ToDoItem, UpdateItem

router = APIRouter()


@router.post("/", response_model=ToDoItem)
def create_todo(request: Request, todoItem: ToDoItem):
    todoItem = jsonable_encoder(todoItem)
    new_todo = request.app.todo_items_container.upsert_item(todoItem)
    return new_todo


@router.get("/", response_model=List[ToDoItem])
def list_todos(request: Request):
    todos = list(request.app.todo_items_container.read_all_items())
    return todos
    
    


@router.put("/update", response_model = ToDoItem)
def replace_todo(request: Request, itemId: str, partitionKey: str, itemWithUpdate:UpdateItem):
    item = request.app.todo_items_container.read_item(itemId, partition_key=partitionKey)
    itemDict = jsonable_encoder(item)
    # The update item must contain id and partition key
    itemWithUpdate.title = itemDict["title"]
    itemWithUpdate.id = itemDict["id"]
    updateDict = jsonable_encoder(itemWithUpdate)
    updatedItem = request.app.todo_items_container.replace_item(itemId, updateDict)    
    return updatedItem



@router.delete("/delete")
def delete_todo(request: Request, itemId: str, partitionKey: str):
    request.app.todo_items_container.delete_item(itemId, partition_key=partitionKey)



