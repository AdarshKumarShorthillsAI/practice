from rest_framework import status
import langchain
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from .models import Message
from django.http import JsonResponse
from .serializers import MessageSerializer
from langchain.schema import (AIMessage, HumanMessage, SystemMessage)

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        print(username)
        print(password)

        user = authenticate(username=username, password=password)

        if user is not None: 
            login(request, user)
            return Response({'message': 'Successfully logged in.'}, status=status.HTTP_200_OK)
        
        else: 
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

@api_view(['POST'])
def add_new_entry(request):
    user_name = request.data.get('username')
    messages = request.data.get('messages')

    existing_message, created = Message.objects.get_or_create(username=user_name)
    print(existing_message)
    print(created)
    existing_message.messages = messages
    existing_message.save()

    return JsonResponse({'message': 'Message added successfully'})


@api_view(['GET'])
def fetch_all_usernames(request):
    usernames = Message.objects.values_list('username', flat=True)
    return JsonResponse({'usernames': list(usernames)})

@api_view(['PUT'])
def update_table(request):
    user_name =  request.data.get('username')
    new_messages = request.data.get('messages')

    try:
        message = Message.objects.get(username=user_name)
        message.messages = new_messages
        message.save()
        return Response({'message': 'Message updated successfully'})
    except Message.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def empty_the_table(request):
    user_name = request.data.get('username')
    try:
        message = Message.objects.get(username=user_name)
        message.delete()
        return Response({'message': 'Table emptied successfully'})
    except Message.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

# @api_view(['GET'])
# def retrieve_table(request, user_name):
#     try:
#         message = Message.objects.get(username=user_name)
#         serialized_message = MessageSerializer(message)
#         return Response(serialized_message.data)
#     except Message.DoesNotExist:
#         return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def retrieve_table(request):
    username = request.data.get('username')
    try:
        # Retrieve the messages for the given username
        messages = Message.objects.get(username=username)
        serializer = MessageSerializer(messages)

        # Deserialize the messages
        deserialized_messages = eval(serializer.data['messages'])

        all_messages = []

        for i, msg_content in enumerate(deserialized_messages):
            i = i + 1
            if i == 1:
                print(msg_content)
                all_messages.append(SystemMessage(content=msg_content))
            elif i % 2 == 0:
                all_messages.append(HumanMessage(content=msg_content))
            else:
                all_messages.append(AIMessage(content=msg_content))

        return JsonResponse(all_messages, safe=False)

    except Message.DoesNotExist:
        return JsonResponse({'message': 'User not found'}, status=404)
