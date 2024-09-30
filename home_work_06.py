import sqlite3
import random

# Создание и настройка базы данных
def create_database():
    conn = sqlite3.connect('wizards.db')
    cursor = conn.cursor()
    
    # Создание таблицы wizards
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS wizards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name VARCHAR(20),
        last_name VARCHAR(20),
        age INTEGER,
        house VARCHAR(20),
        magic_level INTEGER CHECK(magic_level BETWEEN 1 AND 100),
        special_ability VARCHAR(50)
    )
    ''')
    
    conn.commit()
    conn.close()

# Функция для добавления волшебника
def add_wizard(first_name, last_name, age, house, magic_level, special_ability):
    conn = sqlite3.connect('wizards.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO wizards (first_name, last_name, age, house, magic_level, special_ability)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (first_name, last_name, age, house, magic_level, special_ability))
    
    conn.commit()
    conn.close()

# Функция для выбора случайного волшебника
def get_random_wizards(count=2):
    conn = sqlite3.connect('wizards.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, first_name, last_name, magic_level FROM wizards')
    wizards = cursor.fetchall()
    conn.close()
    
    return random.sample(wizards, min(count, len(wizards)))

# Функция для проведения дуэли
def wizard_duel():
    wizards = get_random_wizards(2)
    
    if len(wizards) < 2:
        print("Недостаточно волшебников для проведения дуэли.")
        return
    
    wizard1 = wizards[0]
    wizard2 = wizards[1]

    print(f"Дуэль между {wizard1[1]} {wizard1[2]} (уровень магии: {wizard1[3]}) и {wizard2[1]} {wizard2[2]} (уровень магии: {wizard2[3]})")

    if wizard1[3] > wizard2[3]:
        winner = wizard1
        loser = wizard2
        print(f"Победитель: {winner[1]} {winner[2]}")
    elif wizard1[3] < wizard2[3]:
        winner = wizard2
        loser = wizard1
        print(f"Победитель: {winner[1]} {winner[2]}")
    else:
        print("Ничья! Оба волшебника имеют одинаковый уровень магии.")
        return

    # Обновление уровней магии
    new_winner_magic_level = min(winner[3] + 5, 100)  # Уровень не может превышать 100
    new_loser_magic_level = max(loser[3] - 10, 1)  # Уровень не может быть ниже 1

    update_magic_level(winner[0], new_winner_magic_level)
    update_magic_level(loser[0], new_loser_magic_level)

    print(f"Уровень магии {winner[1]} {winner[2]} обновлен до {new_winner_magic_level}")
    print(f"Уровень магии {loser[1]} {loser[2]} обновлен до {new_loser_magic_level}")

# Функция для обновления уровня магии
def update_magic_level(wizard_id, new_magic_level):
    conn = sqlite3.connect('wizards.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    UPDATE wizards SET magic_level = ? WHERE id = ?
    ''', (new_magic_level, wizard_id))
    
    conn.commit()
    conn.close()

# Функция для поиска волшебников по уникальной способности
def find_wizard_by_ability(ability):
    conn = sqlite3.connect('wizards.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT first_name, last_name FROM wizards WHERE special_ability = ?
    ''', (ability,))
    
    wizards = cursor.fetchall()
    conn.close()
    
    if wizards:
        print("Волшебники с уникальной способностью '{}':".format(ability))
        for wizard in wizards:
            print(f"{wizard[0]} {wizard[1]}")
    else:
        print("Волшебников с уникальной способностью '{}' не найдено.".format(ability))

# Функция для вывода волшебников по дому
def list_wizards_by_house(house):
    conn = sqlite3.connect('wizards.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT first_name, last_name FROM wizards WHERE house = ?
    ''', (house,))
    
    wizards = cursor.fetchall()
    conn.close()
    
    if wizards:
        print("Волшебники из дома '{}':".format(house))
        for wizard in wizards:
            print(f"{wizard[0]} {wizard[1]}")
    else:
        print("Волшебников из дома '{}' не найдено.".format(house))

# Функция для удаления волшебника
def delete_wizard(wizard_id):
    conn = sqlite3.connect('wizards.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    DELETE FROM wizards WHERE id = ?
    ''', (wizard_id,))
    
    conn.commit()
    conn.close()

# Функция для добавления волшебника через пользовательский ввод
def input_wizard():
    first_name = input("Введите имя волшебника: ")
    last_name = input("Введите фамилию волшебника: ")
    age = int(input("Введите возраст волшебника: "))
    house = input("Введите дом (Гриффиндор, Слизерин, Когтевран, Пуффендуй): ")
    magic_level = int(input("Введите уровень магии (1-100): "))
    special_ability = input("Введите уникальную способность: ")

    add_wizard(first_name, last_name, age, house, magic_level, special_ability)
    print("Волшебник успешно добавлен!")

# Инициализация базы данных
create_database()

# Основной цикл программы
while True:
    print("\nМеню:")
    print("1. Добавить волшебника")
    print("2. Найти волшебников по способности")
    print("3. Вывести волшебников по дому")
    print("4. Обновить уровень магии")
    print("5. Удалить волшебника")
    print("6. Провести дуэль")
    print("7. Выход")

    choice = input("Выберите действие: ")
    
    if choice == '1':
        input_wizard()
    elif choice == '2':
        ability_input = input("Введите название способности: ")
        find_wizard_by_ability(ability_input)
    elif choice == '3':
        house_input = input("Введите название дома: ")
        list_wizards_by_house(house_input)
    elif choice == '4':
        wizard_id = int(input("Введите id волшебника: "))
        new_magic_level = int(input("Введите новый уровень магии: "))
        update_magic_level(wizard_id, new_magic_level)
    elif choice == '5':
        wizard_id = int(input("Введите id волшебника для удаления: "))
        delete_wizard(wizard_id)
    elif choice == '6':
        wizard_duel()
    elif choice == '7':
        break
    else:
        print("Неверный выбор. Пожалуйста, попробуйте снова.")