# Приклади MCP Prompts

## 1. Аналіз падіння revenue

```python
@mcp.prompt()
def analyze_revenue_drop():
    return """
    Analyze a revenue drop.

    Follow these steps:

    1. Read the revenue metric definition.
    2. Read relevant business rules.
    3. Compare the current period with the previous period.
    4. Identify the dimensions with the largest decline.
    5. Check whether refunds affected the result.
    6. Summarize the top 3 likely causes.
    """
```

```text
Prompt
  ↓
Read metric definitions
  ↓
Read business rules
  ↓
Call compare_periods
  ↓
Call query_sales
  ↓
Analyze result
  ↓
Prepare summary
```

## 2. Перевірка pull request

```python
@mcp.prompt()
def review_pull_request(pr_number: int):
    return f"""
    Review pull request #{pr_number}.

    First read:
    - coding guidelines
    - architecture rules
    - security rules

    Then:
    1. Get the PR diff.
    2. Identify correctness issues.
    3. Identify security risks.
    4. Check architecture violations.
    5. Separate blocking issues from suggestions.

    Do not add comments automatically.
    """
```

## 3. Запит на повернення коштів

```python
@mcp.prompt()
def investigate_refund_request(customer_id: int):
    return f"""
    Investigate a refund request for customer {customer_id}.

    Read the refund policy first.

    Then:
    1. Get customer information.
    2. Check the subscription.
    3. Review recent payments.
    4. Determine refund eligibility.

    Do not create a refund.

    Return:
    - eligibility
    - reason
    - recommended next action
    """
```

## 4. Аналіз продажів із параметрами

```python
@mcp.prompt()
def analyze_sales(country: str, period: str):
    return f"""
    Analyze sales performance.

    Country: {country}
    Period: {period}

    Compare the period with the previous equivalent period.

    Identify:
    - revenue change
    - purchase count change
    - conversion change

    Return the three most important findings.
    """
```

```text
Analyze Sales

country = Ukraine
period = June 2026
```

## 5. Відповідь на запитання за документацією (RAG)

```python
@mcp.prompt()
def answer_product_question(question: str):
    return f"""
    Answer the following product question:

    {question}

    Search the product documentation first.

    Base the answer only on retrieved documentation.

    If the documentation does not contain the answer,
    clearly say that the information was not found.

    Cite the relevant documentation sections.
    """
```

## 6. Ресторан

```text
Resources:
recipe://pizza
recipe://pasta
recipe://soup

Tools:
heat_oven()
mix()
cut()
```

```text
Prepare a vegetarian dinner.

1. Check vegetarian recipes.
2. Select a dish under 30 minutes.
3. Check available ingredients.
4. Prepare the dish.
5. Explain what was prepared.
```
