EMOJI = {
    "pumpkin": "🎃",
    "destination": "🏠",
    "ambulance": "🚑",
    "trap": "❌",
    "brick": "🧱",
    "bomb": "💣",
    "hint": "📄",
    "rest": "⛽️",
    "start": "💜",
    "empty": " ",
    "safepath": "🟢"
}

MAP = [
    ["🎃", "🎃", "🎃", "🚑", "🟢", "📄"],
    ["🎃", "💣", "🏠", "🟢", "❌", "📄"],
    ["🧱", "🎃", "🟢", "🎃", "🟢", "❌"],
    ["🧱", "🎃", "🧱", "🟢", "🟢", "🟢"],
    ["🎃", "💣", "📄", "🟢", "🟢", "🟢"],
    ["💜", "📄", "⛽️", "🟢", "🎃", "🟢"],
]

CLUES = [
    "Clue1：24589=3",
    "Clue2：35689=4",
    "Clue3：89946=5",
    "Clue4：45678=3"
]

player = {
    "x": 5,
    "y": 0,
    "hp": 3,
    "stamina": 10,
    "bricks": 0,
    "bombs": [],  
    "hints": 0,
    "defeated": 0,
    "wrong_answers": 0,
    "answered_correctly": False,
    "inventory": []
}

total_pumpkins = sum(row.count(EMOJI["pumpkin"]) for row in MAP)

def show_map():
    for i, row in enumerate(MAP):
        row_str = ""
        for j, cell in enumerate(row):
            if i == player["x"] and j == player["y"]:
                row_str += "💜".ljust(4)
            else:
                row_str += cell.ljust(4)
        print(row_str)

def show_inventory():
    print("Inventory：", player["inventory"] if player["inventory"] else "Null")

def show_status():
    print("📍 Current state ".center(50, "★"))
    print("Current position: ({}, {})".format(player['x'], player['y']))
    print("Health:{} | Stamina:{} | Bricks:{} | Bombs:{} | Hints:{} | Defeated Pumpkins:{}".format(
        player["hp"], player["stamina"], player["bricks"], len(player["bombs"]),
        player["hints"], player["defeated"]
    ))
    show_inventory()
    print("🌍 Current MAP ".center(50, "-"))
    show_map()
    print("Enter the direction to continue the game...")

def move():
    direction = input("Enter direction(up/down/left/right): ").strip().lower()
    dx, dy = 0, 0
    if direction == "up": dx = -1
    elif direction == "down": dx = 1
    elif direction == "left": dy = -1
    elif direction == "right": dy = 1
    else:
        print("❗ Wrong direction")
        return

    new_x = player["x"] + dx
    new_y = player["y"] + dy

    if 0 <= new_x < len(MAP) and 0 <= new_y < len(MAP[0]):
        old_x, old_y = player["x"], player["y"]
        current_cell = MAP[old_x][old_y]
        player["x"], player["y"] = new_x, new_y
        if current_cell == EMOJI["start"] or current_cell == EMOJI["empty"]:
            MAP[old_x][old_y] = EMOJI["safepath"]

        handle_cell(MAP[new_x][new_y])

        if player["defeated"] >= total_pumpkins and player["hints"] >= 4 and not player["answered_correctly"]:
            print("✅ All clues have been collected and all pumpkins have been defeated!")
            print("★"*50)
            print("📍Automatic jump to the destination！Please answer the questions based on the prompts！")
            player["x"], player["y"] = 1, 2  
            print("🧩 Clue Summary：")
            for clue in CLUES:
                print(clue)
            print("★"*50)
            solve_riddle()
        print("✅ Command complete, please continue to enter the next command...\n" + "=" * 50)
    else:
        print("🚫 Can't cross the line！")

def handle_cell(cell):
    x, y = player["x"], player["y"]
    if cell == EMOJI["brick"]:
        player["bricks"] += 1
        player["inventory"].append("🧱")
        print("Get Bricks 🧱 ！")
    elif cell == EMOJI["bomb"]:
        player["bombs"].append(2)
        player["inventory"].append("💣")
        print("Get bombs 💣 ！")
    elif cell == EMOJI["rest"]:
        player["stamina"] += 1
        print("Replenish stamina! Stamina +1 ⛽️ ！")
    elif cell == EMOJI["ambulance"]:
        player["hp"] += 1
        print("Health +1 ❤️ ！")
    elif cell == EMOJI["trap"]:
        player["hp"] -= 1
        print("Trap! Health -1 ❤️ ！")
    elif cell == EMOJI["hint"]:
        player["hints"] += 1
        player["inventory"].append("📄")
        print("Hints！ ")
    elif cell == EMOJI["pumpkin"]:
        fight_pumpkin()
        MAP[x][y] = EMOJI["safepath"]
        return
    elif cell == EMOJI["destination"]:
        if player["answered_correctly"] and player["defeated"] >= total_pumpkins:
            print("🎉 Congratulations on the escape!")
            exit()
        else:
            print("Clues not fully collected or pumpkins not removed!")
            return

    if cell not in (EMOJI["destination"], EMOJI["pumpkin"]):
        MAP[x][y] = EMOJI["empty"]

def fight_pumpkin():
    print("🎃 Attention！Pumpkin！")
    if player["bombs"]:
        player["bombs"][0] -= 1
        player["defeated"] += 2
        player["stamina"] -= 1
        print("💣 Bombed a pumpkin！")
        if player["bombs"][0] == 0:
            player["bombs"].pop(0)
            if "💣" in player["inventory"]:
                player["inventory"].remove("💣")
    elif player["bricks"] > 0:
        player["bricks"] -= 1
        player["defeated"] += 1
        player["stamina"] -= 1
        if "🧱" in player["inventory"]:
            player["inventory"].remove("🧱")
        print("🧱 Knock out a pumpkin with a brick！")
    else:
        player["hp"] -= 1
        player["stamina"] -= 1
        print("🎃 Unarmed！ Attacked by pumpkin! Health -1, Stamina-1.")

riddles = [("51787= ", "2")]

def solve_riddle():
    if player["hints"] == 0:
        print("📄 You haven't hinted at a clue.")
        return

    player["hints"] -= 1
    if "📄" in player["inventory"]:
        player["inventory"].remove("📄")

    question, answer = riddles[0]

    print("📌 Please answer the puzzle based on the clues and allow up to 3 wrong answers.")

    while player["wrong_answers"] < 3:
        response = input(f"Question：{question} ")
        if response.strip() == answer:
            player["answered_correctly"] = True
            print("🎉 Answer correctly! Successful escape!")
            exit()
        else:
            player["wrong_answers"] += 1
            if player["wrong_answers"] < 3:
                print("❌ Wrong Answer！Please re-answer：")
            else:
                print("💀 Reach 3 errors and the game fails!")
                exit()

def check_game_over():
    if player["hp"] <= 0 or player["stamina"] <= 0:
        print("🩸 Stamina or Health is 0, the game fails!")
        return True
    return False

def main():
    print("🌟Game on! Welcome to Escape Room!\n")
    turn = 1
    while True:
        print(f"🌀 Round {turn} 🌀")
        show_status()
        move()
        if check_game_over():
            break
        turn += 1

if __name__ == "__main__":
    main()
