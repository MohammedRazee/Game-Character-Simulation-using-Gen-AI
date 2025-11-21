# ============================================
# notes_engine.py
# Handles:
# - Storing discovered clues and notes
# - Adding new notes automatically
# - Viewing notes in a formatted way
# ============================================

from datetime import datetime

# All collected clues/notes stored here
NOTES = []

# --------------------------------------------
# Add a new note if not already present
# --------------------------------------------
def add_note(text):
    """Adds a unique clue/note and prints notification."""
    if text not in NOTES:
        NOTES.append(text)
        print("\n💡  New Clue Added to Notes!")
        print(f"→ \"{text}\"\n")
        return True
    return False


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
        print(f"{i}. {note}")

    print("\n============================================\n")


# --------------------------------------------
# Helper: extract potential clues from AI reply
# --------------------------------------------
def detect_notes(suspect_name, reply):
    """
    Automatically detects important clues from suspect replies.
    Adds them as notes if certain keywords or patterns are triggered.
    """

    reply_low = reply.lower()
    added = False

    # -----------------------------
    # 1. Timeline confessions
    # -----------------------------
    if "11:" in reply_low or "10:" in reply_low:
        if "i was" in reply_low:
            added |= add_note(f"{suspect_name} mentioned a specific time in their alibi.")

    # -----------------------------
    # 2. Admitting presence at clinic
    # -----------------------------
    keywords_presence = [
        "i was near the clinic",
        "i went to the clinic",
        "i was at the clinic",
        "i returned to the clinic",
        "i came back to the clinic"
    ]
    for k in keywords_presence:
        if k in reply_low:
            added |= add_note(f"{suspect_name} admitted being at/near the clinic.")

    # -----------------------------
    # 3. Saw the body (Kabir / others)
    # -----------------------------
    if "saw his body" in reply_low or "saw the body" in reply_low:
        added |= add_note(f"{suspect_name} admitted seeing the body before discovery.")

    # -----------------------------
    # 4. Slips about evidence
    # -----------------------------
    if "cctv" in reply_low and "down" in reply_low:
        added |= add_note(f"{suspect_name} knows about the CCTV outage.")

    if "laptop" in reply_low and ("logged" in reply_low or "used" in reply_low):
        added |= add_note(f"{suspect_name} mentioned laptop activity.")

    if "usb" in reply_low:
        added |= add_note(f"{suspect_name} referenced the missing USB drive.")

    # -----------------------------
    # 5. Contradictions
    # -----------------------------
    contradiction_markers = [
        "i didn't say that",
        "that's not what i meant",
        "you misunderstood",
        "i never said that"
    ]

    for phrase in contradiction_markers:
        if phrase in reply_low:
            added |= add_note(f"{suspect_name} contradicted themselves.")

    # -----------------------------
    # 6. Emotional breakdown clues
    # -----------------------------
    emotional_markers = ["i panicked", "i got scared", "i was afraid", "i freaked out"]

    for phrase in emotional_markers:
        if phrase in reply_low:
            added |= add_note(f"{suspect_name} showed signs of panic or fear.")

    # -----------------------------
    # 7. Motive-based clues
    # -----------------------------
    if "argued" in reply_low or "fight" in reply_low:
        added |= add_note(f"{suspect_name} admitted to arguing with the victim.")

    if "he threatened" in reply_low:
        added |= add_note(f"{suspect_name} described a threat from the victim.")

    return added
