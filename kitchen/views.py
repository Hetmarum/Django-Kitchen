from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView

from kitchen.forms import CookCreationForm
from kitchen.models import Cook, Dish, DishType


class IndexView(TemplateView):
    template_name = "kitchen/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_cooks"] = Cook.objects.count()
        context["num_dishes"] = Dish.objects.count()
        context["num_dish_types"] = DishType.objects.count()
        return context


class CookListView(generic.ListView):
    model = Cook


class CookDetailView(generic.DetailView):
    model = Cook


class CookCreateView(generic.CreateView):
    model = Cook
    form_class = CookCreationForm


class CookUpdateView(generic.UpdateView):
    model = Cook
    fields = ["username", "first_name", "last_name", "email", "years_of_experience", "is_active"]
    success_url = reverse_lazy("kitchen:cook-detail")
    template_name = "kitchen/cook_form.html"

class CookDeleteView(generic.DeleteView):
    model = Cook
    template_name = "kitchen/cook_confirm_delete.html"
    success_url = reverse_lazy("kitchen:cook-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get("HTTP_REFERER")
        return context
