from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
from dotenv import load_dotenv
from supabase import create_client
import os

load_dotenv(override=True)

# ── Database Connection ───────────────────────────────────────────

engine = create_engine(os.getenv("DATABASE_URL"), echo=False, pool_pre_ping=True)
sessionfac=sessionmaker(bind=engine,autoflush=False)

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_ROLE_KEY")
)

def init_session():
    session=sessionfac()
    try:
        yield session
    finally:
        session.close()

session_int=Annotated[Session,Depends(init_session)]

