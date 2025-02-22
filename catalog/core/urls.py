from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet, ReviewViewSet, home, item_detail, register_view, login_view, logout_view, user_list_items
from . import views


router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('api/', include(router.urls)),
    path('item/<int:item_id>', item_detail, name='item_detail'),
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('profile/', user_list_items, name='user_list_items'),
    path('item/<int:item_id>/update-status/', views.update_item_status, name='update_item_status'),
]
