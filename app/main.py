import asyncio
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update, text
from . import database
from pydantic import BaseModel, ConfigDict
from .config import settings
from typing import List
import random

app = FastAPI(
    title="Locust RDB Test",
    debug=settings.DEBUG
)

class DeeplinkUpdate(BaseModel):
    app_id: int

class DeeplinkResponse(BaseModel):
    id: int
    app_id: int
    path: str

    model_config = ConfigDict(from_attributes=True)

async def get_db():
    async with database.AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

@app.get("/deeplinks/", response_model=List[DeeplinkResponse])
async def get_deeplinks(
    skip: int = 0, 
    limit: int = 100, 
    db: AsyncSession = Depends(get_db)
):
    query = select(database.Deeplink).offset(skip).limit(limit)
    result = await db.execute(query)
    deeplinks = result.scalars().all()
    return deeplinks

@app.put("/deeplinks/random", response_model=DeeplinkResponse)
async def update_random_deeplink(db: AsyncSession = Depends(get_db)):
    # 랜덤으로 하나의 레코드 선택
    query = select(database.Deeplink).filter(database.Deeplink.id == random.randint(1, 127862393)).limit(1)
    result = await db.execute(query)
    deeplink = result.scalar_one_or_none()
    
    if not deeplink:
        raise HTTPException(status_code=404, detail="No deeplinks found")
    
    # 새로운 랜덤 app_id 생성
    new_app_id = random.randint(1, 127862393)
    
    # 선택된 레코드의 app_id 업데이트
    update_stmt = (
        update(database.Deeplink)
        .where(database.Deeplink.id == deeplink.id)
        .values(app_id=new_app_id)
    )
    await db.execute(update_stmt)
    await db.commit()
    
    # 업데이트된 레코드 반환
    deeplink.app_id = new_app_id
    return deeplink

async def get_random_deeplink_with_lock(db: AsyncSession):
    # FOR UPDATE와 함께 랜덤 레코드 선택
    query = (
        select(database.Deeplink)
        .filter(database.Deeplink.id == random.randint(1, 127862393))
        .limit(1)
        .with_for_update()
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

@app.put("/deeplinks/random-with-lock", response_model=DeeplinkResponse)
async def update_random_deeplink_with_lock(db: AsyncSession = Depends(get_db)):
    # 트랜잭션 시작
    async with db.begin():
        # 락과 함께 랜덤 레코드 선택
        deeplink = await get_random_deeplink_with_lock(db)
        
        if not deeplink:
            raise HTTPException(status_code=404, detail="No deeplinks found")
        
        # 1초 슬립
        await asyncio.sleep(1)
        
        # 새로운 랜덤 app_id 생성
        new_app_id = random.randint(1, 127862393)
        
        # 선택된 레코드의 app_id 업데이트
        update_stmt = (
            update(database.Deeplink)
            .where(database.Deeplink.id == deeplink.id)
            .values(app_id=new_app_id)
        )
        await db.execute(update_stmt)
        
        # 업데이트된 레코드 반환
        deeplink.app_id = new_app_id
        return deeplink