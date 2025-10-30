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
        },

        "The Chef": {
            "basic_info": "Personal chef responsible for cooking food at the dinner party, cut corners and used cheaper ingredients",
            "timeline": {
                "5:00 - 6:45 PM": "cooking dishes for the party",
                "6:45 - 7:15 PM": "serve dishes to the guests",
                "7:15 - 7:21 PM": "preparing next dishes for the party",
                "7:21 PM": "hears Alice scream, goes with everybody to the second floor",
            },
            "motive": "wants to take shortcuts as a chef and pose as a chef who uses high-quality ingredients",
            "relationship": "Professor Richards' and Adele's personal chef of 10 years",
            "physical_evidence": "was in the kitchen when he heard Alice scream",
            "behavior": "cocky, acts like a know-it-all when it comes to the culinary world",
            "key_facts": "was able to hear Alice scream from Professor Richards' study while in the kitchen"
        },

        "The Maid": {
            "basic_info": "Maid tasked with greeting guests as they arrive to the party and attending to their needs and helping around the house when needed",
            "timeline": {
                "5:00 - 5:05 PM": "greet guests as they arrive to the party and put their coats away on the garment rack",
                "5:06 - 5:24 PM": "gets cleaning supplies to clean the first-floor bathroom",
                "5:24 - 5:56 PM": "cleaning the first-floor bathroom",
                "5:56-6:45 PM": "helping the chef prepare the dishes for the party",
                "6:45-7:21 PM": "helping the chef serve the dishes to the guests",
                "7:21 PM": "hears Alice scream from the dining room"
            },
            "motive": "knows about the letters Alice sent to Professor Richards' that the professor wants to keep hidden",
            "relationship": "Professor Richards' and Adele's maid of 10 years",
            "physical_evidence": "was in the dining room when she heard Alice scream",
            "behavior": "listens to instructions well and respects all others, responds truthfully when asked questions",
            "key_facts": "was cleaning the first-floor bathroom when Abel tried to use the bathroom on the first-floor"
        },

    }
}