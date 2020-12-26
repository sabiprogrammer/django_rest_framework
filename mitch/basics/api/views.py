# from django.shortcuts import render, get_object_or_404
# from rest_framework.parsers import JSONParser

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from basics.api.serializers import PostSerialize
from basics.models import Post


@api_view(['GET'])
def api_post_detail(request, pk):
   try:
      article = Post.objects.get(pk=pk)
   except Post.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

   if request.method == 'GET':
      serializer = PostSerialize(article)
      return Response(serializer.data)


@api_view(['PUT'])
def api_post_update(request, pk):
   try:
      article = Post.objects.get(pk=pk)
   except Post.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

   if request.method == 'PUT':
      serializer = PostSerialize(article, data=request.data)
      data = {}
      if serializer.is_valid():
         serializer.save()
         data["success"] = "update successful"
         return Response(data=data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
def api_post_delete(request, pk):
   try:
      article = Post.objects.get(pk=pk)
   except Post.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

   if request.method == 'DELETE':
      operation = article.delete()
      data = {}
      if operation:
         data['success'] = "Delete successful"
      else:
         data['failure'] = "Delete fail"
      return Response(data=data)


@api_view(['POST'])
def api_post_create(request):
   account = request.user
   blog_post = Post(author=account)

   if request.method == 'POST':
      serializer = PostSerialize(blog_post, data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
