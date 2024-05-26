from django.urls import path

from companies.views.employees import Employees, EmployeeDetail
from companies.views.permissions import PermissionDetail
from companies.views.groups import Groups, GroupDetail
from companies.views.tasks import Tasks, TaskDetail
from companies.views.clients import Clients, ClientDetail
from companies.views.products import Products, ProductDetail 
from companies.views.nfe import EmitirNFeView, ConsultarNFeView, CancelarNFeView, EnviarNFePendenteView, ListarNFePendentesView, ListarTodasNFeView, ConsultarStatusNFeView, GerarDanfeView


urlpatterns = [
    # Employees Endpoints
    path('employees', Employees.as_view()),
    path('employees/<int:employee_id>', EmployeeDetail.as_view()),

    # Groups And Permissions Endpoints
    path('groups', Groups.as_view()),
    path('groups/<int:group_id>', GroupDetail.as_view()),
    path('permissions', PermissionDetail.as_view()),

    # Tasks Endpoints
    path('tasks', Tasks.as_view()),
    path('tasks/<int:task_id>', TaskDetail.as_view()),
    
     # Clients Endpoints
    path('clients', Clients.as_view()),
    path('clients/<int:client_id>', ClientDetail.as_view()),
    
    # Products Endpoints
    path('products', Products.as_view()),
    path('products/<int:product_id>', ProductDetail.as_view()),
    
    # NFe Endpoints
    path('nfe/emitir', EmitirNFeView.as_view(), name='emitir-nfe'),
    path('nfe/consultar/<str:chave>', ConsultarNFeView.as_view(), name='consultar-nfe'),
    path('nfe/cancelar/<str:chave>', CancelarNFeView.as_view(), name='cancelar-nfe'),
    path('nfe/enviar_pendentes', EnviarNFePendenteView.as_view(), name='enviar-nfe-pendentes'),
    path('nfe/pendentes', ListarNFePendentesView.as_view(), name='listar-nfe-pendentes'),
    path('nfe/consultar', ListarTodasNFeView.as_view(), name='listar-todas-nfe'),
    path('nfe/consultar_status/<str:chave>/', ConsultarStatusNFeView.as_view(), name='consultar_status_nfe'),
    path('nfe/danfe/<str:chave_acesso>/', GerarDanfeView.as_view(), name='gerar_danfe'),
    
]
