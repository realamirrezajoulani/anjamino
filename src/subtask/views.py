from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, CreateView
from django.shortcuts import get_object_or_404

from task.models import Task

from .models import Subtask
from .mixins import OwnerOrAdminMixin, _admin_roles


# Create your views here.
class SubtaskListView(ListView):
    model = Subtask
    context_object_name = 'subtasks'
    template_name = 'subtask/get_subtasks.html'

    def get(self, request, *args, **kwargs):
        self.task_obj = get_object_or_404(Task, pk=kwargs['task_pk'])
        parent_list = self.task_obj.list
        user = request.user
        if not (getattr(user, 'role', None) in _admin_roles or parent_list.user_id == user.id):
            return HttpResponseForbidden("You do not have permission to view subtasks for this task")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Subtask.objects.filter(task=self.task_obj)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['task'] = self.task_obj
        return ctx

class SubtaskDetailView(OwnerOrAdminMixin, DetailView):
    model = Subtask
    context_object_name = 'subtask'
    template_name = 'subtask/get_subtask.html'

class SubtaskCreateView(OwnerOrAdminMixin, CreateView):
    model = Subtask
    fields = ('title', 'completion_status')
    template_name = 'subtask/create_subtask.html'

    def dispatch(self, request, *args, **kwargs):
        self.task_obj = get_object_or_404(Task, pk=kwargs['task_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.task = self.task_obj
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('subtask:subtasks', kwargs={'task_pk': self.task_obj.pk})

class SubtaskUpdateView(OwnerOrAdminMixin, UpdateView):
    model = Subtask
    fields = ('title', 'completion_status')
    template_name = 'subtask/update_subtask.html'

    def get_success_url(self):
        return reverse_lazy('subtask:subtasks', kwargs={'task_pk': self.get_object().task.pk})

class SubtaskDeleteView(OwnerOrAdminMixin, DeleteView):
    model = Subtask
    template_name = 'subtask/delete_subtask.html'

    def get_success_url(self):
        return reverse_lazy('subtask:subtasks', kwargs={'task_pk': self.get_object().task.pk})