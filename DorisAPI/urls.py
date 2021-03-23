from django.urls import path
from main.views import gen_key
from main.views import get_answer
from main.views import interpretator

urlpatterns = [
    path('api/get_key', gen_key),
    path('api/get_answer', get_answer),
    path('api/interpretator', interpretator),
]
