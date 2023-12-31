from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import PaperHubUser
from .serializers import UserSignupSerializer
from .serializers import PaperHubUserSerializer
from django.contrib.auth import login

@api_view(['POST'])
def signup(request):
    serializer = UserSignupSerializer(data=request.data)
    
    if serializer.is_valid():
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        
        # Create a PaperHubUser instance for the registered user
        PaperHubUser.objects.create(user=user, role='user')
        login(request, user)
        
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
def update_user(request, user_id):
    try:
        # Retrieve the PaperHubUser instance
        paperhub_user = PaperHubUser.objects.get(id=user_id)
    except PaperHubUser.DoesNotExist:
        return Response({'error': 'PaperHubUser not found'}, status=status.HTTP_404_NOT_FOUND)

    # Retrieve the user data from the request
    data = request.data.get('user', {})

    # Update User information
    user = paperhub_user.user
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.password = data.get('password', user.password)  # You might want to handle password hashing here

    # Save the updated User
    user.save()

    # Update PaperHubUser information
    paperhub_user.role = data.get('role', paperhub_user.role)

    # Update favorite_articles if provided
    favorite_articles = data.get('favorite_articles')
    if favorite_articles is not None:
        paperhub_user.favorite_articles.set(favorite_articles)

    # Update saved_articles if provided
    saved_articles = data.get('saved_articles')
    if saved_articles is not None:
        paperhub_user.saved_articles.set(saved_articles)

    # Save the updated PaperHubUser
    paperhub_user.save()

    # Serialize and return the updated data
    serializer = PaperHubUserSerializer(paperhub_user)
    return Response(serializer.data, status=status.HTTP_200_OK)
    

