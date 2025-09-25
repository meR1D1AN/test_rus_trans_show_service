from django.urls import path

from transport_app.apps import TransportAppConfig
from transport_app.views import (
    LocationCreateView,
    LocationDeleteView,
    LocationDetailView,
    LocationListView,
    LocationUpdateView,
    OrderCreateView,
    OrderDeleteView,
    OrderDetailView,
    OrderListView,
    OrderUpdateView,
    accept_order,
    complete_order,
    upload_document,
)

app_name = TransportAppConfig.name

urlpatterns = [
    path(
        "orders/",
        OrderListView.as_view(),
        name="order_list",
    ),
    path(
        "orders/create/",
        OrderCreateView.as_view(),
        name="order_create",
    ),
    path(
        "orders/<int:pk>/",
        OrderDetailView.as_view(),
        name="order_detail",
    ),
    path(
        "orders/<int:pk>/update/",
        OrderUpdateView.as_view(),
        name="order_update",
    ),
    path(
        "orders/<int:pk>/delete/",
        OrderDeleteView.as_view(),
        name="order_delete",
    ),
    path(
        "<int:pk>/upload_document/",
        upload_document,
        name="upload_document",
    ),
    path(
        "locations/",
        LocationListView.as_view(),
        name="location_list",
    ),
    path(
        "locations/create/",
        LocationCreateView.as_view(),
        name="location_create",
    ),
    path(
        "locations/<int:pk>/",
        LocationDetailView.as_view(),
        name="location_detail",
    ),
    path(
        "locations/<int:pk>/update/",
        LocationUpdateView.as_view(),
        name="location_update",
    ),
    path(
        "locations/<int:pk>/delete/",
        LocationDeleteView.as_view(),
        name="location_delete",
    ),
    path(
        "orders/<int:pk>/accept/",
        accept_order,
        name="accept_order",
    ),
    path(
        "orders/<int:pk>/complete/",
        complete_order,
        name="complete_order",
    ),
]
