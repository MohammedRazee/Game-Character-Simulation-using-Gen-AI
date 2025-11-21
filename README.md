# 🕵️ Murder Mystery AI — Interactive Detective Simulation

An AI-driven **murder mystery interrogation game** where players question three suspects in real-time.  
Each suspect behaves like a human: emotional, defensive, manipulative, or terrified — depending on how you interrogate them.

This project uses **Gemini** to create dynamic, unscripted conversations with each suspect.  
No fixed dialogue. No pre-written responses.  
Players uncover the truth through **confrontation**, **logic**, **evidence**, and **psychological pressure**.

---

## 🎮 What This Project Is

This is a **console-based detective game** powered by Gemini AI.  
The storyline:

**Victim:** Dr. Arjun Mehta  
**Location:** Private clinic  
**Time of death:** ~11:17 PM  
**Suspects:**  
- Nisha Mehta — victim’s wife  
- Rohit Sharma — junior doctor  
- Kabir Rao — hospital administrator  

The player’s goal:  
**Interrogate all suspects → catch contradictions → identify the killer.**

There is *no* pre-written dialogue — every answer comes from AI using the suspect’s personality, emotional state, lies, secrets, and confrontation history.

---

## 🧠 How the Game Works (Technical Overview)

Each suspect has:

- A **personality profile**
- A **guilt truth** (innocent or guilty)
- An **emotional tier system (0–4)** that escalates with confrontation
- A **dynamic prompt builder** that changes based on your questions
- **Confrontation triggers** like:
  - timeline contradictions  
  - evidence pressure  
  - accusing them  
  - catching them lying  
  - asking how they know something they shouldn't  

### The Interrogation Pipeline

When you ask a question:

1. The game detects whether it’s a confrontation (via regex and keywords).  
2. Their **emotional state increases**.  
3. The Behavior Engine chooses the suspect’s emotional reaction style.  
4. A customized prompt is built using the suspect’s profile + emotional tier.  
5. Gemini generates a **roleplayed, in-character** response.  

At the end, you make your final accusation.

The game then reveals whether you caught the killer.

---

# 🚀 Getting Started (Setup Guide)

Follow these steps to run the game on your system.

---

## 1. Clone this repository

```
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

---

## 2. Create a virtual environment

### Windows:
```
python -m venv .venv
.venv\Scripts\activate
```

### Mac/Linux:
```
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install dependencies

```
pip install -r requirements.txt
```

---

## 4. Set up environment variables

Create a `.env` file using:

```
cp .env.example .env
```

Then open `.env` and add your Google API key:

```
GOOGLE_API_KEY=your_actual_key_here
```

---

## 5. Run the game

```
python game.py
```

---

# 🛡️ Security Notes

- `.env` is ignored by git.
- Never commit your API key.
- `.env.example` tells collaborators what variable to set up.

---

# 🧱 Project Structure

```
murder-mystery-ai/
│
├── game.py
├── suspects.py
├── behavior_engine.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

# 🤝 Contributing

Feel free to fork the repo and add improvements such as:
- new suspects
- new cases
- GUI support
- analytics/logging
- additional evidence logic
- automated tests

---

# 🕵️ Have fun solving the case!
