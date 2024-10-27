"""
Модуль для симуляції кидків кубиків та аналізу ймовірностей сум.
Використовує метод Монте-Карло для експериментального визначення ймовірностей
та порівнює їх з теоретичними значеннями.
"""


import random
from typing import Dict
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd



def simulate_dice_rolls(num_simulations: int = 1000000) -> Dict[int, int]:
    """
    Симулює кидки двох кубиків задану кількість разів.

    Args:
        num_simulations: Кількість симуляцій

    Returns:
        Dict[int, int]: Словник, де ключ - сума, значення - кількість випадань
    """
    results = defaultdict(int)

    for _ in range(num_simulations):
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        total = dice1 + dice2
        results[total] += 1

    return results


def calculate_probabilities(results: Dict[int, int]) -> Dict[int, float]:
    """
    Розраховує ймовірності для кожної суми.

    Args:
        results: Словник з результатами симуляцій

    Returns:
        Dict[int, float]: Словник з ймовірностями для кожної суми
    """
    total_rolls = sum(results.values())
    probabilities = {
        sum_value: count / total_rolls
        for sum_value, count in results.items()
    }
    return probabilities


def get_theoretical_probabilities() -> Dict[int, float]:
    """
    Повертає теоретичні ймовірності для кожної суми.

    Returns:
        Dict[int, float]: Словник з теоретичними ймовірностями
    """
    # Всього можливих комбінацій: 6 * 6 = 36
    theoretical = {
        2: 1/36,   # (1,1)
        3: 2/36,   # (1,2), (2,1)
        4: 3/36,   # (1,3), (2,2), (3,1)
        5: 4/36,   # (1,4), (2,3), (3,2), (4,1)
        6: 5/36,   # (1,5), (2,4), (3,3), (4,2), (5,1)
        7: 6/36,   # (1,6), (2,5), (3,4), (4,3), (5,2), (6,1)
        8: 5/36,   # (2,6), (3,5), (4,4), (5,3), (6,2)
        9: 4/36,   # (3,6), (4,5), (5,4), (6,3)
        10: 3/36,  # (4,6), (5,5), (6,4)
        11: 2/36,  # (5,6), (6,5)
        12: 1/36   # (6,6)
    }
    return theoretical


def create_comparison_table(experimental: Dict[int, float],
                          theoretical: Dict[int, float]) -> pd.DataFrame:
    """
    Створює порівняльну таблицю експериментальних і теоретичних ймовірностей.

    Args:
        experimental: Експериментальні ймовірності
        theoretical: Теоретичні ймовірності

    Returns:
        pd.DataFrame: Таблиця порівняння
    """
    data = {
        'Сума': list(range(2, 13)),
        'Експериментальна ймовірність': [experimental[i] for i in range(2, 13)],
        'Теоретична ймовірність': [theoretical[i] for i in range(2, 13)],
        'Різниця': [abs(experimental[i] - theoretical[i]) for i in range(2, 13)]
    }

    df = pd.DataFrame(data)
    df = df.round(4)  # Округлення до 4 знаків після коми
    return df


def plot_probabilities(experimental: Dict[int, float],
                      theoretical: Dict[int, float]) -> None:
    """
    Створює графік порівняння експериментальних і теоретичних ймовірностей.

    Args:
        experimental: Експериментальні ймовірності
        theoretical: Теоретичні ймовірності
    """
    sums = list(range(2, 13))

    plt.figure(figsize=(12, 6))
    width = 0.35

    plt.bar([x - width/2 for x in sums],
            [experimental[x] for x in sums],
            width,
            label='Експериментальні',
            color='skyblue')

    plt.bar([x + width/2 for x in sums],
            [theoretical[x] for x in sums],
            width,
            label='Теоретичні',
            color='lightgreen')

    plt.xlabel('Сума')
    plt.ylabel('Ймовірність')
    plt.title('Порівняння експериментальних і теоретичних ймовірностей')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()


def main():
    """
    Головна функція програми.
    """
    # Встановлюємо seed для відтворюваності результатів
    random.seed(42)

    # Кількість симуляцій
    num_simulations = 1_000_000

    # Проводимо симуляції
    print(f"Проводимо {num_simulations:,} симуляцій...")
    results = simulate_dice_rolls(num_simulations)

    # Розраховуємо ймовірності
    experimental_prob = calculate_probabilities(results)
    theoretical_prob = get_theoretical_probabilities()

    # Створюємо та виводимо порівняльну таблицю
    comparison_table = create_comparison_table(experimental_prob, theoretical_prob)
    print("\nПорівняльна таблиця ймовірностей:")
    print(comparison_table)

    # Зберігаємо таблицю у файл
    comparison_table.to_csv('dice_probabilities.csv', index=False)

    # Візуалізуємо результати
    plot_probabilities(experimental_prob, theoretical_prob)

    # Обчислюємо максимальну різницю
    max_diff = max(abs(experimental_prob[i] - theoretical_prob[i])
                  for i in range(2, 13))
    print(f"\nМаксимальна різниця між експериментальними та "
          f"теоретичними ймовірностями: {max_diff:.4f}")


if __name__ == "__main__":
    main()
