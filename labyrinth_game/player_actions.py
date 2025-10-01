from . import utils


def show_inventory(game_state: dict):
    """
    Показывает содержимое инвентаря игрока."""
    inventory = game_state['player_inventory']
    if inventory:
        print("Ваш инвентарь:", ', '.join(inventory))
    else:
        print("Кажется, ваш инвентарь пуст.")

def get_input(prompt: str = "> "):
    """Получает ввод от игрока"""
    try:
        print(prompt, end='', flush=True)
        return input()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit" 
  
def move_player(game_state: dict, direction: str):
    """Перемещает игрока в указанном направлении, если это возможно."""
    current_room = game_state['current_room']
    current_room_info = game_state['rooms'][current_room]

    if direction in current_room_info['exits']:
        next_room = current_room_info['exits'][direction]

        if next_room == "treasure_room":
            inventory = game_state['player_inventory']
            if "treasure key" in inventory or "rusty key" in inventory:
                print(
                    "Вы используете найденный ключ, чтобы открыть путь"
                    " в комнату сокровищ.")
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return 

        game_state['current_room'] = next_room
        game_state['steps_taken'] += 1
        utils.describe_current_room(game_state)
        utils.random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state: dict, item_name: str):
    """Позволяет игроку взять предмет из текущей комнаты."""
    current_room = game_state['current_room']
    room_info = game_state['rooms'][current_room]

    if item_name in room_info['items']:
        if item_name == "treasure chest":
            print("Сундук слишком тяжелый, чтобы его взять."
                  " Попробуйте открыть его. (команда 'use treasure chest')")
            return
        elif item_name not in game_state['player_inventory']:
          game_state['player_inventory'].append(item_name)
          room_info['items'].remove(item_name)
          print(f"Вы взяли {item_name}.")
        else:
          print(f"У вас уже есть {item_name} в инвентаре.")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state: dict, item_name: str):
    """
    Позволяет игроку использовать предмет из инвентаря.
    Некоторые предметы могут иметь особые эффекты в определенных комнатах.
    """
    current_room = game_state['current_room']
    room_info = game_state['rooms'][current_room]
    if current_room == 'treasure_room' and "treasure chest" in room_info['items']:
        utils.attempt_open_treasure(game_state)
        return
    if item_name not in game_state['player_inventory']:
        print(f"У вас нет предмета '{item_name}' в инвентаре.")
    else:
        match item_name:
            case 'torch':
                print("Вы зажгли факел. Теперь вокруг светлее.")
            case "sword":
                print("Вы достали меч. Теперь вы чувствуете себя увереннее.")
            case "bronze box":
                print("Вы открыли бронзовую шкатулку и нашли внутри 'Ржавый ключ'")
                if 'rusty key' not in game_state['player_inventory']:
                  game_state['player_inventory'].append('rusty key')
            case _:
                print(f"У вас есть {item_name}, но вы не знаете, как им пользоваться.")