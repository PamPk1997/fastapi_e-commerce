from fastapi import APIRouter, WebSocket,WebSocketDisconnect,Depends
from typing import List,Dict
from sqlalchemy.ext.asyncio import AsyncSession 
from config.database import get_async_db
from src.support.services import create_message,get_chat_history


chat_router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: str):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_message(self, message: str, user_id: str):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_text(message)

    async def broadcast(self, message: str):
        for user_id, connections in self.active_connections.items():
            for connection in connections:
                await connection.send_text(message)


manager = ConnectionManager()


@chat_router.websocket("/support/chat/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str, db: AsyncSession = Depends(get_async_db)):
    await manager.connect(websocket, user_id)
    try:
        # Load and send chat history
        chat_history = await get_chat_history(user_id=user_id, db=db, limit=50)
        for message in chat_history:
            await websocket.send_text(message)

        while True:
            data = await websocket.receive_json()
            message_type = data.get("type")
            if message_type == "message": 
                message_content = data.get("content")
                # Save message to DB
                await create_message(user_id, message_content, db)
                # Send message to recipient
                await manager.send_message(data.get("content"), data.get("recipient"))
            elif message_type == "file":
                # Handle file metadata
                file_name = data.get("name")
                file_type = data.get("fileType")
                # Process the file further (e.g., save to storage, send notifications)
                await manager.send_message(f"File received: {file_name}", data.get("recipient"))
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)