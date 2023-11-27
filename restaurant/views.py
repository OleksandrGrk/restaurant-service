from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from restaurant.forms import CookerCreationForm, DishCreationForm, DishTypeCreationForm, CookerSearchForm, \
    DishSearchForm, CookerDishesUpdateForm, DishUpdateForm
from restaurant.models import Dish, Cooker, DishType


class index(generic.ListView):
    model = Cooker
    template_name = "restaurant/index.html"

    def get_context_data(self, **kwargs):
        context = super(index, self).get_context_data(**kwargs)
        context["num_dishes"] = Dish.objects.count()
        context["num_cooks"] = Cooker.objects.count()
        context["num_dish_types"] = DishType.objects.count()

        return context


class CookerListView(LoginRequiredMixin, generic.ListView):
    model = Cooker
    paginate_by = 2
    template_name = "restaurant/cook_list.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CookerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = CookerSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        queryset = Cooker.objects.all()
        form = CookerSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset


class CookerDetailView(generic.DetailView):
    model = Cooker
    template_name = "restaurant/cook_detail.html"


class CookerCreationView(LoginRequiredMixin, generic.CreateView):
    model = Cooker
    form_class = CookerCreationForm
    template_name = "restaurant/cook_create.html"
    success_url = reverse_lazy("restaurant:index")


class DishListView(generic.ListView):
    model = Dish
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Dish.objects.all()
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class DishDetailView(generic.DetailView):
    model = Dish


class DishCreateView(LoginRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishCreationForm
    template_name = "restaurant/dish_create.html"
    success_url = reverse_lazy("restaurant:index")


class DishTypeListView(generic.ListView):
    model = DishType
    template_name = "restaurant/dish_type_list.html"
    context_object_name = "dish_type_list"
    paginate_by = 8


class DishTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = DishType
    form_class = DishTypeCreationForm
    template_name = "restaurant/dish_type_create.html"
    success_url = reverse_lazy("restaurant:index")


class CookerUpdateView(generic.UpdateView):
    model = Cooker
    form_class = CookerDishesUpdateForm
    template_name = "restaurant/cook_update.html"
    success_url = reverse_lazy("restaurant:cook-list")


class DishUpdateView(generic.UpdateView):
    model = Dish
    form_class = DishUpdateForm
    template_name = "restaurant/dish_update.html"
    success_url = reverse_lazy("restaurant:dish-list")

