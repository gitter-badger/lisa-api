from django.contrib.auth.models import User, Group
from lisa_api.api.models import Plugin
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'first_name', 'last_name', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class PluginSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Plugin
        fields = ('url', 'name', 'version')
