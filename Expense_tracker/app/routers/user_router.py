from fastapi import APIRouter, HTTPException,status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from Expense_tracker.app.core.database import get_db
from Expense_tracker.app.schema.apiresponse_schema import ApiResponse
from Expense_tracker.app.schema.user_schema import User,UserResponse
from Expense_tracker.app.models.user_model import UserModel
from Expense_tracker.app.core.security import hash_password
user_router = APIRouter(prefix="/user", tags=["User"])

#create User
@user_router.post("/addUser", response_model=ApiResponse)
def add_user(user: User,db: Session = Depends(get_db)):

    # Check username
    existing_username = (
        db.query(UserModel)
        .filter(UserModel.username == user.username)
        .first()
    )

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists"
        )

    # Check email
    existing_email = (
        db.query(UserModel)
        .filter(UserModel.email == user.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    # Hash password
    password_hash = hash_password(user.password)

    # Create database object
    new_user = UserModel(
        username=user.username,
        email=user.email,
        password_hash=password_hash
    )

    # Save
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return ApiResponse(
        status="success",
        message="User created successfully",
        data={
            "CreatedUser": UserResponse.model_validate(new_user),
        }
    )



#get all users
@user_router.get("/getAll",response_model=ApiResponse)
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)
    else:
        return ApiResponse(
            status="success",
            message="All Users fetched successfully",
            data={"AllUsers": [UserResponse.model_validate(item)
                              for item in users]
                  }
        )

@user_router.get("/getUser/{username}",response_model=ApiResponse)
def get_user(username:str,db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)
    else:
        return ApiResponse(
            status="success",
            message="User fetched successfully",
            data={"User": UserResponse.model_validate(user)}
        )

@user_router.post("/update/{username}",response_model=ApiResponse)
def update_user(user: User,db: Session = Depends(get_db)):
    existing_user=db.query(UserModel).filter(UserModel.username == user.username).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)
    else:
        existing_user.username = user.username
        existing_user.email = user.email
        db.add(existing_user)
        db.commit()
        db.refresh(existing_user)
        return ApiResponse(
            status="success",
            message="User updated successfully",
            data={"UpdatedUser": UserResponse.model_validate(existing_user)}
        )

@user_router.delete("/delete/{username}",response_model=ApiResponse)
def delete_user(username: str,db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,)
    else:
        db.delete(user)
        db.commit()
        return ApiResponse(
            status="success",
            message="User deleted successfully",
            data={"DeletedUser": UserResponse.model_validate(user)}
        )

