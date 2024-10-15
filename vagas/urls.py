from django.urls import path
from .views import login_view,registrar

urlpatterns = [
    path('login/', login_view, name='login'),
    path('registrar/', registrar, name='registrar'),
]
