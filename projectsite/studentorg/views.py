from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import College, Organization, Student, Program, OrgMember
from studentorg.forms import CollegeForm, OrganizationForm, StudentForm, ProgramForm, OrgMemberForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import TemplateView

@method_decorator(login_required, name='dispatch')
class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"

# ✅ College Views
class CollegeList(ListView):
    model = College
    context_object_name = 'colleges'
    template_name = 'college_list.html'
    paginate_by = 5

class CollegeCreateView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_add.html'
    success_url = reverse_lazy('college-list')

class CollegeUpdateView(UpdateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_edit.html'
    success_url = reverse_lazy('college-list')

class CollegeDeleteView(DeleteView):
    model = College
    template_name = 'college_del.html'
    success_url = reverse_lazy('college-list')

# Organization Views
class OrganizationList(ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = 'org_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(OrganizationList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") != None:
            query = self.request.GET.get("q")
            qs = qs.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
        return qs

class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_add.html'
    success_url = reverse_lazy('organization-list')

class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_edit.html'
    success_url = reverse_lazy('organization-list')

class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'org_del.html'
    success_url = reverse_lazy('organization-list')

# Student Views
class StudentList(ListView):
    model = Student
    context_object_name = 'student'
    template_name = 'student_list.html'
    paginate_by = 5

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_add.html'
    success_url = reverse_lazy('student-list')

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_edit.html'
    success_url = reverse_lazy('student-list')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student_del.html'
    success_url = reverse_lazy('student-list')

# Program Views
class ProgramList(ListView):
    model = Program
    context_object_name = 'program'
    template_name = 'prog_list.html'
    paginate_by = 5

class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'prog_add.html'
    success_url = reverse_lazy('prog-list')

class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'prog_edit.html'
    success_url = reverse_lazy('prog-list')

class ProgramDeleteView(DeleteView):
    model = Program
    template_name = 'prog_del.html'
    success_url = reverse_lazy('prog-list')

# OrgMember Views
class OrgMemberList(ListView):
    model = OrgMember
    context_object_name = 'orgmember'
    template_name = 'orgmember_list.html'
    paginate_by = 5

class OrgMemberCreateView(CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'orgmember_add.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'orgmember_edit.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberDeleteView(DeleteView):
    model = OrgMember
    template_name = 'orgmember_del.html'
    success_url = reverse_lazy('orgmember-list')


class AnalyticsDashboardView(TemplateView):
    template_name = 'charts_dashboard.html' # This view will render the charts_dashboard.html template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        program_data = Program.objects.annotate(
            student_count=Count('student')
        ).order_by('prog_name') # Order by program name for consistent chart display

        # Prepare labels (program names) and data (student counts) for Chart.js
        program_labels = [p.prog_name for p in program_data]
        program_student_counts = [p.student_count for p in program_data]

        # Add this data to the context, which will be available in the template
        context['program_labels'] = program_labels
        context['program_student_counts'] = program_student_counts

        # --- Data for Organizations per College Chart ---
        # Query to get the count of organizations for each college.
        # It annotates each College object with an 'organization_count' field.
        college_data = College.objects.annotate(
            organization_count=Count('organization')
        ).order_by('college_name') # Order by college name

        # Prepare labels (college names) and data (organization counts) for Chart.js
        college_labels = [c.college_name for c in college_data]
        college_org_counts = [c.organization_count for c in college_data]

        # Add this data to the context
        context['college_labels'] = college_labels
        context['college_org_counts'] = college_org_counts


        return context
