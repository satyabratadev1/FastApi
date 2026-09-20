from Expense_tracker.app.core.database import Base
from datetime import datetime
from zoneinfo import ZoneInfo
from sqlalchemy import Boolean,Column,Integer,String,Float,DateTime,Date

class ExpenseModel(Base):
    __tablename__ = 'expense'
    id = Column(Integer, primary_key=True,index=True,autoincrement=True)
    title = Column(String(40),nullable=False)
    description = Column(String(500),nullable=False)
    amount = Column(Float,nullable=False)
    show=Column(Boolean,default=True,nullable=False)
    created_at = Column(DateTime,nullable=False,default=lambda: datetime.now(ZoneInfo("Asia/Kolkata")))


