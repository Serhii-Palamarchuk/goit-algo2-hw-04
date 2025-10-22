"""
Базовий клас Trie для роботи з префіксними деревами.
"""

class TrieNode:
    """Вузол префіксного дерева."""
    
    def __init__(self):
        """Ініціалізація вузла."""
        self.children = {}
        self.is_end_of_word = False
        self.value = None


class Trie:
    """Префіксне дерево для зберігання та пошуку рядків."""
    
    def __init__(self):
        """Ініціалізація дерева."""
        self.root = TrieNode()
    
    def put(self, key: str, value) -> None:
        """
        Додає ключ-значення до дерева.
        
        Args:
            key: Рядок-ключ
            value: Значення для збереження
        """
        if not isinstance(key, str):
            raise TypeError("Ключ повинен бути рядком")
        
        node = self.root
        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        node.is_end_of_word = True
        node.value = value
    
    def get(self, key: str):
        """
        Отримує значення за ключем.
        
        Args:
            key: Рядок-ключ
            
        Returns:
            Значення, якщо ключ знайдено, інакше None
        """
        if not isinstance(key, str):
            raise TypeError("Ключ повинен бути рядком")
        
        node = self.root
        for char in key:
            if char not in node.children:
                return None
            node = node.children[char]
        
        return node.value if node.is_end_of_word else None
    
    def contains(self, key: str) -> bool:
        """
        Перевіряє наявність ключа в дереві.
        
        Args:
            key: Рядок-ключ
            
        Returns:
            True, якщо ключ присутній, інакше False
        """
        return self.get(key) is not None
    
    def keys(self) -> list:
        """
        Повертає список усіх ключів у дереві.
        
        Returns:
            Список рядків-ключів
        """
        result = []
        self._collect_keys(self.root, "", result)
        return result
    
    def _collect_keys(self, node: TrieNode, prefix: str, result: list) -> None:
        """
        Рекурсивно збирає всі ключі з дерева.
        
        Args:
            node: Поточний вузол
            prefix: Поточний префікс
            result: Список для збереження ключів
        """
        if node.is_end_of_word:
            result.append(prefix)
        
        for char, child_node in node.children.items():
            self._collect_keys(child_node, prefix + char, result)
