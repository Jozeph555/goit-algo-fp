"""
Модуль для розв'язання задачі вибору їжі з максимальною калорійністю
в межах заданого бюджету.

Реалізує два підходи:
1. Жадібний алгоритм
2. Динамічне програмування
"""


from typing import Dict, List, Tuple


def greedy_algorithm(items: Dict, budget: int) -> Tuple[List[str], int, int]:
    """
    Жадібний алгоритм вибору їжі.
    Обирає страви з найкращим співвідношенням калорій до вартості.

    Args:
        items: Словник з даними про їжу
        budget: Доступний бюджет

    Returns:
        Tuple[List[str], int, int]: 
            - Список обраних страв
            - Загальна вартість
            - Загальна калорійність
    """
    # Розрахунок співвідношення калорій до вартості для кожної страви
    food_efficiency = {
        name: item["calories"] / item["cost"]
        for name, item in items.items()
    }

    # Сортування страв за ефективністю
    sorted_food = sorted(food_efficiency.items(),
                        key=lambda x: x[1],
                        reverse=True)

    selected_items = []
    total_cost = 0
    total_calories = 0

    # Вибір страв
    for food_name, _ in sorted_food:
        food_cost = items[food_name]["cost"]
        if total_cost + food_cost <= budget:
            selected_items.append(food_name)
            total_cost += food_cost
            total_calories += items[food_name]["calories"]

    return selected_items, total_cost, total_calories


def dynamic_programming(items: Dict, budget: int) -> Tuple[List[str], int, int]:
    """
    Алгоритм динамічного програмування для вибору їжі.
    Знаходить оптимальний набір страв для максимізації калорійності.

    Args:
        items: Словник з даними про їжу
        budget: Доступний бюджет

    Returns:
        Tuple[List[str], int, int]: 
            - Список обраних страв
            - Загальна вартість
            - Загальна калорійність
    """
    # Створення списку страв для зручності індексації
    food_items = list(items.items())
    n = len(food_items)

    # Створення таблиці для динамічного програмування
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    # Заповнення таблиці
    for i in range(1, n + 1):
        name, properties = food_items[i-1]
        cost = properties["cost"]
        calories = properties["calories"]

        for j in range(budget + 1):
            if cost <= j:
                dp[i][j] = max(dp[i-1][j],
                             dp[i-1][j-cost] + calories)
            else:
                dp[i][j] = dp[i-1][j]

    # Відновлення розв'язку
    selected_items = []
    total_cost = 0
    curr_budget = budget

    for i in range(n, 0, -1):
        name, properties = food_items[i-1]
        cost = properties["cost"]

        # Якщо значення змінилось, значить ми взяли цю страву
        if dp[i][curr_budget] != dp[i-1][curr_budget]:
            selected_items.append(name)
            total_cost += cost
            curr_budget -= cost

    selected_items.reverse()
    total_calories = dp[n][budget]

    return selected_items, total_cost, total_calories


def compare_algorithms(items: Dict, budget: int) -> None:
    """
    Порівнює результати роботи обох алгоритмів.

    Args:
        items: Словник з даними про їжу
        budget: Доступний бюджет
    """
    print(f"Бюджет: {budget} грн\n")

    # Жадібний алгоритм
    greedy_items, greedy_cost, greedy_calories = greedy_algorithm(items, budget)
    print("Жадібний алгоритм:")
    print(f"Обрані страви: {', '.join(greedy_items)}")
    print(f"Загальна вартість: {greedy_cost} грн")
    print(f"Загальна калорійність: {greedy_calories} калорій")
    print(f"Ефективність: {greedy_calories/greedy_cost:.2f} калорій/грн\n")

    # Динамічне програмування
    dp_items, dp_cost, dp_calories = dynamic_programming(items, budget)
    print("Динамічне програмування:")
    print(f"Обрані страви: {', '.join(dp_items)}")
    print(f"Загальна вартість: {dp_cost} грн")
    print(f"Загальна калорійність: {dp_calories} калорій")
    print(f"Ефективність: {dp_calories/dp_cost:.2f} калорій/грн\n")

    # Порівняння результатів
    calories_diff = dp_calories - greedy_calories
    if calories_diff > 0:
        print(f"Динамічне програмування знайшло рішення краще на {calories_diff} калорій")
    elif calories_diff < 0:
        print(f"Жадібний алгоритм знайшов рішення краще на {-calories_diff} калорій")
    else:
        print("Обидва алгоритми знайшли однаково хороші рішення")


def main():
    """
    Головна функція програми.
    """
    # Тестові дані
    items = {
        "pizza": {"cost": 50, "calories": 300},
        "hamburger": {"cost": 40, "calories": 250},
        "hot-dog": {"cost": 30, "calories": 200},
        "pepsi": {"cost": 10, "calories": 100},
        "cola": {"cost": 15, "calories": 220},
        "potato": {"cost": 25, "calories": 350}
    }

    # Тестування з різними бюджетами
    budgets = [50, 100, 150]
    for budget in budgets:
        print("=" * 50)
        compare_algorithms(items, budget)
        print("=" * 50)
        print()


if __name__ == "__main__":
    main()
