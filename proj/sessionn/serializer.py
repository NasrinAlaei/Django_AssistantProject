from rest_framework import serializers
from .models import User, Session , GeeksModel
from rest_framework.serializers import ModelSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PresentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'profile_picture']

class HostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'profile_picture']


class ParticipatinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'profile_picture']


class SessionSerializer(serializers.ModelSerializer):
    presents = PresentsSerializer(many=True)
    hosts = HostsSerializer(many=True)
    participatins = ParticipatinsSerializer(many=True)
    class Meta:
        model = Session
        fields = '__all__'

class SessionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'

class GeeksModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeeksModel
        fields = '__all__'
