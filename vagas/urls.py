from django.urls import path
from .views import login_view,registrar, vagas_lista

urlpatterns = [
    path('login/', login_view, name='login'),
    path('registrar/', registrar, name='registrar'),
    path('', vagas_lista, name='vagas_lista'),
]
