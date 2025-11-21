# ============================================
# game.py
# Main game loop with:
# - suspect interaction
# - confrontation detection
# - emotional tier escalation
# - Gemini LLM calls
# ============================================

import os
from dotenv import load_dotenv
from suspects import SUSPECTS
from behavior_engine import detect_confrontation, update_emotional_tier, build_prompt

# --------------------------------------------
# Load API KEY
# --------------------------------------------
load_dotenv()
from google import genai
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

# --------------------------------------------
# Gemini call function
# --------------------------------------------
def call_gemini(prompt: str) -> str:
    """Sends the prompt to Gemini and returns text response."""
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text


# --------------------------------------------
# Game state (emotional tiers for each suspect)
# --------------------------------------------
suspect_state = {
    "Nisha": 0,
    "Kabir": 0,
    "Rohit": 0
}


# --------------------------------------------
# Suspect selection UI
# --------------------------------------------
def list_suspects():
    print("\nSuspects:")
    print("1. Nisha Mehta – Victim's wife")
    print("2. Rohit Sharma – Junior doctor")
    print("3. Kabir Rao – Hospital administrator")
    print()


def choose_suspect():
    while True:
        list_suspects()
        choice = input("Talk to which suspect? (1/2/3, or 'q' to stop questioning): ").strip()

        if choice.lower() == "q":
            return None

        if choice in ["1", "2", "3"]:
            mapping = {"1": "Nisha", "2": "Rohit", "3": "Kabir"}
            return mapping[choice]

        print("Invalid choice. Try again.")


# --------------------------------------------
# Interrogation loop
# --------------------------------------------
def question_suspect(name: str):
    print(f"\nYou are now talking to {name}. Type your questions.\nType 'back' to stop.\n")

    while True:
        player_message = input("You: ").strip()

        if player_message.lower() == "back":
            print(f"\nLeaving {name}.\n")
            break

        # 1) Detect confrontation
        ct = detect_confrontation(player_message)

        # 2) Update emotional tier
        suspect_state[name] = update_emotional_tier(name, suspect_state[name])

        # 3) Build LLM prompt
        prompt = build_prompt(
            name,
            emotional_tier=suspect_state[name],
            ct=ct,
            player_message=player_message
        )

        # 4) Call Gemini
        reply = call_gemini(prompt)

        # 5) Print response
        print(f"{name}: {reply}\n")


# --------------------------------------------
# Accuse mechanic
# --------------------------------------------
def accuse():
    print("\nTime to make your accusation!")
    print("Who do you think is the killer?\n")
    print("1. Nisha")
    print("2. Rohit")
    print("3. Kabir\n")

    choice = input("Your accusation (1/2/3): ").strip()

    mapping = {"1": "Nisha", "2": "Rohit", "3": "Kabir"}

    if choice not in mapping:
        print("Invalid choice. Returning to menu.\n")
        return

    accused = mapping[choice]

    # Identify the real killer
    killer = None
    for s in SUSPECTS:
        if SUSPECTS[s]["is_killer"]:
            killer = s
            break

    print("\n=== VERDICT ===")

    if accused == killer:
        print(f"Correct! {accused} was indeed the killer.\n")
    else:
        print(f"Wrong! You accused {accused}, but the real killer was {killer}.\n")

    print("Game Over.\n")


# --------------------------------------------
# Main Game Loop
# --------------------------------------------
def main():
    print("=== Murder Mystery: The Clinic Case ===\n")
    print("CASE BRIEF:")
    print("- Victim: Dr. Arjun Mehta, 42, cardiologist at Silverline Hospital.")
    print("- Scene: Private clinic, found dead late at night. Blunt force head injury.")
    print("- Evidence: Muddy footprints, laptop activity, CCTV outage, missing USB.\n")

    while True:
        suspect = choose_suspect()
        if suspect is None:
            break
        question_suspect(suspect)

    # After the player stops questioning suspects
    accuse()


# --------------------------------------------
# Start game
# --------------------------------------------
if __name__ == "__main__":
    main()
