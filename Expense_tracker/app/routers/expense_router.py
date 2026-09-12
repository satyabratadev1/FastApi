from fastapi import APIRouter, HTTPException,status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from Expense_tracker.app.core.database import get_db
from Expense_tracker.app.schema.apiresponse_schema import ApiResponse
from Expense_tracker.app.schema.expense_schema import ExpenseRequestDto,ExpenseResponseDto
from Expense_tracker.app.models.expense_model import ExpenseModel

expense_router = APIRouter(
    prefix="/expense",
)


@expense_router.post("/addexpense", response_model=ApiResponse)
def create_expenses(expense_request_dto: ExpenseRequestDto,db: Session = Depends(get_db)) -> ApiResponse:
    new_expense= ExpenseModel(**expense_request_dto.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    print("New expense created")
    return ApiResponse(
        status="success",
        message="New expense created successfully",
        data={
            "created_expense" : ExpenseResponseDto.model_validate(new_expense)
        }
    )

#get_by_id
@expense_router.get("/{expense_id}" , response_model=ApiResponse)
def read_expense(expense_id: int, db: Session = Depends(get_db))-> ApiResponse:
    expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Expense not found")
    else:
        return ApiResponse(
            status="success",
            message="Expense found",
            data={
                "expense": ExpenseResponseDto.model_validate(expense)
            }
        )

