
import pytest

@pytest.fixture
def student():
    from taskDZ1 import Student
    return Student("Иван Иванов", "subjects.csv")


def test_getattr_nonexistent_subject(student): # проверяем, что метод getattr вызывает исключение AttributeError для несуществующего предмета.
    with pytest.raises(AttributeError):
        student.getattr("Математика")


def test_add_grade_valid_grade(student): # проверяет, что метод add_grade успешно добавляет оценку в словарь subjects.
    student.subjects = {"Физика": {'grades': [], 'test_scores': []}}
    student.add_grade(subject="Физика", grade=3)
    assert student.subjects == {"Физика": {'grades': [3], 'test_scores': []}}, 'Error: значение в словаре не соответствует введенному'
    

def test_add_grade_invalid_grade(student): # проверяем, что метод add_grade вызывает исключение ValueError, при не верном значении оценки.
    with pytest.raises(ValueError):
        student.add_grade("История", 3.4)


def test_load_subjects_existing_subject(student): # проверяем, что метод load_subjects загружает предметы из файла CSV, когда существует предмет в файле.
    student.load_subjects("subjects.csv")
    assert "Математика" in student.subjects


def test_load_subjects_nonexistent_subject(student): # проверяем, что метод load_subjects не добавляет предмет в словарь subjects, когда предмет отсутствует в файле.
    student.load_subjects("subjects.csv")
    assert "физика" not in student.subjects


if __name__ == '__main__':
    pytest.main(['-v'])

