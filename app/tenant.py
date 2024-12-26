from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from app.database import db_manager

async def get_tenant_id(request: Request) -> str:
    tenant = request.headers.get("X-Tenant-ID")
    if not tenant:
        raise HTTPException(status_code=400, detail="X-Tenant-ID header is required")
    return tenant

async def get_db(request: Request) -> Session:
    tenant = await get_tenant_id(request)
    sessionmaker = db_manager.get_sessionmaker(tenant)
    db_session = sessionmaker()
    try:
        yield db_session
    finally:
        db_session.close()