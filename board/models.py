from django.db import models


# Create your models here.

class Event(models.Model):
    class Meta:
        verbose_name = "事件"
        verbose_name_plural = "事件"
        index_together = [
            ['event_type', 'created_at'],
            ['created_at', 'vote']
        ]

    title = models.CharField(max_length=32, verbose_name="标题")
    content = models.TextField(default='', verbose_name="正文")
    event_type = models.SmallIntegerField(default=0)  # 0 Red 1 Black
    vote = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)


class Vote(models.Model):
    class Meta:
        verbose_name = "投票"
        verbose_name_plural = "投票"
        index_together = [
            ['event_id', 'vote'],
            ['event_id', 'created_at']
        ]

    event_id = models.IntegerField(null=False)
    vote = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
