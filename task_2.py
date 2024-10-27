"""
Модуль для створення фрактального дерева за допомогою turtle graphics.

Фрактал створюється рекурсивно, починаючи з вертикальної лінії,
від якої відходять дві менші лінії під заданими кутами.
Процес повторюється для кожної нової лінії до досягнення
заданої глибини рекурсії.
"""


import turtle
import random


def setup_turtle() -> turtle.Turtle:
    """
    Налаштовує початкові параметри черепашки.

    Returns:
        turtle.Turtle: Налаштований об'єкт черепашки
    """
    screen = turtle.Screen()
    screen.title("Фрактальне дерево")
    screen.bgcolor("light blue")
    screen.setup(800, 800)

    t = turtle.Turtle()
    t.speed('fastest')  # Максимальна швидкість малювання
    t.color("green")    # Колір дерева
    t.left(90)         # Повертаємо черепашку вгору
    t.hideturtle()     # Приховуємо черепашку

    return t


def draw_tree(t: turtle.Turtle, branch_len: float, level: int) -> None:
    """
    Рекурсивно малює фрактальне дерево.

    Args:
        t (turtle.Turtle): Об'єкт черепашки
        branch_len (float): Довжина поточної гілки
        level (int): Поточний рівень рекурсії
    """
    # Базовий випадок: якщо рівень 0 або довжина гілки замала
    if level == 0 or branch_len < 5:
        return

    # Встановлюємо товщину гілки в залежності від її довжини
    t.pensize(max(1, level * 2))

    # Встановлюємо колір в залежності від рівня
    # Від коричневого до зеленого
    if level > 3:
        t.color("brown")
    else:
        t.color("green")

    # Малюємо поточну гілку
    t.forward(branch_len)

    # Зберігаємо поточну позицію та кут
    pos = t.position()
    angle = t.heading()

    # Правий нахил
    right_angle = 30 + random.randint(-10, 10)
    right_length = branch_len * 0.7 + random.randint(-10, 10)/100

    # Лівий нахил
    left_angle = 30 + random.randint(-10, 10)
    left_length = branch_len * 0.7 + random.randint(-10, 10)/100

    # Малюємо праву гілку
    t.right(right_angle)
    draw_tree(t, right_length, level - 1)

    # Повертаємось до позиції після основної гілки
    t.penup()
    t.setposition(pos)
    t.setheading(angle)
    t.pendown()

    # Малюємо ліву гілку
    t.left(left_angle)
    draw_tree(t, left_length, level - 1)

    # Повертаємось до початкової позиції
    t.penup()
    t.setposition(pos)
    t.setheading(angle)
    t.pendown()


def main():
    """
    Головна функція програми.
    """
    random.seed(42)

    # Отримуємо рівень рекурсії від користувача
    while True:
        try:
            level = int(input("Введіть рівень рекурсії (рекомендовано 5-10): "))
            if 1 <= level <= 15:  # Обмежуємо максимальний рівень
                break
            print("Будь ласка, введіть число від 1 до 15")
        except ValueError:
            print("Будь ласка, введіть ціле число")

    # Налаштовуємо черепашку
    t = setup_turtle()

    # Встановлюємо початкову позицію
    t.penup()
    t.goto(0, -200)  # Зміщуємо початкову позицію вниз
    t.pendown()

    # Малюємо дерево
    draw_tree(t, 120, level)  # Початкова довжина гілки 120

    # Чекаємо, поки користувач закриє вікно
    turtle.done()


if __name__ == "__main__":
    main()
