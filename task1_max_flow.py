"""
Завдання 1. Застосування алгоритму максимального потоку для логістики товарів.
Реалізація алгоритму Едмондса-Карпа для знаходження максимального потоку в мережі.
"""

from collections import defaultdict, deque
from typing import Dict, List, Tuple


class MaxFlowNetwork:
    """Клас для роботи з мережею потоків."""
    
    def __init__(self):
        """Ініціалізація мережі."""
        self.graph = defaultdict(dict)  # граф пропускних здатностей
        self.nodes = set()
        
    def add_edge(self, from_node: str, to_node: str, capacity: int):
        """
        Додає ребро до графа.
        
        Args:
            from_node: Вихідна вершина
            to_node: Цільова вершина
            capacity: Пропускна здатність ребра
        """
        self.graph[from_node][to_node] = capacity
        self.nodes.add(from_node)
        self.nodes.add(to_node)
        # Додаємо зворотне ребро з нульовою пропускною здатністю
        if to_node not in self.graph:
            self.graph[to_node] = {}
        if from_node not in self.graph[to_node]:
            self.graph[to_node][from_node] = 0
    
    def bfs(self, source: str, sink: str, parent: Dict[str, str]) -> bool:
        """
        Пошук в ширину для знаходження шляху від джерела до стоку.
        
        Args:
            source: Вершина-джерело
            sink: Вершина-стік
            parent: Словник для збереження батьківських вершин
            
        Returns:
            True, якщо існує шлях від джерела до стоку, інакше False
        """
        visited = {source}
        queue = deque([source])
        
        while queue:
            node = queue.popleft()
            
            for neighbor, capacity in self.graph[node].items():
                if neighbor not in visited and capacity > 0:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    parent[neighbor] = node
                    if neighbor == sink:
                        return True
        
        return False
    
    def edmonds_karp(self, source: str, sink: str) -> Tuple[int, Dict[Tuple[str, str], int]]:
        """
        Алгоритм Едмондса-Карпа для знаходження максимального потоку.
        
        Args:
            source: Вершина-джерело
            sink: Вершина-стік
            
        Returns:
            Кортеж (максимальний потік, словник потоків по ребрах)
        """
        parent = {}
        max_flow = 0
        flow_graph = defaultdict(lambda: defaultdict(int))
        
        # Створюємо копію графа для роботи
        residual_graph = defaultdict(dict)
        for node in self.graph:
            for neighbor, capacity in self.graph[node].items():
                residual_graph[node][neighbor] = capacity
        
        # Зберігаємо копію в об'єкті для використання в bfs
        original_graph = self.graph
        
        while True:
            self.graph = residual_graph
            parent.clear()
            
            if not self.bfs(source, sink, parent):
                break
            
            # Знаходимо мінімальну пропускну здатність на шляху
            path_flow = float('inf')
            s = sink
            while s != source:
                path_flow = min(path_flow, residual_graph[parent[s]][s])
                s = parent[s]
            
            # Оновлюємо залишкові здатності ребер і зворотних ребер
            v = sink
            while v != source:
                u = parent[v]
                residual_graph[u][v] -= path_flow
                residual_graph[v][u] += path_flow
                
                # Записуємо фактичний потік
                if residual_graph[v][u] > 0 and original_graph[u].get(v, 0) > 0:
                    flow_graph[u][v] = residual_graph[v][u]
                
                v = parent[v]
            
            max_flow += path_flow
        
        # Відновлюємо оригінальний граф
        self.graph = original_graph
        
        return max_flow, dict(flow_graph)


def create_logistics_network() -> MaxFlowNetwork:
    """
    Створює логістичну мережу відповідно до завдання.
    
    Returns:
        Об'єкт мережі потоків
    """
    network = MaxFlowNetwork()
    
    # Додаємо ребра згідно з таблицею
    edges = [
        # Від терміналів до складів
        ("Термінал 1", "Склад 1", 25),
        ("Термінал 1", "Склад 2", 20),
        ("Термінал 1", "Склад 3", 15),
        ("Термінал 2", "Склад 3", 15),
        ("Термінал 2", "Склад 4", 30),
        ("Термінал 2", "Склад 2", 10),
        
        # Від складів до магазинів
        ("Склад 1", "Магазин 1", 15),
        ("Склад 1", "Магазин 2", 10),
        ("Склад 1", "Магазин 3", 20),
        ("Склад 2", "Магазин 4", 15),
        ("Склад 2", "Магазин 5", 10),
        ("Склад 2", "Магазин 6", 25),
        ("Склад 3", "Магазин 7", 20),
        ("Склад 3", "Магазин 8", 15),
        ("Склад 3", "Магазин 9", 10),
        ("Склад 4", "Магазин 10", 20),
        ("Склад 4", "Магазин 11", 10),
        ("Склад 4", "Магазин 12", 15),
        ("Склад 4", "Магазин 13", 5),
        ("Склад 4", "Магазин 14", 10),
    ]
    
    for from_node, to_node, capacity in edges:
        network.add_edge(from_node, to_node, capacity)
    
    return network


def add_super_source_and_sink(network: MaxFlowNetwork) -> Tuple[str, str]:
    """
    Додає супер-джерело та супер-стік до мережі.
    
    Args:
        network: Мережа потоків
        
    Returns:
        Кортеж (супер-джерело, супер-стік)
    """
    super_source = "Супер-Джерело"
    super_sink = "Супер-Стік"
    
    # З'єднуємо супер-джерело з терміналами
    network.add_edge(super_source, "Термінал 1", float('inf'))
    network.add_edge(super_source, "Термінал 2", float('inf'))
    
    # З'єднуємо магазини з супер-стоком
    for i in range(1, 15):
        network.add_edge(f"Магазин {i}", super_sink, float('inf'))
    
    return super_source, super_sink


def calculate_terminal_to_store_flows(
    flow_graph: Dict[Tuple[str, str], int],
    network: MaxFlowNetwork
) -> Dict[Tuple[str, str], int]:
    """
    Обчислює потоки від терміналів до магазинів через склади.
    
    Args:
        flow_graph: Словник потоків по ребрах
        network: Мережа потоків
        
    Returns:
        Словник потоків від терміналів до магазинів
    """
    terminal_to_store = defaultdict(int)
    
    # Для кожного магазину знаходимо, скільки товару надходить від кожного термінала
    for store_num in range(1, 15):
        store = f"Магазин {store_num}"
        
        # Знаходимо склад, який постачає цей магазин
        for warehouse_num in range(1, 5):
            warehouse = f"Склад {warehouse_num}"
            
            # Потік від складу до магазину
            warehouse_to_store_flow = flow_graph.get(warehouse, {}).get(store, 0)
            
            if warehouse_to_store_flow > 0:
                # Знаходимо термінали, які постачають цей склад
                terminal1_to_warehouse = flow_graph.get("Термінал 1", {}).get(warehouse, 0)
                terminal2_to_warehouse = flow_graph.get("Термінал 2", {}).get(warehouse, 0)
                
                total_to_warehouse = terminal1_to_warehouse + terminal2_to_warehouse
                
                if total_to_warehouse > 0:
                    # Розподіляємо пропорційно
                    if terminal1_to_warehouse > 0:
                        proportion = terminal1_to_warehouse / total_to_warehouse
                        terminal_to_store[("Термінал 1", store)] += int(warehouse_to_store_flow * proportion)
                    
                    if terminal2_to_warehouse > 0:
                        proportion = terminal2_to_warehouse / total_to_warehouse
                        terminal_to_store[("Термінал 2", store)] += int(warehouse_to_store_flow * proportion)
    
    return dict(terminal_to_store)


def print_flow_table(flow_graph: Dict[Tuple[str, str], int]):
    """
    Виводить таблицю потоків між терміналами та магазинами.
    
    Args:
        flow_graph: Словник потоків по ребрах
    """
    print("\n" + "="*70)
    print("ТАБЛИЦЯ ПОТОКІВ МІЖ ТЕРМІНАЛАМИ ТА МАГАЗИНАМИ")
    print("="*70)
    print(f"{'Термінал':<20} {'Магазин':<20} {'Фактичний Потік':<20}")
    print("-"*70)
    
    # Групуємо за терміналами
    terminal_flows = defaultdict(list)
    for (terminal, store), flow in sorted(flow_graph.items()):
        terminal_flows[terminal].append((store, flow))
    
    total_flow = 0
    for terminal in sorted(terminal_flows.keys()):
        for store, flow in sorted(terminal_flows[terminal]):
            print(f"{terminal:<20} {store:<20} {flow:<20}")
            total_flow += flow
    
    print("-"*70)
    print(f"{'ЗАГАЛЬНИЙ ПОТІК:':<40} {total_flow:<20}")
    print("="*70)


def print_detailed_flows(flow_graph: Dict[Tuple[str, str], int], network: MaxFlowNetwork):
    """
    Виводить детальну інформацію про потоки в мережі.
    
    Args:
        flow_graph: Словник потоків по ребрах
        network: Мережа потоків
    """
    print("\n" + "="*70)
    print("ДЕТАЛЬНИЙ АНАЛІЗ ПОТОКІВ")
    print("="*70)
    
    # Потоки від терміналів до складів
    print("\n1. Потоки від терміналів до складів:")
    print("-"*70)
    print(f"{'Від':<20} {'До':<20} {'Потік/Ємність':<20}")
    print("-"*70)
    
    terminal_total = defaultdict(int)
    for terminal in ["Термінал 1", "Термінал 2"]:
        for warehouse in [f"Склад {i}" for i in range(1, 5)]:
            capacity = network.graph[terminal].get(warehouse, 0)
            flow = flow_graph.get(terminal, {}).get(warehouse, 0)
            if capacity > 0:
                print(f"{terminal:<20} {warehouse:<20} {flow}/{capacity}")
                terminal_total[terminal] += flow
    
    print("-"*70)
    for terminal, total in terminal_total.items():
        print(f"{terminal}: {total} одиниць")
    
    # Потоки від складів до магазинів
    print("\n2. Потоки від складів до магазинів:")
    print("-"*70)
    print(f"{'Від':<20} {'До':<20} {'Потік/Ємність':<20}")
    print("-"*70)
    
    warehouse_total = defaultdict(int)
    for warehouse in [f"Склад {i}" for i in range(1, 5)]:
        for store_num in range(1, 15):
            store = f"Магазин {store_num}"
            capacity = network.graph[warehouse].get(store, 0)
            flow = flow_graph.get(warehouse, {}).get(store, 0)
            if capacity > 0:
                print(f"{warehouse:<20} {store:<20} {flow}/{capacity}")
                warehouse_total[warehouse] += flow
    
    print("-"*70)
    for warehouse, total in warehouse_total.items():
        print(f"{warehouse}: {total} одиниць")


def analyze_results(
    max_flow: int,
    flow_graph: Dict[Tuple[str, str], int],
    network: MaxFlowNetwork,
    terminal_to_store: Dict[Tuple[str, str], int]
):
    """
    Аналізує результати обчислення максимального потоку.
    
    Args:
        max_flow: Максимальний потік
        flow_graph: Словник потоків по ребрах
        network: Мережа потоків
        terminal_to_store: Словник потоків від терміналів до магазинів
    """
    print("\n" + "="*70)
    print("АНАЛІЗ РЕЗУЛЬТАТІВ")
    print("="*70)
    
    print(f"\nМаксимальний потік у мережі: {max_flow} одиниць")
    
    # Питання 1: Які термінали забезпечують найбільший потік товарів до магазинів?
    print("\n1. Які термінали забезпечують найбільший потік товарів до магазинів?")
    print("-"*70)
    
    terminal_totals = defaultdict(int)
    for terminal in ["Термінал 1", "Термінал 2"]:
        for warehouse in [f"Склад {i}" for i in range(1, 5)]:
            flow = flow_graph.get(terminal, {}).get(warehouse, 0)
            terminal_totals[terminal] += flow
    
    for terminal, total in sorted(terminal_totals.items(), key=lambda x: x[1], reverse=True):
        print(f"   {terminal}: {total} одиниць")
    
    max_terminal = max(terminal_totals.items(), key=lambda x: x[1])
    print(f"\n   Відповідь: {max_terminal[0]} забезпечує найбільший потік ({max_terminal[1]} одиниць)")
    
    # Питання 2: Які маршрути мають найменшу пропускну здатність?
    print("\n2. Які маршрути мають найменшу пропускну здатність і як це впливає на загальний потік?")
    print("-"*70)
    
    bottlenecks = []
    for from_node in network.graph:
        if from_node not in ["Супер-Джерело"]:
            for to_node, capacity in network.graph[from_node].items():
                if to_node not in ["Супер-Стік"] and capacity < float('inf'):
                    flow = flow_graph.get(from_node, {}).get(to_node, 0)
                    utilization = (flow / capacity * 100) if capacity > 0 else 0
                    bottlenecks.append((from_node, to_node, capacity, flow, utilization))
    
    # Сортуємо за пропускною здатністю
    bottlenecks.sort(key=lambda x: x[2])
    
    print("   Маршрути з найменшою пропускною здатністю:")
    for from_node, to_node, capacity, flow, utilization in bottlenecks[:5]:
        print(f"   {from_node} -> {to_node}: {capacity} од. (використано {flow}, {utilization:.1f}%)")
    
    # Знаходимо повністю завантажені маршрути
    fully_loaded = [(f, t, c, fl) for f, t, c, fl, u in bottlenecks if u >= 99.9]
    if fully_loaded:
        print(f"\n   Вузькі місця (повністю завантажені маршрути): {len(fully_loaded)}")
        for from_node, to_node, capacity, flow in fully_loaded:
            print(f"   {from_node} -> {to_node}: {capacity} од.")
    
    # Питання 3: Які магазини отримали найменше товарів?
    print("\n3. Які магазини отримали найменше товарів і чи можна збільшити їх постачання?")
    print("-"*70)
    
    store_totals = defaultdict(int)
    for store_num in range(1, 15):
        store = f"Магазин {store_num}"
        for warehouse in [f"Склад {i}" for i in range(1, 5)]:
            flow = flow_graph.get(warehouse, {}).get(store, 0)
            store_totals[store] += flow
    
    sorted_stores = sorted(store_totals.items(), key=lambda x: x[1])
    
    print("   Магазини з найменшим постачанням:")
    for store, total in sorted_stores[:5]:
        print(f"   {store}: {total} одиниць")
        
        # Перевіряємо можливість збільшення
        for warehouse in [f"Склад {i}" for i in range(1, 5)]:
            capacity = network.graph[warehouse].get(store, 0)
            flow = flow_graph.get(warehouse, {}).get(store, 0)
            if capacity > 0:
                available = capacity - flow
                if available > 0:
                    print(f"      - Можна збільшити через {warehouse}: +{available} од.")
    
    # Питання 4: Чи є вузькі місця?
    print("\n4. Чи є вузькі місця, які можна усунути для покращення ефективності?")
    print("-"*70)
    
    if fully_loaded:
        print(f"   Так, виявлено {len(fully_loaded)} вузьких місць:")
        for from_node, to_node, capacity, flow in fully_loaded:
            print(f"   • {from_node} -> {to_node} (ємність: {capacity} од.)")
        
        print("\n   Рекомендації:")
        print("   - Збільшити пропускну здатність повністю завантажених маршрутів")
        print("   - Розглянути альтернативні маршрути постачання")
        print("   - Оптимізувати розподіл товарів між складами")
    else:
        print("   Критичних вузьких місць не виявлено.")
        print("   Мережа працює з резервом пропускної здатності.")


def main():
    """Головна функція програми."""
    print("="*70)
    print("ЛОГІСТИЧНА МЕРЕЖА: АНАЛІЗ МАКСИМАЛЬНОГО ПОТОКУ")
    print("Алгоритм Едмондса-Карпа")
    print("="*70)
    
    # Створюємо мережу
    network = create_logistics_network()
    
    # Додаємо супер-джерело та супер-стік
    super_source, super_sink = add_super_source_and_sink(network)
    
    # Обчислюємо максимальний потік
    print("\nОбчислення максимального потоку...")
    max_flow, flow_graph = network.edmonds_karp(super_source, super_sink)
    
    # Виводимо детальну інформацію
    print_detailed_flows(flow_graph, network)
    
    # Обчислюємо потоки від терміналів до магазинів
    terminal_to_store = calculate_terminal_to_store_flows(flow_graph, network)
    
    # Виводимо таблицю потоків
    print_flow_table(terminal_to_store)
    
    # Аналізуємо результати
    analyze_results(max_flow, flow_graph, network, terminal_to_store)
    
    print("\n" + "="*70)
    print("ЗАВЕРШЕННЯ АНАЛІЗУ")
    print("="*70)


if __name__ == "__main__":
    main()
