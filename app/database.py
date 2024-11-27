from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from .config import settings

# 비동기 엔진 생성
engine = create_async_engine(
    f"mysql+aiomysql://{settings.DB_USER}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}",
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
    connect_args={
        "charset": "utf8mb4",
        "password": settings.DB_PASSWORD
    }
)

# 비동기 세션 생성
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

class Deeplink(Base):
    __tablename__ = "tbl_sl_deeplink_params"

    id = Column(Integer, primary_key=True, autoincrement=True)
    app_id = Column(Integer, nullable=True)
    path = Column(String(1024), nullable=True) 