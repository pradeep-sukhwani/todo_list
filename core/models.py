# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django_extensions.db.models import TimeStampedModel, models
from django_extensions.db.fields import AutoSlugField


STATE_CHOICES = (
    ('pending', 'Pending'),
    ('completed', 'Completed'),
)

TASK_TYPE = (
    ('parent', 'Parent'),
    ('child', 'Child'),
)


class Task(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField("Title", max_length=255, unique=True, db_index=True)
    description = models.TextField("Description", blank=True, null=True)
    state = models.CharField("State", choices=STATE_CHOICES, max_length=10, default='pending')
    due_date = models.DateTimeField("Due Date", blank=True, null=True)
    slug = AutoSlugField(populate_from='title')
    sub_task = models.ManyToManyField("self", blank=True, null=True, help_text="This is for sub task")
    task_type = models.CharField("Task Type", choices=TASK_TYPE, max_length=11, default='parent',
                                 help_text='This is used to differentiate if the task is sub-task then it will be '
                                           'changed child.')
    set_alert = models.PositiveSmallIntegerField(default=0, blank=True, null=True,
                                                 help_text="This is used for alert message. If you want to trigger "
                                                           "alert before due date then only set this.")

    class Meta:
        ordering = ("due_date",)

    def __str__(self):
        return u"{title}_{id}".format(title=self.slug, id=self.id)

    def save(self, **kwargs):
        if self.sub_task:
            self.task_type = 'child'
        super(Task, self).save(**kwargs)
