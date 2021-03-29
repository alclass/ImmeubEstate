from django.urls import path

from . import views

app_name = 'realestateleasedjangoapp'
urlpatterns = [
  # path('', views.IndexView.as_view(), name='index'),
  path('', views.bankaccounks_listing, name='index'),
  path('cobrancas/', views.cobrancas, name='cobrancasroute'),
  path('cobranca/<int:year>/<int:month>/<int:contract_id>/', views.cobranca, name='cobrancaroute'),
]
'''
path('<int:pk>/', views.DetailView.as_view(), name='detail'),
path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
path('<int:question_id>/vote/', views.vote, name='vote'),
'''
