from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class Brand(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=100, unique=True)
    logo = models.ImageField(verbose_name=_("logo"), upload_to="logo/")
    country = CountryField(verbose_name=_("country"))

    class Meta:
        verbose_name = _("brand")
        verbose_name_plural = _("brands")

    def __str__(self):
        return self.name


class Car(models.Model):
    class BodyTypes(models.TextChoices):
        SEDAN = _("Sedan"), _("Sedan")
        LIMOUSINE = _("Limousine"), _("Limousine")
        HATCHBACK = _("Hatchback"), _("Hatchback")
        LIFTBACK = _("Liftback"), _("Liftback")
        STATION_WAGON = _("Station wagon"), _("Station wagon")
        COUPE = _("Coupe"), _("Coupe")
        CONVERTIBLE = _("Convertible"), _("Convertible")
        ROADSTER = _("Roadster"), _("Roadster")
        TARGA = _("Targa"), _("Targa")
        MINIVAN = _("Minivan"), _("Minivan")
        PICKUP = _("Pickup"), _("Pickup")
        CROSSOVER = _("Crossover"), _("Crossover")
        COUPE_CROSSOVER = _("Coupe-crossover"), _("Coupe-crossover")
        COUPE_CONVERTIBLE = _("Coupe-cabriolet"), _("Coupe-cabriolet")
        SPEEDSTER = _("Speedster"), _("Speedster")
        SUV = _("SUV"), _("SUV")

    class Transmissions(models.TextChoices):
        AUTOMATIC = _("Automatic"), _("Automatic")
        MANUAL = _("Manual"), _("Manual")
        SEMI_AUTOMATIC = _("Semi-automatic"), _("Semi-automatic")

    class DriveUnits(models.TextChoices):
        FRONT_WHEEL = _("Front wheel drive"), _("Front wheel drive")
        REAR_WHEEL = _("Rear wheel drive"), _("Rear wheel drive")
        FOUR_WHEEL = _("Four wheel drive"), _("Four wheel drive")

    class EngineTypes(models.TextChoices):
        GASOLINE = _("Gasoline"), _("Gasoline")
        DIESEL = _("Diesel"), _("Diesel")
        HYBRID = _("Hybrid"), _("Hybrid")
        ELECTRIC = _("Electric"), _("Electric")

    car_brand = models.ForeignKey(
        Brand, verbose_name=_("car brand"), on_delete=models.CASCADE
    )
    car_model = models.CharField(verbose_name=_("car model"), max_length=100)
    body_type = models.CharField(
        verbose_name=_("body type"), max_length=50, choices=BodyTypes.choices
    )
    year = models.PositiveIntegerField(verbose_name=_("year of issue"))
    equipment_name = models.CharField(verbose_name=_("equipment name"), max_length=100)
    equipment_description = models.TextField(
        verbose_name=_("equipment description"), blank=True
    )
    transmission = models.CharField(
        verbose_name=_("transmission"), max_length=50, choices=Transmissions.choices
    )
    number_of_gears = models.PositiveSmallIntegerField(
        verbose_name=_("number of gears"),
        validators=(MinValueValidator(4), MaxValueValidator(12)),
    )
    drive_unit = models.CharField(
        verbose_name=_("drive unit"), max_length=50, choices=DriveUnits.choices
    )
    engine_type = models.CharField(
        verbose_name=_("engine's type"), max_length=50, choices=EngineTypes.choices
    )
    working_volume = models.PositiveSmallIntegerField(verbose_name=_("working volume"))
    engine_power = models.PositiveSmallIntegerField(verbose_name=_("engine power"))
    price = models.PositiveIntegerField(verbose_name=_("price"))
    amount = models.PositiveSmallIntegerField(_("amount"))

    class Meta:
        verbose_name = _("car")
        verbose_name_plural = _("cars")

    def __str__(self):
        return f"{self.car_brand} {self.car_model}"


class Photo(models.Model):
    photo = models.ImageField(verbose_name=_("photo"), upload_to="photo/")
    car = models.ForeignKey(Car, verbose_name=_("car"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("photo")
        verbose_name_plural = _("photos")


class CallBack(models.Model):
    full_name = models.CharField(verbose_name=_("full name"), max_length=254)
    phone = PhoneNumberField(verbose_name=_("phone"), region="RU")
    comment = models.TextField(verbose_name=_("comments"), blank=True)

    class Meta:
        verbose_name = _("callback")
        verbose_name_plural = _("callbacks")

    def __str__(self):
        return f"{self.full_name}: {self.phone}"


class Review(models.Model):
    RATING = tuple((i, str(i)) for i in range(1, 6))
    username = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("username"), on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField(_("rating"), choices=RATING)
    text = models.TextField(verbose_name=_("text"))
    date = models.DateTimeField(_("date"), auto_now_add=True)

    class Meta:
        verbose_name = _("review")
        verbose_name_plural = _("reviews")

    def __str__(self):
        return f"{self.username} - {self.rating}"

    def review_len(self):
        return len(self.text)

    def get_name(self):
        if self.username.is_staff:
            return f"{self.username}"
        else:
            return f"{self.username.first_name} {self.username.last_name}"


class TestDrive(models.Model):
    class StatusChoices(models.TextChoices):
        NEW = _("Expect confirmation"), _("Expect confirmation")
        APPROVED = _("Approved"), _("Approved")
        PERFORMED = _("Performed"), _("Performed")

    username = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_("username"), on_delete=models.CASCADE
    )
    phone = PhoneNumberField(verbose_name=_("phone"), region="RU")
    car = models.ForeignKey(Car, verbose_name=_("car"), on_delete=models.CASCADE)
    text = models.TextField(verbose_name=_("text"))
    date = models.DateTimeField(_("date"))
    status = models.CharField(
        verbose_name=_("status"),
        max_length=100,
        choices=StatusChoices.choices,
        default=StatusChoices.NEW,
    )

    class Meta:
        verbose_name = _("test drive")
        verbose_name_plural = _("test drive")

    def __str__(self):
        return f"{self.username} - {self.car}"
