from django.urls import path, include
from .views import *

urlpatterns = [
    path('signUp/', RegistrationView.as_view(), name='registration'),
    path('logIn/', CustomLoginView.as_view(), name='logIn'),
    path('contact/', ContactListView.as_view(), name='contact'),
    path('contact/<int:pk>/', ContactDetailView.as_view(), name='contacts-detail'),
    path('user-profile/', UserProfileListView.as_view(), name='user-profiles'),
    path('user-profile/<int:pk>/', UserProfileDetailView.as_view(), name='user-profile'),
    path('user-profile/<int:pk>/contact/', ContactsOfUserListView.as_view()),
    path('task/', TaskListView.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('user-profile/<int:pk>/task/', TasksOfUserListView.as_view()),
    path('subtask/', SubtaskListView.as_view(), name='tasks'),

]