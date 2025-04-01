from typing import Dict, List

# Декоратор для обробки помилок
def input_error(func):
    """Декоратор для обробки помилок у функціях.
    
    Обробляє такі типи помилок:
    - KeyError: якщо контакт не знайдений
    - ValueError: якщо введено невірний формат
    - IndexError: якщо не вистачає аргументів
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Invalid input format."
        except IndexError:
            return "Not enough arguments."
    return inner

# Клас, що представляє базове поле для всіх інших полів (ім'я, телефон)
class Field:
    """Базовий клас для полів запису контакту (ім'я, телефон тощо)."""
    def __init__(self, value: str):
        """
        Конструктор класу Field.
        
        :param value: Значення поля (наприклад, ім'я або телефон)
        """
        self.value = value

# Клас для зберігання імені контакту, успадкований від Field
class Name(Field):
    """Клас для зберігання імені контакту, успадкований від Field."""
    
    def __init__(self, name: str):
        """
        Конструктор класу Name.
        
        Перевіряє, чи ім'я не порожнє.
        
        :param name: Ім'я контакту
        :raises ValueError: Якщо ім'я порожнє
        """
        if not name.strip():  # Перевірка на порожнє значення
            raise ValueError("Name cannot be empty.")
        super().__init__(name)

# Клас для зберігання номера телефону контакту, успадкований від Field
class Phone(Field):
    """Клас для зберігання номера телефону контакту, успадкований від Field."""
    
    def __init__(self, number: str):
        """
        Конструктор класу Phone.
        
        Перевіряє, чи номер телефону складається з 10 цифр.
        
        :param number: Номер телефону
        :raises ValueError: Якщо номер не складається з 10 цифр
        """
        if not number.isdigit() or len(number) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        super().__init__(number)

# Клас для зберігання одного запису в адресній книзі (контакт)
class Record:
    """Клас для зберігання одного запису контакту: ім'я та список телефонів."""
    
    def __init__(self, name: str):
        """
        Конструктор класу Record.
        
        Створює новий запис з ім'ям та ініціалізує порожній список для телефонів.
        
        :param name: Ім'я контакту
        """
        self.name = Name(name)  # Ім'я контакту
        self.phones = []  # Список телефонів для цього контакту

    def add_phone(self, phone_number: str):
        """Додає новий телефон до контакту."""
        self.phones.append(Phone(phone_number))

    def find_phone(self, phone_number: str):
        """
        Шукає телефон у списку телефонів контакту.
        
        :param phone_number: Номер телефону для пошуку
        :return: Об'єкт Phone, якщо знайдено, або None
        """
        return next((phone for phone in self.phones if phone.value == phone_number), None)

    def __str__(self):
        """Повертає строкове представлення запису контакту."""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

# Клас для зберігання всієї адресної книги
class AddressBook:
    """Клас для зберігання всієї адресної книги, що включає всі контакти."""
    
    def __init__(self):
        """
        Конструктор класу AddressBook.
        
        Ініціалізує порожній словник для зберігання контактів.
        """
        self.records = {}  # Словник для зберігання контактів за ім'ям

    def add_record(self, record: Record):
        """
        Додає запис (контакт) до адресної книги.
        
        :param record: Об'єкт Record для додавання в книгу
        """
        self.records[record.name.value] = record

    def find(self, name: str):
        """
        Шукає запис у адресній книзі за іменем.
        
        :param name: Ім'я для пошуку
        :return: Об'єкт Record, якщо знайдено, або None
        """
        return self.records.get(name, None)

    def delete(self, name: str):
        """
        Видаляє запис з адресної книги за ім'ям.
        
        :param name: Ім'я для видалення
        """
        if name in self.records:
            del self.records[name]

    def __str__(self):
        """Повертає строкове представлення всієї адресної книги."""
        return "\n".join([str(record) for record in self.records.values()])

# Функція для додавання контакту
@input_error
def add_contact(args: List[str], address_book: AddressBook) -> str:
    """
    Додає контакт до адресної книги.
    
    :param args: Список рядків, де args[0] — це ім'я, а args[1] — це номер телефону
    :param address_book: Адресна книга для зберігання контактів
    :return: Результат додавання контакту
    """
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    address_book.add_record(record)
    return f"Contact {name} added."

# Функція для отримання телефону
@input_error
def get_phone(args: List[str], address_book: AddressBook) -> str:
    """
    Отримує номер телефону контакту за ім'ям.
    
    :param args: Список рядків, де args[0] — це ім'я контакту
    :param address_book: Адресна книга для зберігання контактів
    :return: Телефон контактів або повідомлення про помилку
    """
    name = args[0]
    record = address_book.find(name)
    if record:
        return str(record)
    return "Contact not found."

# Головна функція для взаємодії з користувачем через CLI
def main():
    """
    Головна функція для взаємодії з користувачем.
    Дає змогу користувачу додавати, шукати, видаляти контакти та переглядати всю адресну книгу.
    """
    address_book = AddressBook()

    while True:
        com = input("Enter a command: ").lower()

        if com == 'hello':
            print('How can I help you?')

        elif com.startswith('add'):
            parts = com.split(' ')
            if len(parts) < 3:
                print('Invalid format. Use: add [name] [number]')
            else:
                name = parts[1]
                number = parts[2]
                print(add_contact([name, number], address_book))

        elif com.startswith("phone"):
            parts = com.split(" ")
            if len(parts) < 2:
                print("Invalid format. Use: phone [name]")
            else:
                name = parts[1]
                print(get_phone([name], address_book))

        elif com == "all":
            if address_book.records:
                print("Saved contacts:")
                print(address_book)
            else:
                print("No contacts saved yet.")

        elif com == 'exit':
            print('Good bye!')
            break

        else:
            print('Invalid command. Try again.e')

if __name__ == "__main__":
    main()