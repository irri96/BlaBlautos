from django.urls import include, path

from Nucleo.views import classroom, students, teachers

urlpatterns = [
    path('', include('Nucleo.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', classroom.SignUpView.as_view(), name='signup'),
    path('accounts/signup/student/', students.StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/teacher/', teachers.TeacherSignUpView.as_view(), name='teacher_signup'),
]
