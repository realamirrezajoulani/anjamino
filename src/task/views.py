from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, CreateView

from list.models import List
from task.models import Task
from task.mixins import AssignListMixin, OwnerOrAdminMixin, OwnerOrAdminQuerysetMixin, _admin_roles

# Create your views here.
class TaskListView(LoginRequiredMixin, OwnerOrAdminQuerysetMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task/get_tasks.html'

    def get(self, request, *args, **kwargs):
        self.list_obj = get_object_or_404(List, pk=kwargs['list_pk'])
        # permission: check ownership or admin
        user = request.user
        if getattr(user, 'role', None) not in _admin_roles and self.list_obj.user_id != user.id:
            return HttpResponseForbidden("You do not have permission to view tasks for this list")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(list=self.list_obj)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['list'] = self.list_obj
        return ctx

class TaskDetailView(OwnerOrAdminMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'task/get_task.html'

class TaskCreateView(LoginRequiredMixin, AssignListMixin, CreateView):
    model = Task
    fields = ('title', 'detail', 'perority', 'completion_status')
    template_name = 'task/create_task.html'

    def dispatch(self, request, *args, **kwargs):
        # Load parent List and check permission
        self.list_obj = get_object_or_404(List, pk=kwargs['list_pk'])
        user = request.user
        if getattr(user, 'role', None) not in _admin_roles and self.list_obj.user_id != user.id:
            return HttpResponseForbidden("You do not have permission to add a task to this list")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('task:tasks', kwargs={'list_pk': self.list_obj.pk})

class TaskUpdateView(OwnerOrAdminMixin, UpdateView):
    model = Task
    fields = ('title', 'detail', 'perority', 'completion_status')
    template_name = 'task/update_task.html'

    def get_success_url(self):
        return reverse_lazy('task:tasks', kwargs={'list_pk': self.get_object().list.pk})

class TaskDeleteView(OwnerOrAdminMixin, DeleteView):
    model = Task
    template_name = 'task/delete_task.html'

    def get_success_url(self):
        return reverse_lazy('task:tasks', kwargs={'list_pk': self.get_object().list.pk})