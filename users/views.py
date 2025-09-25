from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.views.generic import ListView

from users.models import User


class CustomLoginView(LoginView):
    template_name = "users/login.html"


class UserListView(ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"

    def get_queryset(self):
        # Добавим аннотацию количества заявок
        return User.objects.annotate(order_count=Count("driver_orders") + Count("managed_orders")).order_by(
            "-order_count"
        )
