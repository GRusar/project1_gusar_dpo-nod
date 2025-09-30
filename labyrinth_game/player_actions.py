

def show_inventory(game_state: dict):
    inventory = game_state['player_inventory']
    if inventory:
        print("Ваш инвентарь:", ', '.join(inventory))
    else:
        print("Кажется, ваш инвентарь пуст.")