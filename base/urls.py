from django.urls import path
from . import views


urlpatterns = [
  path('',views.home, name="home"),
  # path('rooms/',views.rooms, name="rooms")
  path('room/<str:pk>',views.room, name="room"),
  path('create-room/', views.createNewRoom, name="create-room"),
  path('update-room/<str:pk>',views.updateRoom,name="update-room"),
  path('delete-room/<str:pk>',views.deleteRoom,name="delete-room"),
  path('login/',views.logIn,name="login"),
  path('logout/',views.logOut,name="logout")
]