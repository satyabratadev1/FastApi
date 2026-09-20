from datetime import datetime
from pydantic import BaseModel,Field



class ExpenseRequestDto(BaseModel):
    title: str=Field(...,min_length=1,max_length=100,description="Title of the Expense")
    amount: float=Field(...,description="Amount of the Expense")
    description: str=Field(...,min_length=1,description="Description of the Expense")
    show : bool=Field(...,description="Show Expense")


class ExpenseResponseDto(BaseModel):
    id: int=Field(...,description="Id of the Expense")
    title: str=Field(...,min_length=1,max_length=100,description="Title of the Expense")
    amount: float=Field(...,description="Amount of the Expense")
    description: str=Field(...,min_length=1,description="Description of the Expense")
    #show: bool=Field(...,description="Show Expense")
    created_at: datetime=Field(...,description="Date and Time of the Expense")

    model_config = {
        "from_attributes" : True
    }
