# Технічне завдання

## 1. Мета

Створити Streamlit-застосунок, який демонструє роботу CrewAI на бізнес-сценарії: AI-команда готує основу маркетингової кампанії для продукту, послуги або бізнес-задачі.

Застосунок має показати послідовний multi-agent workflow:

```text
Strategy -> Channels -> Copy -> Review -> Campaign brief
```

## 2. Основний сценарій користувача

1. Користувач відкриває Streamlit-застосунок.
2. У sidebar обирає OpenRouter model і temperature.
3. У текстовому полі вводить продукт, послугу або бізнес-задачу для кампанії.
4. Натискає кнопку `Запустити CrewAI-команду`.
5. Застосунок створює LLM через OpenRouter, будує CrewAI-команду через `build_crew(topic, llm)` і запускає `crew.kickoff()`.
6. Користувач бачить фінальний campaign brief у Markdown.
7. Користувач може завантажити результат як Markdown-файл.

## 3. Технічні вимоги

| Компонент | Вимога |
|---|---|
| UI framework | Streamlit |
| Agent framework | CrewAI |
| LLM provider | OpenRouter API |
| Base URL | `https://openrouter.ai/api/v1` |
| Default model | `openai/gpt-oss-120b:free` |
| API key | `OPENROUTER_API_KEY` зі `st.secrets` або environment variables |
| Optional model env | `OPENROUTER_MODEL` |
| Crew process | `Process.sequential` |
| Agent delegation | `allow_delegation=False` |
| Output format | Markdown |
| Download filename | `crewai_marketing_campaign.md` |

## 4. UI

| Елемент | Текст |
|---|---|
| Page title | `CrewAI Marketing Campaign` |
| Main title | `CrewAI Marketing Campaign Demo` |
| Caption | `Multi-agent workflow: Strategy -> Channels -> Copy -> Review -> Campaign brief.` |
| Model input label | `OpenRouter model` |
| Temperature slider label | `Temperature` |
| Topic textarea label | `Продукт, послуга або бізнес-задача для кампанії` |
| Default topic | `AI-команда для підготовки маркетингової кампанії нового Python-курсу` |
| Run button | `Запустити CrewAI-команду` |
| Spinner | `CrewAI запускає агентів послідовно...` |
| Missing API key warning | `Додайте OPENROUTER_API_KEY у змінні середовища або Streamlit secrets.` |
| Missing API key error | `Не знайдено OPENROUTER_API_KEY.` |
| Result header | `Фінальний результат CrewAI` |
| Download button | `Завантажити Markdown` |

## 5. Agents

| Agent variable | Role | Goal | Backstory |
|---|---|---|---|
| `strategist` | `Marketing Strategist` | `Сформувати чітку концепцію маркетингової кампанії для бізнес-задачі.` | `Ви стратег з маркетингу, який швидко перетворює опис продукту або бізнес-цілі на зрозуміле позиціонування, аудиторії та ключові повідомлення.` |
| `channel_planner` | `Channel Planner` | `Підібрати ефективні канали кампанії і пояснити роль кожного з них.` | `Ви performance-маркетолог. Ви думаєте про шлях клієнта, бюджет, канали комунікації, формат контенту і прості метрики успіху.` |
| `copywriter` | `Campaign Copywriter` | `Створити тексти кампанії для різних каналів у єдиному тоні.` | `Ви копірайтер, який пише коротко, конкретно і під бізнес-результат. Ви адаптуєте одне повідомлення для email, соцмереж, реклами і сайту.` |
| `reviewer` | `Brand and Risk Reviewer` | `Перевірити кампанію на узгодженість, ризики і практичність запуску.` | `Ви маркетинговий reviewer. Ви помічаєте нечіткі обіцянки, слабкі CTA, ризики для бренду, юридичні нюанси і місця, де буде складно виміряти ефективність кампанії.` |

## 6. Tasks, Prompts, Descriptions, Expected Output

| Task variable | Agent | Prompt / description | Context | Expected output |
|---|---|---|---|---|
| `strategy_task` | `strategist` | `Тема: {topic}` + `Підготуйте основу маркетингової кампанії: бізнес-мету, цільову аудиторію, головний інсайт, позиціонування і ключову пропозицію.` | Немає | `Markdown-секція українською з пунктами: Мета, Аудиторія, Інсайт, Позиціонування, Ключова пропозиція.` |
| `channels_task` | `channel_planner` | `Тема: {topic}` + `На основі стратегії запропонуйте план каналів кампанії: які канали використати, яку роль має кожен канал, які формати контенту потрібні і які метрики варто відстежувати.` | `strategy_task` | `Markdown-таблиця: Канал \| Роль у кампанії \| Формат \| Метрика успіху.` |
| `copy_task` | `copywriter` | `Створіть набір коротких текстів для кампанії на основі стратегії і плану каналів: headline, рекламний текст, пост для соцмереж, email subject, короткий CTA.` | `strategy_task`, `channels_task` | `Markdown-секція з готовими текстами: Headline, Ad copy, Social post, Email subject, CTA.` |
| `review_task` | `reviewer` | `Перевірте кампанію перед запуском. Назвіть слабкі місця, ризики для бренду або довіри, нечіткі обіцянки, проблеми з вимірюванням і запропонуйте конкретні покращення.` | `strategy_task`, `channels_task`, `copy_task` | `Markdown-таблиця: Ризик або слабке місце \| Як покращити.` |
| `final_task` | `strategist` | `Зберіть фінальний план маркетингової кампанії на основі попередніх результатів. Пишіть коротко, структуровано і практично, щоб це можна було використати як основу для реального запуску.` | `strategy_task`, `channels_task`, `copy_task`, `review_task` | `Markdown з секціями: Назва кампанії, Бізнес-мета, Цільова аудиторія, Ключове повідомлення, Канали, Готові тексти, Метрики, Ризики.` |

## 7. Очікувана структура `build_crew`

Функція `build_crew(topic, llm)` має:

1. Створити 4 агентів через helper `create_agent`.
2. Створити 5 задач через `Task`.
3. Передати результати попередніх задач у наступні через `context`.
4. Повернути `Crew` з:

```python
Crew(
    agents=[strategist, channel_planner, copywriter, reviewer],
    tasks=[strategy_task, channels_task, copy_task, review_task, final_task],
    process=Process.sequential,
    verbose=True,
)
```

## 8. Acceptance Criteria

| Критерій | Очікувана поведінка |
|---|---|
| Запуск без API key | Застосунок показує warning, а при натисканні кнопки - error і зупиняє виконання |
| Запуск з API key | Створюється LLM, будується crew, виконується `crew.kickoff()` |
| Результат | Виводиться Markdown з фінальним планом кампанії |
| Download | Користувач може завантажити результат як `crewai_marketing_campaign.md` |
| Тематика | Усі агенти, задачі й тексти відповідають бізнес-сценарію маркетингової кампанії |
| Формат задач | Кожна задача має чіткі `description`, `expected_output`, `agent` і потрібний `context` |

