from django.db import models
from django.db.models import fields
from rest_framework import serializers
from . import models

class communitySerializer(serializers.ModelSerializer):
    class Meta:
        models = models.Community
        fields = '__all__'