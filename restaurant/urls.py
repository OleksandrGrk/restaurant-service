from django.urls import path

from restaurant.views import index, CookerListView

urlpatterns = [
    path("", index, name="index"),
    path("cooks/", CookerListView.as_view(), name="all-cooks")
]

app_name = "restaurant"
