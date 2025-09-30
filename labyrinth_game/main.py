#!/usr/bin/env python3

from . import player_actions, utils

game_state = {
      'player_inventory': [], # Инвентарь игрока
      'current_room': 'entrance', # Текущая комната
      'game_over': False, # Значения окончания игры
      'steps_taken': 0 # Количество шагов
}

def process_command(game_state: dict, command: str):
    action, *args = command.strip().lower().split()
    arg = args[0] if args else None

    match action:
        case "go":
            if not arg:
                print("Укажите направление.")
                return
            player_actions.move_player(game_state, direction = arg)
        case "inventory":
            player_actions.show_inventory(game_state)
        case "look":
            utils.describe_current_room(game_state)
        case "take":
            player_actions.take_item(game_state, item_name = arg)
        case "use":
            pass
            player_actions.use_item(game_state, item_name = arg)
        case "solve":
            pass
            utils.solve_puzzle(game_state)
        case "help":
            utils.show_help()
        case "quit" | "exit":
            game_state['game_over'] = True
            print("Спасибо за игру!")
        case _:
            print("Неизвестная команда. ")
            utils.show_help()

def main():
  print("Добро пожаловать в Лабиринт сокровищ!")
  utils.describe_current_room(game_state)

  while not game_state['game_over']:
    input = player_actions.get_input()
    while not input:
        print("Введите команду (или 'help' для отображения справки)")
        input = player_actions.get_input()
    process_command(game_state, input)

if __name__ == "__main__":
    main()