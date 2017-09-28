from django.shortcuts import render, redirect

from ..log_reg.models import User
from .models import Student, Note, Assignment, Grade
from django.contrib import messages
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import LineChart, BarChart, ColumnChart

# Create your views here.

def index(request):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be logged in to continue!')
        return redirect('users:index')
    else:
        context={
            'user'      :   User.objects.get(id = request.session['user_id']),
            'students'  :   Student.objects.all(),
            'class'     :   Student.objects.filter(teacher = request.session['user_id']),
            'teacher'   :   User.objects.get(id = request.session['user_id']),
            'assignment':   Assignment.objects.filter(teacher = request.session['user_id']),
            'notes'     :   Note.objects.filter(teacher = request.session['user_id'])
        }
    return render(request, 'grades/index.html', context)

def show_class(request, id):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be logged in to continue!')
        return redirect('users:index')
    else:
        context={
            'teacher'   :   User.objects.get(id = id),
            'students'     :   Student.objects.filter(teacher = id)
        }
    return render(request, 'grades/show_students.html', context)

def new_student(request):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be logged in to continue!')
        return redirect('users:index')
    else:
        context={
            'students'  :   Student.objects.all().order_by('last_name')
        }
    return render(request, 'grades/student.html', context)

def create_student(request):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be logged in to continue!')
        return redirect('users:index')
    if request.method == 'POST':
        response_from_model = Student.objects.add(request.POST)
    if response_from_model['status']:
        return redirect('main:new_student')
    else:
        for error in response_from_model['errors']:
            messages.error(request, error)
        return redirect('main:new_student')

def show_student(request):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be logged in to continue!')
        return redirect('users:index')
    else:
        context={
            'students' : Student.objects.all(),
        }
    return render(request, 'grades/show_students.html', context)

def edit_student(request, student_id):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be logged in to continue!')
        return redirect('users:index')
    else:
        context={
            'student'   :   Student.objects.get(id=student_id),
        }
        return render(request, 'grades/edit_student.html', context)

def update_student(request, student_id):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be logged in to continue!')
        return redirect('users:index')
    else:
        if request.method == 'POST':
            response_from_model = Student.objects.update(request.POST, student_id)
        if response_from_model['status']:
            return redirect('main:show_student')

def remove_student(request, student_id):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be logged in to continue!')
    else:
        if request.method == 'POST':
            response_from_model = Student.objects.destroy(request.POST, student_id)
        if response_from_model['status']:
            return redirect('main:show_student')

def new_class(request):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be logged in to continue!')
        return redirect('users:index')
    else:
        context={
            'students'  :   Student.objects.exclude(teacher = request.session['user_id']),
            'class'     :   Student.objects.filter(teacher = request.session['user_id'])
        }
    return render(request, 'grades/class.html', context)

def create_class(request):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be logged in to continue!')
        return redirect('users:index')
    if request.method == 'POST':
        response_from_model = Student.objects.add_student(request.POST)
    if response_from_model['status']:
        return redirect('main:index')
    else:
        for error in response_from_model['errors']:
            messages.error(request, error)
        return redirect('main:new_class')

def delete_class(request, class_id):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be logged in to continue!')
        return redirect('users:index')
    if request.method == 'POST':
        response_from_model = Class.objects.destroy(class_id)
    if response_from_model['status']:
        return redirect('main:index')

def new_assignment(request):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be logged in to continue!')
        return redirect('users:index')
    else:
        context={
            'assignments'   :   Assignment.objects.filter(teacher = request.session['user_id']),
            'math'          :   Assignment.objects.filter(teacher = request.session['user_id']).filter(subject = 'Math'),
            'reading'       :   Assignment.objects.filter(teacher = request.session['user_id']).filter(subject = 'Reading'),
            'science'       :   Assignment.objects.filter(teacher = request.session['user_id']).filter(subject = 'Science'),
            'language'      :   Assignment.objects.filter(teacher = request.session['user_id']).filter(subject = 'Language Arts'),
            'social'        :   Assignment.objects.filter(teacher = request.session['user_id']).filter(subject = 'Social Studies'),
            'music'         :   Assignment.objects.filter(teacher = request.session['user_id']).filter(subject = 'Music'),
            'art'           :   Assignment.objects.filter(teacher = request.session['user_id']).filter(subject = 'Art')
        }
    return render(request, 'grades/assignment.html', context)

def create_assignment(request):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be logged in to continue!')
        return redirect('users:index')
    if request.method == 'POST':
        response_from_model = Assignment.objects.add(request.POST)
    if response_from_model['status']:
        return redirect('main:new_assignment')
    else:
        for error in response_from_model['errors']:
            messages.error(request, error)
        return redirect('main:new_assignment')

def show_assignment(request, assign_id):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be logged in to continue!')
        return redirect('users:index')
    else:
        context={
            'class'     :   Grade.objects.filter(assignment=assign_id).select_related(),
            'assignment':   Assignment.objects.get(id=assign_id)
        }
        return render(request, 'grades/show_assignment.html', context)

def assign_grade(request, assign_id):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be logged in to continue!')
        return redirect('users:index')
    else:
        context={
            'students'      :   Student.objects.filter(teacher = request.session['user_id']),
            'assignment'    :   Assignment.objects.get(id = assign_id),
            'grades'        :   Grade.objects.filter(assignment = assign_id)
        }
        return render(request, 'grades/input_grade.html', context)

def submit_grade(request, assign_id):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be logged in to continue!')
        return redirect('users:index')
    if request.method == 'POST':
        students = request.POST.getlist('student_id')
        grades = request.POST.getlist('grade')
        response_from_model = Grade.objects.input(request.POST, students, grades, assign_id)

    if response_from_model['status']:
        return redirect('main:new_assignment')
    else:
        for error in response_from_model['errors']:
            messages.error(request, error)
        return redirect('main:assign_grade')

def student_grades(request, student_id):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be logged in to continue!')
        return redirect('users:index')
    else:
        student = Student.objects.get(id = student_id)
        context={
            'student'       :   Student.objects.get(id = student_id),
            'math'          :   Grade.objects.filter(student = student).filter(assignment__subject = "Math").select_related(),
            'reading'       :   Grade.objects.filter(student = student).filter(assignment__subject = "Reading").select_related(),
            'science'       :   Grade.objects.filter(student = student).filter(assignment__subject = "Science").select_related(),
            'language'      :   Grade.objects.filter(student = student).filter(assignment__subject = "Language Arts").select_related(),
            'social'        :   Grade.objects.filter(student = student).filter(assignment__subject = "Social Studies").select_related(),
            'music'         :   Grade.objects.filter(student = student).filter(assignment__subject = "Music").select_related(),
            'art'           :   Grade.objects.filter(student = student).filter(assignment__subject = "Art").select_related()
        }
    return render(request, 'grades/student_grades.html', context)

def student_graph(request, student_id):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be logged in to continue!')
        return redirect('users:index')

    if request.method == 'POST':
        assign_id = request.POST.getlist('assignment')
        response_from_model = Grade.objects.find_assigns(request.POST, assign_id, student_id)

        data_source = SimpleDataSource(data=response_from_model)
        student = Student.objects.get(id = student_id)
        # Chart object
        chart = ColumnChart(data_source, options={'title': student.first_name+"'s"+ ' Grade Report'})
        context = {
                'chart'     :   chart,
                'student'   :   student
        }
    return render(request, 'grades/student_graph.html', context)

def add_note(request):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be logged in to continue!')
        return redirect('users:index')

    if request.method =='POST':
        response_from_model = Note.objects.add_note(request.POST)

    if response_from_model['status']:
        return redirect('main:index')
    else:
        for error in response_from_model['errors']:
            messages.error(request, error)
        return redirect('main:index')

def delete_note(request, note_id):
    if not 'user_id' in request.session:
        messages.error(request, 'Must be logged in to continue!')
        return redirect('users:index')

    if request.method =='POST':
        response_from_model = Note.objects.destroy(note_id)
    return redirect('main:index')
