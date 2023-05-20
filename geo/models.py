from django.db import models


class Location(models.Model):
    class Meta:
        db_table = "location"

    name = models.CharField(max_length=100, null=True, blank=True)


class Area(models.Model):
    class Meta:
        db_table = "area"

    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=True)
