# asciinema записи прохождения

Здесь собираем дополнительные демонстрации прохождения игры и материалы для
ручной проверки.

## Доступные записи

| Файл | Описание |
| ---- | -------- |
| `1_some_error_demonstation.cast` | Полное прохождение через `bronze box` с демонстрацией невозможности зайти в сокровищницу, пока ключ не в инвентаре |
| `2_utf_decode_error_demonstration.cast` | Возникновение `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd1...` |

## Просмотр записи asciinema

Файлы с записями можно воспроизвести локально:
```sh
asciinema play <filename>

# Например:
asciinema play 1_some_error_demonstation.cast
```