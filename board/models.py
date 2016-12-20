from django.db import models
from user.models import User


# Create your models here.

class Event(models.Model):
    class Meta:
        verbose_name = "事件"
        verbose_name_plural = "事件"
        index_together = [
            ['event_type', 'created_at'],
            ['created_at', 'vote_count']
        ]

    title = models.CharField(max_length=32, verbose_name="标题")
    content = models.TextField(default='', verbose_name="正文")
    author = models.ForeignKey(User, related_name='events', on_delete=models.CASCADE, blank=None, null=True)
    event_type = models.SmallIntegerField(default=0)  # 0 Red 1 Black
    vote_count = models.IntegerField(default=0)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)


class Vote(models.Model):
    class Meta:
        verbose_name = "投票"
        verbose_name_plural = "投票"
        index_together = [
            ['event', 'vote'],
            ['event', 'created_at']
        ]
        unique_together = (
            ('event', 'author')
        )

    VOTE_CHOICE = [-1, 0, 1]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    vote = models.SmallIntegerField(default=1)
    author = models.ForeignKey(User, related_name='votes', on_delete=models.CASCADE, blank=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Vote {} on {}: {}>".format(self.author, self.event, self.vote)
