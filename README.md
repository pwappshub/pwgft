# Provably-Fair Commitment Verifier (HMAC-SHA256)

This folder contains `verify_hmac_v1.py` — a minimal, dependency-free script that allows anyone to independently verify a game’s **provably-fair commitment** when the game exports a **pre-serialized payload**.

It answers one key question:

- **Does the revealed `serverSeed` reproduce the exact commitment hash shown at the start of the game (for the exact payload string)?**

> Note: this tool verifies the *commitment only*. It does not re-run game logic or compute winners.

---

## Quick start

1. Export / download the game JSON file (it must include a `payload` field).
2. Copy:
   - `serverSeed` (revealed after the game ends)
   - `hash` / commitment (shown at game start)
3. Run:

```bash
python scripts/verify_hmac_v1.py \
  --seed e3c0... \
  --hash f12a... \
  --json game.json
```

If verification succeeds, the script prints `VALID ✅` and exits with code `0`.  
If it fails, it prints `INVALID ❌` and exits with code `1`.

---

## How it works

### 1) Inputs
The script uses three inputs:

- **Seed**: `serverSeed` (revealed after the game ends)
- **Commitment**: `hash` (published at game start)
- **Message**: `payload` (a pre-serialized string stored in the exported JSON)

### 2) Commitment reconstruction
The expected commitment is computed as:

- Algorithm: **HMAC-SHA256**
- Key: `serverSeed` encoded as UTF-8
- Message: `payload` encoded as UTF-8
- Output: hex digest

The computed digest is compared to the provided `hash` (case-insensitive).  
Because HMAC is deterministic, the same `serverSeed` and identical `payload` always produce the same commitment.

---

## Requirements

- Python **3.9+**
- Standard library only (no external dependencies)

---

## JSON format

The JSON file must contain a string field named `payload`.

Minimal example:

```json
{
  "payload": "mines|[0,0,0,-1]|..."
}
```

Rules:

- `payload` **must be a string**
- it must match the server’s payload **byte-for-byte**
  - same separators and ordering
  - same casing
  - no added/removed whitespace
- if your exporter reconstructs the payload (instead of exporting the original serialized string), verification may fail — and that indicates the exported payload is not identical to the server input.

---

## Output and exit codes

The script prints:

- payload (message)
- computed commitment
- provided commitment
- result

Exit codes:

- `0` — commitment is valid
- `1` — commitment is invalid

---

## Troubleshooting

### Missing or invalid payload
If you see an error about `"payload"`:
- ensure the JSON file contains `payload`
- ensure `payload` is a string (not an object/array)

### `INVALID ❌` but you expected `VALID`
Most commonly caused by payload mismatch:
- different serialization on export vs. server
- extra spaces/newlines
- modified separators or field ordering inside the payload string

Verify using the exact serialized payload that the server used to compute the commitment.

### JSON read failure
If the script cannot read the JSON:
- ensure the file is valid JSON
- ensure UTF-8 encoding
- ensure the file path is correct

---

## License

MIT

---

# Проверка честности коммита (HMAC-SHA256)

В этой папке находится `verify_hmac_v1.py` — минимальный скрипт без внешних зависимостей, который позволяет любой стороне проверить **provably-fair коммит** игры, если игра экспортирует **уже сериализованный payload**.

Он отвечает на один главный вопрос:

- **Действительно ли раскрытый `serverSeed` даёт ровно тот же хэш-коммит, который был показан в начале игры (для той же строки payload)?**

> Важно: скрипт проверяет только *коммит*. Он не пересчитывает логику игры и не определяет победителя.

---

## Быстрый старт

1. Экспортируйте / скачайте JSON-файл игры (в нём должно быть поле `payload`).
2. Скопируйте:
   - `serverSeed` (раскрывается после окончания игры)
   - `hash` / commitment (показывается в начале игры)
3. Запустите:

```bash
python scripts/verify_hmac_v1.py \
  --seed e3c0... \
  --hash f12a... \
  --json game.json
```

Если всё корректно, скрипт выведет `VALID ✅` и завершится с кодом `0`.  
Если нет — выведет `INVALID ❌` и завершится с кодом `1`.

---

## Как это работает

### 1) Входные данные
Скрипту нужны три вещи:

- **Seed**: `serverSeed` (раскрывается после окончания игры)
- **Коммит**: `hash` (публикуется в начале)
- **Сообщение**: `payload` (уже сериализованная строка из экспортированного JSON)

### 2) Восстановление коммита
Ожидаемый коммит вычисляется так:

- Алгоритм: **HMAC-SHA256**
- Ключ: `serverSeed` в UTF-8
- Сообщение: `payload` в UTF-8
- Результат: hex-digest

Далее computed digest сравнивается с переданным `hash` (без учёта регистра).  
HMAC детерминирован, поэтому одинаковые `serverSeed` и идентичный `payload` всегда дают один и тот же коммит.

---

## Требования

- Python **3.9+**
- Только стандартная библиотека (без зависимостей)

---

## Формат JSON

В JSON обязательно должно быть строковое поле `payload`.

Минимальный пример:

```json
{
  "payload": "mines|[0,0,0,-1]|..."
}
```

Правила:

- `payload` должен быть **строкой**
- он должен совпадать с тем, что использовал сервер, **байт-в-байт**
  - те же разделители и порядок
  - тот же регистр
  - без добавленных/удалённых пробелов
- если экспортёр “собирает” payload заново (а не экспортирует исходную строку), проверка может не пройти — это означает, что экспортированный payload не идентичен серверному.

---

## Вывод и коды завершения

Скрипт печатает:

- payload (message)
- вычисленный коммит
- предоставленный коммит
- результат

Коды завершения:

- `0` — коммит корректен
- `1` — коммит некорректен

---

## Диагностика ошибок

### Нет payload или неверный тип
Если видите ошибку про `"payload"`:
- проверьте, что в JSON есть поле `payload`
- проверьте, что `payload` — строка (не объект/массив)

### `INVALID ❌`, хотя ожидаете `VALID`
Чаще всего причина — несовпадение payload:
- разная сериализация при экспорте и на сервере
- лишние пробелы/переводы строк
- другой порядок частей или разделители внутри payload

Проверяйте именно исходную сериализованную строку, которую сервер использовал для расчёта коммита.

### Ошибка чтения JSON
Если файл не читается:
- убедитесь, что это валидный JSON
- убедитесь, что кодировка UTF-8
- проверьте путь к файлу

---

## Лицензия

MIT
