from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.transaction import Transaction
from app.schemas.transaction_schema import TransactionCreate, TransactionResponse
from app.utils.role_checker import check_role

router = APIRouter()


# ✅ CREATE (ONLY ADMIN)
@router.post("/transactions", response_model=TransactionResponse)
def create_transaction(
    transaction: TransactionCreate,
    user_role: str = Query(...),
    db: Session = Depends(get_db)
):
    check_role(user_role, ["admin"])

    new_transaction = Transaction(**transaction.dict())
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction


# ✅ GET (ALL ROLES + FILTERING)
@router.get("/transactions")
def get_transactions(
    type: str = None,
    category: str = None,
    date: str = None,
    user_role: str = Query(...),
    db: Session = Depends(get_db)
):
    check_role(user_role, ["admin", "analyst", "viewer"])

    query = db.query(Transaction)

    if type:
        query = query.filter(Transaction.type == type)

    if category:
        query = query.filter(Transaction.category == category)

    if date:
        query = query.filter(Transaction.date == date)

    return query.all()


# ✅ UPDATE (ONLY ADMIN + ERROR HANDLING)
@router.put("/transactions/{id}", response_model=TransactionResponse)
def update_transaction(
    id: int,
    transaction: TransactionCreate,
    user_role: str = Query(...),
    db: Session = Depends(get_db)
):
    check_role(user_role, ["admin"])

    transaction_db = db.query(Transaction).filter(Transaction.id == id).first()

    if not transaction_db:
        raise HTTPException(status_code=404, detail="Transaction not found")

    for key, value in transaction.dict().items():
        setattr(transaction_db, key, value)

    db.commit()
    db.refresh(transaction_db)

    return transaction_db


# ✅ DELETE (ONLY ADMIN + ERROR HANDLING)
@router.delete("/transactions/{id}")
def delete_transaction(
    id: int,
    user_role: str = Query(...),
    db: Session = Depends(get_db)
):
    check_role(user_role, ["admin"])

    transaction = db.query(Transaction).filter(Transaction.id == id).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.delete(transaction)
    db.commit()

    return {"message": "Transaction deleted successfully"}
