"""
Задание № 2. Атрибуты и взаимодействие классов.
В квизе к предыдущей лекции мы реализовали возможность выставлять студентам оценки за домашние задания.
Теперь это могут делать только Reviewer (реализуйте такой метод)!
А что могут делать лекторы? Получать оценки за лекции от студентов :)
Реализуйте метод выставления оценок лекторам у класса Student (оценки по 10-балльной шкале,
хранятся в атрибуте-словаре у Lecturer, в котором ключи – названия курсов,
а значения – списки оценок). Лектор при этом должен быть закреплен за тем курсом, на который записан студент.
Зачёт
У Reviewer реализован метод выставления оценок студентам.
У Student реализован метод rate_lecture(), который:
Работает только для лекторов (Lecturer).
Проверяет, что лектор прикреплен к курсу студента.
Записывает оценки в словарь grades лектора.
Ошибки обрабатываются корректно (как в примере).
"""


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if not isinstance(lecturer, Lecturer):  # Оценки могут выставляться только лекторам
            return 'Ошибка'

        if not isinstance(grade, int) or grade < 0 or grade > 10:  # Оценка должна быть целым числом от 0 до 10
            return 'Ошибка'

        if course not in self.courses_in_progress:  # Студент не записан на этот курс
            return 'Ошибка'

        if course not in lecturer.courses_attached:  # Лектор не ведёт этот курс
            return 'Ошибка'

        if course in lecturer.grades:
            lecturer.grades[course].append(grade)
        else:
            lecturer.grades[course] = [grade]
        return


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}  # Словарь для хранения оценок от студентов


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):  # Теперь только Reviewer могут оценивать студентов
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')
student = Student('Алёхина', 'Ольга', 'Ж')

student.courses_in_progress += ['Python', 'Java']
lecturer.courses_attached += ['Python', 'C++']
reviewer.courses_attached += ['Python', 'C++']

# У Student реализован метод rate_lecture(), который
print(student.rate_lecture(lecturer, 'Python', 7))  # None
print(student.rate_lecture(lecturer, 'Java', 8))  # Ошибка
print(student.rate_lecture(lecturer, 'С++', 8))  # Ошибка
print(student.rate_lecture(reviewer, 'Python', 6))  # Ошибка

print(lecturer.grades)  # {'Python': [7]}

# Только у Reviewer реализован метод выставления оценок студентам
print(reviewer.rate_hw(student, 'Python', 10))  # None
print(reviewer.rate_hw(student, 'C++', 10))  # Ошибка
print(reviewer.rate_hw(student, 'Java', 10))  # Ошибка

print(student.grades)  # {'Python': [10]}

# print(lecturer.rate_hw(student, 'Python', 10))  # AttributeError: 'Lecturer' object has no attribute 'rate_hw'
