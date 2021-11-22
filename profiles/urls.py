from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views
from profiles import views
from profiles.api.serializers import AccountSerializer

app_name = "profiles"

urlpatterns = [
    path("<str:username>/", views.ProfileDetailView.as_view(), name="detail"),
    path("<str:username>/follow/", views.FollowView.as_view(), name="follow"),
    # path("<str:username>/manage/", views.ManageUserView.as_view(), name="manage"),
    # path("api/<pk>/account/", views.AccountDetail.as_view(), name="account"),
    # path("api/<str:username>/account/edit/", views.AccountEditView.as_view(), name="edit"),
    path("api/<pk>/account/edit/", views.AccountInfoUpdateView.as_view(), name="edit"),
    # path("api/create/", views.AccountCreate.as_view(), name="create"),
    # path("user/add/", AccountCreateView.as_view(), name="user-add"),
    # path(">str:username>/<int:pk>/", AccountUpdateView.as_view(), name="user-update"),
    # path(">str:username>/<int:pk>/delete", AccountDeleteView.as_view(), name="user-delete"),
]
