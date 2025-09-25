from django.urls import path
from django.contrib.auth.views import LogoutView
from chat.views import CustomLoginView, signup_view

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', signup_view, name='signup'),
]