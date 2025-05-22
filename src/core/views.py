from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Q
from django.apps import apps

# Create your views here.
class SearchView(LoginRequiredMixin, TemplateView):
    template_name = "core/search_result.html"

    search_models = [
        'list.List',
        'task.Task',
        'subtask.Subtask',
    ]
    
    
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()
        ctx['q'] = query
        results = {}

        if query:
            for model_label in self.search_models:
                Model = apps.get_model(model_label)

                lookup = Q(title__icontains=query)
                qs = Model.objects.filter(lookup)
                if qs.exists():

                    verbose = Model._meta.verbose_name_plural
                    results[verbose] = qs

        ctx['results'] = results
        return ctx