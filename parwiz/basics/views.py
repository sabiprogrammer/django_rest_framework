from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status
from rest_framework import mixins

#AUTHENTICATON
from rest_framework.authentication import BasicAuthentication, TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Article
from .serialize import ArtSerialize


# Create your views here.

# MODAL VIEWSET
class ArticleModalViewSet(viewsets.ModelViewSet):
   serializer_class = ArtSerialize
   queryset = Article.objects.all()

# END MODAL VIEWSET


# VIEWSET Generic Class BASED API VIEWS
class ArticleViewSet2(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
   
   serializer_class = ArtSerialize
   queryset = Article.objects.all()




# END VIEWSET Generic Class BASED API VIEWS

# VIEWSET BASED API VIEWS
class ArticleViewSet(viewsets.ViewSet):
   def list (self, request):
      articles = Article.objects.all()
      serializer = ArtSerialize(articles, many=True)
      return Response(serializer.data)
   
   def create(self, request):
      serializer = ArtSerialize(data=request.data)

      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
   def retrieve(self, request, pk=None):
      query_set = Article.objects.all()
      article = get_object_or_404(query_set, pk=pk)
      serializer = ArtSerialize(article)
      return Response(serializer.data)
   
   def update(self, request, pk=None):
      article = Article.objects.get(pk=pk)
      serializer = ArtSerialize(article, data=request.data)

      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# END VIEWSET BASED API VIEWS


# GENERIC CLASS BASED API VIEWS
class GenericApiViews(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                      mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
   serializer_class = ArtSerialize
   lookup_field = 'id'
   queryset = Article.objects.all()

   #AUTHENTICATON
   # authentication_classes = [SessionAuthentication, BasicAuthentication]
   authentication_classes = [TokenAuthentication]
   permission_classes = [IsAuthenticated]

   def get(self, request, id=None):
      if id:
         return self.retrieve(request)
      else:
         return self.list(request)

   def post(self, request, id):
      return self.create(request)
   
   def put(self, request, id=None):
      return self.update(request, id)
   
   def delete(self, request, id):
      return self.destroy(request, id)

# END GENERIC CLASS BASED API VIEWS


# CLASS BASED API VIEWS
class ArticleAPIView(APIView):
   def get(self, request):
      articles = Article.objects.all()
      serializer = ArtSerialize(articles, many=True)
      return Response(serializer.data)
   
   def post(self, request):
      serializer = ArtSerialize(data=request.data)

      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetail(APIView):
   def get_object(self, id):
      try:
         return Article.objects.get(id=id)
      except Article.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)
   
   def get(self, request, id):
      article = self.get_object(id)
      serializer = ArtSerialize(article)
      return Response(serializer.data)
   
   def put(self, request, id):
      article = self.get_object(id)
      serializer = ArtSerialize(article, data=request.data)

      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   def delete(self, request, id):
      article = self.get_object(id)
      article.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
# END CLASS BASED API VIEWS


# FUNCTION BASED API VIEWS
@api_view(['GET', 'POST'])
# @csrf_exempt
# import these authentication middlewares and read more about them if you want to use them for FBV API
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([isAuthenticated])
def article_list(request):
   if request.method == 'GET':
      articles = Article.objects.all()
      serializer = ArtSerialize(articles, many=True)
      # return JsonResponse(serializer.data, safe=False)
      return Response(serializer.data)

   elif request.method == 'POST':
      # data = JSONParser().parse(request)
      serializer = ArtSerialize(data=request.data)

      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def article_detail(request, pk):
   try:
      article = Article.objects.get(pk=pk)
   except Article.DoesNotExist:
      # return HttpResponse(status=400)
      return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

   if request.method == 'GET':
      serializer = ArtSerialize(article)
      return Response(serializer.data)

   elif request.method == 'PUT':
      # data = JSONParser().parse(request)
      serializer = ArtSerialize(article, data=request.data)

      if serializer.is_valid():
         serializer.save()
         # return JsonResponse(serializer.data)
         return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
   elif request.method == 'DELETE':
      article.delete()
      return Response(status=status.HTTP_204_NO_CONTENT)
# END FUNCTION BASED API VIEWS
