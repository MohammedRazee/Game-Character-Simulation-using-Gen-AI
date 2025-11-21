import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])


# TODO: import whatever you used to talk to Gemini.
# For example, if you made a helper in test_agent.py, you might do:
# from test_agent import call_gemini

# For now, I'll assume you will implement this function using your existing ADK code.
def call_gemini(prompt: str, history: list[str]) -> str:
    """
    Replace this with your actual Gemini ADK call.
    `history` is a list of previous messages in this conversation with this suspect.
    Return the model's reply as plain text.
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response.text


# ---------- GAME DATA ----------

CASE = {
    "victim": "Dr. Arjun Mehta, 42, renowned cardiologist at Silverline Hospital.",
    "scene": "He was found dead in his private clinic late at night. The room was messy, one window slightly open, a coffee mug on the table, and a broken photo frame on the floor.",
    "time": "Body discovered at 11:30 PM by the night security guard.",
}

SUSPECTS = [
    {
        "id": 1,
        "name": "Nisha Mehta",
        "role": "Victim's wife",
        "bio": "Runs a boutique. Recently seen arguing with the victim about money.",
        "is_killer": False,
        "secret": "She was planning to file for divorce but didn’t want it public yet.",
    },
    {
        "id": 2,
        "name": "Rohit Sharma",
        "role": "Junior doctor",
        "bio": "Ambitious, talented, and often overshadowed by the victim.",
        "is_killer": True,  # <- The actual murderer
        "secret": "He tampered with some records and feared the victim would expose him.",
    },
    {
        "id": 3,
        "name": "Kabir Rao",
        "role": "Hospital administrator",
        "bio": "Handles finances, under pressure due to audits.",
        "is_killer": False,
        "secret": "Has been embezzling small amounts of money but unrelated to the murder.",
    },
]


# Each suspect has their own conversation history so they stay consistent.
conversation_histories: dict[int, list[str]] = {s["id"]: [] for s in SUSPECTS}


def build_suspect_prompt(suspect: dict, player_message: str) -> str:
    """
    Build a detailed prompt that tells Gemini:
    - Who the suspect is
    - The case background
    - Whether they are the killer
    - What their personality is
    - What the player just asked
    """
    guilt_text = (
        "You ARE the murderer. You must hide this fact but your answers may contain subtle slips if the player is clever."
        if suspect["is_killer"]
        else "You are NOT the murderer. You should defend yourself, but you might still look suspicious."
    )

    prompt = f"""
You are roleplaying as a suspect in a murder mystery game.

CASE DETAILS:
- Victim: {CASE["victim"]}
- Scene: {CASE["scene"]}
- Time: {CASE["time"]}

YOUR CHARACTER:
- Name: {suspect["name"]}
- Role: {suspect["role"]}
- Background: {suspect["bio"]}
- Hidden secret (don't state directly unless heavily pressured): {suspect["secret"]}
- Truth about guilt: {guilt_text}

ROLEPLAY RULES:
- Answer ONLY as {suspect["name"]}. Stay in first person.
- Keep responses between 2–5 sentences.
- You can lie, deflect, or get emotional, but stay consistent with your story.
- Reveal hints gradually. Don't confess immediately even if you are guilty.
- If asked directly about the murder, respond in character, staying believable.

PLAYER QUESTION:
{player_message}
"""
    return prompt.strip()


def list_suspects():
    print("\nSuspects:")
    for s in SUSPECTS:
        print(f"{s['id']}. {s['name']} – {s['role']}")
    print()


def choose_suspect() -> dict:
    while True:
        list_suspects()
        choice = input("Talk to which suspect? (1/2/3, or 'q' to stop questioning): ").strip()
        if choice.lower() == "q":
            return None
        try:
            cid = int(choice)
            suspect = next((s for s in SUSPECTS if s["id"] == cid), None)
            if suspect:
                return suspect
            else:
                print("Invalid suspect, try again.")
        except ValueError:
            print("Please enter a number.")


def question_suspect(suspect: dict):
    sid = suspect["id"]
    history = conversation_histories[sid]

    print(f"\nYou are now talking to {suspect['name']} ({suspect['role']}).")
    print("Type your questions. Type 'back' to stop talking to this suspect.\n")

    while True:
        player_msg = input("You: ").strip()
        if player_msg.lower() in {"back", "exit"}:
            print(f"Leaving {suspect['name']}.\n")
            break

        history.append(f"Player: {player_msg}")
        prompt = build_suspect_prompt(suspect, player_msg)

        # Call Gemini
        reply = call_gemini(prompt, history)

        history.append(f"{suspect['name']}: {reply}")
        print(f"{suspect['name']}: {reply}\n")


def accuse():
    print("\nTime to make your accusation!")
    list_suspects()
    choice = input("Who do you think is the killer? (1/2/3): ").strip()
    try:
        cid = int(choice)
        suspect = next((s for s in SUSPECTS if s["id"] == cid), None)
        if not suspect:
            print("Invalid choice.")
            return

        killer = next(s for s in SUSPECTS if s["is_killer"])
        if suspect["id"] == killer["id"]:
            print(f"\nCorrect! {suspect['name']} was indeed the killer.")
        else:
            print(f"\nWrong! You accused {suspect['name']}, but the real killer was {killer['name']}.")
        print("Game over.")
    except ValueError:
        print("That wasn't a valid number.")
    except StopIteration:
        print("Configuration error: no killer defined.")


def main():
    print("=== Murder Mystery: The Clinic Case ===")
    print("\nCASE BRIEF:")
    print(f"- Victim: {CASE['victim']}")
    print(f"- Scene: {CASE['scene']}")
    print(f"- Time: {CASE['time']}\n")

    while True:
        suspect = choose_suspect()
        if suspect is None:
            break
        question_suspect(suspect)

    accuse()


if __name__ == "__main__":
    main()
