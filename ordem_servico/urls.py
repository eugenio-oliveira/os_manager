from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_ordens, name='lista_ordens'),
    path('nova/', views.criar_ordem, name='criar_ordem'),
    path('editar/<int:ordem_id>/', views.editar_ordem, name='editar_ordem'),
    path('buscar-clientes/', views.buscar_clientes_ajax, name='buscar_clientes_ajax'),
    path('criar-cliente/', views.criar_cliente_ajax, name='criar_cliente_ajax'),
    path('detalhe/<int:ordem_id>/', views.detalhar_ordem, name='detalhar_ordem'),

]
