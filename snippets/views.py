from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from snippets.serializers import SnippetSerializer
from snippets.models import snippets
from rest_framework.views import APIView
#________________________________________________________________api_view________________________________________________________________
# Create your views here.
# @api_view(['GET',"POST"])
# def snippet_list(request,format=None):
#     if request.method == 'GET':
#         snippet = snippets.objects.all()
#         serializer = SnippetSerializer(snippet, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
# @api_view(['GET','PUT',"DELETE"])
# def snippet_details(request,pk,format=None):
#     """Retrive ,update ,delete a code snippet"""
#     # try:
#     #     snippet = snippets.objects.get(pk=pk)
#     #     serializer = SnippetSerializer(snippet)
#     #     return JsonResponse(serializer.data)
#     # except snippets.DoesNotExist:
#     #     return HttpResponse(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         snippet = snippets.objects.get(pk=pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         snippet = snippets.objects.get(pk=pk)
#         serializer = SnippetSerializer(snippet,data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         snippet = snippets.objects.get(pk=pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


#________________________________________________________________API_VIEWS________________________________________________________________
# class SnippetList(APIView):
#     """List all snippets,or create a new snippet"""
#     def get(self, request,format=None):
#         snippets = snippets.objects.all()
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
#     def post(self, request,format=None):
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# class SnippetDetail(APIView):
#     """Retrieve, update or delete a snippet"""
#     def get_object(self,pk):
#         try:
#             return snippets.objects.get(pk=pk)
#         except snippets.DoesNotExist:
#             raise Http404
#     def get(self,request,pk,format=None):
#         snippet = self.get_object(pk)
#         serializer = SnippetSerializer(snippet)
#         return Response(serializer.data)
#     def put(self,request,pk,format=None):
#         snippet = self.get_object(pk)
#         data = JSONParser().parse(request)
#         serializer = SnippetSerializer(snippet,data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)   
#     def delete(self,request,pk,format=None):
#         snippet = self.get_object(pk)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#________________________________________________________________mix_in________________________________________________________________
# from rest_framework import mixins,generics
# class SnippetList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = snippets.objects.all()
#     serializer_class=SnippetSerializer
#     def get(self,request,*args, **kwargs):
#         return self.list(request,*args,**kwargs)
#     def post(self,request,*args, **kwargs):
#         return self.create(request,*args,**kwargs)
# class SnippetDetail(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = snippets.objects.all()
#     serializer_class=SnippetSerializer
#     def get(self,request,*args, **kwargs):
#         return self.retrieve(request,*args,**kwargs)
#     def put(self,request,*args, **kwargs):
#         return self.update(request,*args,**kwargs)
#     def delete(self,request,*args, **kwargs):
#         return  self.destroy(request,*args,**kwargs) 
#________________________________________________________________ListCreateApiviews________________________________________________________________
from rest_framework import generics
from rest_framework import permissions
from snippets.permissions import isOwnerOrReadOnly
class SnippetList(generics.ListCreateAPIView):
    queryset=snippets.objects.all()
    serializer_class=SnippetSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=snippets.objects.all()
    serializer_class=SnippetSerializer  
    permission_classes=[permissions.IsAuthenticatedOrReadOnly,isOwnerOrReadOnly]
from django.contrib.auth.models import User
from snippets.serializers import UserSerializer

class UserList(generics.ListCreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
