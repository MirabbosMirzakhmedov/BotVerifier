import itertools

# List of products
products = [
    {"name": "Banana", "price": 1.5},
    {"name": "Oil", "price": 3},
    {"name": "Meat", "price": 10},
    {"name": "Bread", "price": 2},
    {"name": "Drinks", "price": 7},
    {"name": "Milk", "price": 6},
    {"name": "Oat", "price": 5},
    {"name": "Potato", "price": 2},
    {"name": "Carrot", "price": 2},
    {"name": "Onion", "price": 2},
]

# Budget
budget = 30

# Minimum amount for the total cost of the combinations
min_amount = 27

# "Important" products
important_products = [
    {"name": "Meat", "price": 10},
    {"name": "Drinks", "price": 7},
]

# List to store the combinations
combination_list = []

# Generate combinations with different numbers of products
for num_products in range(1, len(products) + 1):
    # Generate combinations with the current number of products
    combinations = itertools.combinations(products, num_products)
    # Iterate over the combinations
    for combination in combinations:
        # Add the "important" products to the combination
        combination = list(combination) + important_products
        # Calculate the total cost of the combination
        total_cost = sum(product["price"] for product in combination)
        # If the total cost is greater than or equal to the minimum amount and less than or equal to the budget, add the combination to the list
        if total_cost >= min_amount and total_cost <= budget:
            combination_list.append({"combination": combination, "total_cost": total_cost})

# Sort the list of combinations based on the total cost
combination_list.sort(key=lambda x: x["total_cost"])

# Iterate over the sorted list of combinations and print them
for i, combination in enumerate(combination_list, start=1):
    print(f"{i}st combination")
    print('------------------')
    for product in combination["combination"]:
        print(f"{product['name']} - {product['price']}€")
    print(f"TOTAL COST: {combination['total_cost']}€\n\n")
