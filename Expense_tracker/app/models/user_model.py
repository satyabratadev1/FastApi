from Expense_tracker.app.core.database import Base
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy import Boolean,Column,Integer,String,Float,DateTime,Date

class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,index=True,autoincrement=True)
    username = Column(String,index=True,unique=True,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password_hash = Column(String,nullable=False)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(ZoneInfo("Asia/Kolkata")))

