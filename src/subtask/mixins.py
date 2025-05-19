from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin

from subtask.models import Subtask
from task.models import Task


_admin_roles = {'admin', 'super admin'}

class OwnerOrAdminMixin:
    """
    Allows access only if the user is admin/super-admin or owner of the parent List.
    """
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        # Determine parent list
        if hasattr(self, 'task_obj'):
            parent_list = self.task_obj.list
        else:
            obj = self.get_object()
            parent_list = obj.task.list

        if getattr(user, 'role', None) in _admin_roles or parent_list.user_id == user.id:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have permission to access this page")