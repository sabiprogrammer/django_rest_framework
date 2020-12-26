from rest_framework import serializers
from basics.models import Post


class PostSerialize(serializers.ModelSerializer):
   class Meta:
      model = Post
      fields = ['title', 'image', 'date']