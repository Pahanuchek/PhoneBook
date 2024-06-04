from csv import DictReader, DictWriter
from os.path import exists


FILE_NAME = "phone_book.csv"


class LenException(Exception):
    def __init__(self, text):
        self.text = text


def create_contact() -> dict:
    flag = False
    while not flag:
        try:
            first_name = input("Введите имя: ")
            if len(first_name) < 2:
                raise LenException("Слишком короткое имя.")
            second_name = input("Введите фамили: ")
            if len(second_name) < 4:
                raise LenException("Слишком короткая фамилия.")
            phone_number = input("Введите номер телефона: ")
            if len(phone_number) != 11:
                raise  LenException("Номер телефона должен содержать 11 цифр.")
        except LenException as err:
            print(err)
        else:
            flag = True
    return {"Имя": first_name, "Фамилия": second_name,"Номер телефона": phone_number}


def create_file(file_name):
    with open(file_name, 'w', encoding='utf-8') as data:
        data = DictWriter(data, fieldnames=["Имя", "Фамилия", "Номер телефона"])
        data.writeheader()


def add_contact(file_name):
    contact = create_contact()
    prev_record = read_contacts(file_name)
    prev_record.append(contact)
    with open(file_name, 'w', encoding='utf-8') as data:
        data = DictWriter(data, fieldnames=["Имя", "Фамилия", "Номер телефона"])
        data.writeheader()
        data.writerows(prev_record)


def read_contacts(file_name) -> list:
    with open(file_name, encoding='utf-8') as data:
        contacts = DictReader(data)
        return list(contacts)


def remove_contact(file_name, number):
    contacts = read_contacts(file_name)
    try:
        if len(contacts) == 0:
            raise LenException("Телефонная книга пуста.")
        elif len(contacts) < number:
            raise LenException("Контакт не существует.")
    except LenException as err:
        print(err)
        print()
        return
    else:
        contact = contacts.pop(number - 1)
        with open(file_name, 'w', encoding='utf-8') as data:
            data = DictWriter(data, fieldnames=["Имя", "Фамилия", "Номер телефона"])
            data.writeheader()
            data.writerows(contacts)
        return contact


def get_contact(file_name, number):
    contacts = read_contacts(file_name)
    try:
        if len(contacts) == 0:
            raise LenException("Телефонная книга пуста.")
        elif len(contacts) < number:
            raise LenException("Контакт не существует.")
    except LenException as err:
        print(err)
        print()
        return
    else:
        return contacts[number - 1]


def copy_contacts(file_1, file_2):
    contacts = read_contacts(file_1)
    try:
        if len(contacts) == 0:
            raise LenException("Телефонная книга пуста.")
    except LenException as err:
        print(err)
        return
    else:
        with open(file_2, 'w', encoding='utf-8') as data:
            data = DictWriter(data, fieldnames=["Имя", "Фамилия", "Номер телефона"])
            data.writeheader()
            data.writerows(contacts)


def copy_contact(file_1, file_2, number):
    contact = get_contact(file_1, number)
    if contact:
        contacts = read_contacts(file_2)
        contacts.append(contact)
        with open(file_2, 'w', encoding='utf-8') as data:
            data = DictWriter(data, fieldnames=["Имя", "Фамилия", "Номер телефона"])
            data.writeheader()
            data.writerows(contacts)
    return contact

def main():
    while True:
        enter = input("Введите номер операции:\n1. Создать файл"
                      "\n2. Прочитать контакты\n3. Добавить контакт"
                      "\n4. Удалить контакт\n5. Просмотреть контакт"
                      "\n6. Скопировать контакты из файла в файл"
                      "\n7. Скопировать контакт из файла в файл"
                      "\n8. Выйти\nВвод: ")
        print()
        if enter == '8':
            print("До свидания")
            break
        elif enter == '2':
            file_name = input("Введите имя файла из которого нужно прочитать контакт: ")
            if not exists(file_name):
                print("Создайте файл, и добавьте контакты.")
            contacts = read_contacts(file_name)
            print(f"Контакты из файла {file_name}:")
            for contact in contacts:
                for key, value in contact.items():
                    print(f"{key} - {value}")
                print("----------------------------")
            print()
        elif enter == '3':
            file_name = input("Введите имя файла в который нужно добавить контакт: ")
            if not exists(file_name):
                print("Файл отсутствует, создайте файл.")
                print()
                continue
            add_contact(file_name)
            print(f"Контакт добавлен в файл {file_name}")
            print()
        elif enter == '1':
            file_name = input("Введите имя файла: ")
            if not exists(file_name):
                create_file(file_name)
                print(f'Файл {file_name} создан.')
                print()
            else:
                print("Файл уже существует.")
                print()
        elif enter == '4':
            file_name = input("Введите имя файла, из которого хотите удалить контакт: ")
            if not exists(file_name):
                print("Файл не существует.")
                print()
                continue
            number = int(input("Введите номер контакта, который хотите удалить: "))
            contact = remove_contact(file_name, number)
            if contact:
                print(f'Контакт {contact["Имя"]} удален.')
                print()

        elif enter == '5':
            file_name = input("Введите имя файла, из которого хотите удалить контакт: ")
            if not exists(file_name):
                print("Файл не существует.")
                print()
                continue
            number = int(input("Введите номер контакта, который хотите просмотреть: "))
            contact = get_contact(file_name, number)
            if contact:
                for key, value in contact.items():
                    print(f"{key} - {value}")
                print()

        elif enter == '6':
            file_1 = input("Введите имя файла, из которого хотите скопировать контакты: ")
            file_2 = input("Введите имя файла,в который хотите скопировать контакты: ")
            if not exists(file_1):
                print("Файл из которого хотите скопировать контакты не существует.")
                print()
                continue
            elif not exists(file_2):
                print("Файл в который хотите скопировать контакты не существует, "
                      "создайте файл и повторите снова.")
                print()
                continue
            copy_contacts(file_1, file_2)
            print(f"Контакты скопированы из файла {file_1} в {file_2}")
            print()

        elif enter == '7':
            file_1 = input("Введите имя файла, из которого хотите скопировать контакт: ")
            file_2 = input("Введите имя файла,в который хотите скопировать контакт: ")
            if not exists(file_1):
                print("Файл из которого хотите скопировать контакт не существует.")
                print()
                continue
            elif not exists(file_2):
                print("Файл в который хотите скопировать контакт не существует, "
                      "создайте файл и повторите снова.")
                print()
                continue
            number = int(input("Введите порядковый номер контакта, который хотите скопировать: "))
            contact = copy_contact(file_1, file_2, number)
            if contact:
                print(f"Контакт {contact['Имя']} скопирован из файла {file_1} в {file_2}")
                print()


if __name__ == '__main__':
    main()
