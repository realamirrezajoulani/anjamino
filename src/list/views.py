from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from task.models import List
from django.views.generic import ListView, UpdateView, DeleteView, DetailView, CreateView

from .mixins import OwnerOrAdminMixin, OwnerOrAdminQuerysetMixin, AssignOwnerMixin, _admin_roles

# Create your views here.
class ListListView(LoginRequiredMixin, OwnerOrAdminQuerysetMixin, ListView):
    model = List
    context_object_name = 'lists'
    template_name = 'list/get_lists.html'

class ListDetailView(OwnerOrAdminMixin, DetailView):
    model = List
    context_object_name = 'list'
    template_name = 'list/get_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # Filter tasks by permission
        user = self.request.user
        tasks = self.object.task_set.all()
        if getattr(user, 'role', None) not in _admin_roles:
            tasks = tasks.filter(list__user=user)
        ctx['tasks'] = tasks
        return ctx

class ListCreateView(LoginRequiredMixin, AssignOwnerMixin, CreateView):
    model = List
    fields = ('title', 'color')
    template_name = 'list/create_list.html'
    success_url = reverse_lazy('list:lists')

class ListUpdateView(OwnerOrAdminMixin, UpdateView):
    model = List
    fields = ('title', 'color')
    template_name = 'list/update_list.html'
    success_url = reverse_lazy('list:lists')

class ListDeleteView(OwnerOrAdminMixin, DeleteView):
    model = List
    template_name = 'list/delete_list.html'
    success_url = reverse_lazy('list:lists')