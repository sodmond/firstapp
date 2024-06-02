from django.db import models

# Create your models here.
class User(models.Model):
    username = models.TextField()

    def __str__(self):
        return f"Post by {self.username} at {self.timestamp}"

class Post(models.Model):
    title = models.TextField()
    story = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey("User", on_delete=models.CASCADE)
    #author = models.ForeignKey(User)

    def __str__(self):
        return f"Post by {self.author} at {self.timestamp}"

#class Comment(models.Model)