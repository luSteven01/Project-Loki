from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
from services import (
    ChatRequest, ChatResponse, GameSession,
    create_session, get_session, update_session,
    initialize_database, check_openai_connection, check_mongodb_connection,
    generate_ai_response, get_api_stats
)
from prompt import get_system_prompt
from story import STORY_DATA

app = FastAPI(title="Professor Richards Detective Game API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("🕵️ Professor Richards Detective Game API starting...")
    await initialize_database()
    print("✅ API ready!")

@app.get("/")
async def root():
    return {
        "message": "Professor Richards Detective Game API",
        "status": "running",
        "case": "Murder at Professor Richards' Dinner Party",
        "endpoints": {
            "chat": "/chat - Main conversation endpoint",
            "health": "/health - API health check",
            "case-info": "/case-info - Basic case information"
        }
    }

@app.get("/health")
async def health_check():
    openai_status = await check_openai_connection()
    mongodb_status = await check_mongodb_connection()

    return {
        "api": "healthy",
        "openai": openai_status,
        "mongodb": mongodb_status,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_with_detective_ai(request: ChatRequest):
    """Main chat endpoint with RAG"""

    try:
        # Create or get session
        if not request.session_id:
            session_id = await create_session()
            session = await get_session(session_id)
        else:
            session = await get_session(request.session_id)
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
            session_id = session.id

        # Prepare conversation history
        conversation_messages = [
            {"role": "system", "content": get_system_prompt()}
        ]

        # Add previous messages from this session
        for msg in session.messages:
            conversation_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        # Add current user message
        conversation_messages.append({
            "role": "user",
            "content": request.message
        })

        # Generate AI response
        ai_response = await generate_ai_response(conversation_messages)

        # Save conversation to database
        session.messages.extend([
            {
                "role": "user",
                "content": request.message,
                "timestamp": datetime.now().isoformat()
            },
            {
                "role": "assistant",
                "content": ai_response,
                "timestamp": datetime.now().isoformat()
            }
        ])

        await update_session(session)

        return ChatResponse(
            response=ai_response,
            session_id=session_id
        )

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate response")

@app.get("/session/{session_id}")
async def get_session_info(session_id: str):
    """Get session information"""
    session = await get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session_id": session.id,
        "created_at": session.created_at,
        "message_count": len(session.messages),
        "ended": session.ended
    }

@app.get("/session/{session_id}/history")
async def get_conversation_history(session_id: str):
    """Get full conversation history"""
    session = await get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session_id": session.id,
        "messages": session.messages
    }

@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    from services import db
    result = await db.sessions.delete_one({"id": session_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Session not found")

    return {"message": "Session deleted successfully"}

@app.get("/case-info")
async def get_case_info():
    """Get basic case information"""
    return {
        "case": STORY_DATA["case_overview"],
        "crime_scene": STORY_DATA["crime_scene"],
        "suspect_names": list(STORY_DATA["suspects"].keys()),
        "key_times": {
            "murder_occurred": "5:57-5:58 PM",
            "body_discovered": "7:22-7:23 PM",
            "party_started": "~5:00 PM"
        }
    }

@app.get("/suspects")
async def get_suspects_summary():
    """Get summary of all suspects"""
    suspects_summary = {}
    for name, data in STORY_DATA["suspects"].items():
        suspects_summary[name] = {
            "description": data["basic_info"],
            "motive": data["motive"],
            "key_behavior": data["behavior"]
        }
    return suspects_summary

@app.get("/timeline")
async def get_timeline():
    """Get key timeline events"""
    return {
        "critical_events": {
            "5:20-5:30 PM": "Schumacher steals research materials",
            "5:32-5:45 PM": "Abel wanders upstairs, discovers office",
            "5:45-5:50 PM": "Abel in office, finds missing research",
            "5:50-5:57 PM": "Abel argues with Professor Richards",
            "5:57-5:58 PM": "MURDER - Abel accidentally shoves Professor",
            "6:00-6:30 PM": "Abel and Diane plan cover-up",
            "6:47-6:54 PM": "Diane plants extension cord evidence",
            "7:22-7:23 PM": "Alice discovers body and screams"
        }
    }

@app.get("/stats")
async def get_stats():
    """Get API usage statistics"""
    return await get_api_stats()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)