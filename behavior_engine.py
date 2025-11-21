# ============================================
# behavior_engine.py
# Handles:
# - Confrontation detection
# - Emotional tier updates
# - Prompt assembly using MASTER_TEMPLATE
# - Fully compatible with suspects.py structure
# ============================================

import re
from suspects import MASTER_TEMPLATE, SUSPECTS, CT_EFFECTS

# ============================================
# Confrontation Pattern Definitions
# ============================================
# Confrontation Types:
# 1 = Timeline challenge
# 2 = Evidence confrontation
# 3 = Knowledge contradiction
# 4 = Behavior contradiction
# 5 = Direct accusation
# 0 = Neutral question

CT_PATTERNS = {
    1: [
        r"timeline",
        r"where were you",
        r"what time",
        r"\b11:",
        r"\b10:",
        r"your story doesn't match",
        r"your timeline"
    ],
    2: [
        r"footprint",
        r"dna",
        r"hair",
        r"evidence",
        r"cctv",
        r"camera",
        r"laptop",
        r"usb",
        r"file",
        r"record",
        r"clock",
        r"photo frame",
        r"fingerprint"
    ],
    3: [
        r"how do you know",
        r"you shouldn't know",
        r"only the killer would know",
        r"how would you know"
    ],
    4: [
        r"contradiction",
        r"earlier you said",
        r"you said something else",
        r"changing your story",
        r"that's not what you said"
    ],
    5: [
        r"you killed",
        r"you murdered",
        r"you're the killer",
        r"you did it",
        r"you are the murderer"
    ]
}


# ============================================
# Detect confrontation type
# Returns CT number 0–5
# ============================================
def detect_confrontation(player_message: str) -> int:
    """Identify confrontation type based on keywords/patterns."""
    msg = player_message.lower()

    for ct, patterns in CT_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, msg):
                return ct

    return 0  # Normal question


# ============================================
# Emotional Tier Update
# ============================================
def update_emotional_tier(suspect_name: str, current_tier: int) -> int:
    """Increase emotional tier by 1 up to suspect's max tier."""
    max_tier = SUSPECTS[suspect_name]["max_tier"]
    new_tier = min(current_tier + 1, max_tier)
    return new_tier


# ============================================
# Build Prompt for Gemini
# ============================================
def build_prompt(
    suspect_name: str,
    emotional_tier: int,
    ct: int,
    player_message: str
) -> str:
    """
    Fills the MASTER_TEMPLATE with all necessary suspect information.
    This function is extremely sensitive to template structure—
    do NOT modify the variable names unless suspects.py changes.
    """

    suspect = SUSPECTS[suspect_name]

    # Emotional tier description
    tier_desc = suspect["tiers"][emotional_tier]

    # Confrontation behavior description
    if ct == 0:
        ct_desc = "Normal question; respond in character without escalation."
    else:
        # Safe: CT_EFFECTS maps exactly {suspect_name: {ct: desc}}
        ct_desc = CT_EFFECTS[suspect_name][ct]

    # Fill master template safely — exact key names from suspects.py
    prompt = MASTER_TEMPLATE.format(
        SUSPECT_NAME=suspect_name,
        ROLE=suspect["role"],
        PERSONALITY_DESCRIPTION=suspect["personality"],
        PUBLIC_MOTIVE=suspect["public_motive"],
        HIDDEN_MOTIVES=suspect["hidden_motives"],
        GUILTY_OR_INNOCENT="GUILTY" if suspect["is_killer"] else "INNOCENT",
        CURRENT_EMOTIONAL_TIER=emotional_tier,
        EMOTIONAL_TIER_DESCRIPTION=tier_desc,
        CONFRONTATION_BEHAVIOR_DESCRIPTION=ct_desc,
        PLAYER_MESSAGE=player_message
    )

    return prompt
