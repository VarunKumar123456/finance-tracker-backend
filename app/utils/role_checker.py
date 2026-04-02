from fastapi import HTTPException

def check_role(user_role: str, allowed_roles: list):
    if user_role not in allowed_roles:
        raise HTTPException(
            status_code=403,
            detail=f"Access denied for role: {user_role}"
        )
