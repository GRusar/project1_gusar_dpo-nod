"""
Константы и настройки для текстовой игры-лабиринта с 
загадками и случайными событиями
"""

"""Команды игрока

COMMANDS - словарь доступных команд и их описаний"""
COMMANDS = {
    "go <direction>": "Перейти в направлении (north/south/east/west)",
    "<direction>": "Перейти в направлении (north/south/east/west)",         
    "look": "Осмотреть текущую комнату",
    "take <item>": "Поднять предмет",
    "use <item>": "Использовать предмет из инвентаря",
    "inventory": "Показать инвентарь",
    "solve": "Попытаться решить загадку в комнате",
    "quit": "Выйти из игры",
    "help": "Показать это сообщение"  
}


"""Направления движения
DIRECTIONS - допустимые направления движения игрока"""
DIRECTIONS = {
  "north" : "north",
  "south" : "south",
  "east"  : "east",
  "west"  : "west",
}
north = DIRECTIONS["north"]
south = DIRECTIONS["south"]
east  = DIRECTIONS["east"]
west  = DIRECTIONS["west"]


"""Случайные события

RANDOM_EVENT_PROBABILITY - верхний порог для генерации случайного числа 
для наступления случайного события

RANDOM_EVENT_TRIGGER_THRESHOLD - число от 1 до RANDOM_EVENT_PROBABILITY, 
устанавливает порог срабатывания случайного события 
(если сгенерированное число равно этому числу, то событие происходит)

RANDOM_EVENT_SCENARIOS - список возможных сценариев случайных событий
"""
RANDOM_EVENT_PROBABILITY = 10
RANDOM_EVENT_TRIGGER_THRESHOLD = 0
RANDOM_EVENT_SCENARIOS = ["trap", "find_coin", "fright"]


"""Параметры форматирования и случайных событий.

HELP_ALIGNMENT - ширина поля для выравнивания справки по командам.
EVENT_SCENARIO_STEP_OFFSET - смещение количества шагов при генерации сценария.
EVENT_SCENARIO_INVENTORY_SCALE - множитель, учитывающий размер инвентаря.
EVENT_SCENARIO_ADDITIVE_SHIFT - дополнительное смещение для устойчивого seed.
TRAP_DAMAGE_MODULO - диапазон генерации вероятности урона ловушки.
TRAP_DAMAGE_THRESHOLD - порог, ниже которого игрок получает травму.
"""
HELP_ALIGNMENT = 16
EVENT_SCENARIO_STEP_OFFSET = 1
EVENT_SCENARIO_INVENTORY_SCALE = 1
EVENT_SCENARIO_ADDITIVE_SHIFT = 17
TRAP_DAMAGE_MODULO = 9
TRAP_DAMAGE_THRESHOLD = 3


"""Описание комнат лабиринта

Каждая комната представлена словарём с ключами:
- description: текстовое описание комнаты
- exits: словарь с направлениями и названиями комнат, куда можно выйти
- items: список предметов, которые можно найти в комнате
- puzzle: кортеж (вопрос, ответ) для загадки в комнате или None, если загадки нет
"""
ROOMS = {
    'entrance': {
        'description': 'Вы в темном входе лабиринта...',
        'exits': {north: 'hall', east: 'trap_room'},
        'items': ['torch'],
        'puzzle': None
    },
    'hall': {
        'description': (
          'Большой зал с эхом. По центру стоит пьедестал с запечатанным сундуком.'
        ),
        'exits': {south: 'entrance', west: 'library', north: 'treasure_room'},
        'items': [],
        'puzzle': (
          (
            'На пьедестале надпись: "Назовите число, которое идет после девяти". '
            'Введите ответ цифрой или словом.'
          ), ['10', 'десять', 'ten']
        )
    },
    'trap_room': {
          'description': (
            'Комната с хитрой плиточной поломкой. '
            'На стене видна надпись: "Осторожно — ловушка".'
          ),
          'exits': {west: 'entrance'},
          'items': ['rusty key'],
          'puzzle': (
            (
              'Система плит активна. Чтобы пройти, назовите слово "шаг" '
              'три раза подряд (введите "шаг шаг шаг")'
            ), ['шаг шаг шаг', 'step step step']
          )
    },
    'library': {
          'description': (
            'Пыльная библиотека. На полках старые свитки. '
            'Где-то здесь может быть ключ от сокровищницы.'
          ),
          'exits': {east: 'hall', north: 'armory', west: 'garden'},
          'items': ['ancient book'],
          'puzzle': (
            (
              'В одном свитке загадка: "Что всегда идёт, но никогда не двигается?" '
              '(ответ одно слово)'
            ), ['время', 'time']
          )
    },
        'armory': {
          'description': (
              'Старая оружейная комната. На стене висит меч, '
              'рядом — небольшая бронзовая шкатулка.'
            ),
          'exits': {south: 'library', west: 'dungeon'},
          'items': ['sword', 'bronze box'],
          'puzzle': None
    },
    'treasure_room': {
          'description': 
            'Комната, на столе большой сундук. Дверь заперта — нужен особый ключ.',
          'exits': {south: 'hall'},
          'items': ['treasure chest'],
          'puzzle': (
            (
              'Дверь защищена кодом. Введите код '
              '(подсказка: это число пятикратного шага, 2*5= ? )'
            ),
            ['10', 'десять', 'ten']
          )
    },
    'dungeon': {
        'description': (
          'Сырой подвал с цепями на стенах. Слышны капли воды. '
          'В углу — ржавая решетка.'
        ),
        'exits': {east: 'armory'},
        'items': ['ancient book'],
        'puzzle': (
            'Что можно увидеть с закрытыми глазами? (одно слово)',
            ['сон', 'dream']
        )
    },
    'garden': {
        'description': (
          'Таинственный сад внутри лабиринта. Здесь пахнет цветами, '
          'но слышен шорох листвы.'
        ),
        'exits': {east: 'library'},
        'items': ['magic seed'],
        'puzzle': (
          'На камне написано: "Что всегда смотрит на солнце?"',
          ['подсолнух', 'sunflower']
        )
    }
}
