from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import ToDoItem

router = APIRouter()


@router.post("/insert", response_model=ToDoItem)
async def create_todo(request: Request, todo_item: ToDoItem):
    todo_item = jsonable_encoder(todo_item)
    new_todo = await request.app.todo_items_container.create_item(todo_item)
    return new_todo

@router.get("/listall", response_description="List of all To-do items", response_model=List[ToDoItem])
async def list_todos(request: Request):
    todos = [todo async for todo in request.app.todo_items_container.read_all_items()]
    return todos
    

@router.put("/update", response_model = ToDoItem, )
async def replace_todo(request: Request, item_with_update:ToDoItem):
    """
    Update an item. Id (which is also the PartitionKey in this case) values should reference the item to be updated:

    - **id**: [Mandatory] Old Item ID
    - **name**: [Optional] The new name.
    - **description**: [Optional] The new description
    - **isComplete**: [Optional] boolean flag to mark a Todo complete or incomplete
    """
    existing_item = await request.app.todo_items_container.read_item(item_with_update.id,partition_key = item_with_update.id)
    existing_item_dict = jsonable_encoder(existing_item)
    update_dict = jsonable_encoder(item_with_update)
    for (k) in update_dict.keys():
        if update_dict[k]:
            existing_item_dict[k] = update_dict[k]
    updatedItem = await request.app.todo_items_container.replace_item(item_with_update.id, existing_item_dict)    
    return updatedItem



@router.delete("/delete")
async def delete_todo(request: Request, item_id: str, pk: str):
     await request.app.todo_items_container.delete_item(item_id, partition_key=pk)



