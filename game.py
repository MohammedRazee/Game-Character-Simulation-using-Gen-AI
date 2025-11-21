# ============================================
# game.py
# Main game loop with:
# - suspect interaction
# - confrontation detection
# - emotional tier escalation
# - automatic clue extraction
# - notes system integration
# - Gemini LLM calls
# ============================================

import os
from dotenv import load_dotenv

from suspects import SUSPECTS
from behavior_engine import detect_confrontation, update_emotional_tier, build_prompt
from notes_engine import detect_notes, show_notes

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
    print("3. Kabir Rao – Hospital administrator\n")


def choose_suspect():
    """Menu for selecting a suspect to interrogate."""
    while True:
        list_suspects()
        choice = input("Talk to which suspect? (1/2/3, 'n' for notes, 'q' to stop questioning): ").strip().lower()

        if choice == "q":
            return None

        if choice in ["n", "notes"]:
            show_notes()
            continue

        mapping = {"1": "Nisha", "2": "Rohit", "3": "Kabir"}
        if choice in mapping:
            return mapping[choice]

        print("Invalid choice. Try again.\n")


# --------------------------------------------
# Interrogation loop
# --------------------------------------------
def question_suspect(name: str):
    """Handles full conversation flow with a suspect."""
    print(f"\nYou are now talking to {name}.")
    print("Type your questions below.")
    print("Type 'back' to stop. Type 'n' to view notes.\n")

    while True:
        player_message = input("You: ").strip()

        # Notes access inside interrogation
        if player_message.lower() in ["n", "notes"]:
            show_notes()
            continue

        if player_message.lower() == "back":
            print(f"\nLeaving {name}.\n")
            break

        # 1) Detect confrontation type
        ct = detect_confrontation(player_message)

        # 2) Update emotional tier
        suspect_state[name] = update_emotional_tier(name, suspect_state[name])

        # 3) Build system prompt for AI
        prompt = build_prompt(
            name,
            emotional_tier=suspect_state[name],
            ct=ct,
            player_message=player_message
        )

        # 4) Get suspect's AI-generated reply
        reply = call_gemini(prompt)
        print(f"\n{name}: {reply}\n")

        # 5) Detect clues in reply and add to notes
        detect_notes(name, reply)


# --------------------------------------------
# Accuse mechanic
# --------------------------------------------
def accuse():
    """Allows the player to accuse a suspect."""
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
    """Main game controller: menus, navigation, interrogation access."""
    print("=== Murder Mystery: The Clinic Case ===\n")
    print("CASE BRIEF:")
    print("- Victim: Dr. Arjun Mehta, 42, cardiologist at Silverline Hospital.")
    print("- Scene: Private clinic, found dead late at night. Blunt force head injury.")
    print("- Evidence: Muddy footprints, laptop activity, CCTV outage, missing USB.\n")

    while True:
        print("Choose an option:")
        print("1. Interrogate a suspect")
        print("2. View Notes")
        print("3. Accuse the killer")
        print("4. Quit\n")

        choice = input("Enter choice: ").strip().lower()

        if choice == "1":
            suspect = choose_suspect()
            if suspect:
                question_suspect(suspect)

        elif choice in ["2", "n", "notes"]:
            show_notes()

        elif choice == "3":
            accuse()
            break

        elif choice in ["4", "q"]:
            print("\nExiting the game. Goodbye.\n")
            break

        else:
            print("Invalid option. Try again.\n")


# --------------------------------------------
# Start game
# --------------------------------------------
if __name__ == "__main__":
    main()
