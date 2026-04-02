from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.transaction import Transaction
from app.utils.role_checker import check_role

router = APIRouter()


# ✅ ANALYTICS (ADMIN + ANALYST ONLY)
@router.get("/analytics")
def get_analytics(
    user_role: str = Query(...),
    db: Session = Depends(get_db)
):
    check_role(user_role, ["admin", "analyst"])

    total_income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.type == "income"
    ).scalar() or 0

    total_expense = db.query(func.sum(Transaction.amount)).filter(
        Transaction.type == "expense"
    ).scalar() or 0

    balance = total_income - total_expense

    category_data = db.query(
        Transaction.category,
        func.sum(Transaction.amount)
    ).group_by(Transaction.category).all()

    category_breakdown = [
        {"category": cat, "total": total}
        for cat, total in category_data
    ]

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "category_breakdown": category_breakdown
    }
