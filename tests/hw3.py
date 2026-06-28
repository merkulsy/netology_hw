# 3 task
# Я работаю секретарём, и мне постоянно приходят различные документы. Я должен быть очень внимателен,
# чтобы не потерять ни один документ. Каталог документов хранится в следующем виде:
# 	documents = [
# 		{"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
# 		{"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
# 		{"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
# 		{"type": "driver license", "number": "5455 028765", "name": "Василий Иванов"},
# 	]
# Перечень полок, на которых находятся документы, хранится в следующем виде:
# 	directories = {
# 		'1': ['2207 876234', '11-2', '5455 028765'],
# 		'2': ['10006'],
# 		'3': []
# 	}
# Необходимо реализовать следующие функции.
# get_name — функция. Принимает номер документа и выводит имя человека, которому он принадлежит.
# Если такого документа не существует, вывести “Документ не найден”.
# get_directory — функция. Принимает номер документа и выводит номер полки, на которой он находится.
# Если такой документ не найден, на полках вывести “Полки с таким документом не найдено”.
# add — функция, которая добавит новый документ в каталог и перечень полок.
# В результате корректного выполнения задания будет выведен следующий результат:
# Аристарх Павлов
# 1
# Документ не найден
# 3
# Александр Пушкин
# Полки с таким документом не найдено

documents = [
        {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
        {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
        {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
        {"type": "driver license", "number": "5455 028765", "name": "Василий Иванов"},
      ]

directories = {
        '1': ['2207 876234', '11-2', '5455 028765'],
        '2': ['10006'],
        '3': []
      }

def get_name(doc_number):
    for element in documents:
        if element['number'] == doc_number:
            return element['name']
    return 'Документ не найден'

def get_directory(doc_number):
    for k,v in directories.items():
        if doc_number in v:
            return k
    return 'Полки с таким документом не найдено'

def add(document_type, number, name, shelf_number):
    directories.setdefault(str(shelf_number), [])
    if number not in directories[str(shelf_number)]:
        directories[str(shelf_number)].append(str(number))
        documents.append({
            "type": document_type,
            "number": number,
            "name": name
        })


if __name__ == '__main__':
    print(get_name("10006"))
    print(get_directory("11-2"))
    print(get_name("101"))
    add('international passport', '311 020203', 'Александр Пушкин', 3)
    print(get_directory("311 020203"))
    print(get_name("311 020203"))
    print(get_directory("311 020204"))
    add('passport', '311', 'Алекс Пуш', 4)
    print(get_name("311"))
    print(get_directory("311"))
    print(documents)
    print(directories)
    add('passport', '311', 'Алекс Пуш', 4)
    print(get_name("311"))
    print(get_directory("311"))
    print(documents)
    print(directories)