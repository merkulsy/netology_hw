"""
Задание № 3. Полиморфизм и магические методы
Перегрузите магический метод __str__ у всех классов.
У проверяющих он должен выводить информацию в следующем виде:
print(some_reviewer)
Имя: Some
Фамилия: Buddy
У лекторов:
print(some_lecturer)
Имя: Some
Фамилия: Buddy
Средняя оценка за лекции: 9.9
А у студентов так:
print(some_student)
Имя: Ruoy
Фамилия: Eman
Средняя оценка за домашние задания: 9.9
Курсы в процессе изучения: Python, Git
Завершенные курсы: Введение в программирование
Реализуйте возможность сравнивать (через операторы сравнения) между собой лекторов по средней оценке за лекции
и студентов по средней оценке за домашние задания.
Зачёт
Перегружен str для всех классов (формат вывода соответствует условию).
Реализовано сравнение (>, <, ==) лекторов и студентов по средней оценке.
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

    def _get_average_grade(self):  # Внутренний метод для вычисления средней оценки
        all_grades = []
        for course_grades in self.grades.values():
            all_grades.extend(course_grades)
        return round(sum(all_grades) / len(all_grades), 1) if all_grades else 0

    def __str__(self):
        # Вычисляем среднюю оценку по всем курсам
        avg_grade = self._get_average_grade()
        # Преобразуем списки курсов в строки через запятую
        courses_in_progress_str = ', '.join(self.courses_in_progress) if self.courses_in_progress else "Нет"
        finished_courses_str = ', '.join(self.finished_courses) if self.finished_courses else "Нет"

        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: {avg_grade}\n'
                f'Курсы в процессе изучения: {courses_in_progress_str}\n'
                f'Завершенные курсы: {finished_courses_str}')

    # Методы сравнения для студентов
    def __lt__(self, other):  # Меньше (<)
        if isinstance(other, Student):
            return self._get_average_grade() < other._get_average_grade()
        else:
            raise TypeError('Можно сравнивать только Student с другим Student')

    def __le__(self, other):  # Меньше или равно (<=)
        if isinstance(other, Student):
            return self._get_average_grade() <= other._get_average_grade()
        else:
            raise TypeError('Можно сравнивать только Student с другим Student')

    def __gt__(self, other):  # Больше (>)
        if isinstance(other, Student):
            return self._get_average_grade() > other._get_average_grade()
        else:
            raise TypeError('Можно сравнивать только Student с другим Student')

    def __ge__(self, other):  # Больше или равно (>=)
        if isinstance(other, Student):
            return self._get_average_grade() >= other._get_average_grade()
        else:
            raise TypeError('Можно сравнивать только Student с другим Student')

    def __eq__(self, other):  # Равно (==)
        if isinstance(other, Student):
            return self._get_average_grade() == other._get_average_grade()
        else:
            raise TypeError('Можно сравнивать только Student с другим Student')

    def __ne__(self, other):  # Не равно (!=)
        if isinstance(other, Student):
            return self._get_average_grade() != other._get_average_grade()
        else:
            raise TypeError('Можно сравнивать только Student с другим Student')


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}  # Словарь для хранения оценок от студентов

    def _get_average_grade(self):  # Внутренний метод для вычисления средней оценки
        all_grades = []
        for course_grades in self.grades.values():
            all_grades.extend(course_grades)
        return round(sum(all_grades) / len(all_grades), 1) if all_grades else 0

    def __str__(self):
        # Вычисляем среднюю оценку по всем курсам
        avg_grade = self._get_average_grade()

        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за лекции: {avg_grade}')

    # Методы сравнения для лекторов
    def __lt__(self, other):  # Меньше (<)
        if isinstance(other, Lecturer):
            return self._get_average_grade() < other._get_average_grade()
        else:
            raise TypeError('Можно сравнивать только Lecturer с другим Lecturer')

    def __le__(self, other):  # Меньше или равно (<=)
        if isinstance(other, Lecturer):
            return self._get_average_grade() <= other._get_average_grade()
        else:
            raise TypeError('Можно сравнивать только Lecturer с другим Lecturer')

    def __gt__(self, other):  # Больше (>)
        if isinstance(other, Lecturer):
            return self._get_average_grade() > other._get_average_grade()
        else:
            raise TypeError('Можно сравнивать только Lecturer с другим Lecturer')

    def __ge__(self, other):  # Больше или равно (>=)
        if isinstance(other, Lecturer):
            return self._get_average_grade() >= other._get_average_grade()
        else:
            raise TypeError('Можно сравнивать только Lecturer с другим Lecturer')

    def __eq__(self, other):  # Равно (==)
        if isinstance(other, Lecturer):
            return self._get_average_grade() == other._get_average_grade()
        else:
            raise TypeError('Можно сравнивать только Lecturer с другим Lecturer')

    def __ne__(self, other):  # Не равно (!=)
        if isinstance(other, Lecturer):
            return self._get_average_grade() != other._get_average_grade()
        else:
            raise TypeError('Можно сравнивать только Lecturer с другим Lecturer')


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):  # Теперь только Reviewer могут оценивать студентов
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}')


lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')
student = Student('Алёхина', 'Ольга', 'Ж')
student2 = Student('Сидорова', 'Мария', 'Ж')
lecturer2 = Lecturer('Александр', 'Александров')

student.courses_in_progress += ['Python', 'Java']
lecturer.courses_attached += ['Python', 'C++']
reviewer.courses_attached += ['Python', 'C++']
student2.courses_in_progress += ['Python']
lecturer2.courses_attached += ['Python']

reviewer.rate_hw(student, 'Python', 10)
reviewer.rate_hw(student, 'Python', 9)
reviewer.rate_hw(student2, 'Python', 8)
reviewer.rate_hw(student2, 'Python', 9)

student.rate_lecture(lecturer, 'Python', 10)
student.rate_lecture(lecturer, 'Python', 10)
student.rate_lecture(lecturer, 'Python', 9)
student.rate_lecture(lecturer2, 'Python', 10)
student.rate_lecture(lecturer2, 'Python', 10)

print(reviewer)
print(lecturer)
print(student)
print(student2)
print(lecturer2)

print(student == student2)
print(student != student2)
print(student < student2)
print(student > student2)
print(student >= student2)
print(student <= student2)

print(lecturer == lecturer2)
print(lecturer != lecturer2)
print(lecturer < lecturer2)
print(lecturer > lecturer2)
print(lecturer >= lecturer2)
print(lecturer <= lecturer2)