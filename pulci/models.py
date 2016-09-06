from django.db import models

# Create your models here.
class Citation(models.Model):
    """Class to store a citation. """
    text = models.TextField()
    date = models.DateField()
    who = models.CharField(max_length=10,
                           choices = (('V', "větší"),('M', "menší"),('VM', "sestry")))
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.text


