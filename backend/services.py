from pydantic import BaseModel
from typing import List, Optional
import os
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from openai import AsyncOpenAI
import uuid
from dotenv import load_dotenv

load_dotenv()

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key")
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "professor_richards_case")

print(f"🔑 OpenAI API Key: {OPENAI_API_KEY[:20]}...")
print(f"🔗 MongoDB URL: {MONGODB_URL[:50]}...")
print(f"📁 Database: {DATABASE_NAME}")

# Initialize clients
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
mongodb_client = AsyncIOMotorClient(MONGODB_URL, tlsAllowInvalidCertificates=True)
db = mongodb_client[DATABASE_NAME]

# Pydantic models
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

class GameSession(BaseModel):
    id: str
    created_at: datetime
    messages: List[dict] = []
    ended: bool = False


# Database operations
async def create_session() -> str:
    """Create new game session"""
    session_id = str(uuid.uuid4())
    session = GameSession(
        id=session_id,
        created_at=datetime.now()
    )
    await db.sessions.insert_one(session.dict())
    return session_id

async def get_session(session_id: str) -> Optional[GameSession]:
    """Get session from database"""
    session_data = await db.sessions.find_one({"id": session_id})
    if session_data:
        return GameSession(**session_data)
    return None

async def update_session(session: GameSession):
    """Update session in database"""
    await db.sessions.update_one(
        {"id": session.id},
        {"$set": session.dict()}
    )

async def initialize_database():
    """Initialize database indexes"""
    await db.sessions.create_index("id", unique=True)

async def check_openai_connection():
    """Check OpenAI API connection"""
    try:
        test_response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        return "connected"
    except:
        return "error"

async def check_mongodb_connection():
    """Check MongoDB connection"""
    try:
        await db.sessions.find_one()
        return "connected"
    except:
        return "error"

async def generate_ai_response(conversation_messages: List[dict]) -> str:
    """Generate AI response using OpenAI"""
    response = await openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation_messages,
        temperature=0.7,
        max_tokens=800
    )
    return response.choices[0].message.content

async def get_api_stats():
    """Get API usage statistics"""
    total_sessions = await db.sessions.count_documents({})
    total_messages = await db.sessions.aggregate([
        {"$unwind": "$messages"},
        {"$count": "total"}
    ]).to_list(length=1)

    total_message_count = total_messages[0]["total"] if total_messages else 0

    return {
        "total_sessions": total_sessions,
        "total_messages": total_message_count,
        "average_messages_per_session": round(total_message_count / total_sessions, 1) if total_sessions > 0 else 0,
        "case_type": "Professor Richards Murder Investigation"
    }