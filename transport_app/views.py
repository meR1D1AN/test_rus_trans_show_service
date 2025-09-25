from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from conts.choices import OrderChoices, RoleChoices

from .forms import DocumentForm, LocationForm, OrderForm
from .models import Location, Order


class ManagerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.role == RoleChoices.MANAGER
            or self.request.user.role == RoleChoices.ADMIN
        )


class OrderCreateView(LoginRequiredMixin, ManagerRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = "transport_app/order_form.html"
    success_url = reverse_lazy("transport_app:order_list")

    def form_valid(self, form):
        form.instance.manager = self.request.user
        return super().form_valid(form)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "transport_app/order_list.html"
    context_object_name = "orders"
    paginate_by = 50

    def get_queryset(self):
        user = self.request.user
        if user.role == RoleChoices.MANAGER:
            return Order.objects.filter(manager=user)
        if user.role == RoleChoices.DRIVER:
            return Order.objects.filter(driver=user)
        if user.role == RoleChoices.ADMIN:
            return Order.objects.all()
        return Order.objects.none()


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "transport_app/order_detail.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["document_form"] = DocumentForm()
        ctx["is_driver"] = self.request.user.role == RoleChoices.DRIVER
        return ctx


class OrderUpdateView(LoginRequiredMixin, ManagerRequiredMixin, UpdateView):
    model = Order
    template_name = "transport_app/order_form.html"
    form_class = OrderForm


class OrderDeleteView(LoginRequiredMixin, ManagerRequiredMixin, DeleteView):
    model = Order
    template_name = "transport_app/order_confirm_delete.html"


@login_required
@require_http_methods(["POST"])
def upload_document(request, pk):
    order = get_object_or_404(Order, pk=pk)
    form = DocumentForm(request.POST, request.FILES)
    if form.is_valid():
        doc = form.save(commit=False)
        doc.order = order
        doc.save()
        return redirect("transport_app:order_detail", pk=pk)
    return render(
        request,
        "transport_app/order_detail.html",
        {"order": order, "form": form},
        status=400,
    )


class BaseLocationListView(LoginRequiredMixin):
    model = Location


class LocationListView(BaseLocationListView, ListView):
    template_name = "transport_app/location_list.html"
    context_object_name = "locations"
    paginate_by = 50


class LocationDetailView(BaseLocationListView, DetailView):
    template_name = "transport_app/location_detail.html"
    context_object_name = "location"


class LocationCreateView(BaseLocationListView, CreateView):
    form_class = LocationForm
    template_name = "transport_app/location_form.html"
    success_url = reverse_lazy("transport_app:location_list")

    def form_valid(self, form):
        form.instance.driver = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("transport_app:location_list")


class LocationUpdateView(BaseLocationListView, UpdateView):
    form_class = LocationForm
    template_name = "transport_app/location_form.html"
    success_url = reverse_lazy("transport_app:location_list")


class LocationDeleteView(BaseLocationListView, DeleteView):
    template_name = "transport_app/location_confirm_delete.html"
    success_url = reverse_lazy("transport_app:location_list")


@login_required
def accept_order(request, pk):
    order = get_object_or_404(Order, pk=pk, driver=request.user)
    if order.status == OrderChoices.ASSIGNED:
        order.status = OrderChoices.IN_PROGRESS
        order.save()
    return redirect("transport_app:order_list")


@login_required
def complete_order(request, pk):
    order = get_object_or_404(Order, pk=pk, driver=request.user)
    if order.status == OrderChoices.IN_PROGRESS:
        order.status = OrderChoices.COMPLETED
        order.save()
    return redirect("transport_app:order_list")
