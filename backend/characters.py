# Character definitions for the detective game
from story import STORY_DATA

CHARACTERS = {
    "detective": {
        "id": "detective",
        "name": "Detective AI",
        "role": "AI Detective Assistant",
        "description": "An AI detective assistant helping you investigate the murder case",
        "avatar": "🕵️",
        "system_prompt_generator": lambda: get_detective_prompt()
    },
    "abel": {
        "id": "abel",
        "name": "Abel",
        "role": "Former Student",
        "description": "Professor Richards' former student, ambitious Software Engineering student",
        "avatar": "👨‍💻",
        "system_prompt_generator": lambda: get_suspect_prompt("Abel")
    },
    "diane": {
        "id": "diane",
        "name": "Diane",
        "role": "University Dean",
        "description": "Abel's mother, dean of the university",
        "avatar": "👩‍💼",
        "system_prompt_generator": lambda: get_suspect_prompt("Diane")
    },
    "schumacher": {
        "id": "schumacher",
        "name": "Professor Schumacher",
        "role": "Colleague",
        "description": "Professor Richards' colleague, jealous of credit for research projects",
        "avatar": "👨‍🏫",
        "system_prompt_generator": lambda: get_suspect_prompt("Professor Schumacher")
    },
    "alice": {
        "id": "alice",
        "name": "Alice",
        "role": "TA (Actually Daughter)",
        "description": "Professor Richards' estranged daughter, posing as his TA",
        "avatar": "👩‍🎓",
        "system_prompt_generator": lambda: get_suspect_prompt("Alice")
    },
    "adele": {
        "id": "adele",
        "name": "Adele",
        "role": "Wife",
        "description": "Professor Richards' wife, party hostess",
        "avatar": "👩‍🦰",
        "system_prompt_generator": lambda: get_suspect_prompt("Adele")
    },
    "chef": {
        "id": "chef",
        "name": "The Chef",
        "role": "Personal Chef",
        "description": "Personal chef responsible for cooking food at the dinner party",
        "avatar": "👨‍🍳",
        "system_prompt_generator": lambda: get_suspect_prompt("The Chef")
    },
    "maid": {
        "id": "maid",
        "name": "The Maid",
        "role": "Maid",
        "description": "Maid that greets everyone at the party and tends to household tasks",
        "avatar": "👩‍🦳",
        "system_prompt_generator": lambda: get_suspect_prompt("The Maid")
    }
}

def get_detective_prompt() -> str:
    """Generate system prompt for detective AI assistant"""
    case_info = STORY_DATA["case_overview"]
    crime_scene = STORY_DATA["crime_scene"]
    suspects = STORY_DATA["suspects"]

    prompt = f"""You are an AI detective assistant helping investigate a murder case.

**CASE OVERVIEW:**
Victim: {case_info['victim']}, {case_info['age']} {case_info['occupation']}
Time of Death: {case_info['time_of_death']}
Location: {case_info['location']}
Cause of Death: {case_info['cause_of_death']}
Discovered: {case_info['discovery_time']}

**CRIME SCENE:**
{crime_scene['description']}

**EVIDENCE FOUND:**
"""
    for evidence in crime_scene['evidence']:
        prompt += f"- {evidence}\n"

    prompt += "\n**SUSPECTS:**\n"
    for name, data in suspects.items():
        prompt += f"\n**{name}:**\n"
        prompt += f"- {data['basic_info']}\n"
        prompt += f"- Motive: {data['motive']}\n"
        prompt += f"- Behavior: {data['behavior']}\n"

    prompt += """

**YOUR ROLE:**
- Help the investigator analyze evidence and suspect behavior
- Ask probing questions to uncover the truth
- Provide insights based on the evidence and timelines
- Guide the investigation towards solving the case
- Be professional, analytical, and thorough in your responses

**IMPORTANT:**
- You know all the facts about the case but should reveal them gradually
- Encourage the investigator to think critically
- Don't immediately reveal who the killer is - let them figure it out
- Provide helpful hints when they're stuck
"""

    return prompt

def get_suspect_prompt(suspect_name: str) -> str:
    """Generate system prompt for a suspect character"""
    suspect_data = STORY_DATA["suspects"][suspect_name]

    prompt = f"""You are roleplaying as {suspect_name} in a murder investigation scenario.

**YOUR CHARACTER:**
{suspect_data['basic_info']}

**YOUR TIMELINE (what you actually did):**
"""

    for time, action in suspect_data['timeline'].items():
        prompt += f"- {time}: {action}\n"

    prompt += f"""
**YOUR MOTIVE:**
{suspect_data['motive']}

**YOUR RELATIONSHIP TO VICTIM:**
{suspect_data['relationship']}

**YOUR BEHAVIOR/PERSONALITY:**
{suspect_data['behavior']}

**KEY FACTS YOU KNOW:**
{suspect_data['key_facts']}

**ROLEPLAY INSTRUCTIONS:**
- Stay in character as {suspect_name}
- Answer questions from the investigator's perspective
- You may be evasive about certain details, especially if they incriminate you
- Show your personality and emotions appropriate to the situation
- If you're guilty or hiding something, show nervousness or defensiveness when appropriate
- If you're innocent, you may be confused, scared, or eager to help
- Don't volunteer information that would immediately solve the case
- Be realistic - people don't always remember every detail perfectly
- You may lie or withhold information to protect yourself or others
- React emotionally when appropriate (fear, anger, sadness, defensiveness)

**IMPORTANT:**
- Do NOT break character
- Do NOT explain the entire case or reveal everything at once
- Let information come out naturally through conversation
- Show human emotions and realistic reactions
"""

    return prompt

def get_character_info(character_id: str) -> dict:
    """Get character information without the prompt generator"""
    if character_id not in CHARACTERS:
        return None

    char = CHARACTERS[character_id].copy()
    # Remove the prompt generator from the returned info
    char.pop('system_prompt_generator', None)
    return char

def get_all_characters() -> list:
    """Get list of all available characters"""
    return [
        {
            "id": char_id,
            "name": char_data["name"],
            "role": char_data["role"],
            "description": char_data["description"],
            "avatar": char_data["avatar"]
        }
        for char_id, char_data in CHARACTERS.items()
    ]

def get_system_prompt_for_character(character_id: str) -> str:
    """Get the system prompt for a specific character"""
    if character_id not in CHARACTERS:
        raise ValueError(f"Character '{character_id}' not found")

    return CHARACTERS[character_id]["system_prompt_generator"]()
