# Currency Converter AI Agent

## 🌐 Project Overview

This project is a sophisticated AI agent designed to perform real-time currency conversions. It goes beyond a simple API call by using an LLM to reason about user queries, handle natural language inputs like "dollars" or "yen," and securely fetch up-to-date exchange rates using a dedicated tool.

This agent is part of my #TheAgenticQuest, a journey to build and document 100 AI agents to master the principles of agentic AI.

## ⚙️ How It Works

The agent operates on a multi-step, tool-chaining process:

1.  **User Input:** The agent receives a natural language query, such as "How much is 100 dollars in euros?"
2.  **LLM Reasoning:** The agent's core, powered by the Groq Llama 3 model, analyzes the query. It identifies that the user has provided currency names ("dollars") instead of standard codes ("USD").
3.  **Tool Selection (`get_currency_code`):** The LLM intelligently selects the `get_currency_code` tool to translate the natural language into a standard three-letter currency code.
4.  **Tool Chaining (`convert_currency`):** Once it has the standard codes, the LLM calls the `convert_currency` tool with the correct parameters (`amount=100`, `source_currency='USD'`, `target_currency='EUR'`).
5.  **API Integration:** The `convert_currency` tool makes a secure API request to the ExchangeRate-API to get the current exchange rate.
6.  **Final Response:** The LLM receives the API's output and formats it into a concise, human-friendly response for the user.

This process highlights the agent's ability to plan and execute a sequence of actions to fulfill a request.

## 🛠️ Technology Stack

* **LLM:** [Llama 3](https://llama.meta.com/) (via [Groq](https://groq.com/) for fast inference)
* **Framework:** [LangChain](https://www.langchain.com/)
* **Tools & APIs:** Two custom tools were built: `get_currency_code` (for name-to-code conversion) and `convert_currency` (using [ExchangeRate-API](https://www.exchangerate-api.com/)).
* **Environment:** GitHub Codespaces

## 🚀 Getting Started

Follow these steps to set up and run the agent in your own environment.

### Prerequisites

* A [Groq API Key](https://console.groq.com/keys)
* An [ExchangeRate-API Key](https://www.exchangerate-api.com/)
* Python 3.10 or higher

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [Your Repository URL Here]
    cd [Your Repository Name Here]
    ```

2.  **Install dependencies:**
    ```bash
    pip install -U langchain-groq langchain-community requests python-dotenv
    ```

3.  **Set up environment variables:**
    Create a `.env` file in the project's root directory and add your API keys.

    ```
    GROQ_API_KEY="your_groq_api_key_here"
    EXCHANGE_RATE_API_KEY="your_exchange_rate_api_key_here"
    ```

### Usage

Run the agent from your terminal. It will start an interactive command-line interface.

```bash
python main.py
