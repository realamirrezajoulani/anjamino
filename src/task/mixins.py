from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin

from task.models import Task

_admin_roles = {'admin', 'super admin'}

class OwnerOrAdminMixin(LoginRequiredMixin):
    """
    Grants access only if the user is an admin/super-admin or owner of the parent List.
    """
    def dispatch(self, request, *args, **kwargs):
        # Determine the Task or List instance
        obj = getattr(self, 'object', None) or self.get_object()
        # If obj is a Task, its parent List is obj.list; if List, obj itself.
        parent_list = obj.list if hasattr(obj, 'list') else obj
        user = request.user
        if getattr(user, 'role', None) in _admin_roles or parent_list.user_id == user.id:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have permission to access this page")

class OwnerOrAdminQuerysetMixin:
    """
    For ListView: admins see all tasks, others see only tasks in their own lists.
    """
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if getattr(user, 'role', None) in _admin_roles:
            return qs
        return qs.filter(list__user=user)

class AssignListMixin:
    """
    Auto-assign the parent List on form_valid.
    """
    def form_valid(self, form):
        form.instance.list = self.list_obj
        return super().form_valid(form)