from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from openai import AsyncOpenAI
import uuid
from dotenv import load_dotenv 

load_dotenv()

app = FastAPI(title="Professor Richards Detective Game API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment variables 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-openai-api-key")
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "professor_richards_case")

print(f"🔑 OpenAI API Key: {OPENAI_API_KEY[:20]}...")
print(f"🔗 MongoDB URL: {MONGODB_URL[:50]}...")
print(f"📁 Database: {DATABASE_NAME}")

# Initialize clients
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
mongodb_client = AsyncIOMotorClient(MONGODB_URL)
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

# Story database for RAG
STORY_DATA = {
    "case_overview": {
        "victim": "Professor Richards",
        "age": "retirement age",
        "occupation": "university professor",
        "date": "dinner party evening",
        "time_of_death": "5:57-5:58 PM",
        "location": "Professor Richards' office in his house",
        "cause_of_death": "head trauma from hitting desk edge",
        "murder_weapon": "blunt force from desk edge after being shoved",
        "discovery_time": "7:22-7:23 PM by Alice"
    },
    
    "crime_scene": {
        "description": "Professor's home office, door was found open, Professor found unconscious on floor with head injury",
        "evidence": [
            "Professor found on office floor with head trauma",
            "Missing research materials from office",
            "Extension cord placed near body (planted by Diane)",
            "Office door was open when Alice discovered body",
            "Research dossier was empty/missing papers"
        ]
    },
    
    "suspects": {
        "Abel": {
            "basic_info": "Professor Richards' former student, ambitious Software Engineering student aiming for FAANG job, Diane's son",
            "timeline": {
                "5:02 PM": "arrives at party with mother Diane",
                "5:31 PM": "excuses self to use bathroom, first floor bathroom busy",
                "5:32 PM": "checks second floor bathroom, also busy (Schumacher inside)",
                "5:32-5:45 PM": "wanders second floor hallway, discovers Professor's office with door cracked open",
                "5:45-5:50 PM": "enters office, notices Professor's research dossier is missing papers",
                "5:50-5:57 PM": "argues with Professor Richards when caught in office",
                "5:57-5:58 PM": "accidentally shoves Professor Richards, who hits head on desk edge",
                "5:58-6:00 PM": "panics, goes downstairs to find mother",
                "6:00-6:30 PM": "discusses cover-up plan with mother Diane on front porch"
            },
            "motive": "curiosity about missing research materials, then panic after accidental killing",
            "relationship": "former student, generally respectful but gets lost in his own world when focused",
            "physical_evidence": "was in office at time of death, had access and opportunity",
            "behavior": "ambitious, easily distracted, tends to wander when bored, panics under pressure",
            "key_facts": "ACTUAL KILLER - accidentally killed Professor during confrontation, mother helped cover up"
        },
        
        "Diane": {
            "basic_info": "Abel's mother, dean of the university, helps cover up Abel's crime",
            "timeline": {
                "5:02 PM": "arrives with son Abel",
                "5:30-5:45 PM": "accidentally spills drink on Professor's shirt in living room, Alice witnesses",
                "5:45-6:00 PM": "takes breather on front porch with Schumacher",
                "6:00-6:30 PM": "meets with Abel on front porch, learns about accident, plans cover-up",
                "6:30-6:43 PM": "examines Professor's office alone",
                "6:43-6:47 PM": "goes to car, retrieves extension cord from trunk",
                "6:47-6:54 PM": "returns to office, places extension cord near body to stage accident",
                "6:54-7:20 PM": "hides in upstairs bathroom to avoid being seen",
                "7:21-7:22 PM": "leaves bathroom when Alice screams"
            },
            "motive": "protecting her son Abel from murder charges",
            "relationship": "Abel's mother, university dean, respected academic",
            "physical_evidence": "tampered with crime scene by adding extension cord",
            "behavior": "protective mother, intelligent, capable of planning cover-up",
            "key_facts": "ACCESSORY AFTER THE FACT - helped stage scene to look like accident, planted evidence"
        },
        
        "Professor Schumacher": {
            "basic_info": "Professor Richards' colleague, jealous of credit for research projects",
            "timeline": {
                "5:01 PM": "arrives at party",
                "5:20-5:25 PM": "excuses self, secretly goes to Professor's office",
                "5:25-5:30 PM": "steals research materials from office for his own use",
                "5:30-5:34 PM": "hides in upper floor bathroom (Abel tries to use this bathroom)",
                "5:34-5:50 PM": "wanders front porch, seen by Diane",
                "5:50-6:30 PM": "converses with Adele (Professor's wife) in kitchen"
            },
            "motive": "jealousy over Professor taking credit for collaborative research, theft of research materials",
            "relationship": "colleague and collaborator, but growing resentment over recognition",
            "physical_evidence": "stole research materials before murder occurred",
            "behavior": "jealous, opportunistic, sneaky behavior around research theft",
            "key_facts": "stole research materials but BEFORE the murder happened - not the killer but committed theft"
        },
        
        "Alice": {
            "basic_info": "Professor Richards' estranged daughter, poses as his TA at the party",
            "timeline": {
                "5:03 PM": "arrives at party, introduces self as Professor's TA",
                "5:19-5:23 PM": "uses and clogs first floor bathroom",
                "6:00-6:12 PM": "takes walk on front porch, overhears Diane and Abel discussing 'missing papers'",
                "6:12-7:15 PM": "helps prepare dishes in dining room (NO WITNESSES 6:12-6:45 PM)",
                "7:18-7:22 PM": "searches house looking for Professor Richards and Diane",
                "7:22-7:23 PM": "discovers Professor's body in office, screams to alert everyone"
            },
            "motive": "wanted to confront father about their estranged relationship, reveal identity as his daughter",
            "relationship": "estranged daughter posing as TA, seeking reconciliation",
            "physical_evidence": "discovered the body, had period with no witnesses",
            "behavior": "secretive about true identity, emotional about father relationship",
            "key_facts": "victim's daughter in disguise, discovered body but NOT the killer"
        },
        
        "Adele": {
            "basic_info": "Professor Richards' wife, helps with party hosting and cooking",
            "timeline": {
                "5:02-5:30 PM": "conversations with party guests in living room",
                "5:30-5:50 PM": "helps chef in kitchen",
                "5:50-6:30 PM": "extended conversation with Schumacher in kitchen (suspicious timing)",
                "6:30 PM onward": "hosting duties and party activities"
            },
            "motive": "marital relationship details unclear, possibly suspicious conversation timing with Schumacher",
            "relationship": "wife, party hostess",
            "physical_evidence": "no direct evidence linking to crime",
            "behavior": "dutiful wife and hostess, but suspicious private conversation with Schumacher",
            "key_facts": "had suspicious timing with Schumacher but no clear evidence of involvement in murder"
        }
    }
}

def get_system_prompt():
    return f"""
You are an AI detective assistant helping investigate a murder case at Professor Richards' house during a dinner party.

CASE: Professor Richards Murder Investigation
VICTIM: Professor Richards (university professor, recently retired)
WHEN: During dinner party at his home, death occurred 5:57-5:58 PM
WHERE: Professor's home office  
HOW: Head trauma from hitting desk edge after being shoved
DISCOVERED: 7:22-7:23 PM by Alice, who screamed and alerted everyone

CRIME SCENE: {STORY_DATA['crime_scene']['description']}

EVIDENCE FOUND: {', '.join(STORY_DATA['crime_scene']['evidence'])}

SUSPECT PROFILES:

ABEL (Student/Son):
- Profile: {STORY_DATA['suspects']['Abel']['basic_info']}
- Key Timeline: 5:32-5:45 PM wandering upstairs hallway | 5:45-5:50 PM in Professor's office discovering missing research | 5:50-5:57 PM arguing with Professor | 5:57-5:58 PM accidentally shoves Professor (MOMENT OF DEATH) | 5:58-6:30 PM planning cover-up with mother
- Motive: {STORY_DATA['suspects']['Abel']['motive']}
- Behavior: {STORY_DATA['suspects']['Abel']['behavior']}

DIANE (Mother/Dean):
- Profile: {STORY_DATA['suspects']['Diane']['basic_info']}  
- Key Timeline: 6:00-6:30 PM learns about accident, plans cover-up | 6:43-6:54 PM plants extension cord near body to stage accident | 6:54-7:20 PM hiding in bathroom
- Motive: {STORY_DATA['suspects']['Diane']['motive']}
- Evidence: {STORY_DATA['suspects']['Diane']['physical_evidence']}

PROFESSOR SCHUMACHER (Colleague):
- Profile: {STORY_DATA['suspects']['Professor Schumacher']['basic_info']}
- Key Timeline: 5:20-5:30 PM steals research materials from office BEFORE murder | 5:50-6:30 PM suspicious long conversation with Adele in kitchen
- Motive: {STORY_DATA['suspects']['Professor Schumacher']['motive']}
- Evidence: {STORY_DATA['suspects']['Professor Schumacher']['physical_evidence']}

ALICE (Daughter):
- Profile: {STORY_DATA['suspects']['Alice']['basic_info']}
- Key Timeline: 6:00-6:12 PM overhears discussion about "missing papers" | 6:12-6:45 PM NO WITNESSES | 7:22-7:23 PM discovers body and screams
- Motive: {STORY_DATA['suspects']['Alice']['motive']}
- Behavior: {STORY_DATA['suspects']['Alice']['behavior']}

ADELE (Wife):
- Profile: {STORY_DATA['suspects']['Adele']['basic_info']}
- Key Timeline: 5:50-6:30 PM extended private conversation with Schumacher in kitchen during critical time period
- Relationship: {STORY_DATA['suspects']['Adele']['relationship']}

INSTRUCTIONS:
- Help investigate this complex murder case involving family secrets and academic rivalries
- Never directly reveal that Abel is the accidental killer or that Diane helped cover it up
- Focus on timeline inconsistencies, missing alibis, and suspicious behavior
- Point out when suspects had opportunity, means, and motive
- Note that research materials were stolen BEFORE the murder occurred
- Emphasize the importance of the 5:57-5:58 PM timeframe (actual murder) vs 7:22-7:23 PM (discovery)
- Help analyze the staged crime scene with the planted extension cord
- Encourage investigation of family relationships and hidden identities
- Point out suspicious timing of various activities during the party
- Keep responses engaging like a detective partner analyzing clues
"""

# Database operations (same as original)
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

@app.on_event("startup")
async def startup_event():
    print("🕵️ Professor Richards Detective Game API starting...")
    await db.sessions.create_index("id", unique=True)
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
    try:
        test_response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        openai_status = "connected"
    except:
        openai_status = "error"
    
    try:
        await db.sessions.find_one()
        mongodb_status = "connected"
    except:
        mongodb_status = "error"
    
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
        
        # Generate AI response using OpenAI
        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_messages,
            temperature=0.7,
            max_tokens=800
        )
        
        ai_response = response.choices[0].message.content
        
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)