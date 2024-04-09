from django.db import models
from cloudinary.models import CloudinaryField
# Type choices
STARTER = 'Starter'
ENTREE = 'Entree'
DESSERT = 'Dessert'
DRINK = 'Drink'
TYPE = ((STARTER, "Starter"), (ENTREE, "Entree"), (DESSERT, "Dessert"), (DRINK, "Drink"))
# Create your models here.
class MenuItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    kcal = models.IntegerField()
    type = models.CharField(max_length=15, choices=TYPE, default=STARTER)
    photo = CloudinaryField('image', default='placeholder')
    badge = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name} | {self.type}"