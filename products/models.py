from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    title = models.CharField(max_length=250)
    pub_date = models.DateTimeField()
    body = models.TextField()
    url = models.TextField()
    image = models.ImageField(upload_to='images/')
    icon = models.ImageField(upload_to='images/', blank=True)
    votes_total = models.IntegerField(default=1)
    hunter = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def pretty_pub_date(self):
        return self.pub_date.strftime('%B %e, %Y')

    def summary(self):
        # body = str(self.body)
        # summ = body.find('[\.\!\?]')
        # summ += 1
        return self.body[:200]


