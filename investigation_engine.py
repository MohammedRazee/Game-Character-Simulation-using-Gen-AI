# ============================================
# investigation_engine.py
# Handles:
# - Evidence investigation system
# - Discovery of clues
# - Chain-unlocked discoveries
# - Integration with notes_engine
# ============================================

from notes_engine import add_note

# Track unlocked investigation areas
UNLOCKED = {
    "drawer": False,
    "usb_port": False,
    "corridor_camera": False
}


# --------------------------------------------
# Helper to print section header
# --------------------------------------------
def print_header(title):
    print("\n============================================")
    print(f"{title}")
    print("============================================\n")


# --------------------------------------------
# Footprints Investigation
# --------------------------------------------
def check_footprints():
    print_header("FOOTPRINT ANALYSIS")

    clues = [
        ("Two distinct sets of footprints were found — confirming multiple people were present.",
         "Evidence"),
        ("One set matches medical clogs typically worn by hospital staff.",
         "Evidence"),
        ("Another set matches formal shoes — conflicting with some suspect alibis.",
         "Contradiction"),
        ("Footprints are angled toward the open window — suggesting someone escaped.",
         "Location"),
    ]

    for text, cat in clues:
        print(f"• {text}")
        add_note(text, category=cat)


    # Unlock: Window + footprints imply escape route
    if not UNLOCKED["corridor_camera"]:
        UNLOCKED["corridor_camera"] = True
        print("\n🔓 New discovery unlocked: Corridor Camera Check!\n")


# --------------------------------------------
# Laptop Investigation
# --------------------------------------------
def check_laptop():
    print_header("LAPTOP INVESTIGATION")

    clues = [
        ("Laptop was last accessed at 11:14 PM — very close to the estimated time of death.",
         "Timeline"),
        ("Someone attempted to delete sensitive patient records but failed.",
         "Evidence"),
        ("Login ID used was traced to Rohit's credentials.",
         "Contradiction"),
        ("USB port shows scratch marks — frequent insertion/removal.",
         "Evidence"),
    ]

    for text, cat in clues:
        print(f"• {text}")
        add_note(text, category=cat)

    if not UNLOCKED["usb_port"]:
        UNLOCKED["usb_port"] = True
        print("\n🔓 New discovery unlocked: USB Port Examination!\n")


# --------------------------------------------
# Window Investigation
# --------------------------------------------
def check_window():
    print_header("WINDOW EXAMINATION")

    clues = [
        ("The window was open during the estimated time of death.",
         "Location"),
        ("Mud traces on the sill indicate someone climbed in or out.",
         "Evidence"),
        ("Fingerprints appear smudged — wiped intentionally.",
         "Evidence"),
    ]

    for text, cat in clues:
        print(f"• {text}")
        add_note(text, category=cat)

    # Connection to footprints is purely conceptual in notes; no new unlock.


# --------------------------------------------
# Coffee Mug Investigation
# --------------------------------------------
def check_coffee_mug():
    print_header("COFFEE MUG ANALYSIS")

    clues = [
        ("Coffee mug contains black coffee — no milk.",
         "Evidence"),
        ("Rohit is known to dislike black coffee — contradiction if he claims he drank it.",
         "Contradiction"),
        ("No lipstick marks present — suggesting Nisha likely did not use it.",
         "Elimination"),
    ]

    for text, cat in clues:
        print(f"• {text}")
        add_note(text, category=cat)


# --------------------------------------------
# Photo Frame Investigation
# --------------------------------------------
def check_photo_frame():
    print_header("PHOTO FRAME EXAMINATION")

    clues = [
        ("The frame was not dropped — it appears thrown during a struggle.",
         "Evidence"),
        ("Photo shows victim with hospital staff; Kabir appears tense in the picture.",
         "Motive"),
        ("Scratches on the back suggest recent handling.",
         "Evidence"),
    ]

    for text, cat in clues:
        print(f"• {text}")
        add_note(text, category=cat)

    if not UNLOCKED["drawer"]:
        UNLOCKED["drawer"] = True
        print("\n🔓 New discovery unlocked: Office Drawer!\n")


# --------------------------------------------
# Clinic Room General Sweep
# --------------------------------------------
def check_clinic_room():
    print_header("CLINIC ROOM EXAMINATION")

    clues = [
        ("Overturned chair indicates a physical struggle occurred.",
         "Evidence"),
        ("Blood spatter angle suggests attacker taller than the victim.",
         "Profile"),
        ("A loose pen with Rohit’s initials was found under the table.",
         "Contradiction"),
    ]

    for text, cat in clues:
        print(f"• {text}")
        add_note(text, category=cat)


# --------------------------------------------
# UNLOCKED DISCOVERY: Drawer
# --------------------------------------------
def check_drawer():
    print_header("OFFICE DRAWER EXAMINATION")

    clues = [
        ("Financial audit documents reveal ongoing tension between Kabir and the victim.",
         "Motive"),
        ("Loan application forms signed fraudulently — connects to Nisha's motive.",
         "Motive"),
        ("Drawer contains a note hinting that Rohit accessed confidential patient files.",
         "Evidence"),
    ]

    for text, cat in clues:
        print(f"• {text}")
        add_note(text, category=cat)


# --------------------------------------------
# UNLOCKED DISCOVERY: USB Port
# --------------------------------------------
def check_usb_port():
    print_header("USB PORT CHECK")

    clues = [
        ("Port shows heavy scratch marks — indicates frequent USB insertion.",
         "Evidence"),
        ("Damage suggests removal happened recently — supports missing USB clue.",
         "Evidence"),
    ]

    for text, cat in clues:
        print(f"• {text}")
        add_note(text, category=cat)


# --------------------------------------------
# UNLOCKED DISCOVERY: Corridor Camera
# --------------------------------------------
def check_corridor_camera():
    print_header("CORRIDOR CAMERA CHECK")

    clues = [
        ("Backup corridor camera captured a shadow entering the clinic around 11:12 PM.",
         "Timeline"),
        ("Shadow height matches Rohit more closely than Kabir or Nisha.",
         "Profile"),
        ("Camera went offline 2 minutes later — consistent with deliberate sabotage.",
         "Evidence"),
    ]

    for text, cat in clues:
        print(f"• {text}")
        add_note(text, category=cat)


# --------------------------------------------
# INVESTIGATION MENU
# --------------------------------------------
def investigate():
    while True:
        print("\n========== 🔍 INVESTIGATION MENU ==========\n")
        print("MAIN EVIDENCE AREAS:")
        print("1. Footprints")
        print("2. Laptop")
        print("3. Window")
        print("4. Coffee Mug")
        print("5. Photo Frame")
        print("6. Clinic Room Sweep")

        print("\nUNLOCKED DISCOVERIES:")

        counter = 7
        option_map = {}

        if UNLOCKED["drawer"]:
            print(f"{counter}. Office Drawer")
            option_map[str(counter)] = "drawer"
            counter += 1

        if UNLOCKED["usb_port"]:
            print(f"{counter}. USB Port Examination")
            option_map[str(counter)] = "usb_port"
            counter += 1

        if UNLOCKED["corridor_camera"]:
            print(f"{counter}. Corridor Camera Check")
            option_map[str(counter)] = "corridor_camera"
            counter += 1

        print(f"{counter}. Back\n")
        option_map[str(counter)] = "back"

        choice = input("Choose an area to investigate: ").strip()

        # Base options
        if choice == "1":
            check_footprints()
        elif choice == "2":
            check_laptop()
        elif choice == "3":
            check_window()
        elif choice == "4":
            check_coffee_mug()
        elif choice == "5":
            check_photo_frame()
        elif choice == "6":
            check_clinic_room()

        # Unlocked options
        elif choice in option_map:
            if option_map[choice] == "drawer":
                check_drawer()
            elif option_map[choice] == "usb_port":
                check_usb_port()
            elif option_map[choice] == "corridor_camera":
                check_corridor_camera()
            elif option_map[choice] == "back":
                return

        else:
            print("Invalid option. Try again.\n")
