from django.urls import path

from . import views
from profiles.views import ManageUserView

app_name = "profiles"

urlpatterns = [
    path("<str:username>/", views.ProfileDetailView.as_view(), name="detail"),
    path("<str:username>/follow/", views.FollowView.as_view(), name="follow"),
    path("<str:username>/manage/", views.ManageUserView.as_view(), name="manage")
    # path("user/add/", AccountCreateView.as_view(), name="user-add"),
    # path(">str:username>/<int:pk>/", AccountUpdateView.as_view(), name="user-update"),
    # path(">str:username>/<int:pk>/delete", AccountDeleteView.as_view(), name="user-delete"),
]
