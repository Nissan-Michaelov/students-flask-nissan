from flask import Flask, redirect, url_for, render_template
app = Flask(__name__)
from setup_db import execute_query

@app.route('/register/<student_id>/<course_id>')
def register(student_id, course_id):
    """
    this endpoint inserts a student into student_courses table so student_id is registered to course_id. 
    Then show all courses for this student.
    """
    execute_query(f"INSERT INTO students_courses (student_id, course_id) VALUES ('{student_id}', '{course_id}')")
    redirect(url_for('registrations', student_id = student_id))

@app.route('/registrations/<student_id>')
def registrations(student_id):
    """
    1. Get course IDs for this student using students_courses
    """
    course_ids = execute_query(f"SELECT course_id FROM students_courses WHERE student_id={student_id}")
    clean_ids = [ c[0] for c in course_ids ]
    course_names = []
    for i in clean_ids:
        course_names.append(execute_query(f"SELECT name FROM courses WHERE course_id={i}"))
    student_names=execute_query(f"SELECT name FROM students WHERE student_id={student_id}")
    return render_template("registrations.html", student_name=student_names, course_names=course_names)