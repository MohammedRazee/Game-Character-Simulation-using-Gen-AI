# ============================================
# notes_engine.py
# Handles:
# - Storing discovered clues and notes
# - Adding new notes automatically (pattern-based)
# - Viewing notes in a formatted way with categories
# ============================================

import re
from datetime import datetime

# All collected clues/notes stored here as dicts:
# { "text": str, "category": str, "timestamp": datetime }
NOTES = []


# --------------------------------------------
# Internal helper: check if note already exists
# --------------------------------------------
def _note_exists(text: str) -> bool:
    for n in NOTES:
        if n["text"] == text:
            return True
    return False


# --------------------------------------------
# Add a new note (with category)
# --------------------------------------------
def add_note(text: str, category: str = "General"):
    """
    Adds a unique clue/note and prints notification.
    Notes are tagged with a category (e.g. 'Timeline', 'Location', 'Motive').
    """
    if _note_exists(text):
        return False

    NOTES.append(
        {
            "text": text,
            "category": category,
            "timestamp": datetime.now(),
        }
    )

    print("\n💡  New Clue Added to Notes!")
    print(f"   [{category}] {text}\n")
    return True


# --------------------------------------------
# Display all notes in a clean format
# --------------------------------------------
def show_notes():
    """Prints all notes discovered so far."""
    print("\n============ 📝 DETECTIVE NOTES ============\n")

    if not NOTES:
        print("No notes have been discovered yet.\n")
        print("============================================\n")
        return

    for i, note in enumerate(NOTES, start=1):
        category = note["category"]
        text = note["text"]
        print(f"{i}. [{category}] {text}")

    print("\n============================================\n")


# --------------------------------------------
# CLUE RULES
# Pattern-based detection for important details
# --------------------------------------------

# Each rule:
# - category: label for UI
# - patterns: list of regex strings (checked case-insensitive)
# - note_template: formatted with {suspect}
CLUE_RULES = [
    # --- Presence / Location near the clinic ---
    {
        "category": "Location",
        "patterns": [
            r"\bnear the clinic\b",
            r"\bat the clinic\b",
            r"\bwent to the clinic\b",
            r"\bwent back to the clinic\b",
            r"\breturned to the clinic\b",
            r"\bcame back to the clinic\b",
        ],
        "note_template": "{suspect} admitted being at or near the clinic that night.",
    },
    # --- Direct admission of lying / changing story ---
    {
        "category": "Contradiction",
        "patterns": [
            r"\bi lied\b",
            r"\bi wasn['’]t (entirely )?truthful\b",
            r"\bi wasn['’]t honest\b",
            r"\bi didn['’]t tell the truth\b",
            r"\bi hid something\b",
        ],
        "note_template": "{suspect} admitted they lied or were not fully truthful earlier.",
    },
    # --- Timeline / specific time mentions with alibi ("I was ... at <time>") ---
    {
        "category": "Timeline",
        "patterns": [
            r"\bi was\b.*\b11:\d{2}\b",
            r"\bi was\b.*\b10:\d{2}\b",
            r"\bat around 11\b",
            r"\baround 11[: ]\d{0,2}\b",
        ],
        "note_template": "{suspect} gave a specific time in their alibi.",
    },
    # --- Seeing the body before discovery ---
    {
        "category": "Crime Scene Knowledge",
        "patterns": [
            r"\bsaw (his|the) body\b",
            r"\bfound (his|the) body\b",
            r"\bsaw him lying there\b",
        ],
        "note_template": "{suspect} claims to have seen the body before or during discovery.",
    },
    # --- CCTV / technical knowledge ---
    {
        "category": "Crime Scene Knowledge",
        "patterns": [
            r"\bcctv\b.*\b(out|down|off|wasn['’]t working)\b",
            r"\bthe cameras? (was|were) (down|off|disabled)\b",
        ],
        "note_template": "{suspect} knows about the CCTV outage.",
    },
    # --- Laptop / records ---
    {
        "category": "Evidence",
        "patterns": [
            r"\blaptop\b.*\b(logged in|logged on|used|opened)\b",
            r"\bi logged into\b.*\blaptop\b",
            r"\baccessed his laptop\b",
        ],
        "note_template": "{suspect} mentioned using or accessing the victim's laptop.",
    },
    # --- USB drive ---
    {
        "category": "Evidence",
        "patterns": [
            r"\busb\b",
            r"\bpen[- ]?drive\b",
        ],
        "note_template": "{suspect} referenced the missing USB or storage device.",
    },
    # --- Generic contradiction markers ---
    {
        "category": "Contradiction",
        "patterns": [
            r"\bi didn['’]t say that\b",
            r"\bthat['’]s not what i (meant|said)\b",
            r"\byou misunderstood\b",
            r"\bi never said that\b",
        ],
        "note_template": "{suspect} contradicted or backtracked on an earlier statement.",
    },
    # --- Emotional breakdown / panic ---
    {
        "category": "Emotional State",
        "patterns": [
            r"\bi panicked\b",
            r"\bi got scared\b",
            r"\bi was afraid\b",
            r"\bi freaked out\b",
            r"\bi lost it\b",
        ],
        "note_template": "{suspect} showed signs of panic or fear under pressure.",
    },
    # --- Motive: arguments / fights ---
    {
        "category": "Motive",
        "patterns": [
            r"\bwe (had )?(a )?fight\b",
            r"\bwe argued\b",
            r"\bwe were arguing\b",
            r"\bhe yelled at me\b",
            r"\bwe were not on good terms\b",
        ],
        "note_template": "{suspect} admitted to arguing or having conflict with the victim.",
    },
    # --- Motive: threats ---
    {
        "category": "Motive",
        "patterns": [
            r"\bhe threatened (me|to)\b",
            r"\bhe said he would ruin me\b",
            r"\bhe said he['’]d (destroy|end) my career\b",
        ],
        "note_template": "{suspect} described a threat from the victim.",
    },
]


# --------------------------------------------
# Helper: run all rules against reply text
# --------------------------------------------
def detect_notes(suspect_name: str, reply: str) -> bool:
    """
    Automatically detects important clues from suspect replies.
    Uses regex-based CLUE_RULES to add meaningful notes.

    Returns True if at least one new note was added.
    """
    reply_low = reply.lower()
    added_any = False

    for rule in CLUE_RULES:
        category = rule["category"]
        note_template = rule["note_template"]

        for pattern in rule["patterns"]:
            if re.search(pattern, reply_low):
                note_text = note_template.format(suspect=suspect_name)
                added = add_note(note_text, category=category)
                if added:
                    added_any = True
                # We don't break here; same reply can trigger multiple rules.

    return added_any
