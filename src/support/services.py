from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models import ChatMessageTable


# Create a new chat message
async def create_message(db: AsyncSession, user_id: int, message: str):
    db_message = ChatMessageTable(user_id=user_id, message=message)
    db.add(db_message)
    await db.commit()  # Await commit
    await db.refresh(db_message)  # Await refresh
    return db_message

# Get chat history
async def get_chat_history(user_id:int ,db: AsyncSession, limit: int = 50):
  query = (
        select(ChatMessageTable)
        .where(ChatMessageTable.user_id == user_id)
        .order_by(ChatMessageTable.created_at.desc())
        .limit(limit)
    )
  result = await db.execute(query)
  return result.scalars().all()
