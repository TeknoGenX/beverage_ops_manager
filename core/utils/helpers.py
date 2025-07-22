# helpers.py

def format_currency(amount, currency="USD"):
    """
    Format a number as a currency string.

    Args:
        amount (float): The amount of money.
        currency (str): The currency code (default: "USD").

    Returns:
        str: Formatted currency string.
    """
    try:
        return f"{currency} {amount:,.2f}"
    except (TypeError, ValueError):
        return f"{currency} 0.00"


def parse_percentage(value):
    """
    Parse a percentage string and return its float value.

    Args:
        value (str): Percentage string, e.g., "15%".

    Returns:
        float: The numeric value of the percentage.
    """
    try:
        return float(str(value).replace("%", "")) / 100
    except (TypeError, ValueError):
        return 0.0


def safe_int(value, default=0):
    """
    Safely convert a value to integer.

    Args:
        value: The value to convert.
        default (int): Default value if conversion fails.

    Returns:
        int: Converted integer or default.
    """
    try:
        return int(value)
    except (TypeError, ValueError):
        return default