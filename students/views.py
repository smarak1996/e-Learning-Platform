from django.shortcuts import render

from django.urls import reverse
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from braces.views import LoginRequiredMixin
from .forms import CourseEnrollForm
from django.http import HttpResponseRedirect

class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    #success_url = reverse('student_course_list')
    def form_valid(self, form):
        result = super(StudentRegistrationView, self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password1'])
        login(self.request, user)
        return result

    def get_success_url(self):
        return reverse('students:student_course_list')

class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm
    template_name="forms.html"

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('students:student_course_detail', args=[self.course.id])

from django.views.generic.list import ListView
from courses.models import Course

class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'
    def get_queryset(self):
        qs = super(StudentCourseListView, self).get_queryset()
        return qs.filter(students__in=[self.request.user])

from django.views.generic.detail import DetailView
class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'
    def get_queryset(self):
        qs = super(StudentCourseDetailView, self).get_queryset()
        print("000000000000000000000000000000000000000000000000000000000000000hello")
        print(qs.filter(students__in=[self.request.user]))
        return qs.filter(students__in=[self.request.user])
    def get_context_data(self, **kwargs):
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        context = super(StudentCourseDetailView,self).get_context_data(**kwargs)
        print("222222222222222222222222222222222")
        print(context)
        print("nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
        # get course object
        course = self.get_object()
        print(course)
        print("rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
        print(self.kwargs)
        print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
        if 'module_id' in self.kwargs:
            print("99999999999999999")
            # get current module
            context['module'] = course.modules.get(id=self.kwargs['module_id'])
            print(context['module'])

        else:
            # get first module
            print("66666666666666666666666666666")
            print(course.modules.all())
            context['module'] = course.modules.all()[0]
        print(context['module'])
        return context
