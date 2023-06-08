from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexRedirectView.as_view()),
    path("cars/", views.cars, name="cars"),
    path("car/<int:pk>/", views.CarDetailView.as_view(), name="car"),
    path("brands/", views.BrandListView.as_view(), name="brands"),
    path("brand/<int:pk>/", views.BrandDetailView.as_view(), name="brand"),
    path("test-drive/<int:pk>", views.test_drive_create, name="test_drive"),
    path("requests/", views.requests, name="requests"),
    path("callback/", views.CallBackCreateView.as_view(), name="callback"),
    path("reviews/", views.reviews, name="reviews"),
    path("contacts/", views.ContactTemplateView.as_view(), name="contacts"),
]
