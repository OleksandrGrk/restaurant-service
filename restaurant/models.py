from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Cooker(AbstractUser):
    years_of_experience = models.IntegerField(null=True)

    class Meta:
        ordering = ["username"]

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("restaurant:cook-detail", kwargs={"pk": self.pk})


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE, related_name="dishes")
    cooks = models.ManyToManyField(Cooker, related_name="dishes")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
