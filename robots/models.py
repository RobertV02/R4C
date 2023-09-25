from django.db import models


class Robot(models.Model):
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(blank=False, null=False)
    def __str__(self):
        return f"{self.model}-{self.version}"

    @property
    def serial(self):
        return f"{self.model}-{self.version}"