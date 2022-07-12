from fastapi import FastAPI
from dotenv import dotenv_values
from azure.cosmos import CosmosClient, PartitionKey, exceptions
from routes import router as todo_router

config = dotenv_values(".env")
app = FastAPI()
DATABASE_NAME = "todo-db"
CONTAINER_NAME = "todo-items"

app.include_router(todo_router, tags=["todos"], prefix="/todos")

@app.on_event("startup")
def startup_db_client():
    app.cosmos_client = CosmosClient(config["URI"], credential = config["KEY"])
    app.database = get_db(DATABASE_NAME)
    app.todo_items_container = get_container(CONTAINER_NAME)
    print("Database :", app.database)
    print("Container :", app.todo_items_container)

def get_db(db_name):
    try:
        return app.cosmos_client.create_database(db_name)
    except exceptions.CosmosResourceExistsError:
        return app.cosmos_client.get_database_client(db_name)

def get_container(container_name):
    try:
        return app.database.create_container(id=CONTAINER_NAME, partition_key=PartitionKey(path="/title"))
    except exceptions.CosmosResourceExistsError:
        return app.database.get_container_client(CONTAINER_NAME)
    except exceptions.CosmosHttpResponseError:
        raise



