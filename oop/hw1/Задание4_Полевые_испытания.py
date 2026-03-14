"""
Задание № 4. Полевые испытания
Создайте по 2 экземпляра каждого класса, вызовите все созданные методы, а также реализуйте две функции:
для подсчета средней оценки за домашние задания по всем студентам в рамках конкретного курса
(в качестве аргументов принимаем список студентов и название курса);
для подсчета средней оценки за лекции всех лекторов в рамках курса
(в качестве аргумента принимаем список лекторов и название курса).
Зачёт
Созданы по 2 экземпляра каждого класса.
Проверены все методы (включая новые).
Реализованы 2 функции:
Подсчет средней оценки студентов по курсу.
Подсчет средней оценки лекторов по курсу.
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
        if not isinstance(lecturer, Lecturer):
            return 'Ошибка: Оценки могут выставляться только лекторам'

        if not isinstance(grade, int) or grade < 0 or grade > 10:
            return 'Ошибка: Оценка должна быть целым числом от 0 до 10'

        if course not in self.courses_in_progress:
            return 'Ошибка: Студент не записан на этот курс'

        if course not in lecturer.courses_attached:
            return 'Ошибка: Лектор не ведёт этот курс'

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
    def rate_hw(self, student, course, grade):  # Только Reviewer могут оценивать студентов
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


# Функция для подсчета средней оценки за домашние задания по всем студентам в рамках курса
def average_hw_grade_for_course(students_list, course_name):
    if not students_list:
        return 0

    all_grades = []
    for student in students_list:
        if course_name in student.grades:
            all_grades.extend(student.grades[course_name])

    if not all_grades:
        return 0

    return round(sum(all_grades) / len(all_grades), 1)


# Функция для подсчета средней оценки за лекции всех лекторов в рамках курса
def average_lecture_grade_for_course(lecturers_list, course_name):
    if not lecturers_list:
        return 0

    all_grades = []
    for lecturer in lecturers_list:
        if course_name in lecturer.grades:
            all_grades.extend(lecturer.grades[course_name])

    if not all_grades:
        return 0

    return round(sum(all_grades) / len(all_grades), 1)


student = Student('Алёхина', 'Ольга', 'Ж')
student2 = Student('Сидорова', 'Мария', 'Ж')
lecturer = Lecturer('Иван', 'Иванов')
lecturer2 = Lecturer('Олег', 'Олегов')
reviewer = Reviewer('Пётр', 'Петров')
reviewer2 = Reviewer('Александр', 'Александров')

student.courses_in_progress += ['Python', 'Java', 'C++']
student2.courses_in_progress += ['Python', 'SQL']
lecturer.courses_attached += ['Python', 'Java', 'C++']
lecturer2.courses_attached += ['Python']
reviewer.courses_attached += ['Python', 'Java', 'C++']
reviewer2.courses_attached += ['Python', 'Java']


reviewer.rate_hw(student, 'Python', 10)
reviewer.rate_hw(student, 'Java', 9)
reviewer.rate_hw(student, 'C++', 9)
reviewer2.rate_hw(student, 'Python', 9)
reviewer.rate_hw(student2, 'Python', 10)
reviewer2.rate_hw(student2, 'Python', 10)

student.rate_lecture(lecturer, 'Python', 10)
student.rate_lecture(lecturer, 'Python', 10)
student.rate_lecture(lecturer, 'Java', 10)
student.rate_lecture(lecturer, 'C++', 10)
student2.rate_lecture(lecturer, 'Python', 10)
student.rate_lecture(lecturer2, 'Python', 9)
print(student2.rate_lecture(lecturer2, 'Python', 9))

# Проверки на ошибки в выставлении оценок
print(student.rate_lecture(reviewer, 'Python', 9))
print(student.rate_lecture(lecturer, 'Python', 100))
print(student.rate_lecture(lecturer, 'SQL', 10))
print(student2.rate_lecture(lecturer, 'SQL', 10))
print()

print(student, student2, lecturer, lecturer2, reviewer, reviewer2, sep='\n\n')
print()

print(student.grades)
print(student2.grades)
print('student != student2 is', student != student2)
print('student < student2 is', student < student2)
print('student > student2 is', student > student2)
print('student >= student2 is', student >= student2)
print('student <= student2 is', student <= student2)
print()

print(lecturer.grades)
print(lecturer2.grades)
print('lecturer == lecturer2 is', lecturer == lecturer2)
print('lecturer != lecturer2 is', lecturer != lecturer2)
print('lecturer < lecturer2 is', lecturer < lecturer2)
print('lecturer > lecturer2 is', lecturer > lecturer2)
print('lecturer >= lecturer2 is', lecturer >= lecturer2)
print('lecturer <= lecturer2 is', lecturer <= lecturer2)


all_students = [student, student2]
all_lecturers = [lecturer, lecturer2]

print("\nСредние оценки за домашние задания по курсам:")
print(f"Python: {average_hw_grade_for_course(all_students, 'Python')}")
print(f"Java: {average_hw_grade_for_course(all_students, 'Java')}")
print(f"C++: {average_hw_grade_for_course(all_students, 'C++')}")
print(f"SQL: {average_hw_grade_for_course(all_students, 'SQL')}")

print("\nСредние оценки за лекции по курсам:")
print(f"Python: {average_lecture_grade_for_course(all_lecturers, 'Python')}")
print(f"Java: {average_lecture_grade_for_course(all_lecturers, 'Java')}")
print(f"C++: {average_lecture_grade_for_course(all_lecturers, 'C++')}")
print(f"SQL: {average_lecture_grade_for_course(all_lecturers, 'SQL')}")
