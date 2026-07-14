"""Google ADK: агент з одним локальним інструментом.

Встановлення:
    pip install google-adk

Перед запуском задайте ключ Gemini:
    export GOOGLE_API_KEY="your-key"

Запуск:
    python google_adk_demo.py
"""

import asyncio

# Agent описує LLM-агента: модель, інструкцію та доступні йому інструменти.
from google.adk.agents import Agent
# Runner керує запуском агента: передає повідомлення, викликає tools
# і повертає події (events) роботи агента.
from google.adk.runners import Runner
# InMemorySessionService зберігає історію діалогу лише в оперативній пам'яті.
# Це зручно для demo, але після завершення програми дані зникають.
from google.adk.sessions import InMemorySessionService
# google.genai.types містить типи Gemini API. Content — повідомлення,
# Part — його окрема частина, наприклад текст.
from google.genai import types


def get_lesson_info(lesson_number: int) -> dict[str, str]:
    """Повертає коротку програму вказаного заняття курсу Python AI.

    Це локальний, контрольований інструмент: він не читає файли та не робить
    мережевих запитів. У реальному проєкті тут може бути запит до вашої БД.
    """
    lessons = {
        19: {
            "topic": "Agentic Development і CrewAI",
            "practice": "Побудувати маленький agentic workflow з ролями та перевіркою.",
        }
    }
    return lessons.get(lesson_number, {"error": "Інформації про це заняття немає."})


# Створюємо агента й даємо йому лише один безпечний локальний інструмент.
agent = Agent(
    name="course_assistant",
    model="gemini-2.5-flash",
    instruction=(
        "Ви асистент курсу зі створення AI-додатків на Python. "
        "Відповідайте українською, коротко і практично. "
        "Для питань про конкретне заняття використовуйте інструмент get_lesson_info."
    ),
    tools=[get_lesson_info],
)


async def main() -> None:
    app_name = "python_ai_course_demo"
    user_id = "student_1"
    session_id = "lesson_19_demo"

    # Сесія пов'язує кілька повідомлень одного користувача в один діалог.
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )
    # Runner не зберігає історію самостійно — для цього він використовує session_service.
    runner = Runner(agent=agent, app_name=app_name, session_service=session_service)

    # ADK очікує повідомлення у форматі Content/Part, а не звичайний рядок.
    message = types.Content(
        role="user",
        parts=[types.Part(text="Що будемо робити на занятті 19?")],
    )

    # run_async повертає події: виклики моделі, tools і фінальну відповідь.
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=message,
    ):
        if event.is_final_response() and event.content:
            print(event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(main())
