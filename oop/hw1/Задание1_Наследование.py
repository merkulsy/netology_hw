"""
Задание № 1. Наследование
Исходя из квиза к предыдущему занятию, у нас уже есть класс преподавателей и класс студентов
(вы можете взять этот код за основу или написать свой). Студентов пока оставим без изменения,
а вот преподаватели бывают разные, поэтому теперь класс Mentor должен стать родительским классом,
а от него нужно реализовать наследование классов Lecturer (лекторы) и Reviewer (эксперты, проверяющие домашние задания).
Очевидно, имя, фамилия и список закрепленных курсов логично реализовать на уровне родительского класса.
А чем же будут специфичны дочерние классы? Об этом в следующих заданиях.
А пока можете проверить, что успешно реализовали дочерние классы
Зачёт
Созданы классы Lecturer и Reviewer, наследующие от Mentor.
Проверка через isinstance() возвращает True.
Атрибуты courses_attached корректно наследуются и инициализируются пустым списком.
"""


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


class Lecturer(Mentor):
    pass


class Reviewer(Mentor):
    pass


lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')
print(isinstance(lecturer, Mentor))  # True
print(isinstance(reviewer, Mentor))  # True
print(lecturer.courses_attached)  # []
print(reviewer.courses_attached)  # []
