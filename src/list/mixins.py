from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden

_admin_roles = {'admin', 'super admin'}

class OwnerOrAdminMixin(LoginRequiredMixin):
    """
    Grants access only if user is admin/super-admin or owner of the List.
    """
    def dispatch(self, request, *args, **kwargs):
        obj = getattr(self, 'object', None) or self.get_object()
        user = request.user
        if getattr(user, 'role', None) in _admin_roles or obj.user_id == user.id:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have permission to access this page")

class OwnerOrAdminQuerysetMixin:
    """
    For ListView: admins see all lists, non-admins see only their own.
    """
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if getattr(user, 'role', None) in _admin_roles:
            return qs
        return qs.filter(user=user)

class AssignOwnerMixin:
    """
    Auto-assign current user as owner of new List.
    """
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)