"""LangGraph: агентний цикл LLM -> tool -> LLM.

Встановлення:
    pip install -U langgraph langchain-openai

Перед запуском задайте ключ:
    export OPENAI_API_KEY="your-key"

Запуск:
    python langgraph_demo.py
"""

# HumanMessage — тип повідомлення від користувача у history графа.
from langchain_core.messages import HumanMessage
# @tool перетворює Python-функцію на інструмент, який можна передати моделі.
from langchain_core.tools import tool
# ChatOpenAI — інтеграція LangChain для виклику моделей OpenAI.
from langchain_openai import ChatOpenAI
# StateGraph описує workflow як граф. MessagesState — готовий state
# зі списком повідомлень; START і END позначають початок і кінець графа.
from langgraph.graph import END, START, MessagesState, StateGraph
# ToolNode сам виконує tool calls моделі. tools_condition вирішує,
# чи перейти до ToolNode, чи завершити граф після відповіді моделі.
from langgraph.prebuilt import ToolNode, tools_condition


# Декоратор формує опис інструмента зі signature та docstring функції.
@tool
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


# bind_tools передає моделі схеми доступних інструментів, щоб вона могла
# повертати структурований запит на їх виклик замість звичайного тексту.
tools = [get_lesson_info]
llm = ChatOpenAI(model="gpt-5-mini", temperature=0).bind_tools(tools)


def call_model(state: MessagesState) -> dict:
    """Викликає модель; вона може відповісти або попросити викликати tool."""
    system_message = (
        "Ви асистент курсу зі створення AI-додатків на Python. "
        "Відповідайте українською, коротко і практично. "
        "Для питань про конкретне заняття використовуйте get_lesson_info."
    )
    response = llm.invoke([{"role": "system", "content": system_message}, *state["messages"]])
    return {"messages": [response]}


def build_graph():
    # StateGraph зберігає history повідомлень і правила переходів між вузлами.
    graph = StateGraph(MessagesState)
    graph.add_node("agent", call_model)
    # ToolNode отримує tool call з останнього повідомлення моделі та викликає Python-функцію.
    graph.add_node("tools", ToolNode(tools))
    graph.add_edge(START, "agent")
    # Після моделі: є tool call -> tools, немає -> END.
    graph.add_conditional_edges("agent", tools_condition, {"tools": "tools", END: END})
    # Результат tool повертаємо моделі, щоб вона сформулювала відповідь користувачу.
    graph.add_edge("tools", "agent")
    return graph.compile()


if __name__ == "__main__":
    app = build_graph()
    result = app.invoke({"messages": [HumanMessage(content="Що будемо робити на занятті 19?")]})
    print(result["messages"][-1].content)
