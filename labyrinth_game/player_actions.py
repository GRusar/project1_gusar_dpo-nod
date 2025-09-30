

def show_inventory(game_state: dict):
    inventory = game_state['player_inventory']
    if inventory:
        print("Ваш инвентарь:", ', '.join(inventory))
    else:
        print("Кажется, ваш инвентарь пуст.")

def get_input(prompt="> "):
  try:
      print(prompt, end='', flush=True)
  except (KeyboardInterrupt, EOFError):
      print("\nВыход из игры.")
      return "quit" 