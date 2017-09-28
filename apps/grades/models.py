from __future__ import unicode_literals

from ..log_reg.models import User
from django.db import models
import time
import datetime

class SubjectManager(models.Manager):
    def join():
            response_to_views = {}
            return response_to_views
class AssignmentManager(models.Manager):
    def add(self, postData):
            response_to_views = {}
            errors = []

            if not len(postData['name']):
                errors.append('Assignment Name is required.')

            if errors:
                response_to_views['status'] = False
                response_to_views['erros'] = errors

            else:
                teacher = User.objects.get(id=postData['user_id'])

                assignment = self.create(assignment_name=postData['name'], subject=postData['subject'], teacher=teacher)

                response_to_views['status'] = True
                response_to_views['assignment'] = assignment

            return response_to_views

class GradeManager(models.Manager):
    def input(self, postData, students, grades, assign_id):
            response_to_views = {}
            errors = []

            for kid, grade in zip(students, grades):

                print kid, grade+"*****"

                assignment = Assignment.objects.get(id = assign_id)
                student = Student.objects.get(id = kid)

                this_grade = self.create(grado=grade, student=student, assignment=assignment)
                print this_grade

            response_to_views['status'] = True

            return response_to_views

    def find_assigns(self, postData, assign_id, student_id):
            response_to_views = {}
            data = [['Assignment', 'Grade']]
            errors = []

            student = Student.objects.get(id = student_id)

            for assign in assign_id:

                assignment = Assignment.objects.get(id = assign)
                grade = Grade.objects.filter(student = student).filter(assignment = assignment)[0]
                plot = [assignment.assignment_name, grade.grado]
                data.append(plot)

            return data

class StudentManager(models.Manager):
    def add(self, postData):
        response_to_views = {}
        errors = []

        if not len(postData['first_name']):
            errors.append('First Name is required.')

        if not len(postData['last_name']):
            errors.append('Last Name is required.')

        if errors:
            response_to_views['status'] = False
            response_to_views['erros'] = errors
        else:
            student = self.create(first_name = postData['first_name'], last_name = postData['last_name'])

            response_to_views['status'] = True
            response_to_views['student'] = student

        return response_to_views

    def add_student(self, postData):
        response_to_views = {}
        errors = []

        this_teacher = User.objects.get(id = postData['user_id'])

        student = Student.objects.get(id = postData['student_id'])

        student.teacher.add(this_teacher)

        response_to_views['status'] = True

        return response_to_views

    def update(self, postData, student_id):
        response_to_views = {}
        errors = []

        this_student = Student.objects.get(id=student_id)

        if postData['first_name']:
            this_student.first_name = postData['first_name']
            this_student.save()

        if postData['last_name']:
            this_student.last_name = postData['last_name']
            this_student.save()

        response_to_views['status'] = True

        return response_to_views

    def destroy(self, postData, student_id):
        response_to_views = {}
        errors = []

        this_student = Student.objects.get(id = student_id)

        this_student.delete()

        response_to_views['status'] = True

        return response_to_views

class NoteManager(models.Manager):
    def add_note(self, postData):
        response_to_views = {}
        errors = []

        this_teacher = User.objects.get(id = postData['user_id'])

        note = self.create(content=postData['content'], teacher = this_teacher)

        response_to_views['note'] = note
        response_to_views['status'] = True

        return response_to_views

    def destroy(self, note_id):
        response_to_views = {}

        this_note = Note.objects.get(id = note_id)
        this_note.delete()

        response_to_views['status'] = True

        return response_to_views

class Subject(models.Model):
    subject_name = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = SubjectManager()

class Assignment(models.Model):
    assignment_name = models.CharField(max_length = 255)
    subject = models.CharField(max_length = 255)
    teacher = models.ForeignKey(User, related_name="teacher_assignment", null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = AssignmentManager()

class Student(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    teacher = models.ManyToManyField(User, related_name = "teacher_student")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = StudentManager()

class Grade(models.Model):
    grado = models.IntegerField(default=0)
    student = models.ForeignKey(Student, related_name="student_grade")
    assignment = models.ForeignKey(Assignment, related_name="assignment_grade")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = GradeManager()

class Note(models.Model):
    content = models.TextField(max_length = 1000)
    teacher = models.ForeignKey(User, related_name="teacher_note")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = NoteManager()
