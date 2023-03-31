from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=30, blank=True, primary_key=True)
    description = models.CharField(max_length=150, blank=True, null=True)
    extract_html = models.CharField(max_length=2500, blank=True, null=True)
    thumbnail_url = models.CharField(max_length=600, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'authors'

    def __str__(self):
        return self.name