# Взять класс студент из дз 12-го семинара, добавить запуск из командной строки
# (передача в качестве аргумента название csv-файла с предметами), логирование и 
# написать 3-5 тестов с использованием pytest.

import csv
import logging
import argparse

class Student:
    """
    Класс, представляющий студента.

    Атрибуты:
    - name (str): ФИО студента
    - subjects (dict): словарь, содержащий предметы и их оценки и результаты тестов

    Методы:
    - __init__(self, name, subjects_file): конструктор класса
    - __setattr__(self, name, value): дескриптор, проверяющий ФИО на первую заглавную букву и наличие только букв
    - __getattr__(self, name): получение значения атрибута
    - __str__(self): возвращает строковое представление студента
    - load_subjects(self, subjects_file): загрузка предметов из файла CSV
    - get_average_test_score(self, subject): возвращает средний балл по тестам для заданного предмета
    - get_average_grade(self): возвращает средний балл по всем предметам
    - add_grade(self, subject, grade): добавление оценки по предмету
    - add_test_score(self, subject, test_score): добавление результата теста по предмету
    - save_subjects(self, subjects_file): запись результатов в файл CSV
    - parse_arguments(): запуск из командной строки с указанием файла CSV в аргументе
    - setup_logging(): логирование операций старт/стоп программы и записи в CSV-файл
    """

    def __init__(self, name, subjects_file):
        self.name = name
        self.subjects = {}
        self.load_subjects(subjects_file)
        self.save_subjects(subjects_file)

    def __setattr__(self, name, value):
        if name == 'name':
            if not value.replace(' ', '').isalpha() or not value.istitle():
                raise ValueError("ФИО должно состоять только из букв и начинаться с заглавной буквы")
        super().__setattr__(name, value)

    def __getattr__(self, name):
        if name in self.subjects:
            return self.subjects[name]
        else:
            raise AttributeError(f"Предмет {name} не найден")

    def __str__(self):
        return f"Студент: {self.name}\nПредметы: {', '.join(self.subjects.keys())}"

    def load_subjects(self, subjects_file):
        with open(subjects_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                subject = row[0]
                if subject not in self.subjects:
                    self.subjects[subject] = {'grades': [], 'test_scores': []}
    
    def add_grade(self, subject, grade):
        if subject not in self.subjects:
            self.subjects[subject] = {'grades': [], 'test_scores': []}
        if not isinstance(grade, int) or grade < 2 or grade > 5:
            raise ValueError("Оценка должна быть целым числом от 2 до 5")
        self.subjects[subject]['grades'].append(grade)
        
    def add_test_score(self, subject, test_score):
        if subject not in self.subjects:
            self.subjects[subject] = {'grades': [], 'test_scores': []}
        if not isinstance(test_score, int) or test_score < 0 or test_score > 100:
            raise ValueError("Результат теста должен быть целым числом от 0 до 100")
        self.subjects[subject]['test_scores'].append(test_score)
        
    def get_average_test_score(self, subject):
        if subject not in self.subjects:
            raise ValueError(f"Предмет {subject} не найден")
        test_scores = self.subjects[subject]['test_scores']
        if len(test_scores) == 0:
            return 0
        return sum(test_scores) / len(test_scores)

    def get_average_grade(self):
        total_grades = []
        for subject in self.subjects:
            grades = self.subjects[subject]['grades']
            if len(grades) > 0:
                total_grades.extend(grades)
        if len(total_grades) == 0:
            return 0
        return sum(total_grades) / len(total_grades)
    
    def save_subjects(self, subjects_file):
        with open(subjects_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for subject, values in self.subjects.items():
                writer.writerow([subject, ','.join(map(str, values['grades'])), ','.join(map(str, values['test_scores']))])
                if values['grades'] != [] or values['test_scores'] != []:
                    logging.info(f"Entry has been created to file {subjects_file} - Subject: {subject}, Grades: {values['grades']}, Test_scores: {values['test_scores']}")



def parse_arguments():
    parser = argparse.ArgumentParser(description='Краткое описание:')
    parser.add_argument('subjects_file', help='укажите CSV-файл с предметами - subjects.csv')
    return parser.parse_args()


def setup_logging():
    logging.basicConfig(filename='program.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')


if __name__ == '__main__':
    setup_logging()
    logging.info('Program start')
    args = parse_arguments()
    student = Student("Иван Иванов", args.subjects_file)

    student.add_grade("Математика", 4)
    student.add_test_score("Математика", 85)

    student.add_grade("История", 5)
    student.add_test_score("История", 92)

    student.add_grade("Математика", 4)
    student.add_test_score("Математика", 75)
    student.add_grade("Физика", 3)
    student.add_test_score("Физика", 50)

    average_grade = student.get_average_grade()
    print(f"Средний балл: {average_grade}")

    average_test_score = student.get_average_test_score("Математика")
    print(f"Средний результат по тестам по математике: {average_test_score}")
    average_test_score = student.get_average_test_score("История")
    print(f"Средний результат по тестам по истории: {average_test_score}")
    student.save_subjects("subjects.csv")
    print(student)
    logging.info('Program stop')