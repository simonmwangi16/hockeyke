from django.db import models


class Standings(models.Model):
    class Meta:
        managed = False
        verbose_name = "Standings"
        verbose_name_plural = "Standings"