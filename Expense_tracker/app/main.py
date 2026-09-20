from fastapi import  FastAPI
from Expense_tracker.app.routers.expense_router import expense_router
from Expense_tracker.app.core.database import Base,engine


app = FastAPI()

Base.metadata.create_all(bind=engine)
#This initiates the database creation for us

app.include_router(expense_router)
#This would add the external router to the main app


@app.get("/")
async def root():
    return {"message": "System is up"}