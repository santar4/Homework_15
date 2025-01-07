# Santar4 Art Gallery and File Upload API

API для завантаження, зберігання та обробки художніх творів, а також файлів.

## Опис

Цей API дозволяє завантажувати зображення та інші файли на сервер. Крім того, файли можна  завантажувати на сервер та із сервера за допомогою відповідних API.

## Використанні Технології

- **FastAPI** — фреймворк для створення API
- **Uvicorn** — ASGI сервер для запуску FastAPI додатків
- **PIL (Pillow)** — бібліотека для обробки зображень
- **Python 3.7+**

## Встановлення

1. **Клонуйте репозиторій**:
   ```bash
   git clone https://github.com/santar4/Homework_15
   
   ```
   
2. **Встановіть залежності**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Запустіть сервер**:

    Запустіть сервер за допомогою Uvicorn:

    ```bash
    uvicorn main:app --reload
    ```