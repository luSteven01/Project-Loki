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

app = FastAPI(title="Detective Game RAG API", version="1.0.0")

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
DATABASE_NAME = os.getenv("DATABASE_NAME", "detective_game")

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
        "victim": "James Kim",
        "age": 45,
        "occupation": "cafe owner",
        "date": "March 15, 2024",
        "time": "9:30 PM",
        "location": "Mystery Cafe office",
        "cause_of_death": "head trauma from blunt object",
        "murder_weapon": "coffee grinder with blood traces found"
    },
    
    "crime_scene": {
        "description": "Office was locked from inside, window was open, papers scattered suggesting struggle",
        "evidence": [
            "blood splatter on office wall",
            "coffee grinder with blood and hair",
            "victim's phone showing missed calls",
            "office window open (unusual for March weather)",
            "desk drawer was forced open"
        ]
    },
    
    "suspects": {
        "Sarah Kim": {
            "basic_info": "28-year-old barista, worked at cafe for 3 years, single mother with financial struggles",
            "timeline": {
                "9:00 PM": "serving last customers in main hall, confirmed by CCTV and witnesses",
                "9:15 PM": "washing dishes in kitchen with coworker Jenny until 9:20 PM",
                "9:30 PM": "claims she was in staff bathroom - NO WITNESSES OR ALIBI",
                "9:45 PM": "found back in main hall, called police after hearing 'noise' from office"
            },
            "motive": "recently passed over for promotion despite being promised the position 6 months ago. James hired external candidate instead. Also facing severe financial pressure as single mother.",
            "relationship": "professional relationship deteriorated recently. James criticized her work and threatened to reduce her hours due to 'attitude problems'",
            "physical_evidence": "small fresh cut on right hand (claims from broken glass), knows coffee grinder operation very well",
            "behavior": "usually calm and controlled but colleagues noticed increased irritability. Fidgets when discussing James. Avoids eye contact when asked about 9:30 PM timeframe",
            "statements": {
                "about_promotion": "He promised me that position six months ago. Then suddenly hired some outsider. Said I wasn't management material.",
                "about_timeline": "I went to bathroom around 9:30. Is that a crime? I didn't see anything unusual.",
                "about_relationship": "James wasn't easy to work for but I would never hurt anyone. I needed this job."
            },
            "key_facts": "ACTUAL MURDERER - lied about bathroom alibi, had means (grinder knowledge), motive (promotion/money), and opportunity (no alibi at 9:30)"
        },
        
        "Michael Park": {
            "basic_info": "52-year-old businessman, James's former business partner, forced out 6 months ago",
            "timeline": {
                "9:00 PM": "claims he was at home watching TV, lives alone since divorce",
                "9:15 PM": "still at home according to his account",
                "9:30 PM": "went to corner store, bought cigarettes - CONFIRMED by receipt and CCTV at 9:35 PM",
                "9:45 PM": "walking back home, saw police cars heading toward cafe area"
            },
            "motive": "lost significant money when forced out of cafe partnership. James bought him out below market value. Recently filed lawsuit for additional compensation",
            "relationship": "former best friends turned bitter enemies over money. Had public arguments about business decisions",
            "physical_evidence": "no direct connection to crime scene. Phone records show no calls during relevant time",
            "behavior": "intelligent but bitter, feels victimized by James. Controlled anger but no history of violence",
            "statements": {
                "about_partnership": "He cheated me out of thousands. Promised equal partnership then pushed me out. Classic narcissist.",
                "about_timeline": "I was home feeling sorry for myself, then went for cigarettes. Pathetic evening but I have receipts.",
                "about_violence": "I handle problems through lawyers, not violence. Killing him wouldn't get my money back."
            },
            "key_facts": "has strong motive but SOLID ALIBI - store receipt and CCTV confirm he was buying cigarettes at time of murder"
        },
        
        "Emma Wilson": {
            "basic_info": "42-year-old marketing consultant, James's estranged wife, currently in divorce proceedings",
            "timeline": {
                "9:00 PM": "at home helping children (ages 8 and 10) with homework - children confirm",
                "9:15 PM": "putting children to bed, reading bedtime stories",
                "9:30 PM": "children asleep, alone in living room watching Netflix - viewing history confirms",
                "9:45 PM": "tried calling James about weekend visitation, left voicemail - phone records confirm"
            },
            "motive": "contentious divorce with James hiding assets and threatening full custody of children",
            "relationship": "marriage emotionally dead for 2 years. James became controlling and financially manipulative",
            "physical_evidence": "has spare key to cafe office but key is MISSING from her keychain",
            "behavior": "strong-willed, protective of children. Shows relief when discussing James in past tense",
            "statements": {
                "about_marriage": "James changed after cafe success. Became obsessed with control, treated me like employee.",
                "about_children": "My kids are my priority now, not James and his problems.",
                "about_missing_key": "I'm not sure where that key went. Maybe lost it during the move to new house."
            },
            "key_facts": "has motive and missing office key, but was with children during crucial timeline - children provide alibi"
        },
        
        "David Chen": {
            "basic_info": "35-year-old tech entrepreneur, frequent customer and recent investor in cafe",
            "timeline": {
                "9:00 PM": "at cafe discussing business with James, conversation became heated",
                "9:15 PM": "argument escalated, James accused David of trying to take over business - witnessed by customers",
                "9:30 PM": "claims he left angrily and went to his car - NO WITNESSES to departure",
                "9:45 PM": "in parking lot making phone calls to investors - phone records verify"
            },
            "motive": "discovered James was using his $50,000 investment for personal expenses instead of cafe expansion",
            "relationship": "started as mutual respect, became suspicious when James was evasive about financial records",
            "physical_evidence": "fingerprints on office door handle (explains he touched it looking for James after argument)",
            "behavior": "smooth talker who becomes aggressive when cornered. Very knowledgeable about cafe finances and layout",
            "statements": {
                "about_investment": "He took my 50K and used it for God knows what. The expansion plans were fake.",
                "about_argument": "I told him I wanted my money back or I'd expose him. He got defensive and started yelling.",
                "about_timeline": "I was angry but I'm a businessman, not a thug. I left to cool down and consider legal options."
            },
            "key_facts": "left cafe around murder time with no witnesses, but phone records show he was making calls in parking lot at 9:45"
        }
    }
}

# RAG system prompt
def get_system_prompt():
    return f"""
You are an AI detective assistant helping investigate a murder case. You have access to case files, witness statements, and evidence.

CASE: Mystery Cafe Murder
VICTIM: James Kim (45, cafe owner) 
TIME: March 15, 2024, 9:30 PM
LOCATION: Mystery Cafe office
WEAPON: Coffee grinder

CRIME SCENE: {STORY_DATA['crime_scene']['description']}

EVIDENCE FOUND: {', '.join(STORY_DATA['crime_scene']['evidence'])}

SUSPECTS AND DETAILS:

1. SARAH KIM (28, barista):
{STORY_DATA['suspects']['Sarah Kim']['basic_info']}
Timeline: {' | '.join([f"{time}: {action}" for time, action in STORY_DATA['suspects']['Sarah Kim']['timeline'].items()])}
Motive: {STORY_DATA['suspects']['Sarah Kim']['motive']}
Key Evidence: {STORY_DATA['suspects']['Sarah Kim']['physical_evidence']}
Behavior: {STORY_DATA['suspects']['Sarah Kim']['behavior']}

2. MICHAEL PARK (52, ex-business partner):
{STORY_DATA['suspects']['Michael Park']['basic_info']}
Timeline: {' | '.join([f"{time}: {action}" for time, action in STORY_DATA['suspects']['Michael Park']['timeline'].items()])}
Motive: {STORY_DATA['suspects']['Michael Park']['motive']}
Key Evidence: {STORY_DATA['suspects']['Michael Park']['physical_evidence']}

3. EMMA WILSON (42, victim's wife):
{STORY_DATA['suspects']['Emma Wilson']['basic_info']}
Timeline: {' | '.join([f"{time}: {action}" for time, action in STORY_DATA['suspects']['Emma Wilson']['timeline'].items()])}
Motive: {STORY_DATA['suspects']['Emma Wilson']['motive']}
Key Evidence: {STORY_DATA['suspects']['Emma Wilson']['physical_evidence']}

4. DAVID CHEN (35, investor):
{STORY_DATA['suspects']['David Chen']['basic_info']}
Timeline: {' | '.join([f"{time}: {action}" for time, action in STORY_DATA['suspects']['David Chen']['timeline'].items()])}
Motive: {STORY_DATA['suspects']['David Chen']['motive']}
Key Evidence: {STORY_DATA['suspects']['David Chen']['physical_evidence']}

INSTRUCTIONS:
- Answer questions about the case using the information provided above
- Never directly reveal that Sarah Kim is the murderer
- Provide factual information from case files and evidence
- Help the detective analyze clues and make connections
- When discussing alibis, emphasize who has witnesses vs who doesn't
- Point out suspicious behaviors and inconsistencies when asked
- Encourage deeper investigation with follow-up questions
- Keep responses conversational and engaging like a real detective partner
- If asked about your analysis or who you suspect, provide careful reasoning without giving away the answer
"""

# Database models
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
    print("🕵️ Detective Game API starting...")
    # Create database index
    await db.sessions.create_index("id", unique=True)
    print("✅ API ready!")

@app.get("/")
async def root():
    return {
        "message": "Detective Game RAG API", 
        "status": "running",
        "endpoints": {
            "chat": "/chat - Main conversation endpoint",
            "health": "/health - API health check"
        }
    }

@app.get("/health")
async def health_check():
    try:
        # Test OpenAI connection
        test_response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        openai_status = "connected"
    except:
        openai_status = "error"
    
    try:
        # Test MongoDB connection
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
        "suspect_names": list(STORY_DATA["suspects"].keys())
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
        "average_messages_per_session": round(total_message_count / total_sessions, 1) if total_sessions > 0 else 0
    }

def get_system_prompt():
    return f"""
You are an AI detective assistant helping investigate a murder case at Mystery Cafe. You have complete access to case files, witness statements, evidence, and suspect profiles.

CASE DETAILS:
Victim: {STORY_DATA['case_overview']['victim']} ({STORY_DATA['case_overview']['age']}, {STORY_DATA['case_overview']['occupation']})
When: {STORY_DATA['case_overview']['date']} at {STORY_DATA['case_overview']['time']}
Where: {STORY_DATA['case_overview']['location']}
How: {STORY_DATA['case_overview']['cause_of_death']}
Weapon: {STORY_DATA['case_overview']['murder_weapon']}

CRIME SCENE:
{STORY_DATA['crime_scene']['description']}
Evidence found: {', '.join(STORY_DATA['crime_scene']['evidence'])}

SUSPECT PROFILES:

SARAH KIM (Barista):
- Profile: {STORY_DATA['suspects']['Sarah Kim']['basic_info']}
- 9:00 PM: {STORY_DATA['suspects']['Sarah Kim']['timeline']['9:00 PM']}
- 9:15 PM: {STORY_DATA['suspects']['Sarah Kim']['timeline']['9:15 PM']}  
- 9:30 PM: {STORY_DATA['suspects']['Sarah Kim']['timeline']['9:30 PM']} ⚠️ NO ALIBI
- 9:45 PM: {STORY_DATA['suspects']['Sarah Kim']['timeline']['9:45 PM']}
- Motive: {STORY_DATA['suspects']['Sarah Kim']['motive']}
- Evidence: {STORY_DATA['suspects']['Sarah Kim']['physical_evidence']}
- Behavior: {STORY_DATA['suspects']['Sarah Kim']['behavior']}

MICHAEL PARK (Ex-partner):
- Profile: {STORY_DATA['suspects']['Michael Park']['basic_info']}
- 9:30 PM: {STORY_DATA['suspects']['Michael Park']['timeline']['9:30 PM']} ✅ CONFIRMED ALIBI
- Motive: {STORY_DATA['suspects']['Michael Park']['motive']}
- Evidence: {STORY_DATA['suspects']['Michael Park']['physical_evidence']}

EMMA WILSON (Wife):
- Profile: {STORY_DATA['suspects']['Emma Wilson']['basic_info']}
- 9:00-9:15 PM: {STORY_DATA['suspects']['Emma Wilson']['timeline']['9:15 PM']}
- 9:30 PM: {STORY_DATA['suspects']['Emma Wilson']['timeline']['9:30 PM']}
- Motive: {STORY_DATA['suspects']['Emma Wilson']['motive']}
- Evidence: {STORY_DATA['suspects']['Emma Wilson']['physical_evidence']}

DAVID CHEN (Investor):
- Profile: {STORY_DATA['suspects']['David Chen']['basic_info']}
- 9:15 PM: {STORY_DATA['suspects']['David Chen']['timeline']['9:15 PM']}
- 9:30 PM: {STORY_DATA['suspects']['David Chen']['timeline']['9:30 PM']} ⚠️ NO WITNESSES
- 9:45 PM: {STORY_DATA['suspects']['David Chen']['timeline']['9:45 PM']}
- Motive: {STORY_DATA['suspects']['David Chen']['motive']}

INSTRUCTIONS:
- Help the detective analyze the case by providing information from the files above
- Never directly say "Sarah Kim is the murderer" - let the detective figure it out
- When asked about alibis, emphasize who has confirmed witnesses vs who doesn't
- Point out key evidence like the missing office key, suspicious behavior, access to murder weapon
- Encourage analysis of timeline gaps and inconsistencies
- Answer questions about motives, relationships, and evidence factually
- If asked for your analysis, point toward suspicious elements without directly accusing
- Keep responses conversational like talking to a partner detective
- When detective asks about specific times (9:30 PM), emphasize who has/doesn't have alibis
"""

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
