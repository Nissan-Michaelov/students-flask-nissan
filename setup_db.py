import sqlite3
import faker
import random


def execute_query(sql):
    with sqlite3.connect("students.db") as conn:
        cur = conn.cursor()
        cur.execute(sql)
        return cur.fetchall()


def create_tables():
    execute_query("""
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_name TEXT NOT NULL,
            teacher_email TEXT NOT NULL UNIQUE
        )
    """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_name TEXT NOT NULL,
            teacher_id INTEGER NOT NULL,
            FOREIGN KEY (teacher_id) REFERENCES teachers (teacher_id)
        )
    """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            student_email TEXT NOT NULL UNIQUE
        )
    """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS students_courses (
            students_courses_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            course_id INTEGER,
            FOREIGN KEY(student_id) REFERENCES students (student_id),
            FOREIGN KEY(course_id) REFERENCES courses (course_id)
        )
    """)


def create_fake_data(students_num=40, teachers_num=4):
    fake = faker.Faker()
    for student in range(students_num):
        execute_query(
            f"INSERT INTO students (student_name, student_email) VALUES ('{fake.name()}', '{fake.email()}')")
    for teacher in range(teachers_num):
        execute_query(
            f"INSERT INTO teachers (teacher_name, teacher_email) VALUES ('{fake.name()}', '{fake.email()}')")
    courses = ['python', 'java', 'html', 'css', 'javascript']
    teacher_ids = [tup[0]
                   for tup in execute_query("SELECT teacher_id FROM teachers")]
    for course in courses:
        execute_query(
            f"INSERT INTO courses (course_name, teacher_id) VALUES ('{course}', '{random.choice(teacher_ids)}')")

if __name__ == "__main__":
    create_tables()
    create_fake_data()