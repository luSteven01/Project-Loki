# Character definitions for the detective game
from story import STORY_DATA
import os

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
        "description": "Professor Richards' colleague",
        "avatar": "👨‍🏫",
        "system_prompt_generator": lambda: get_suspect_prompt("Professor Schumacher")
    },
    "alice": {
        "id": "alice",
        "name": "Alice",
        "role": "TA (Actually Daughter)",
        "description": "Professor Richards' TA",
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

def load_prompt_from_file(character_id: str) -> str:
    """Load prompt from file for a given character"""
    prompt_file = os.path.join(os.path.dirname(__file__), "prompts", f"{character_id}.txt")
    try:
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        raise ValueError(f"Prompt file not found for character: {character_id}")

def get_detective_prompt() -> str:
    """Load system prompt for detective AI assistant from file"""
    return load_prompt_from_file("detective")

def get_suspect_prompt(suspect_name: str) -> str:
    """Load system prompt for a suspect character from file"""
    # Map suspect names to character IDs
    name_to_id = {
        "Abel": "abel",
        "Diane": "diane",
        "Professor Schumacher": "schumacher",
        "Alice": "alice",
        "Adele": "adele",
        "The Chef": "chef",
        "The Maid": "maid"
    }

    character_id = name_to_id.get(suspect_name)
    if not character_id:
        raise ValueError(f"Unknown suspect name: {suspect_name}")

    return load_prompt_from_file(character_id)

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
