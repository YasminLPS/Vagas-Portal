from django.urls import path
from .views import login_view,registrar, vagas_lista, criar_vaga

urlpatterns = [
    path('login/', login_view, name='login'),
    path('registrar/', registrar, name='registrar'),
    path('', vagas_lista, name='vagas_lista'),
    path('criar/', criar_vaga, name='criar_vaga'),

]
