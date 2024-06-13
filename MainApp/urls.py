from django.urls import path
from . import views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    
    path("api/menu-items", views.MenuItemsView, name="menu-items"),

    path("index/", views.IndexView, name="index"),
    path("login/", views.LoginView, name="login"),
    path("register/", views.RegisterView, name="register"),
    path("member-list/", views.MemberListView, name="member-list"),
    
    path("update-member-role/<int:pk>/<str:role>", views.MemberListUpdateRole, name="update-member-role"),



    path("member-view/", views.MemberView, name = "memer-view"),
    
    path("order-list/", views.OrderView.as_view(), name = 'order-list'),
    
    path("api-order/", views.APIOrderView.as_view(), name = 'API-order'),
    path("api-login/", obtain_auth_token, name="api-login"),
   
    # path("login/", views.RegisterView, name = 'login'),
    # path("api/update/<int:pk>", views.UpdateOrderView.as_view(), name = 'get-post-delete'),
    
   
]
