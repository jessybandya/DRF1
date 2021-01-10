from rest_framework import generics
from rest_framework.views import APIView
from blog.models import Post
from .serializers import PostSerializer
from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, BasePermission, IsAdminUser, DjangoModelPermissions
from rest_framework import viewsets
from rest_framework import filters
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from blog.models import Post
from .serializers import PostSerializer
from rest_framework import viewsets, filters, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser


class PostUserWritePermission(BasePermission):
    message = 'Editing posts is restricted to the author only.'

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user

# User Filter
# class PostList(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = PostSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return Post.objects.filter(author=user)

class PostList(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Post, slug=item)

    # Define Custom Queryset
    def get_queryset(self):
        return Post.objects.all()
#
class PostDetail(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        slug = self.request.query_params.get('slug', None)
        print(slug)
        return Post.objects.filter(slug=slug)
    def get_object(self, queryset=None, **kwargs):
        item = self.kwargs.get('pk')
        return get_object_or_404(Post, slug=item)

class PostListDetailfilter(generics.ListAPIView):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^slug']
#
#     # '^' Starts-with search.
#     # '=' Exact matches.
#     # '@' Full-text search. (Currently only supported Django's PostgreSQL backend.)
#     # '$' Regex search.
#
#
class PostSearch(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^slug']


# Post Admin

# class CreatePost(generics.CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
class CreatePost(APIView):
    permission_classes = [PostUserWritePermission]
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]


    def post(self, request, format=None):
        print(request.data)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminPostDetail(generics.RetrieveAPIView):
    permission_classes = [PostUserWritePermission]
    permission_classes = [IsAuthenticated]

    queryset = Post.objects.all()
    serializer_class = PostSerializer

class EditPost(generics.UpdateAPIView):
    permission_classes = [PostUserWritePermission]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

class DeletePost(generics.RetrieveDestroyAPIView):
    permission_classes = [PostUserWritePermission]
    serializer_class = PostSerializer
    queryset = Post.objects.all()