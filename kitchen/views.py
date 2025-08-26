from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView

from kitchen.forms import (
    CookCreationForm,
    DishForm,
    IngredientSearchForm,
    DishSearchForm,
    CookSearchForm,
)
from kitchen.models import Cook, Dish, DishType, Ingredient
from kitchen.utils import ConfirmDeleteMixin


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "kitchen/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_cooks"] = Cook.objects.count()
        context["num_dishes"] = Dish.objects.count()
        context["num_dish_types"] = DishType.objects.count()
        return context


class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        order_by = self.request.GET.get("order_by", "")

        context["search_form"] = CookSearchForm(initial={"title": username})
        context["current_order"] = order_by
        return context

    def get_queryset(self):
        queryset = Cook.objects.all()
        form = CookSearchForm(self.request.GET)
        if form.is_valid():
            search_term = form.cleaned_data["title"]
            if search_term:
                queryset = queryset.filter(
                    Q(username__icontains=search_term)
                    | Q(first_name__icontains=search_term)
                    | Q(last_name__icontains=search_term)
                )

        order_by = self.request.GET.get("order_by")
        if order_by:
            if order_by == "full_name_asc":
                queryset = queryset.order_by("first_name", "last_name")
            elif order_by == "full_name_desc":
                queryset = queryset.order_by("-first_name", "-last_name")
            elif order_by == "experience_asc":
                queryset = queryset.order_by("years_of_experience")
            elif order_by == "experience_desc":
                queryset = queryset.order_by("-years_of_experience")

        return queryset


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not (self.request.user.is_superuser or self.request.user.is_staff):
            form.fields.pop("is_staff", None)
            form.fields.pop("is_active", None)
        return form

    def get_success_url(self):
        return reverse_lazy(
            "kitchen:cook-detail", kwargs={"pk": self.object.pk}
        )


class CookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Cook
    fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "years_of_experience",
        "is_active",
        "is_staff",
    ]
    template_name = "kitchen/cook_form.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not (self.request.user.is_superuser or self.request.user.is_staff):
            form.fields.pop("is_staff", None)
            form.fields.pop("is_active", None)
        return form

    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        if user.is_superuser and not self.request.user.is_superuser:
            raise PermissionDenied("You cannot edit a superuser.")
        return user

    def get_success_url(self):
        return reverse_lazy(
            "kitchen:cook-detail", kwargs={"pk": self.object.pk}
        )


class CookDeleteView(
    LoginRequiredMixin,
    generic.DeleteView,
    ConfirmDeleteMixin
):
    model = Cook
    template_name = "kitchen/confirm_delete.html"
    success_url = reverse_lazy("kitchen:cook-list")

    def get_object(self, queryset=None):
        user = super().get_object(queryset)

        if user.is_superuser and not self.request.user.is_superuser:
            raise PermissionDenied("You cannot delete a superuser.")

        if user == self.request.user:
            raise PermissionDenied("You cannot delete your own account.")

        return user


class CookPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "kitchen/password_change_form.html"
    success_url = reverse_lazy("kitchen:cook-password-change-done")

    def get_success_url(self):
        return reverse_lazy(
            "kitchen:cook-password-change-done",
            kwargs={"pk": self.request.user.pk}
        )

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != kwargs["pk"] and not request.user.is_superuser:
            raise PermissionDenied(
                "You cannot change another cook's password."
            )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cook"] = Cook.objects.get(pk=self.kwargs["pk"])
        return context


class CookPasswordChangeDoneView(LoginRequiredMixin, TemplateView):
    template_name = "kitchen/password_change_done.html"


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    template_name = "kitchen/dish_type_list.html"
    context_object_name = "dish_type_list"
    paginate_by = 10


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish_type-list")
    template_name = "kitchen/dish_type_form.html"


class DishTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish_type-list")
    template_name = "kitchen/dish_type_form.html"


class DishTypeDeleteView(
    LoginRequiredMixin,
    generic.DeleteView,
    ConfirmDeleteMixin
):
    model = DishType
    template_name = "kitchen/confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish_type-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        order_by = self.request.GET.get("order_by", "")

        context["search_form"] = DishSearchForm(initial={"title": name})
        context["current_order"] = order_by
        return context

    def get_queryset(self):
        queryset = Dish.objects.select_related("dish_type").all()
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            search_term = form.cleaned_data["title"]
            if search_term:
                queryset = queryset.filter(name__icontains=search_term)

        order_by = self.request.GET.get("order_by")
        if order_by:
            if order_by == "dish_type_asc":
                queryset = queryset.order_by("dish_type__name", "name")
            elif order_by == "dish_type_desc":
                queryset = queryset.order_by("-dish_type__name", "name")
            elif order_by == "name_asc":
                queryset = queryset.order_by("name")
            elif order_by == "name_desc":
                queryset = queryset.order_by("-name")
            elif order_by == "price_asc":
                queryset = queryset.order_by("price")
            elif order_by == "price_desc":
                queryset = queryset.order_by("-price")

        return queryset


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    fields = "__all__"


class DishUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm


class DishDeleteView(
    LoginRequiredMixin,
    generic.DeleteView,
    ConfirmDeleteMixin
):
    model = Dish
    template_name = "kitchen/confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-list")


class IngredientListView(LoginRequiredMixin, generic.ListView):
    model = Ingredient
    template_name = "kitchen/ingredient_list.html"
    context_object_name = "ingredient_list"
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = IngredientSearchForm(initial={"title": name})
        return context

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        form = IngredientSearchForm(self.request.GET)
        if form.is_valid():
            search_term = form.cleaned_data["title"]
            if search_term:
                queryset = queryset.filter(name__icontains=search_term)
        return queryset


class IngredientCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("kitchen:ingredient-list")
    template_name = "kitchen/ingredient_type_form.html"


class IngredientUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("kitchen:ingredient-list")
    template_name = "kitchen/ingredient_type_form.html"


class IngredientDeleteView(
    LoginRequiredMixin,
    generic.DeleteView,
    ConfirmDeleteMixin
):
    model = Ingredient
    template_name = "kitchen/confirm_delete.html"
    success_url = reverse_lazy("kitchen:ingredient-list")
