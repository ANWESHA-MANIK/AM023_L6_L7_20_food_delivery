
import math
import re


def parse_order(items_csv):
    if not isinstance(items_csv, str):
        raise ValueError("Order must be a string")

    if not items_csv.strip():
        raise ValueError("Order cannot be empty")

    order = {}

    for item in items_csv.split(','):
        parts = item.split(':')

        if len(parts) != 2:
            raise ValueError("Each item must have name:quantity format")

        name, qty = parts
        name = name.strip()
        qty = qty.strip()

        if not name:
            raise ValueError("Item name cannot be empty")

        try:
            quantity = int(qty)
        except ValueError:
            raise ValueError("Quantity must be an integer")

        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        order[name] = quantity

    return order


def delivery_eta(distance_km):
    try:
        distance = float(distance_km)
    except (ValueError, TypeError):
        raise ValueError("Distance must be a valid number")

    if not math.isfinite(distance) or distance < 0:
        raise ValueError("Distance must be finite and non-negative")

    return int(15 + distance * 4)


def coupon_discount(code):
    if not isinstance(code, str):
        raise ValueError("Coupon code must be a string")

    match = re.fullmatch(r"SAVE(\d+)", code.strip(), re.IGNORECASE)

    if not match:
        raise ValueError("Invalid coupon code")

    return int(match.group(1))


def main():
    print("==== Running parse_order ====")
    user_input = input("Enter items as name:qty CSV (e.g. pizza:2,burger:1): ")
    try:
        result = parse_order(user_input)
        print("Order:", result)
    except ValueError as error:
        print("Invalid order:", error)

    print("\n==== Running delivery_eta ====")
    user_input = input("Enter distance in km (e.g. 4.5): ")
    try:
        result = delivery_eta(user_input)
        print("ETA in Minutes:", result)
    except ValueError as error:
        print("Invalid distance:", error)

    print("\n==== Running coupon_discount ====")
    user_input = input("Enter a coupon code (e.g. SAVE50): ")
    try:
        result = coupon_discount(user_input)
        print("Discount:", result)
    except ValueError as error:
        print("Invalid coupon:", error)


if __name__ == "__main__":
    main()
