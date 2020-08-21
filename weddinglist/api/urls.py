from django.urls import path
from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from . import views

app_name = 'api'

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('gift/', views.GiftViewSet.as_view(), name='gift_list'),
    path('gift/<pk>', views.GiftDetailView.as_view(), name='gift_detail'),
    path('gift_list/', views.GiftListsView.as_view(), name='gift_lists'),
    path('gift_list/<pk>', views.GiftListDetailView.as_view(), name='gift_list_detail'),
    path('gift_list/<pk>/purchase/<int:gift_id>', views.PurchaseGiftView.as_view(), name='gift_purchase'),
    path('gift_list/<int:giftlist_id>/pdf/',
         views.GiftListPdfView.as_view(),
         name='gift_list_pdf'),
]
