from django import forms
from django.contrib.auth.forms import UserCreationForm

from restaurant.models import Cooker


class CookerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cooker
        fields = UserCreationForm.Meta.fields + ("years_of_experience",)



