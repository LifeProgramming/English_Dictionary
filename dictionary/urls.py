from django.urls import path
from . import views

urlpatterns=[
    path('', views.index, name='index' ),
    path('word', views.word, name='word'),
    path('personal-dictionary', views.PerDictView, name='personal-dictionary'),
    path('personal-dictionary/delete/<int:pk>', views.delete, name='delete-word'),
]