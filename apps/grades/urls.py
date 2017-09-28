from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^new_student$', views.new_student, name = 'new_student'),
    url(r'^new_class$', views.new_class, name = 'new_class'),
    url(r'^create_student$', views.create_student, name = 'create_student'),
    url(r'^show_student$', views.show_student, name = 'show_student'),
    url(r'^edit_student/(?P<student_id>\d+)$', views.edit_student, name = 'edit_student'),
    url(r'^update_student/(?P<student_id>\d+)$', views.update_student, name = 'update_student'),
    url(r'^remove_student/(?P<student_id>\d+)$', views.remove_student, name = 'remove_student'),
    url(r'^create_class$', views.create_class, name = 'create_class'),
    url(r'^(?P<id>\d+)$', views.show_class, name = 'show_class'),
    url(r'^new_assignment$', views.new_assignment, name = 'new_assignment'),
    url(r'^create_assignment$', views.create_assignment, name = 'create_assignment'),
    url(r'^show_assignment/(?P<assign_id>\d+)$', views.show_assignment, name = 'show_assignment'),
    url(r'^add_note$', views.add_note, name = 'add_note'),
    url(r'^delete_note/(?P<note_id>\d+)$', views.delete_note, name = 'delete_note'),
    url(r'^assign_grade/(?P<assign_id>\d+)$', views.assign_grade, name = 'assign_grade'),
    url(r'^submit_grade/(?P<assign_id>\d+)$', views.submit_grade, name = 'submit_grade'),
    url(r'^student_grades/(?P<student_id>\d+)$', views.student_grades, name = 'student_grades'),
    url(r'^student_graph/(?P<student_id>\d+)$', views.student_graph, name = 'student_graph'),
    url(r'^delete/(?P<class_id>\d+)$', views.delete_class, name = 'delete_class'),
]
