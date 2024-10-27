"""
Модуль для реалізації алгоритму Дейкстри з використанням бінарної купи
для знаходження найкоротших шляхів у зваженому графі.

Основні компоненти:
1. Створення зваженого графа
2. Реалізація алгоритму Дейкстри з використанням heapq
"""


from typing import Dict
import heapq
from collections import defaultdict


class Graph:
    """
    Клас для представлення зваженого графа.
    """
    def __init__(self):
        """Ініціалізація графа з використанням defaultdict"""
        self.edges = defaultdict(dict)
        self.nodes = set()

    def add_node(self, node: str) -> None:
        """Додавання вершини"""
        self.nodes.add(node)

    def add_edge(self, u: str, v: str, weight: int) -> None:
        """Додавання ребра з вагою"""
        self.edges[u][v] = weight
        self.edges[v][u] = weight  # для неорієнтованого графа

    def get_neighbors(self, node: str) -> Dict[str, int]:
        """Отримання сусідів вершини"""
        return self.edges[node]


def dijkstra(graph: Graph, start: str) -> Dict[str, float]:
    """
    Реалізує алгоритм Дейкстри з використанням бінарної купи.

    Args:
        graph (Graph): Зважений граф
        start (str): Початкова вершина

    Returns:
        Dict[str, float]: Словник відстаней від початкової вершини до всіх інших
    """
    # Ініціалізація відстаней
    distances = {node: float('infinity') for node in graph.nodes}
    distances[start] = 0

    # Використання бінарної купи для оптимізації вибору вершин
    heap = [(0, start)]  # (відстань, вершина)
    visited = set()

    while heap:
        # Вибір вершини з найменшою відстанню
        current_distance, current = heapq.heappop(heap)

        if current in visited:
            continue

        visited.add(current)

        # Перегляд всіх сусідів поточної вершини
        for neighbor, weight in graph.get_neighbors(current).items():
            if neighbor not in visited:
                distance = current_distance + weight

                # Якщо знайдено коротший шлях
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(heap, (distance, neighbor))

    return distances


def main():
    """
    Головна функція програми.
    """
    # Створення тестового графа
    graph = Graph()

    # Додавання вершин
    vertices = ["A", "B", "C", "D", "E"]
    for vertex in vertices:
        graph.add_node(vertex)

    # Додавання ребер з вагами
    edges = [
        ("A", "B", 4), ("A", "C", 2),
        ("B", "C", 1), ("B", "D", 5),
        ("C", "D", 8), ("C", "E", 10),
        ("D", "E", 2)
    ]

    for u, v, w in edges:
        graph.add_edge(u, v, w)

    # Знаходження найкоротших шляхів від вершини A
    start_vertex = "A"
    distances = dijkstra(graph, start_vertex)

    # Виведення результатів
    print(f"\nНайкоротші шляхи від вершини {start_vertex}:")
    for vertex in sorted(graph.nodes):
        if vertex != start_vertex:
            print(f"До {vertex}: {distances[vertex]}")


if __name__ == "__main__":
    main()
