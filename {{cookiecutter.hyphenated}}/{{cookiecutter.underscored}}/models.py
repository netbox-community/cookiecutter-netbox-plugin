from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel


class {{ cookiecutter.__model_name }}(NetBoxModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "{{ cookiecutter.__model_name }}s"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:{{ cookiecutter.underscored }}:{{ cookiecutter.__model_name|lower }}", args=[self.pk])
