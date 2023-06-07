from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext as _
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from cars import forms, models
from users.type import Request


class IndexRedirectView(RedirectView):
    url = "cars"


def cars(request: HttpRequest) -> HttpResponse:
    cars: QuerySet[models.Car]
    if "q" in request.GET:
        form = forms.PostSearchForm(request.GET)
        if form.is_valid():
            vector = SearchVector(
                "car_brand__name",
                "car_model",
                "car_brand__country",
                "body_type",
                "equipment_name",
                "year",
            )
            cars = (
                models.Car.objects.annotate(search=vector)
                .filter(amount__gt=0)
                .filter(search=form.cleaned_data["q"])
            )
    else:
        form = forms.PostSearchForm()
        cars = models.Car.objects.filter(amount__gt=0)
    context = {"cars": cars, "form": form}
    return render(request, "cars/cars.html", context)


class CarDetailView(DetailView):
    model = models.Car
    template_name = "cars/car_detail.html"


class BrandListView(ListView):
    model = models.Brand
    template_name = "cars/brands.html"


class BrandDetailView(DetailView):
    model = models.Brand
    template_name = "cars/brand_detail.html"


class CallBackCreateView(CreateView):
    form_class = forms.CallBackForm
    template_name = "cars/callback.html"
    success_url = "/callback/"

    def form_valid(self, form):
        messages.success(self.request, _("Callback has been left, expect a call"))
        return super().form_valid(form)


def reviews(request: HttpRequest) -> HttpResponse:
    form = forms.ReviewForm()
    if request.method == "POST":
        form = forms.ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.username = request.user
            review.save()
            messages.success(
                request, _("Review was successfully posted on the website")
            )
            form = forms.ReviewForm()
    paginator = Paginator(models.Review.objects.all().order_by("-date"), 3)
    try:
        page_number = int(request.GET["page"])
    except (KeyError, ValueError):
        page_number = 1
    else:
        if page_number < 1:
            page_number = 1
        elif page_number > paginator.num_pages:
            page_number = paginator.num_pages
    reviews = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(
        number=page_number, on_each_side=1, on_ends=1
    )
    context = {
        "form": form,
        "reviews": reviews,
        "page_range": page_range,
    }
    return render(request, "cars/reviews.html", context)


class ContactTemplateView(TemplateView):
    template_name = "cars/contacts.html"


class TestDriveCreateView(CreateView):
    model = models.TestDrive
    fields = "__all__"
    template_name = "cars/test_drive.html"
    success_url = "/cars/"


@login_required
def requests(request: Request) -> HttpResponse:
    requests = (
        models.TestDrive.objects.filter(username=request.user)
        .filter(
            date__gte=f"{datetime.today().year}-{datetime.today().month}-{datetime.today().day}"
        )
        .exclude(status=_("Performed"))
        .order_by("date")
    )
    context = {"requests": requests}
    return render(request, "cars/requests.html", context)
