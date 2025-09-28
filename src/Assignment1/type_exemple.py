def calculate_total_price(items: list[float], tax_rate: float) -> float:
    """Calculate total price including tax."""
    subtotal = sum(items)
    return subtotal * (1 + tax_rate)


# Usage
prices = [10.99, 25.50, 5.99]
total = calculate_total_price(prices, 0.19)
print(f"Total: {total:.2f}")
