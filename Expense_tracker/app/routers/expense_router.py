from fastapi import APIRouter, HTTPException,status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from Expense_tracker.app.core.database import get_db
from Expense_tracker.app.schema.apiresponse_schema import ApiResponse
from Expense_tracker.app.schema.expense_schema import ExpenseRequestDto,ExpenseResponseDto
from Expense_tracker.app.models.expense_model import ExpenseModel

expense_router = APIRouter(prefix="/expense", tags=["Expense"])


#add expense
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

@expense_router.get("/getAll" , response_model=ApiResponse)
def get_all_expenses(db: Session = Depends(get_db)) -> ApiResponse:
    expenses = db.query(ExpenseModel).filter(ExpenseModel.show==True).all()
    if not expenses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Expense not found")
    else:
        return ApiResponse(
            status="success",
            message="Expenses found successfully",
            data={
                "All_expenses": [ExpenseResponseDto.model_validate(expense)
                                 for expense in expenses]
            }
        )
@expense_router.get("/search",response_model=ApiResponse,status_code=status.HTTP_200_OK)
def search_by_title(title: str, db: Session = Depends(get_db))-> ApiResponse:
    expense=db.query(ExpenseModel).filter(ExpenseModel.title.ilike(f"%{title}%")).all()
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Expense not found")
    else:
        return ApiResponse(
            status="success",
            message="Expense found successfully",
            data={"expense": [ExpenseResponseDto.model_validate(item)
                  for item in expense]
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


@expense_router.put("/{expense_id}" , response_model=ApiResponse)
def update_expense(expense_id: int,expense_request_dto:ExpenseRequestDto,db:Session=Depends(get_db))-> ApiResponse:
    expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Expense not found")
    else:
        expense.title = expense_request_dto.title
        expense.description = expense_request_dto.description
        expense.amount = expense_request_dto.amount
        expense.show = expense_request_dto.show
        db.add(expense)
        db.commit()
        db.refresh(expense)
        return ApiResponse(
            status="success",
            message="Expense updated successfully",
            data={
                "expense": ExpenseResponseDto.model_validate(expense)
            }
        )


@expense_router.delete("/{expense_id}" , response_model=ApiResponse)
def delete_expense(expense_id: int, db: Session = Depends(get_db))-> ApiResponse:
    expense = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Expense not found")
    else:
        db.delete(expense)
        db.commit()

        return ApiResponse(
            status="success",
            message="Expense deleted successfully"
        )


