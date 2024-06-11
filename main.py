import uvicorn
from fastapi import FastAPI, HTTPException, Path
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import datetime
from pydantic import BaseModel
from bson import ObjectId

class Settings(BaseSettings):
    mongo_uri: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    root_path: str = ""

settings = Settings()

db_client = AsyncIOMotorClient(settings.mongo_uri)
db = db_client.todoDb

description = """
C'est ma première application avec le framework Python FastAPI
"""
app = FastAPI(
	title="My Todo App",
	description=description,
	version="v1.0.0",
	docs_url="/",
	root_path=settings.root_path,
)

class Todo(BaseModel):
    title: str
    completed: bool = False

class TodoId(BaseModel):
    id: str
    
class TodoRecord(TodoId, Todo):
    created_date: datetime
    updated_date: datetime
    
@app.get("/todos", response_model=list[TodoRecord])
async def get_todos() -> list[TodoRecord]:
    """
    Afficher la liste des tâches
    """
    todos: list[TodoRecord] = []
    async for doc in db.todos.find():
        todos.append(
            TodoRecord(
                id=str(doc["_id"]),
                title=doc["title"],
                completed=doc["completed"],
                created_date=doc["created_date"],
                updated_date=doc["updated_date"],
            )
        )

    return todos

@app.post("/todos", response_model=TodoId)
async def create_todo(payload: Todo) -> TodoId:
    """
    Créer une nouvelle tâche Todo
    """
    now = datetime.utcnow()
    insert_result = await db.todos.insert_one(
        {
            "title": payload.title,
            "completed": payload.completed,
            "created_date": now,
            "updated_date": now,
        }
    )

    return TodoId(id=str(insert_result.inserted_id))
    
class NotFoundException(BaseModel):
    detail: str = "Not Found"

MONGO_ID_REGEX = r"^[a-f\d]{24}$"

@app.get(
    "/todos/{id}",
    response_model=TodoRecord,
    responses={
        404: {"description": "Not Found", "model": NotFoundException},
    },
)
async def get_todo(
    id: str = Path(description="Todo ID", pattern=MONGO_ID_REGEX)
) -> TodoRecord:
    """
    Get a Todo
    """
    doc = await db.todos.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Not Found")

    return TodoRecord(
        id=str(doc["_id"]),
        title=doc["title"],
        completed=doc["completed"],
        created_date=doc["created_date"],
        updated_date=doc["updated_date"],
    )

@app.put(
    "/todos/{id}",
    response_model=TodoId,
    responses={
        404: {"description": "Not Found", "model": NotFoundException},
    },
)

async def update_todo(
    payload: Todo,
    id: str = Path(description="Todo ID", pattern=MONGO_ID_REGEX),
) -> TodoId:
    """
    Mettre à jour une tâche Todo
    """
    now = datetime.utcnow()
    update_result = await db.todos.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "title": payload.title,
                "completed": payload.completed,
                "updated_date": now,
            }
        },
    )

    if update_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Not Found")

    return TodoId(id=id)
    
@app.delete(
    "/todos/{id}",
    response_model=bool,
    responses={
        404: {"description": "Not Found", "model": NotFoundException},
    },
)
async def delete_todo(
    id: str = Path(description="Todo ID", pattern=MONGO_ID_REGEX),
) -> bool:
    """
    Delete a Todo
    """
    delete_result = await db.todos.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not Found")

    return True

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        reload=True,
    )
    
