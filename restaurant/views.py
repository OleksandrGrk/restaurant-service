from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from restaurant.forms import CookerCreationForm
from restaurant.models import Dish, Cooker, DishType


def index(request):
    num_dishes = Dish.objects.count()
    num_cooks = Cooker.objects.count()
    num_dish_types = DishType.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_dishes": num_dishes,
        "num_cooks": num_cooks,
        "num_dish_types": num_dish_types,
        "num_visits": num_visits + 1
    }
    return render(request, template_name="restaurant/index.html", context=context)


class CookerListView(generic.ListView):
    model = Cooker
    paginate_by = 5
    template_name = "restaurant/cook_list.html"


class CookerDetailView(generic.DetailView):
    model = Cooker
    template_name = "restaurant/cook_detail.html"


class CookerCreationView(generic.CreateView):
    model = Cooker
    form_class = CookerCreationForm
    template_name = "restaurant/cook_create.html"


class DishListView(generic.ListView):
    model = Dish


class DishDetailView(generic.DetailView):
    model = Dish


class DishTypeListView(generic.ListView):
    model = DishType
    template_name = "restaurant/dish_type_list.html"
    context_object_name = "dish_type_list"
