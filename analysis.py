orders = [
    {"item": "Pizza", "price": 141, "quantity": 3},
    {"item": "Burger", "price": 171, "quantity": 1},
    {"item": "Coffee", "price": 194, "quantity": 3},
    {"item": "Pasta", "price": 137, "quantity": 1},
    {"item": "Pizza", "price": 206, "quantity": 3}
]

print("\nRestaurant Order Analytics\n")

total_revenue = 0

for order in orders:
    total = order["price"] * order["quantity"]
    total_revenue += total

    print(f'''
Item      : {order["item"]}
Price     : {order["price"]}
Quantity  : {order["quantity"]}
Total     : {total}
-----------------------------
''')

print(f"Overall Revenue: {total_revenue}")