"""OpenAI Agents SDK: агент з одним локальним інструментом.

Встановлення:
    pip install openai-agents

Перед запуском задайте ключ:
    export OPENAI_API_KEY="your-key"

Запуск:
    python openai_agents_sdk_demo.py
"""

# Agent описує LLM-агента: інструкції, модель та список доступних tools.
# Runner запускає агентний цикл: модель -> tool (за потреби) -> модель.
# function_tool перетворює звичайну Python-функцію на tool з JSON-схемою
# аргументів, яку SDK будує з type hints і docstring.
from agents import Agent, Runner, function_tool


# Декоратор реєструє функцію як інструмент, який модель може викликати.
@function_tool
def get_lesson_info(lesson_number: int) -> str:
    """Повертає коротку програму вказаного заняття курсу Python AI."""
    lessons = {
        19: (
            "Заняття 19: Agentic Development і CrewAI. "
            "Практика: спроєктувати маленький agentic workflow з ролями, "
            "інструментами та checklist перевірки."
        )
    }
    return lessons.get(lesson_number, "Інформації про це заняття немає.")


# Агент не виконує Python-код напряму: він лише вирішує, коли попросити Runner
# викликати один із переданих tools.
agent = Agent(
    name="Course assistant",
    model="gpt-5-mini",
    instructions=(
        "Ви асистент курсу зі створення AI-додатків на Python. "
        "Відповідайте українською, коротко і практично. "
        "Для питань про конкретне заняття використовуйте get_lesson_info."
    ),
    tools=[get_lesson_info],
)


def main() -> None:
    # run_sync зручно використовувати у звичайному Python-скрипті.
    # У notebook або async-застосунку використовуйте: await Runner.run(...)
    # Runner виконує потрібні tool calls та повертає фінальний результат у final_output.
    result = Runner.run_sync(agent, "Що будемо робити на занятті 19?")
    print(result.final_output)


if __name__ == "__main__":
    main()
