from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import serializers, status, viewsets
from rest_framework.response import Response
from .models import Post
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

#token = Token.objects.create(user=user)
#print(token.key)

# Create your views here.
def index(request):
    context = {
        "posts":[
            {"name":"post1", "content":"content1"},
            {"name":"post2", "content":"content2"},
        ]
    }
    return render(request, "index.html", context)

@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def example_view(request, format=None):
    content = {
        'user': str(request.user), # `django.contrib.auth.User` instance
        'auth': str(request.auth), # None
    }
    return Response(content)

'''
@api_view(['GET'])
def post_list(request):
    # Retrieve all list of posts from the database
    posts = Post.objects.all()

    # Manually create a list of distionaries respresenting post data
    post_data = []
    for post in posts:
        post_data.append({
            'title': post.title,
            'posts': post.story,
            'timestamp': post.timestamp.strftime('%Y-%m-%d'),
            'author': post.author,
        })
    
    # Create a JSON Response
    response_data = {'posts': post_data}
    return Response(response_data)
'''
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'story', 'author', 'timestamp']

'''
@api_view(['GET'])
def post_list(request):
    querySet = Post.objects.all()
    serializer = PostSerializer(querySet, many=True)
    return Response(serializer.data)
'''

# Funtional-Based Views
@api_view(['GET', 'POST'])
def blog_post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Class-Based Views
class BlogPostList(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Generic Views
'''
class BlogPostList(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class BlogPostCreate(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# Viewset and Routers
class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
'''