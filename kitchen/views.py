from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin

from kitchen.forms import (
    CookCreationForm,
    DishForm,
    IngredientSearchForm,
    DishSearchForm,
    CookSearchForm,
)
from kitchen.models import Cook, Dish, DishType, Ingredient
from kitchen.utils import ConfirmDeleteMixin, FormTemplateMixin


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
            if "," in order_by:
                fields = [field.strip() for field in order_by.split(",")]
                queryset = queryset.order_by(*fields)
            else:
                queryset = queryset.order_by(order_by)

        return queryset


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = (
        Cook.objects
        .prefetch_related("dishes__dish_type", "dishes__ingredients")
    )


class CookCreateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    FormTemplateMixin,
    generic.CreateView
):
    model = Cook
    form_class = CookCreationForm

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def handle_no_permission(self):
        raise PermissionDenied("You are not allowed to create cooks.")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not (self.request.user.is_superuser or self.request.user.is_staff):
            form.fields.pop("is_staff", None)
            form.fields.pop("is_active", None)
        return form

    def get_success_url(self):
        return reverse_lazy(
            "kitchen:cook-detail",
            kwargs={"pk": self.object.pk}
        )


class CookUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    FormTemplateMixin,
    generic.UpdateView
):
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

    def test_func(self):

        if self.request.user.is_superuser or self.request.user.is_staff:
            return True
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        raise PermissionDenied("You cannot update this cook.")

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
            "kitchen:cook-detail",
            kwargs={"pk": self.object.pk}
        )


class CookDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DeleteView,
    ConfirmDeleteMixin
):
    model = Cook
    template_name = "kitchen/confirm_delete.html"
    success_url = reverse_lazy("kitchen:cook-list")

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def handle_no_permission(self):
        raise PermissionDenied("You are not allowed to delete cooks.")

    def get_object(self, queryset=None):
        user = super().get_object(queryset)

        if user.is_superuser and not self.request.user.is_superuser:
            raise PermissionDenied("You cannot delete a superuser.")

        if user == self.request.user:
            raise PermissionDenied("You cannot delete your own account.")

        return user


class CookPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "registration/password_change_form.html"
    success_url = reverse_lazy("kitchen:cook-password-change-done")

    def get_success_url(self):
        return reverse_lazy(
            "kitchen:cook-password-change-done",
            kwargs={"pk": self.request.user.pk}
        )

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != kwargs["pk"] and not (
            request.user.is_superuser or request.user.is_staff
        ):
            raise PermissionDenied(
                "You cannot change another cook's password."
            )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cook"] = Cook.objects.get(pk=self.kwargs["pk"])
        return context


class CookPasswordChangeDoneView(LoginRequiredMixin, TemplateView):
    template_name = "registration/password_change_done.html"


class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    template_name = "kitchen/dish_type_list.html"
    context_object_name = "dish_type_list"
    paginate_by = 10


class DishTypeCreateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    FormTemplateMixin,
    generic.CreateView
):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish_type-list")

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def handle_no_permission(self):
        raise PermissionDenied("You are not allowed to create cooks.")


class DishTypeUpdateView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    FormTemplateMixin,
    generic.UpdateView
):
    model = DishType
    fields = "__all__"
    success_url = reverse_lazy("kitchen:dish_type-list")

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def handle_no_permission(self):
        raise PermissionDenied("You cannot update dish types.")


class DishTypeDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DeleteView,
    ConfirmDeleteMixin
):
    model = DishType
    template_name = "kitchen/confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish_type-list")

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def handle_no_permission(self):
        raise PermissionDenied("You are not allowed to delete dish types.")


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
            if "," in order_by:
                fields = [field.strip() for field in order_by.split(",")]
                queryset = queryset.order_by(*fields)
            else:
                queryset = queryset.order_by(order_by)

        return queryset


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish
    queryset = (
        Dish.objects
        .select_related("dish_type")
        .prefetch_related("cooks", "ingredients")
    )


class DishCreateView(
    LoginRequiredMixin,
    FormTemplateMixin,
    generic.CreateView
):
    model = Dish
    form_class = DishForm
    multipart = True
    extra_scripts = """
        <script>
            $("#id_dish_type").select2();
            $("#id_cooks").select2();
            $("#id_ingredients").select2();
        </script>
    """


class DishUpdateView(
    LoginRequiredMixin,
    FormTemplateMixin,
    generic.UpdateView
):
    model = Dish
    form_class = DishForm
    multipart = True
    extra_scripts = """
        <script>
            $("#id_dish_type").select2();
            $("#id_cooks").select2();
            $("#id_ingredients").select2();
        </script>
    """


class DishDeleteView(
    LoginRequiredMixin,
    UserPassesTestMixin,
    generic.DeleteView,
    ConfirmDeleteMixin
):
    model = Dish
    template_name = "kitchen/confirm_delete.html"
    success_url = reverse_lazy("kitchen:dish-list")

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

    def handle_no_permission(self):
        raise PermissionDenied("You are not allowed to delete dishes.")


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


class IngredientCreateView(
    LoginRequiredMixin,
    FormTemplateMixin,
    generic.CreateView
):
    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("kitchen:ingredient-list")


class IngredientUpdateView(
    LoginRequiredMixin,
    FormTemplateMixin,
    generic.UpdateView
):
    model = Ingredient
    fields = "__all__"
    success_url = reverse_lazy("kitchen:ingredient-list")


class IngredientDeleteView(
    LoginRequiredMixin,
    generic.DeleteView,
    ConfirmDeleteMixin
):
    model = Ingredient
    template_name = "kitchen/confirm_delete.html"
    success_url = reverse_lazy("kitchen:ingredient-list")
