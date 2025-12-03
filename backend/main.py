from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
import os
from services import (
    ChatRequest, ChatResponse, GameSession,
    create_session, get_session, update_session,
    initialize_database, check_openai_connection, check_mongodb_connection,
    generate_ai_response, get_api_stats, db
)
# from prompt import get_system_prompt
from story import STORY_DATA
from characters import get_all_characters, get_system_prompt_for_character, get_character_info
from evidence import (
    get_all_evidence, get_evidence_by_id, validate_evidence_code,
    get_evidence_validation_prompt, get_evidence_discovery_message
)

# Request model for character-specific chat endpoints
class CharacterChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

# Request model for evidence discovery
class EvidenceDiscoveryRequest(BaseModel):
    session_id: str
    code: str

# Request model for evidence validation
class EvidenceValidationRequest(BaseModel):
    evidence_id: str
    code: str
    reason: str

app = FastAPI(title="Professor Richards Detective Game API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_path = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_path):
    app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.on_event("startup")
async def startup_event():
    print("🕵️ Professor Richards Detective Game API starting...")
    await initialize_database()
    print("✅ API ready!")

@app.get("/")
async def serve_ui():
    """Serve the investigation UI"""
    index_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        raise HTTPException(status_code=404, detail="UI not found")

@app.get("/api")
async def api_info():
    """API information and available endpoints"""
    return {
        "message": "Professor Richards Detective Game API",
        "status": "running",
        "case": "Murder at Professor Richards' Dinner Party",
        "endpoints": {
            "chat": "/chat - Main conversation endpoint",
            "chat_character": "/chat/{character_id} - Chat with specific character (e.g., /chat/abel, /chat/detective)",
            "health": "/health - API health check",
            "case-info": "/case-info - Basic case information",
            "characters": "/characters - List all characters",
            "evidence": "/evidence - List all evidence",
            "evidence_detail": "/evidence/{evidence_id} - Get evidence details",
            "evidence_discover_gloves": "/evidence/discover/gloves - Discover gloves (Code: GL001)",
            "evidence_discover_papers": "/evidence/discover/research_papers - Discover research papers (Code: RP002)",
            "evidence_discover_shirt": "/evidence/discover/torn_shirt - Discover torn shirt (Code: TS003)",
            "evidence_discover_button": "/evidence/discover/button - Discover button (Code: BT004)",
            "evidence_discover_knife": "/evidence/discover/knife - Discover kitchen knife (Code: KN005) - MISLEADING",
            "session_evidence": "/session/{session_id}/evidence - Get discovered evidence for session"
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
    """Main chat endpoint with character support"""

    try:
        # Validate character_id
        char_info = get_character_info(request.character_id)
        if not char_info:
            raise HTTPException(status_code=400, detail=f"Invalid character_id: {request.character_id}")

        # Create or get session
        if not request.session_id:
            session_id = await create_session(request.character_id)
            session = await get_session(session_id)
        else:
            session = await get_session(request.session_id)
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
            # Verify character_id matches the session
            if session.character_id != request.character_id:
                raise HTTPException(
                    status_code=400,
                    detail=f"Session is for character '{session.character_id}', not '{request.character_id}'"
                )
            session_id = session.id

        # Get character-specific system prompt
        system_prompt = get_system_prompt_for_character(request.character_id)

        # Prepare conversation history
        conversation_messages = [
            {"role": "system", "content": system_prompt}
        ]

        # Add previous messages from this session
        for msg in session.messages:
            # Convert character_id role to 'assistant' for OpenAI API
            role = msg["role"]
            if role not in ["system", "user", "assistant"]:
                role = "assistant"
            conversation_messages.append({
                "role": role,
                "content": msg["content"]
            })

        print('after for loop')

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
                # "role": request.character_id,  # Save character_id
                "role": "assistant",    # OpenAI restricts roles to system/user/assistant
                "content": ai_response,
                "timestamp": datetime.now().isoformat()
            }
        ])

        await update_session(session)

        return ChatResponse(
            response=ai_response,
            session_id=session_id,
            character_id=request.character_id
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {str(e)}")

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

@app.get("/characters")
async def list_characters():
    """Get list of all available characters"""
    return {
        "characters": get_all_characters()
    }

@app.get("/character/{character_id}")
async def get_character(character_id: str):
    """Get details of a specific character"""
    char_info = get_character_info(character_id)
    if not char_info:
        raise HTTPException(status_code=404, detail="Character not found")
    return char_info

@app.post("/chat/{character_id}", response_model=ChatResponse)
async def chat_with_character(character_id: str, request: CharacterChatRequest):
    """Chat endpoint for a specific character"""

    try:
        # Validate character_id
        char_info = get_character_info(character_id)
        if not char_info:
            raise HTTPException(status_code=404, detail=f"Character not found: {character_id}")

        # Create or get session
        if not request.session_id:
            session_id = await create_session(character_id)
            session = await get_session(session_id)
        else:
            session = await get_session(request.session_id)
            if not session:
                raise HTTPException(status_code=404, detail="Session not found")
            # Verify character_id matches the session
            if session.character_id != character_id:
                raise HTTPException(
                    status_code=400,
                    detail=f"Session is for character '{session.character_id}', not '{character_id}'"
                )
            session_id = session.id

        # Get character-specific system prompt
        system_prompt = get_system_prompt_for_character(character_id)

        # Prepare conversation history
        conversation_messages = [
            {"role": "system", "content": system_prompt}
        ]

        # Add previous messages from this session
        for msg in session.messages:
            # Convert character_id role to 'assistant' for OpenAI API
            role = msg["role"]
            if role not in ["system", "user", "assistant"]:
                role = "assistant"
            conversation_messages.append({
                "role": role,
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
                "role": character_id,
                "content": ai_response,
                "timestamp": datetime.now().isoformat()
            }
        ])

        await update_session(session)

        return ChatResponse(
            response=ai_response,
            session_id=session_id,
            character_id=character_id
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate response: {str(e)}")

@app.get("/history")
async def get_all_conversation_history():
    """Get all conversation history grouped by character"""
    try:
        # Get all sessions from database
        sessions_cursor = db.sessions.find({})
        sessions_list = await sessions_cursor.to_list(length=None)

        # Group sessions by character
        history_by_character = {}

        for session_data in sessions_list:
            character_id = session_data.get("character_id", "detective")

            if character_id not in history_by_character:
                char_info = get_character_info(character_id)
                history_by_character[character_id] = {
                    "character": char_info if char_info else {"id": character_id, "name": "Unknown"},
                    "sessions": []
                }

            history_by_character[character_id]["sessions"].append({
                "session_id": session_data["id"],
                "created_at": session_data["created_at"],
                "message_count": len(session_data.get("messages", [])),
                "messages": session_data.get("messages", []),
                "ended": session_data.get("ended", False)
            })

        # Sort sessions by created_at (most recent first)
        for character_id in history_by_character:
            history_by_character[character_id]["sessions"].sort(
                key=lambda x: x["created_at"],
                reverse=True
            )

        return {
            "total_characters": len(history_by_character),
            "total_sessions": len(sessions_list),
            "history": history_by_character
        }

    except Exception as e:
        print(f"Error in history endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve history: {str(e)}")

@app.get("/history/{character_id}")
async def get_character_conversation_history(character_id: str):
    """Get conversation history for a specific character"""
    try:
        # Validate character exists
        char_info = get_character_info(character_id)
        if not char_info:
            raise HTTPException(status_code=404, detail="Character not found")

        # Get all sessions for this character
        sessions_cursor = db.sessions.find({"character_id": character_id})
        sessions_list = await sessions_cursor.to_list(length=None)

        # Format sessions
        sessions_formatted = []
        for session_data in sessions_list:
            sessions_formatted.append({
                "session_id": session_data["id"],
                "created_at": session_data["created_at"],
                "message_count": len(session_data.get("messages", [])),
                "messages": session_data.get("messages", []),
                "ended": session_data.get("ended", False)
            })

        # Sort by created_at (most recent first)
        sessions_formatted.sort(key=lambda x: x["created_at"], reverse=True)

        return {
            "character": char_info,
            "total_sessions": len(sessions_formatted),
            "sessions": sessions_formatted
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in character history endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve history: {str(e)}")

@app.get("/evidence")
async def list_evidence():
    """Get list of all available evidence"""
    all_evidence = get_all_evidence()
    # Return evidence without codes and validation prompts
    evidence_list = []
    for evidence_id, evidence_data in all_evidence.items():
        evidence_list.append({
            "id": evidence_data["id"],
            "name": evidence_data["name"],
            "description": evidence_data["description"],
            "belongs_to": evidence_data["belongs_to"],
            "location": evidence_data.get("location", "Unknown")
        })
    return {"evidence": evidence_list}

@app.get("/evidence/{evidence_id}")
async def get_evidence(evidence_id: str):
    """Get details of a specific evidence (without code)"""
    evidence = get_evidence_by_id(evidence_id)
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")

    # Return evidence without code and validation prompt
    return {
        "id": evidence["id"],
        "name": evidence["name"],
        "description": evidence["description"],
        "belongs_to": evidence["belongs_to"],
        "location": evidence.get("location", "Unknown"),
        "discovery_hint": evidence.get("discovery_hint", "")
    }

@app.post("/evidence/discover/gloves")
async def discover_gloves(request: EvidenceDiscoveryRequest):
    """Discover gloves evidence (Code: GL001)"""
    return await _discover_evidence_helper(request, "gloves")

@app.post("/evidence/discover/research_papers")
async def discover_research_papers(request: EvidenceDiscoveryRequest):
    """Discover research papers evidence (Code: RP002)"""
    return await _discover_evidence_helper(request, "research_papers")

@app.post("/evidence/discover/torn_shirt")
async def discover_torn_shirt(request: EvidenceDiscoveryRequest):
    """Discover torn shirt evidence (Code: TS003)"""
    return await _discover_evidence_helper(request, "torn_shirt")

@app.post("/evidence/discover/button")
async def discover_button(request: EvidenceDiscoveryRequest):
    """Discover button evidence (Code: BT004)"""
    return await _discover_evidence_helper(request, "button")

@app.post("/evidence/discover/knife")
async def discover_knife(request: EvidenceDiscoveryRequest):
    """Discover kitchen knife evidence (Code: KN005) - MISLEADING EVIDENCE"""
    return await _discover_evidence_helper(request, "knife")

async def _discover_evidence_helper(request: EvidenceDiscoveryRequest, evidence_id: str):
    """
    Helper function to discover evidence and add validation prompt to session
    Requires correct evidence code
    """
    try:
        # Get session
        session = await get_session(request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        # Validate evidence exists
        evidence = get_evidence_by_id(evidence_id)
        if not evidence:
            raise HTTPException(status_code=404, detail="Evidence not found")

        # Validate code
        if not validate_evidence_code(evidence_id, request.code):
            raise HTTPException(status_code=400, detail="Invalid evidence code")

        # Check if already discovered
        if evidence_id in session.discovered_evidence:
            return {
                "message": "Evidence already discovered",
                "evidence": evidence["name"],
                "already_discovered": True
            }

        # Add to discovered evidence
        session.discovered_evidence.append(evidence_id)

        # Add validation prompt to session messages
        validation_prompt = get_evidence_validation_prompt(evidence_id)
        discovery_message = get_evidence_discovery_message(evidence_id)

        session.messages.append({
            "role": "system",
            "content": validation_prompt,
            "timestamp": datetime.now().isoformat(),
            "type": "evidence_discovery"
        })

        # Update session
        await update_session(session)

        return {
            "message": "Evidence discovered successfully",
            "evidence_id": evidence_id,
            "evidence_name": evidence["name"],
            "discovery_hint": discovery_message,
            "session_id": session.id,
            "ai_instruction": validation_prompt  # Show what was sent to AI
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in evidence discovery: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to discover evidence: {str(e)}")

@app.get("/session/{session_id}/evidence")
async def get_session_evidence(session_id: str):
    """Get all evidence discovered in a session"""
    session = await get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    discovered = []
    for evidence_id in session.discovered_evidence:
        evidence = get_evidence_by_id(evidence_id)
        if evidence:
            discovered.append({
                "id": evidence["id"],
                "name": evidence["name"],
                "description": evidence["description"],
                "belongs_to": evidence["belongs_to"]
            })

    return {
        "session_id": session_id,
        "discovered_evidence": discovered,
        "total_discovered": len(discovered)
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)