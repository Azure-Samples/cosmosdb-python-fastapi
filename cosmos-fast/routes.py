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

@router.get("/", response_description="Fetch all ToDo items", response_model=List[ToDoItem])
def list_todos(request: Request):
    query = "SELECT * FROM todo_items"
    todos = list(request.app.todo_items_container.query_items(query, enable_cross_partition_query=True))
    return todos
    

@router.put("/update", response_model = ToDoItem)
def update_todo(request: Request, itemId: str, partitionKey: str, itemWithUpdate:UpdateItem):
    item = request.app.todo_items_container.read_item(itemId, partition_key=partitionKey)
    itemDict = jsonable_encoder(item)
    updateDict = jsonable_encoder(itemWithUpdate)
    for key in updateDict.keys():
        if (updateDict[key]) :
            itemDict[key] = updateDict[key]
    updatedItem = request.app.todo_items_container.replace_item(itemId, itemDict)    
    return updatedItem


@router.delete("/delete")
def update_todo(request: Request, itemId: str, partitionKey: str):
    request.app.todo_items_container.delete_item(itemId, partition_key=partitionKey)



