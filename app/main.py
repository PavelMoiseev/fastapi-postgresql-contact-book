import json
import secrets
import uvicorn

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from .db_queries import db_create_table, db_add_user, db_get_user
from .schemas import User

db_create_table()
security = HTTPBasic()
app = FastAPI()


def authorize(credentials: HTTPBasicCredentials = Depends(security)):
    is_user_ok = secrets.compare_digest(credentials.username, "atompostgres")
    is_pass_ok = secrets.compare_digest(credentials.password, "asDkjH!_aSa")

    if not (is_user_ok and is_pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.get("/")
async def root():
    return "Phonebook"


@app.post("/add_user", dependencies=[Depends(authorize)])
async def add_user(parametrs: User):
    db_add_user(parametrs)
    return "User is added"


@app.get("/get_user", dependencies=[Depends(authorize)])
async def get_user(lastname):
    df = db_get_user(lastname)
    if df.empty:
        return "User is not found"
    result = df.to_json(orient="values")
    parsed = json.loads(result)
    return json.dumps(parsed)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
