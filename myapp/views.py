from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from django.contrib.auth import authenticate, login
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.throttling import UserRateThrottle
from rest_framework.exceptions import Throttled
from rest_framework.decorators import action
from .models import *


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
    }

class Signup(APIView):

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message':'signup successfull, Welcome aboard!'},status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data= data)
        if serializer.is_valid():
            email= serializer.data.get('email')
            password= serializer.data.get('password')
            user = authenticate(request, email= email, password= password)
            if user is not None:
                token = get_tokens_for_user(user)
                login(request,user)
                return Response({'message':f'login successful, {serializer.data.get("email")}', 'token':token},status=status.HTTP_200_OK)
        return Response({'errors': 'email or password is incorrect'},status=status.HTTP_400_BAD_REQUEST)
    
class Search(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        search_keyword = request.query_params.get('search')
        if search_keyword:
            users = User.objects.filter(Q(email__icontains=search_keyword) | Q(username__icontains=search_keyword))
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'Search keyword is required'}, status=status.HTTP_400_BAD_REQUEST)

class RequestRate(UserRateThrottle):
    rate = '3/minute'

class FriendRequests(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    throttle_classes = [RequestRate]

    def create(self, request):
        try: 
            self.check_throttles(request)
        except Throttled as e:
            return Response({'message':f'you cannot send more than 3 request in a minute {e.detail}'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
    
        serializer = FriendRequestSerializer(data=request.data)
        if serializer.is_valid():
            if FriendRequest.objects.filter(
                    from_user=request.user, 
                    to_user=serializer.validated_data['to_user'],
                    status='pending').exists():
                return Response({'detail': 'Friend request already sent.'}, status=status.HTTP_400_BAD_REQUEST)

            if FriendRequest.objects.filter(
                    from_user=serializer.validated_data['to_user'],
                    to_user=request.user,
                    status='pending').exists():
                return Response({'detail': 'You have a pending friend request from this user.'}, status=status.HTTP_400_BAD_REQUEST)
            print(request.data)
            serializer.save(from_user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        try:
            friend_request = FriendRequest.objects.get(pk=pk, to_user=request.user)
            friend_request.status = 'accepted'
            friend_request.save()
            return Response({'detail': 'Friend request accepted.'}, status=status.HTTP_200_OK)
        except:
            return Response({'detail': 'Friend Request not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        friend_request = FriendRequest.objects.get(pk=pk, to_user=request.user)
        friend_request.status = 'rejected'
        friend_request.save()
        return Response({'detail': 'Friend request rejected.'}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def list_pending_requests(self, request):
        pending_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
        serializer = FriendRequestSerializer(pending_requests, many=True)
        if not pending_requests.exists():
            return Response({'message': 'Nothing to see here'}, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def list_friends(self, request):
        friends = User.objects.filter(
            Q(sent_requests__to_user=request.user, sent_requests__status='accepted') | 
            Q(received_requests__from_user=request.user, received_requests__status='accepted')
        ).distinct()
        if not friends.exists():
            return Response({'message': 'Nothing to see here'}, status=status.HTTP_200_OK)

        data= [{'id': friend.id, 'username': friend.username, 'email': friend.email} for friend in friends]
        return Response(data, status=status.HTTP_200_OK)
        