from . import constants


def describe_current_room(game_state: dict) -> None:
    current_room = game_state['current_room']
    room_info = constants.ROOMS[current_room]
    print(f"Вы находитесь в комнате: {current_room.upper()}")
    print(f"{room_info['description']}")
    if room_info['items']:
        print(f"Заметные предметы: {', '.join(room_info['items'])}")
    print("Выходы: ")
    for number, (direction, name) in enumerate(room_info['exits'].items(), 1):
        print(f"  {number}. {direction} -> {name}")
    if room_info['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение") 