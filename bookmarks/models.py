from django.db import models

# Create your models here.
class Bookmark(models.Model):

        title = models.CharField(max_length=100)
        url = models.URLField()
        description = models.TextField()
        category = models.CharField(max_length=10,
                                    choices = (("D", "Děti"), ("T", "Tvoření"))
                                    )
        date = models.DateField()

        def __str__(self):
            return self.title
