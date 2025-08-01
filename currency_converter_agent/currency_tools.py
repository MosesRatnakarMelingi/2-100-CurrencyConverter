import os
import requests
from dotenv import load_dotenv
from langchain_core.tools import tool

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
EXCHANGE_RATE_API_KEY = os.getenv("EXCHANGE_RATE_API_KEY")
BASE_URL = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API_KEY}/latest/"

# Mapping for common currency names and symbols to their 3-letter codes
CURRENCY_CODES = {
    "usd": "USD", "dollar": "USD", "dollars": "USD", "$": "USD",
    "eur": "EUR", "euro": "EUR", "euros": "EUR", "€": "EUR",
    "jpy": "JPY", "yen": "JPY",
    "gbp": "GBP", "pound": "GBP", "pounds": "GBP", "£": "GBP",
    "cad": "CAD", "canadian dollar": "CAD",
    "php": "PHP", "philippine peso": "PHP",
    "inr": "INR", "indian rupee": "INR", "rupee": "INR", "₹": "INR"
    # Add more mappings as needed
}

@tool
def get_currency_code(currency: str) -> str:
    """
    Finds the 3-letter currency code for a given currency name or symbol.
    Returns the code if found, otherwise returns an error message.

    Args:
        currency (str): The currency name or symbol (e.g., "dollar", "€", "INR").

    Returns:
        A string with the 3-letter currency code or an error message.
    """
    code = CURRENCY_CODES.get(currency.lower())
    if code:
        return code
    return f"Error: Could not find currency code for '{currency}'. Please provide a standard 3-letter code like 'USD'."

@tool
def convert_currency(amount: float, source_currency: str, target_currency: str) -> str:
    """
    Converts an amount from a source currency to a target currency.

    Args:
        amount (float): The amount of money to convert.
        source_currency (str): The currency code of the source currency (e.g., "USD").
        target_currency (str): The currency code of the target currency (e.g., "EUR").

    Returns:
        A string with the converted amount and the target currency,
        or an error message if the conversion fails.
    """
    try:
        # Construct the API URL for the source currency
        url = f"{BASE_URL}{source_currency.upper()}"
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        # Check if the API request was successful
        if data.get("result") != "success":
            return f"Error: API request failed. Reason: {data.get('error-type')}"

        # Get the exchange rate
        exchange_rate = data["conversion_rates"].get(target_currency.upper())

        if exchange_rate is None:
            return f"Error: Could not find exchange rate for {target_currency.upper()}"

        # Calculate the converted amount
        converted_amount = amount * exchange_rate

        # Format the output string
        return f"{amount} {source_currency.upper()} is equal to {converted_amount:.2f} {target_currency.upper()}"

    except requests.exceptions.RequestException as e:
        return f"Error connecting to the Exchange Rate API: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"