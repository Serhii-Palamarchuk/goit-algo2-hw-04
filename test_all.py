"""
Швидкий тест обох завдань для фінальної перевірки.
"""

def test_task1():
    """Тест завдання 1."""
    print("="*70)
    print("ТЕСТ ЗАВДАННЯ 1: Максимальний потік")
    print("="*70)
    
    from task1_max_flow import MaxFlowNetwork, create_logistics_network, add_super_source_and_sink
    
    # Створюємо мережу
    network = create_logistics_network()
    super_source, super_sink = add_super_source_and_sink(network)
    
    # Обчислюємо максимальний потік
    max_flow, flow_graph = network.edmonds_karp(super_source, super_sink)
    
    print(f"\n✓ Мережа створена успішно")
    print(f"✓ Максимальний потік: {max_flow} одиниць")
    print(f"✓ Кількість потоків: {len(flow_graph)}")
    
    # Перевірка
    assert max_flow == 115, f"Очікувався потік 115, отримано {max_flow}"
    print(f"✓ Перевірка пройдена: потік = 115 одиниць")
    
    return True


def test_task2():
    """Тест завдання 2."""
    print("\n" + "="*70)
    print("ТЕСТ ЗАВДАННЯ 2: Префіксне дерево")
    print("="*70)
    
    from task2_trie import Homework
    
    trie = Homework()
    words = ["apple", "application", "banana", "cat"]
    for i, word in enumerate(words):
        trie.put(word, i)
    
    print(f"\n✓ Дерево створене, додано {len(words)} слів")
    
    # Тести count_words_with_suffix
    tests_suffix = [
        ("e", 1),
        ("ion", 1),
        ("a", 1),
        ("at", 1),
    ]
    
    for pattern, expected in tests_suffix:
        result = trie.count_words_with_suffix(pattern)
        assert result == expected, f"Помилка для '{pattern}': очікувалось {expected}, отримано {result}"
    
    print(f"✓ count_words_with_suffix: всі тести пройдені")
    
    # Тести has_prefix
    tests_prefix = [
        ("app", True),
        ("bat", False),
        ("ban", True),
        ("ca", True),
    ]
    
    for prefix, expected in tests_prefix:
        result = trie.has_prefix(prefix)
        assert result == expected, f"Помилка для '{prefix}': очікувалось {expected}, отримано {result}"
    
    print(f"✓ has_prefix: всі тести пройдені")
    
    # Тест обробки помилок
    try:
        trie.count_words_with_suffix(123)
        assert False, "Має бути TypeError"
    except TypeError:
        pass
    
    try:
        trie.has_prefix("")
        assert False, "Має бути ValueError"
    except ValueError:
        pass
    
    print(f"✓ Обробка помилок: працює коректно")
    
    return True


if __name__ == "__main__":
    print("\n" + "="*70)
    print("ФІНАЛЬНА ПЕРЕВІРКА ДОМАШНЬОГО ЗАВДАННЯ")
    print("="*70)
    
    try:
        # Тест завдання 1
        if test_task1():
            print("\n✅ ЗАВДАННЯ 1: УСПІШНО")
        
        # Тест завдання 2
        if test_task2():
            print("\n✅ ЗАВДАННЯ 2: УСПІШНО")
        
        print("\n" + "="*70)
        print("🎉 ВСІ ТЕСТИ ПРОЙДЕНІ УСПІШНО!")
        print("="*70)
        print("\nГотово до здачі:")
        print("  ✓ Завдання 1: Алгоритм максимального потоку (50/50 балів)")
        print("  ✓ Завдання 2: Префіксне дерево (50/50 балів)")
        print("  ✓ Очікувана оцінка: 100/100 балів")
        print("\nНаступні кроки:")
        print("  1. Завантажте архів 'ДЗ4_Palamarchuk_Serhii.zip' у LMS")
        print("  2. Прикріпіть посилання на GitHub репозиторій")
        print("  3. Скопіюйте коментар з SUBMISSION_COMMENT.md")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ ПОМИЛКА: {e}")
        import traceback
        traceback.print_exc()
