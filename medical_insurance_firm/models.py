from django.db import models


class Firm(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'firm'