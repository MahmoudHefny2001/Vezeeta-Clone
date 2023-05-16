from django.db import models


class Firm(models.Model):
    name = models.CharField(max_length=200)