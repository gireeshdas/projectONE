from django.urls import path
from owner import views
urlpatterns=[
    path("index",views.AdminDashBoardView.as_view(),name="dashboard"),
    path("orders/latest",views.OrdersListView.as_view(),name="neworders"),
    path("orders/details/<int:id>",views.OrdersDetailView.as_view(),name="order-details"),
    path("logout",views.logoutView.as_view(),name="logout")


]