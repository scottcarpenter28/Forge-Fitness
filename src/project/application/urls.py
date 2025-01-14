from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.login, name="login"),
    path("accounts/logout/", views.logout, name="logout"),
    path("create-account/", views.create_account, name="create_account"),
    path("create-routine/", views.create_routine, name="create_routine"),
    path(
        "update-routine/<str:routine_id>/", views.update_routine, name="update_routine"
    ),
    path(
        "delete-routine/<str:routine_id>/", views.delete_routine, name="delete_routine"
    ),
    path("my-routines", views.my_routines, name="my_routines"),
    path("run-routine/<str:routine_id>/", views.run_routine, name="run_routine"),
]
