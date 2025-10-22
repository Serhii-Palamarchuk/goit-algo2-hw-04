"""
Завдання 2. Розширення функціоналу префіксного дерева.
Реалізація методів count_words_with_suffix та has_prefix.
"""

from trie import Trie, TrieNode


class Homework(Trie):
    """Розширений клас Trie з додатковими методами."""
    
    def count_words_with_suffix(self, pattern: str) -> int:
        """
        Підраховує кількість слів, що закінчуються заданим суфіксом.
        
        Args:
            pattern: Суфікс для пошуку (регістрозалежний)
            
        Returns:
            Кількість слів з заданим суфіксом
            
        Raises:
            TypeError: Якщо pattern не є рядком
            ValueError: Якщо pattern є порожнім рядком
        """
        # Валідація вхідних даних
        if not isinstance(pattern, str):
            raise TypeError("Параметр pattern повинен бути рядком")
        
        if not pattern:
            raise ValueError("Параметр pattern не може бути порожнім рядком")
        
        # Збираємо всі слова з дерева
        all_words = []
        self._collect_all_words(self.root, "", all_words)
        
        # Підраховуємо слова з заданим суфіксом
        count = 0
        for word in all_words:
            if word.endswith(pattern):
                count += 1
        
        return count
    
    def has_prefix(self, prefix: str) -> bool:
        """
        Перевіряє наявність слів із заданим префіксом.
        
        Args:
            prefix: Префікс для пошуку (регістрозалежний)
            
        Returns:
            True, якщо існує хоча б одне слово з префіксом, інакше False
            
        Raises:
            TypeError: Якщо prefix не є рядком
            ValueError: Якщо prefix є порожнім рядком
        """
        # Валідація вхідних даних
        if not isinstance(prefix, str):
            raise TypeError("Параметр prefix повинен бути рядком")
        
        if not prefix:
            raise ValueError("Параметр prefix не може бути порожнім рядком")
        
        # Проходимо по дереву відповідно до префікса
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        
        # Перевіряємо, чи існує хоча б одне слово з цим префіксом
        return self._has_words_from_node(node)
    
    def _collect_all_words(self, node: TrieNode, current_word: str, result: list) -> None:
        """
        Рекурсивно збирає всі слова з дерева.
        
        Args:
            node: Поточний вузол
            current_word: Поточне слово
            result: Список для збереження слів
        """
        if node.is_end_of_word:
            result.append(current_word)
        
        for char, child_node in node.children.items():
            self._collect_all_words(child_node, current_word + char, result)
    
    def _has_words_from_node(self, node: TrieNode) -> bool:
        """
        Перевіряє, чи існують слова, що починаються з даного вузла.
        
        Args:
            node: Вузол для перевірки
            
        Returns:
            True, якщо існує хоча б одне слово, інакше False
        """
        # Якщо це кінець слова, повертаємо True
        if node.is_end_of_word:
            return True
        
        # Перевіряємо дочірні вузли
        for child_node in node.children.values():
            if self._has_words_from_node(child_node):
                return True
        
        return False


def run_basic_tests():
    """Запускає базові тести з умови завдання."""
    print("="*70)
    print("БАЗОВІ ТЕСТИ")
    print("="*70)
    
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)
    
    print("\nДодані слова:", words)
    
    # Тести для count_words_with_suffix
    print("\n" + "-"*70)
    print("Тестування count_words_with_suffix:")
    print("-"*70)
    
    test_cases_suffix = [
        ("e", 1, "apple"),
        ("ion", 1, "application"),
        ("a", 1, "banana"),
        ("at", 1, "cat"),
    ]
    
    all_passed = True
    for pattern, expected, explanation in test_cases_suffix:
        result = trie.count_words_with_suffix(pattern)
        status = "✓" if result == expected else "✗"
        print(f"{status} count_words_with_suffix('{pattern}'): {result} (очікувалось {expected}) - {explanation}")
        if result != expected:
            all_passed = False
        assert result == expected, f"Помилка: очікувалось {expected}, отримано {result}"
    
    # Тести для has_prefix
    print("\n" + "-"*70)
    print("Тестування has_prefix:")
    print("-"*70)
    
    test_cases_prefix = [
        ("app", True, "apple, application"),
        ("bat", False, "немає слів"),
        ("ban", True, "banana"),
        ("ca", True, "cat"),
    ]
    
    for prefix, expected, explanation in test_cases_prefix:
        result = trie.has_prefix(prefix)
        status = "✓" if result == expected else "✗"
        print(f"{status} has_prefix('{prefix}'): {result} (очікувалось {expected}) - {explanation}")
        if result != expected:
            all_passed = False
        assert result == expected, f"Помилка: очікувалось {expected}, отримано {result}"
    
    if all_passed:
        print("\n" + "="*70)
        print("✓ ВСІ БАЗОВІ ТЕСТИ ПРОЙДЕНІ УСПІШНО!")
        print("="*70)
    else:
        print("\n" + "="*70)
        print("✗ ДЕЯКІ ТЕСТИ НЕ ПРОЙДЕНІ!")
        print("="*70)


def run_additional_tests():
    """Запускає додаткові тести для перевірки граничних випадків."""
    print("\n" + "="*70)
    print("ДОДАТКОВІ ТЕСТИ")
    print("="*70)
    
    trie = Homework()
    
    # Тест 1: Порожнє дерево
    print("\n1. Порожнє дерево:")
    print("-"*70)
    assert trie.count_words_with_suffix("test") == 0, "Помилка: порожнє дерево"
    print("✓ count_words_with_suffix на порожньому дереві: 0")
    assert trie.has_prefix("test") == False, "Помилка: порожнє дерево"
    print("✓ has_prefix на порожньому дереві: False")
    
    # Тест 2: Регістрозалежність
    print("\n2. Регістрозалежність:")
    print("-"*70)
    trie.put("Apple", 0)
    trie.put("apple", 1)
    assert trie.count_words_with_suffix("e") == 2, "Помилка: обидва слова закінчуються на 'e'"
    print("✓ Знайдено 2 слова з суфіксом 'e': Apple та apple")
    assert trie.count_words_with_suffix("E") == 0, "Помилка: регістр має значення"
    print("✓ Регістр враховується для суфіксів (E != e)")
    assert trie.has_prefix("App") == True, "Помилка: регістр має значення"
    print("✓ Регістр враховується для префіксів")
    assert trie.has_prefix("app") == True, "Помилка: регістр має значення"
    print("✓ Окремо для 'app' та 'App'")
    
    # Тест 3: Слова, що є префіксами інших слів
    print("\n3. Слова-префікси:")
    print("-"*70)
    trie = Homework()
    trie.put("test", 0)
    trie.put("testing", 1)
    trie.put("tested", 2)
    assert trie.count_words_with_suffix("test") == 1, "Помилка: 'test'"
    print("✓ Суфікс 'test': 1 слово")
    assert trie.count_words_with_suffix("ed") == 1, "Помилка: 'tested'"
    print("✓ Суфікс 'ed': 1 слово")
    assert trie.has_prefix("test") == True, "Помилка: префікс 'test'"
    print("✓ Префікс 'test' існує")
    
    # Тест 4: Довгі слова
    print("\n4. Великі набори даних:")
    print("-"*70)
    trie = Homework()
    for i in range(1000):
        trie.put(f"word{i}", i)
    assert trie.count_words_with_suffix("999") == 1, "Помилка: великий набір"
    print("✓ Робота з 1000 слів (суфікс)")
    assert trie.has_prefix("word99") == True, "Помилка: великий набір"
    print("✓ Робота з 1000 слів (префікс)")
    
    # Тест 5: Обробка помилок
    print("\n5. Обробка некоректних даних:")
    print("-"*70)
    trie = Homework()
    trie.put("test", 0)
    
    try:
        trie.count_words_with_suffix(123)
        print("✗ Не виявлено помилку TypeError для count_words_with_suffix")
        assert False, "Має бути TypeError"
    except TypeError as e:
        print(f"✓ TypeError для count_words_with_suffix: {e}")
    
    try:
        trie.has_prefix(None)
        print("✗ Не виявлено помилку TypeError для has_prefix")
        assert False, "Має бути TypeError"
    except TypeError as e:
        print(f"✓ TypeError для has_prefix: {e}")
    
    try:
        trie.count_words_with_suffix("")
        print("✗ Не виявлено помилку ValueError для порожнього рядка")
        assert False, "Має бути ValueError"
    except ValueError as e:
        print(f"✓ ValueError для порожнього суфікса: {e}")
    
    try:
        trie.has_prefix("")
        print("✗ Не виявлено помилку ValueError для порожнього рядка")
        assert False, "Має бути ValueError"
    except ValueError as e:
        print(f"✓ ValueError для порожнього префікса: {e}")
    
    # Тест 6: Спеціальні символи
    print("\n6. Спеціальні символи:")
    print("-"*70)
    trie = Homework()
    trie.put("hello-world", 0)
    trie.put("test@example.com", 1)
    trie.put("user_name", 2)
    assert trie.count_words_with_suffix("world") == 1, "Помилка: дефіс"
    print("✓ Робота з дефісом")
    assert trie.count_words_with_suffix(".com") == 1, "Помилка: крапка"
    print("✓ Робота з крапкою")
    assert trie.has_prefix("user_") == True, "Помилка: підкреслення"
    print("✓ Робота з підкресленням")
    
    print("\n" + "="*70)
    print("✓ ВСІ ДОДАТКОВІ ТЕСТИ ПРОЙДЕНІ УСПІШНО!")
    print("="*70)


def run_performance_tests():
    """Запускає тести продуктивності."""
    import time
    
    print("\n" + "="*70)
    print("ТЕСТИ ПРОДУКТИВНОСТІ")
    print("="*70)
    
    trie = Homework()
    
    # Тест 1: Додавання великої кількості слів
    print("\n1. Додавання 10,000 слів:")
    print("-"*70)
    start = time.time()
    for i in range(10000):
        trie.put(f"word{i:05d}", i)
    elapsed = time.time() - start
    print(f"✓ Час виконання: {elapsed:.4f} секунд")
    print(f"✓ Швидкість: {10000/elapsed:.0f} слів/сек")
    
    # Тест 2: Пошук суфіксів
    print("\n2. Пошук суфіксів у 10,000 слів:")
    print("-"*70)
    start = time.time()
    result = trie.count_words_with_suffix("00")
    elapsed = time.time() - start
    print(f"✓ Знайдено слів: {result}")
    print(f"✓ Час виконання: {elapsed:.4f} секунд")
    
    # Тест 3: Перевірка префіксів
    print("\n3. Перевірка префіксів у 10,000 слів:")
    print("-"*70)
    start = time.time()
    result = trie.has_prefix("word99")
    elapsed = time.time() - start
    print(f"✓ Результат: {result}")
    print(f"✓ Час виконання: {elapsed:.4f} секунд")
    
    # Тест 4: Багато коротких слів
    print("\n4. Робота з 5,000 короткими словами:")
    print("-"*70)
    trie2 = Homework()
    short_words = []
    for i in range(5000):
        word = chr(97 + (i % 26)) * ((i % 5) + 1)  # a, aa, aaa, b, bb, etc.
        short_words.append(word)
        trie2.put(word, i)
    
    start = time.time()
    count = trie2.count_words_with_suffix("a")
    elapsed = time.time() - start
    print(f"✓ Слів з суфіксом 'a': {count}")
    print(f"✓ Час виконання: {elapsed:.4f} секунд")
    
    print("\n" + "="*70)
    print("✓ ТЕСТИ ПРОДУКТИВНОСТІ ЗАВЕРШЕНІ!")
    print("="*70)


if __name__ == "__main__":
    print("ЗАВДАННЯ 2: РОЗШИРЕННЯ ФУНКЦІОНАЛУ ПРЕФІКСНОГО ДЕРЕВА")
    
    # Запускаємо базові тести з умови завдання
    run_basic_tests()
    
    # Запускаємо додаткові тести
    run_additional_tests()
    
    # Запускаємо тести продуктивності
    run_performance_tests()
    
    print("\n" + "="*70)
    print("ВСЬОГО ТЕСТІВ ЗАВЕРШЕНО УСПІШНО!")
    print("="*70)
