"""
Модуль для анімованої візуалізації обходів бінарного дерева.
Реалізує обхід у глибину (DFS) та в ширину (BFS) з анімацією кроків.
"""


import uuid
from typing import List, Dict
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Node:
    """Клас для представлення вузла бінарного дерева."""
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


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


def generate_color_gradient(steps: int) -> List[str]:
    """Генерує градієнт кольорів від темного до світлого."""
    colors = []
    for i in range(steps):
        intensity = int(255 * (i + 1) / steps)
        color = f"#{intensity:02x}{intensity//2:02x}ff"
        colors.append(color)
    return colors


def get_all_nodes(root: Node) -> List[Node]:
    """Отримує список всіх вузлів дерева."""
    nodes = []
    stack = [root]
    while stack:
        node = stack.pop()
        nodes.append(node)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return nodes


def create_graph_state(root: Node):
    """Створює стан графа для анімації."""
    tree = nx.DiGraph()
    pos = {root.id: (0, 0)}
    tree = add_edges(tree, root, pos)
    return tree, pos


def dfs_iterative(root: Node) -> List[Dict]:
    """Ітеративний обхід дерева в глибину."""
    if not root:
        return []

    # Підраховуємо загальну кількість вершин
    total_nodes = len(get_all_nodes(root))
    # Генеруємо кольори відповідно до кількості вершин
    colors = generate_color_gradient(total_nodes)

    visited = set()
    stack = [root]
    states = []
    step = 0

    while stack:
        node = stack.pop()  # Беремо останній елемент (pop замість popleft)
        if node.id not in visited:
            visited.add(node.id)
            node.color = colors[step]
            step += 1

            # Зберігаємо поточний стан дерева
            state = {n.id: n.color for n in get_all_nodes(root)}
            states.append(state)

            # Додаємо спочатку правого, потім лівого нащадка
            # для обходу зліва направо
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

    return states


def bfs_iterative(root: Node) -> List[Dict]:
    """Ітеративний обхід дерева в ширину."""
    if not root:
        return []

    # Підраховуємо загальну кількість вершин
    total_nodes = len(get_all_nodes(root))
    # Генеруємо кольори відповідно до кількості вершин
    colors = generate_color_gradient(total_nodes)

    visited = set()
    queue = deque([root])
    states = []
    step = 0

    while queue:
        node = queue.popleft()
        if node.id not in visited:
            visited.add(node.id)
            node.color = colors[step % len(colors)]
            step += 1
            state = {n.id: n.color for n in get_all_nodes(root)}
            states.append(state)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return states


def animate_traversal(root: Node, traversal_func, traversal_name: str):
    """Створює анімацію обходу дерева."""
    states = traversal_func(root)
    fig, ax = plt.subplots(figsize=(8, 5))

    def update(frame):
        ax.clear()

        # Оновлюємо кольори вузлів відповідно до поточного стану
        for node in get_all_nodes(root):
            node.color = states[frame][node.id]

        # Оновлюємо граф
        tree, pos = create_graph_state(root)
        colors = [node[1]['color'] for node in tree.nodes(data=True)]
        labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

        nx.draw(tree, pos=pos, labels=labels, arrows=False,
                node_size=2500, node_color=colors, ax=ax)
        ax.set_title(f"{traversal_name} - Крок {frame + 1}")

    # Створюємо анімацію
    anim = FuncAnimation(fig, update, frames=len(states),
                        interval=1000, repeat=False)

    # Зберігаємо анімацію у файл
    anim.save(f'{traversal_name}_traversal.gif',
              writer='pillow')

    plt.show()


def main():
    """Головна функція"""
    root = Node(0)  # Рівень 0 (корінь)

    # Рівень 1
    root.left = Node(4)
    root.right = Node(1)

    # Рівень 2
    root.left.left = Node(5)
    root.left.right = Node(9)
    root.right.left = Node(2)
    root.right.right = Node(8)

    # Рівень 3
    root.left.left.left = Node(7)
    root.left.left.right = Node(12)
    root.left.right.left = Node(15)
    root.left.right.right = Node(10)
    root.right.left.left = Node(3)
    root.right.left.right = Node(6)
    root.right.right.left = Node(11)
    root.right.right.right = Node(14)

    # Рівень 4 (додатково для більшої глибини)
    root.left.left.left.left = Node(13)
    root.left.left.right.right = Node(16)
    root.right.right.left.left = Node(17)
    root.right.right.right.right = Node(20)

    # Анімація DFS
    print("Анімація обходу в глибину (DFS)...")
    animate_traversal(root, dfs_iterative, "DFS")

    # Скидання кольорів
    for node in get_all_nodes(root):
        node.color = "skyblue"

    # Анімація BFS
    print("Анімація обходу в ширину (BFS)...")
    animate_traversal(root, bfs_iterative, "BFS")

if __name__ == "__main__":
    main()
