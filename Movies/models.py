from django.db import models

# Create your models here.

Grade = {
	('excellent',1),
	('average',0),
	('bad',-1)
}

class Movie(models.Model):
    name = models.CharField(max_length = 100)
    actor = models.CharField(max_length = 100)
    genre = models.CharField(max_length = 30)
    rating = models.CharField(choices = Grade, default = 'average', max_length = 50)
    
    def __str__(self):
        return self.name