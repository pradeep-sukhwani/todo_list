# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

import pytest
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.urls import reverse
from requests import get, post
from django.conf import settings

from core.models import Task


class TestMyView(object):

    def create_user(self):
        user = User.objects.create(username="testuser", email="testuser@test.com", password="django123")
        return user

    def create_task(self):
        task = Task.objects.create(title="test", description="test", user=self.create_user, due_date=datetime.today(),
                                   set_alert=3)
        return task

    def get_hostname(self):
        if settings.DEBUG:
            host_name = "https://pradeepsukhwani.pythonanywhere.com/"
        else:
            host_name = "http://localhost:8000"
        return host_name

    @pytest.mark.django_db(transaction=True)
    def test_login(self):
        response = post(self.get_hostname() + reverse("api_login", kwargs={"api_name": "todo"}),
                        data={'username': "ps", 'password': 'django123'})
        assert response.status_code == 200

    @pytest.mark.django_db(transaction=True)
    def test_logout(self):
        response = get(self.get_hostname() + reverse("api_logout", kwargs={"api_name": "todo"}),
                       params={'user': self.create_user(), "testing": True})
        assert response.status_code == 200

    @pytest.mark.django_db(transaction=True)
    def test_task_create(self):
        response = post(self.get_hostname() + reverse("api_task", kwargs={"api_name": "todo"}),
                        data={"title": "test2", "description": "test2", "user": self.create_user(), "testing": True,
                              "datetime": datetime.today().strftime("%d/%m/%Y %H:%M:%S"), "set_alert": 3})
        assert response.status_code == 200
