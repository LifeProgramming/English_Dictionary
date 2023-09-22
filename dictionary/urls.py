from django.urls import path
from . import views

urlpatterns=[
    path('login', views.loginUser, name='login'),
    path('login_completed',views.loginCompleted, name='loginCompleted' ),
    path('', views.index, name='index' ),
    path('logout', views.logoutUser, name='logout' ),
    path('register', views.registerUser, name='register' ),
    path('register', views.registerUser, name='register' ),
    path('register_completed', views.registerCompleted, name='registerCompleted' ),
    path('word', views.word, name='word'),
    path('personal-dictionary', views.PerDictView, name='personal-dictionary'),
    path('personal-dictionary/delete/<int:pk>', views.delete, name='delete-word'),
]