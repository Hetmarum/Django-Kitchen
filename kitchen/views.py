from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView

from kitchen.forms import CookCreationForm, DishForm
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
    fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "years_of_experience",
        "is_active",
    ]
    template_name = "kitchen/cook_form.html"

    def get_success_url(self):
        return reverse_lazy("kitchen:cook-detail", kwargs={"pk": self.object.pk})


class CookDeleteView(generic.DeleteView):
    model = Cook
    template_name = "kitchen/cook_confirm_delete.html"
    success_url = reverse_lazy("kitchen:cook-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get("HTTP_REFERER")
        return context


class DishTypeListView(generic.ListView):
    model = DishType
    template_name = "kitchen/dish_type_list.html"
    context_object_name = "dish_type_list"


class DishTypeCreateView(generic.CreateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish_type-list")
    template_name = "kitchen/dish_type_form.html"


class DishTypeUpdateView(generic.UpdateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish_type-list")
    template_name = "kitchen/dish_type_form.html"


class DishTypeDeleteView(generic.DeleteView):
    model = DishType
    template_name = "kitchen/dish_type_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish_type-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get("HTTP_REFERER")
        return context


class DishListView(generic.ListView):
    model = Dish


class DishDetailView(generic.DetailView):
    model = Dish


class DishCreateView(generic.CreateView):
    model = Dish
    fields = "__all__"


class DishUpdateView(generic.UpdateView):
    model = Dish
    form_class = DishForm


class DishDeleteView(generic.DeleteView):
    model = Dish
    template_name = "kitchen/dish_confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["previous_url"] = self.request.META.get("HTTP_REFERER")
        return context
