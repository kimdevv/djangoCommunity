from django.db import models

# Create your models here.
class Board(models.Model):
    user = models.IntegerField(null=True)
    nickname = models.CharField(max_length=20, null=True)
    title = models.CharField(max_length=30)
    body = models.TextField(default="")
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    board = models.ForeignKey(Board, null=True, on_delete=models.CASCADE, related_name="comments")
    user = models.IntegerField(null=True)
    nickname = models.CharField(max_length=20, null=True)
    comment = models.TextField(default="")
    created_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.comment