# Evidence system for the detective game

EVIDENCE = {
    "gloves": {
        "id": "gloves",
        "name": "Gloves",
        "belongs_to": "diane",
        "code": "GL001",
        "description": "A pair of gloves found at the crime scene",
        "location": "Near the crime scene",
        "discovery_hint": "You found a pair of gloves. They might be important evidence.",
        "validation_prompt": """
            IMPORTANT EVIDENCE DISCOVERED: Gloves (Code: GL001)

            When the detective mentions or asks about the gloves, you MUST:
            1. Ask them: "Can you explain the reason and code for this evidence?"
            2. Wait for their response
            3. They must provide BOTH:
            - A reasonable explanation of why this evidence is important
            - The correct evidence code: GL001
            4. Only continue the conversation if BOTH are correct

            Do not reveal the code. Make them prove they have it.
        """
    },
    "research_papers": {
        "id": "research_papers",
        "name": "Research Papers",
        "belongs_to": "schumacher",
        "code": "RP002",
        "description": "Research papers found in a suspicious location",
        "location": "Professor Schumacher's possession",
        "discovery_hint": "You discovered research papers that seem out of place.",
        "validation_prompt": """
            IMPORTANT EVIDENCE DISCOVERED: Research Papers (Code: RP002)

            When the detective mentions or asks about the research papers, you MUST:
            1. Ask them: "Can you explain the reason and code for this evidence?"
            2. Wait for their response
            3. They must provide BOTH:
            - A reasonable explanation of why this evidence is important
            - The correct evidence code: RP002
            4. Only continue the conversation if BOTH are correct

            Do not reveal the code. Make them prove they have it.
        """
    },
    "torn_shirt": {
        "id": "torn_shirt",
        "name": "Torn Shirt",
        "belongs_to": "abel",
        "code": "TS003",
        "description": "A torn shirt with a missing button",
        "location": "Found in Abel's vicinity",
        "discovery_hint": "You found a torn shirt. It looks like a button is missing.",
        "validation_prompt": """
            IMPORTANT EVIDENCE DISCOVERED: Torn Shirt (Code: TS003)

            When the detective mentions or asks about the torn shirt, you MUST:
            1. Ask them: "Can you explain the reason and code for this evidence?"
            2. Wait for their response
            3. They must provide BOTH:
            - A reasonable explanation of why this evidence is important
            - The correct evidence code: TS003
            4. Only continue the conversation if BOTH are correct

            Do not reveal the code. Make them prove they have it.
        """
    },
    "button": {
        "id": "button",
        "name": "Button",
        "belongs_to": "schumacher",
        "code": "BT004",
        "description": "A button found in Professor Schumacher's hand, matches the torn shirt",
        "location": "In Professor Schumacher's hand",
        "related_to": "torn_shirt",
        "discovery_hint": "You found a button in Professor Schumacher's hand. It looks familiar...",
        "validation_prompt": """
            IMPORTANT EVIDENCE DISCOVERED: Button (Code: BT004)

            When the detective mentions or asks about the button, you MUST:
            1. Ask them: "Can you explain the reason and code for this evidence?"
            2. Wait for their response
            3. They must provide BOTH:
            - A reasonable explanation of why this evidence is important (hint: it might be related to the torn shirt)
            - The correct evidence code: BT004
            4. Only continue the conversation if BOTH are correct

            Do not reveal the code. Make them prove they have it.
        """
    },
    "knife": {
        "id": "knife",
        "name": "Kitchen Knife",
        "belongs_to": "chef",
        "code": "KN005",
        "description": "A kitchen knife found near the crime scene",
        "location": "Near the office entrance",
        "is_misleading": True,
        "discovery_hint": "You found a kitchen knife near the crime scene. It looks suspicious...",
        "validation_prompt": """
            IMPORTANT EVIDENCE DISCOVERED: Kitchen Knife (Code: KN005)

            WARNING: This is MISLEADING evidence. The knife was placed to distract the detective.

            When the detective mentions or asks about the knife, you MUST:
            1. Ask them: "Can you explain the reason and code for this evidence?"
            2. Wait for their response
            3. They must provide BOTH:
            - A reasonable explanation of why this evidence is important
            - The correct evidence code: KN005
            4. Only continue the conversation if BOTH are correct

            IMPORTANT: This knife is a red herring. It has no connection to the actual murder.
            The chef used it for cooking earlier, but it was moved near the crime scene to mislead investigators.
            Do not reveal this is misleading evidence unless the detective presents strong reasoning.

            Do not reveal the code. Make them prove they have it.
        """
    }
}

def get_evidence_by_id(evidence_id: str) -> dict:
    """Get evidence by ID"""
    return EVIDENCE.get(evidence_id)

def get_all_evidence() -> dict:
    """Get all evidence"""
    return EVIDENCE

def validate_evidence_code(evidence_id: str, code: str) -> bool:
    """Validate evidence code"""
    evidence = get_evidence_by_id(evidence_id)
    if not evidence:
        return False
    return evidence["code"] == code.upper().strip()

def get_evidence_validation_prompt(evidence_id: str) -> str:
    """Get validation prompt for discovered evidence"""
    evidence = get_evidence_by_id(evidence_id)
    if not evidence:
        return ""
    return evidence.get("validation_prompt", "")

def get_evidence_discovery_message(evidence_id: str) -> str:
    """Get discovery message for evidence"""
    evidence = get_evidence_by_id(evidence_id)
    if not evidence:
        return ""
    return evidence.get("discovery_hint", "")
