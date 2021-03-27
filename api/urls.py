from django.urls import path, include

from .views import TodoCompletedList, TodoListCreate, TodoRetrieveUpdateDestroyAPIView, TodoComplete, signup, login

urlpatterns = [
    path('todos/', TodoListCreate.as_view()),
    path('todos/<int:pk>/', TodoRetrieveUpdateDestroyAPIView.as_view()),
    path('todos/<int:pk>/complete', TodoComplete.as_view()),
    path('todos/completed', TodoCompletedList.as_view()),

    path('signup/', signup),
    path('login/', login)

]