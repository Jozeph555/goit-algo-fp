"""
Модуль для роботи з однозв'язним списком.

Містить реалізацію базових, а також додаткових операцій:
- Реверсування списку
- Сортування вставками
- Об'єднання відсортованих списків
"""


class Node:
    """
    Клас для представлення вузла однозв'язного списку.

    Attributes:
        data: Дані, що зберігаються у вузлі
        next: Посилання на наступний вузол
    """
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    """
    Клас для представлення однозв'язного списку.

    Attributes:
        head: Посилання на перший вузол списку
    """
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        """Вставка вузла на початок списку"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        """Вставка вузла в кінець списку"""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return

        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new_node

    def print_list(self):
        """Виведення всіх елементів списку"""
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")

    def reverse(self):
        """
        Реверсування однозв'язного списку.

        Змінює напрямки всіх посилань між вузлами.
        Складність: O(n), де n - кількість вузлів.
        """
        prev = None
        current = self.head

        while current:
            # Зберігаємо посилання на наступний вузол
            next_node = current.next
            # Змінюємо напрямок поточного посилання
            current.next = prev
            # Переміщуємо prev і current на один крок вперед
            prev = current
            current = next_node

        # Оновлюємо head
        self.head = prev

    def insertion_sort(self):
        """
        Сортування списку методом вставки.

        Складність: O(n^2), де n - кількість вузлів.
        """
        if self.head is None or self.head.next is None:
            return

        sorted_head = None
        current = self.head

        while current:
            # Зберігаємо наступний вузол
            next_node = current.next

            # Вставляємо current у відсортовану частину
            if sorted_head is None or sorted_head.data >= current.data:
                current.next = sorted_head
                sorted_head = current
            else:
                search = sorted_head
                while search.next and search.next.data < current.data:
                    search = search.next

                current.next = search.next
                search.next = current

            current = next_node

        self.head = sorted_head

    @staticmethod
    def merge_sorted_lists(list1, list2):
        """
        Об'єднання двох відсортованих списків в один відсортований список.

        Args:
            list1: Перший відсортований список
            list2: Другий відсортований список

        Returns:
            LinkedList: Новий відсортований список

        Складність: O(n + m), де n і m - довжини списків.
        """
        merged_list = LinkedList()

        # Якщо один зі списків порожній, повертаємо інший
        if not list1.head:
            return list2
        if not list2.head:
            return list1

        # Вказівники для обох списків
        current1 = list1.head
        current2 = list2.head

        # Вибираємо перший елемент для merged_list
        if current1.data <= current2.data:
            merged_list.head = Node(current1.data)
            current1 = current1.next
        else:
            merged_list.head = Node(current2.data)
            current2 = current2.next

        current_merged = merged_list.head

        # Об'єднуємо списки
        while current1 and current2:
            if current1.data <= current2.data:
                current_merged.next = Node(current1.data)
                current1 = current1.next
            else:
                current_merged.next = Node(current2.data)
                current2 = current2.next
            current_merged = current_merged.next

        # Додаємо залишок першого списку
        while current1:
            current_merged.next = Node(current1.data)
            current1 = current1.next
            current_merged = current_merged.next

        # Додаємо залишок другого списку
        while current2:
            current_merged.next = Node(current2.data)
            current2 = current2.next
            current_merged = current_merged.next

        return merged_list


# Тестування функціоналу
def test_linked_list_operations():
    """
    Функція для тестування всіх операцій з однозв'язним списком.
    """
    # Створення та заповнення першого списку
    print("Створення першого списку:")
    list1 = LinkedList()
    list1.insert_at_end(1)
    list1.insert_at_end(3)
    list1.insert_at_end(5)
    print("Список 1:", end=" ")
    list1.print_list()

    # Створення та заповнення другого списку
    print("\nСтворення другого списку:")
    list2 = LinkedList()
    list2.insert_at_end(2)
    list2.insert_at_end(4)
    list2.insert_at_end(6)
    print("Список 2:", end=" ")
    list2.print_list()

    # Тестування реверсування
    print("\nТестування реверсування списку 1:")
    list1.reverse()
    print("Реверсований список 1:", end=" ")
    list1.print_list()

    # Тестування сортування
    print("\nТестування сортування реверсованого списку 1:")
    list1.insertion_sort()
    print("Відсортований список 1:", end=" ")
    list1.print_list()

    # Тестування об'єднання списків
    print("\nТестування об'єднання відсортованих списків:")
    merged_list = LinkedList.merge_sorted_lists(list1, list2)
    print("Об'єднаний відсортований список:", end=" ")
    merged_list.print_list()


if __name__ == "__main__":
    test_linked_list_operations()
