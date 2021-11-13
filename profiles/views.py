from django.contrib.auth.models import User
from django.http.response import HttpResponseBadRequest
from django.views.generic import DetailView, View
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse, HttpResponseBadRequest
from django.urls import reverse_lazy

from feed.models import Post
from followers.models import Follower
# from profiles.forms import AccountForm
from profiles.models import User, create_user_profile


'''
GET
'''
class ProfileDetailView(DetailView):
    http_method_names = ["get"]
    template_name = "profiles/detail.html"
    model = User
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username"

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        user = self.get_object()
        context = super().get_context_data(**kwargs)
        context["total_posts"] = Post.objects.filter(author=user).count()
        # Final project TODO: Added total followers to profiles
        context["total_followers"] = Follower.objects.filter(following=user).count()
        if self.request.user.is_authenticated:
            context["you_follow"] = Follower.objects.filter(following=user, followed_by=self.request.user).exists()
        return context


'''
API View
'''
class FollowView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()

        if "action" not in data or "username" not in data:
            return HttpResponseBadRequest("Missing data")

        try:
            other_user = User.objects.get(username=data["username"])
        except User.DoesNotExist:
            return HttpResponseBadRequest("Missing user")

        if data["action"] == "follow":
            # follow
            follower, created = Follower.objects.get_or_create(
                followed_by=request.user,
                following=other_user,
            )
        else:
            # unfollow
            try:
                follower = Follower.objects.get(
                    followed_by=request.user,
                    following=other_user,
                )
            except Follower.DoesNotExist:
                follower = None

            if follower:
                follower.delete()
        
        return JsonResponse({
            'success': True,
            "wording": "Unfollow" if data["action"] == "follow" else "Follow"
        })


'''
GET - display account information (only if logged in as that specific user)
'''
class AccountView(DetailView):
    pass


'''
TODO: Change to POST method to update account only (change view name too - UpdateAccountView)

API View
'''
class ManageUserView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    http_method_names = ["get", "post"]
    template_name = "profiles/manageprofile.html"
    model = User
    context_object_name = "user"
    slug_field = "username"
    slug_url_kwarg = "username"
    success_url = "../../{username}/profile"
    success_message = "Your profile has been successfully updated"
    fields = ["username", "first_name", "last_name", "email", 'password']

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        obj = form.save(commit=False)
        form.send_email()
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        return self.get_success_message % dict(
            cleaned_data,
            calculated_field=self.object.calculated_field,
        )

    def get_success_url(self):
        return reverse_lazy("detail", kwargs={"username": self.request.user.username})


'''
TODO: Similar to manage but create a new user instead - POST only
API View
'''
# class AccountCreateView(CreateView):
#     http_method_names = ["get", "post"]
#     template_name = "profiles/createprofile.html"
#     model = User
#     context_object_name = "user"
#     slug_field = "username"
#     slug_url_kwarg = "username"
#     success_url = "../../{username}/profile"
#     success_message = "Your profile has been successfully created"
#     fields = ["username", "first_name", "last_name", "email", "password"]


'''
TODO: Delete request for users to remove their accounts from the site
API View
'''
# class AccountDeleteView(DeleteView):
#     model = User
#     success_url = reverse_lazy("user-list")
