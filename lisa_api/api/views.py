from django.contrib.auth.models import User, Group
from lisa_api.api.models import Plugin
from rest_framework import viewsets
from lisa_api.api.serializers import UserSerializer, GroupSerializer, PluginSerializer
import pip
import logging
logger = logging.getLogger('lisa_api')


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PluginViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows plugins to be viewed or edited.
    """
    queryset = Plugin.objects.all()
    serializer_class = PluginSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        version_str = ''
        if instance.version:
            version_str = ''.join(["==", instance.version])
        pip.main(['install', 'lisa-plugins-' + instance.name + version_str])
        logger.info(msg="Plugin installed")

    def perform_destroy(self, instance):
        pip.main(['uninstall', '--yes', 'lisa-plugins-' + instance.name])
        instance.delete()
        logger.info(msg="Delete plugin")
