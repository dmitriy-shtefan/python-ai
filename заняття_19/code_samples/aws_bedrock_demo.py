"""AWS Bedrock: tool calling через Converse API.

Встановлення:
    pip install boto3

Налаштуйте AWS credentials одним зі стандартних способів, наприклад:
    aws configure

За потреби вкажіть регіон і модель, для якої у вашому акаунті відкрито Model access:
    export AWS_REGION="us-east-1"
    export BEDROCK_MODEL_ID="amazon.nova-lite-v1:0"

Запуск:
    python aws_bedrock_demo.py
"""

import os

# boto3 — офіційний AWS SDK для Python. Через boto3.client(...) створюємо
# клієнт конкретного AWS-сервісу; тут це Bedrock Runtime для inference.
import boto3
# ClientError дозволяє окремо показати помилки AWS: відсутні credentials,
# немає доступу до моделі або вибрано неправильний регіон.
from botocore.exceptions import ClientError


MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "amazon.nova-lite-v1:0")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

SYSTEM_PROMPT = (
    "Ви асистент курсу зі створення AI-додатків на Python. "
    "Відповідайте українською, коротко і практично. "
    "Для питань про конкретне заняття використовуйте get_lesson_info."
)

# Bedrock не перетворює Python-функцію на tool автоматично. Тому описуємо
# інструмент JSON Schema: модель бачить його назву, призначення і аргументи.
TOOL_CONFIG = {
    "tools": [
        {
            "toolSpec": {
                "name": "get_lesson_info",
                "description": "Повертає коротку програму заняття курсу Python AI.",
                "inputSchema": {
                    "json": {
                        "type": "object",
                        "properties": {
                            "lesson_number": {
                                "type": "integer",
                                "description": "Номер заняття.",
                            }
                        },
                        "required": ["lesson_number"],
                    }
                },
            }
        }
    ]
}


def get_lesson_info(lesson_number: int) -> dict[str, str]:
    """Локальна реалізація інструмента, яку викликає саме наша програма."""
    lessons = {
        19: {
            "topic": "Agentic Development і CrewAI",
            "practice": "Побудувати маленький agentic workflow з ролями та перевіркою.",
        }
    }
    return lessons.get(lesson_number, {"error": "Інформації про це заняття немає."})


def run_tool(tool_use: dict) -> dict[str, str]:
    """Безпечно зіставляє запит моделі лише з дозволеним Python-інструментом."""
    if tool_use["name"] == "get_lesson_info":
        return get_lesson_info(tool_use["input"]["lesson_number"])
    return {"error": f"Інструмент {tool_use['name']} не дозволений."}


def get_text(message: dict) -> str:
    """Збирає текстові блоки з відповіді Bedrock у звичайний рядок."""
    return "".join(block["text"] for block in message["content"] if "text" in block)


def main() -> None:
    # bedrock-runtime — клієнт для виклику моделей, на відміну від bedrock
    # control-plane клієнта, який використовують для керування ресурсами.
    client = boto3.client("bedrock-runtime", region_name=AWS_REGION)
    messages = [
        {
            "role": "user",
            "content": [{"text": "Що будемо робити на занятті 19?"}],
        }
    ]

    try:
        # Converse — уніфікований Bedrock API для повідомлень різних моделей.
        # Якщо модель просить tool, у відповіді буде stopReason == "tool_use".
        response = client.converse(
            modelId=MODEL_ID,
            system=[{"text": SYSTEM_PROMPT}],
            messages=messages,
            toolConfig=TOOL_CONFIG,
            inferenceConfig={"maxTokens": 300, "temperature": 0},
        )

        while response["stopReason"] == "tool_use":
            assistant_message = response["output"]["message"]
            # Зберігаємо запит tool від моделі в історії діалогу.
            messages.append(assistant_message)
            tool_results = []

            for block in assistant_message["content"]:
                if "toolUse" not in block:
                    continue
                tool_use = block["toolUse"]
                result = run_tool(tool_use)
                # toolResult повертаємо як user message, зв'язуючи його з
                # конкретним toolUseId. Тоді модель може сформувати відповідь.
                tool_results.append(
                    {
                        "toolResult": {
                            "toolUseId": tool_use["toolUseId"],
                            "content": [{"json": result}],
                        }
                    }
                )

            messages.append({"role": "user", "content": tool_results})
            response = client.converse(
                modelId=MODEL_ID,
                system=[{"text": SYSTEM_PROMPT}],
                messages=messages,
                toolConfig=TOOL_CONFIG,
                inferenceConfig={"maxTokens": 300, "temperature": 0},
            )

        print(get_text(response["output"]["message"]))
    except ClientError as error:
        print(f"Помилка AWS Bedrock: {error.response['Error']['Message']}")


if __name__ == "__main__":
    main()
