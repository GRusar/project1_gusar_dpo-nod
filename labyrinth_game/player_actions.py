from . import constants
from . import utils

def show_inventory(game_state: dict):
    inventory = game_state['player_inventory']
    if inventory:
        print("Ваш инвентарь:", ', '.join(inventory))
    else:
        print("Кажется, ваш инвентарь пуст.")

def get_input(prompt: str = "> "):
  try:
      print(prompt, end='', flush=True)
      return input()
  except (KeyboardInterrupt, EOFError):
      print("\nВыход из игры.")
      return "quit" 
  
def move_player(game_state: dict, direction: str):
    current_room = game_state['current_room']
    room_info = constants.ROOMS[current_room]

    if direction in room_info['exits']:
        new_room = room_info['exits'][direction]
        game_state['current_room'] = new_room
        game_state['steps_taken'] += 1
        utils.describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state: dict, item_name: str):
    current_room = game_state['current_room']
    room_info = constants.ROOMS[current_room]

    if item_name in room_info['items']:
        if not item_name in game_state['player_inventory']:
          game_state['player_inventory'].append(item_name)
          room_info['items'].remove(item_name)
          print(f"Вы взяли {item_name}.")
        else:
          print(f"У вас уже есть {item_name} в инвентаре.")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state: dict, item_name: str):
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
                if not 'rusty key' in game_state['player_inventory']:
                  game_state['player_inventory'].append('rusty key')
            case _:
                print(f"У вас есть {item_name}, но вы не знаете, как им пользоваться.")