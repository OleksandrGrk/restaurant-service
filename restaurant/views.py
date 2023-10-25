from django.shortcuts import render
from django.views import generic

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
    template_name = "restaurant/cooks-list.html"

