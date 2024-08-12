from rest_framework import status
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .models import User,Session, GeeksModel
from rest_framework.decorators import action
from .serializer import *
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from django.utils.decorators import method_decorator  
from django.views.decorators.csrf import csrf_exempt 
import base64
from django.core.files.base import ContentFile
from datetime import datetime,timedelta

import json
from rest_framework import generics
from rest_framework.views import APIView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime



# CreateSession view handles the creation of new session objects considering overlapping sessions.
class CreateSession(APIView):

    def post(self, request, *args, **kwargs):
        # Initialize a serializer
        session_serializer = SessionCreateSerializer(data=request.data)

        # If the serializer data is valid...
        if session_serializer.is_valid():
            # Combine participants, hosts, and presenters into one list of users.
            session_users = list(session_serializer.validated_data['participatins']) + \
                            list(session_serializer.validated_data['hosts']) + \
                            list(session_serializer.validated_data['presents'])
            
            # Fetch all sessions from the database that involve any of the session users
            sessions = Session.objects.filter(
                Q(participatins__in=session_users) | Q(hosts__in=session_users) | Q(presents__in=session_users)
            ).distinct()

            # Get the start and end times, and the date for the session.
            start = session_serializer.validated_data['time_start']
            end = session_serializer.validated_data['time_end']
            date = session_serializer.validated_data['session_date']


            # Filter to find any sessions that have a time overlap on the same date and time.
            overlapping_sessions = sessions.filter(
                (Q(time_start__lte=start) & Q(time_end__gte=start) & Q(session_date=date)) |
                (Q(time_start__lte=end) & Q(time_end__gte=end) & Q(session_date=date))
            )
            for overlapping_session in overlapping_sessions:
                print(overlapping_session.title)
            # If there are overlapping sessions...
            if overlapping_sessions:
                # Return an error response indicating a scheduling conflict.
                return Response(
                    {'error': 'For participants, hosts, or presenters specified in this meeting, another meeting has already been specified at this time.!'}, 
                    status.HTTP_406_NOT_ACCEPTABLE
                )
            else:
                # If there are no conflicts, save the session and return the serialized data for the newly created session.
                session_serializer.save()
                return Response(session_serializer.data, status=status.HTTP_201_CREATED)
        else:
            # If the serializer data is not valid, return a HTTP 400 Bad Request response.
            return Response(None, status=status.HTTP_400_BAD_REQUEST)


class UpdateSession(APIView):

    def put(self, request, *args, **kwargs):
        session_id = self.kwargs['pk']
        session = Session.objects.get(pk=session_id)
        session_serializer = SessionCreateSerializer(session, data=self.request.data)
    
        if session_serializer.is_valid():
            # Combine participants, hosts, and presenters into one list of users.
            session_users = list(session_serializer.validated_data['participatins']) + \
                            list(session_serializer.validated_data['hosts']) + \
                            list(session_serializer.validated_data['presents'])
            
            # Fetch all sessions from the database that involve any of the session users
            sessions = Session.objects.filter(
                Q(participatins__in=session_users) | Q(hosts__in=session_users) | Q(presents__in=session_users)
            ).distinct()

            # Get the start and end times, and the date for the session.
            start = session_serializer.validated_data['time_start']
            end = session_serializer.validated_data['time_end']
            date = session_serializer.validated_data['session_date']


            # Filter to find any sessions that have a time overlap on the same date and time.
            overlapping_sessions = sessions.filter(
                (Q(time_start__lte=start) & Q(time_end__gte=start) & Q(session_date=date) & ~Q(pk=session_id)) |
                (Q(time_start__lte=end) & Q(time_end__gte=end) & Q(session_date=date) & ~Q(pk=session_id))
            )
            for overlapping_session in overlapping_sessions:
                print(overlapping_session.title)
            # If there are overlapping sessions...
            if overlapping_sessions:
                # Return an error response indicating a scheduling conflict.
                return Response(
                    {'error': 'For participants, hosts, or presenters specified in this meeting, another meeting has already been specified at this time.!'}, 
                    status.HTTP_406_NOT_ACCEPTABLE
                )
            else:
                # If there are no conflicts, save the session and return the serialized data for the newly created session.
                session_serializer.save()
                return Response(session_serializer.data, status=status.HTTP_200_OK)        
        else:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

class GetUserSessions(APIView):
    # It filters the User queryset for the given username and 
    # returns the first instance or an error response if the user does not exist.
    def get_object(self, username):
        try:
            # Attempt to get the first user matching the provided username
            user = User.objects.filter(username=username).first()
            return user
        except User.DoesNotExist:
            # If no user is found, return an HTTP 404 NOT FOUND response
            return Response({'error': 'user not found!'}, status.HTTP_404_NOT_FOUND)

    # It retrieves all sessions related to a given user, either where the 
    # user participates, hosts, or is present, and returns serialized session data.
    def get(self, request, *args, **kwargs):
        # Retrieve a specific user using the 'username' kwarg
        user = self.get_object(kwargs['username'])

        # Retrieve all sessions where the user is participating, hosting, or is present
        # The .distinct() method ensures that each session is unique in the queryset
        sessions = Session.objects.filter(
            Q(participatins=user) |
            Q(hosts=user) |
            Q(presents=user)
        ).distinct()

        # Serialize the queryset of sessions
        session_serializer = SessionSerializer(sessions, many=True) 

        # Return the serialized data with an HTTP 200 OK response
        return Response(session_serializer.data, status=status.HTTP_200_OK)


class ArchivedSessions(generics.ListAPIView):
    serializer_class = SessionSerializer  # Specifies the serializer.

    def get_queryset(self):
        current_date = datetime.today()  # Get the current date and time.
        current_time = datetime.now().strftime("%H:%M:%S")
        # Return the queryset consisting of Archived Sessions objects,
        return Session.objects.filter(session_date__lte=current_date, time_end__lte=current_time)

class AllSessions(generics.ListAPIView):
    serializer_class = SessionSerializer  # Specifies the serializer.
    queryset = Session.objects.all()      # Sets the queryset to include all Session objects.


class SaveSessionMessage(APIView):

    # This method attempts to retrieve a Session object by its primary key.
    # If it does not exist, an error response is returned.
    def get_object(self, session):
        try:
            session = Session.objects.filter(pk=session).first()  # Get the first session that matches the primary key.
            return session
        except Session.DoesNotExist:
            return Response({'error': 'Session not found!'}, status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        try:
            data = request.data  # Retrieve the data sent with the POST request.
            session = self.get_object(data['session'])  # Retrieve the relevant session object.

            # If a message history does not exist or is empty, initialize an empty dictionary.
            # Else, evaluate the existing message string as a dictionary.
            if session.message is None or session.message == '':
                messages = {}
            else:
                messages = eval(session.message)

            current_datetime = datetime.now()  # Get the current datetime.
            # Format the current datetime as a string in the format 'Year-Month-Day Hour:Minute:Second'.
            date_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            
            # Add the new message to the messages dictionary with the formatted date time as key.
            messages[date_time] = {
                'user': data['user'],
                'message': data['message']
            }
            session.message = str(messages)  # Convert the updated message dictionary back to a string.
            session.save()  # Save the updated session object to the database.
        except:
            # If any part of the process fails, return a 400 BAD REQUEST response.
            return Response({'error':'Your request failed. Please send all required data!'}, status=status.HTTP_400_BAD_REQUEST)
        
        # If the message is saved successfully, return a success response.
        return Response({'message': 'Message saved successfully!'}, status=status.HTTP_200_OK)


#########################################################
######################################################### 


@method_decorator(csrf_exempt, name='dispatch')  
class UserViewSet(viewsets.ModelViewSet):
  # authentication_classes = [SessionAuthentication, BasicAuthentication]
  # permission_classes = [permissions.AllowAny,]
   queryset = User.objects.all()
   serializer_class = UserSerializer




@method_decorator(csrf_exempt, name='dispatch')     
class SessionViewSet(viewsets.ModelViewSet):
   # authentication_classes = [SessionAuthentication, BasicAuthentication]
   # permission_classes = [IsAuthenticated,]
    queryset = Session.objects.all()
    serializer_class = SessionCreateSerializer
    def create(self,request):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        try:
          self.perform_create(serializer)
        except ValidationError as e:
          return Response({'error':str(e)}, status = status.HTTP_400_BAD_REQUEST)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED, headers=headers)
    
    manual_parameters = [
        openapi.Parameter('user', openapi.IN_QUERY, description="user id", type=openapi.TYPE_INTEGER, required=False),]
    @swagger_auto_schema(operation_summary="get logs by admin", manual_parameters=manual_parameters)
    @action(detail=False, methods=['get'])
    def get_session_by_user(self,request):    
       
        try:
            user = User.objects.get(pk=request.user.pk)
            queryset = self.get_queryset().filter(Q(participatins__in = list([user])) | Q(hosts__in = list([user])) | Q(presents__in = list([user])))
            serializer = self.get_serializer(queryset,many = True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return JsonResponse({'error': 'user is not found!'})
        
        
    
    @action(detail=False, methods=['post'])
    def get_session_by_date(self,request):
        time_start = request.data.get('time_start')
        
        queryset = self.get_queryset().filter(time_start__date =time_start )
        serializer = self.get_serializer(queryset, many = True)
        return Response(serializer.data)
    
   # @action(detail=False, methods=['post'])
'''def archive_sessions():
       now = datetime.now()
       sessions_to_archive = Session.objects.filter(time_end__lt=now)
       for session in sessions_to_archive:
           session.is_archived = True
           session.save()
'''
from rest_framework.mixins import (CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin)
from rest_framework.parsers import FormParser, MultiPartParser

class GeeksModelViewSet( CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, viewsets.GenericViewSet):
   # permission_classes = [IsAuthenticated,]
   # authentication_classes = [SessionAuthentication, BasicAuthentication]
    queryset = GeeksModel.objects.all()
    serializer_class = GeeksModelSerializer
    parser_classes = (FormParser, MultiPartParser)
    
 
    
'''class ArchivedSessionViewSet( viewsets.ReadOnlyModelViewSet):
    queryset = Session.objects.filter(is_archived = True)
    serializer_class = SessionSerializer
   '''

