"""
Модуль для візуалізації бінарної купи.

Використовує базову структуру бінарного дерева для відображення купи.
"""

import uuid
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    """
    Клас для представлення вузла у візуалізації купи.
    """
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


class BinaryHeap:
    """
    Клас для представлення та візуалізації бінарної купи.
    """
    def __init__(self, heap_type="min"):
        """
        Ініціалізація бінарної купи.

        Args:
            heap_type (str): Тип купи ("min" або "max")
        """
        self.heap = []
        self.heap_type = heap_type

    def parent(self, i: int) -> int:
        """Повертає індекс батьківського вузла"""
        return (i - 1) // 2

    def left_child(self, i: int) -> int:
        """Повертає індекс лівого нащадка"""
        return 2 * i + 1

    def right_child(self, i: int) -> int:
        """Повертає індекс правого нащадка"""
        return 2 * i + 2

    def insert(self, key: int) -> None:
        """
        Вставка нового елемента в купу.
        
        Args:
            key (int): Значення для вставки
        """
        self.heap.append(key)
        self._heapify_up(len(self.heap) - 1)

    def _heapify_up(self, i: int) -> None:
        """Відновлення властивостей купи знизу вгору"""
        parent = self.parent(i)
        if self.heap_type == "min":
            if i > 0 and self.heap[i] < self.heap[parent]:
                self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
                self._heapify_up(parent)
        else:
            if i > 0 and self.heap[i] > self.heap[parent]:
                self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
                self._heapify_up(parent)

    def create_tree_representation(self) -> Node:
        """
        Створює деревоподібне представлення купи для візуалізації.
        
        Returns:
            Node: Корінь дерева
        """
        if not self.heap:
            return None

        def create_node(i: int) -> Node:
            if i >= len(self.heap):
                return None

            # Створюємо вузол з поточним значенням
            node = Node(self.heap[i])

            # Визначаємо колір вузла в залежності від властивостей купи
            if i == 0:  # Корінь
                node.color = "lightgreen"
            elif self.heap_type == "min":
                if i > 0 and self.heap[i] < self.heap[self.parent(i)]:
                    node.color = "red"  # Порушення властивості мінімальної купи
            else:  # max heap
                if i > 0 and self.heap[i] > self.heap[self.parent(i)]:
                    node.color = "red"  # Порушення властивості максимальної купи

            # Рекурсивно створюємо лівого та правого нащадків
            left_idx = self.left_child(i)
            right_idx = self.right_child(i)

            node.left = create_node(left_idx)
            node.right = create_node(right_idx)

            return node

        return create_node(0)

def add_edges(graph, node, pos, x=0, y=0, layer=1):
    """Додає ребра до графу для візуалізації."""
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            l = add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            r = add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def visualize_heap(heap: BinaryHeap, title: str = "Бінарна купа"):
    """
    Візуалізує бінарну купу.
    
    Args:
        heap (BinaryHeap): Купа для візуалізації
        title (str): Заголовок візуалізації
    """
    root = heap.create_tree_representation()
    if not root:
        print("Купа порожня")
        return

    tree = nx.DiGraph()
    pos = {root.id: (0, 0)}
    tree = add_edges(tree, root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    plt.figure(figsize=(10, 6))
    nx.draw(tree, pos=pos, labels=labels, arrows=False,
            node_size=2500, node_color=colors)
    plt.title(title)
    plt.show()


def main():
    """
    Демонстрація роботи візуалізації бінарної купи.
    """
    # Створення та заповнення мінімальної купи
    min_heap = BinaryHeap("min")
    values = [4, 8, 2, 5, 1, 6, 3]
    for val in values:
        min_heap.insert(val)

    # Візуалізація мінімальної купи
    visualize_heap(min_heap, "Мінімальна купа")

    # Створення та заповнення максимальної купи
    max_heap = BinaryHeap("max")
    for val in values:
        max_heap.insert(val)

    # Візуалізація максимальної купи
    visualize_heap(max_heap, "Максимальна купа")


if __name__ == "__main__":
    main()
