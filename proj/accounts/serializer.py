from rest_framework import serializers  
from .models import User  
import base64  
import uuid  
from django.core.files.base import ContentFile  

class UserSerializer(serializers.ModelSerializer):
       
    profile_picture = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)  

    def to_internal_value(self, data):  
        if 'profile_picture' in data:  
            format, imgstr = data['profile_picture'].split(';base64,')   
            ext = format.split('/')[-1]   
            data['profile_picture'] = ContentFile(base64.b64decode(imgstr), name=str(uuid.uuid4())[:10] + '.' + ext)  
        return super(UserSerializer, self).to_internal_value(data)  

    def to_representation(self, instance):  
        response = super().to_representation(instance)  
        if instance.profile_picture:  
            response['profile_picture'] = instance.profile_picture.url  
        return response  
   


    class UserSerializer(serializers.ModelSerializer):  
      image = Base64ImageField()
      class Meta:  
        model = User  
        fields = '__all__'

   ''' def create(self, vallidated_data):
        image = vallidated_data.pop('image')
        data = vallidated_data.pop('data')
        return User.objects.create(data =data , image=image)    '''
