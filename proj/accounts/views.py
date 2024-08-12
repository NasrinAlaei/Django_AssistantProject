from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from . models import User
from .serializer import UserSerializer
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required

#@login_required(login_url='')
class UserViewset(viewsets.ModelViewSet):
   # permission_classes = [IsAuthenticated,]
#    authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer


'''class UserViewset(viewsets.ModelViewSet):
    
    def userimag(self,request):    
       if request.method == 'POST':
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data , status=201)
            return Response(serializer.errors, status=400)    '''
