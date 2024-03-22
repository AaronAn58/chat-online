from django.shortcuts import render
from rest_framework.views import APIView

from chat_server.chat_server.serializers import CustomModelSerializer
from chat_server.friends.models import Friends


# Create your views here.

class GetFriendsSerializer(CustomModelSerializer):
    user = CustomModelSerializer()

    class Meta:
        model = Friends
        field = ['user']


class GetFriendsViewSet(APIView):
    serializer_class = GetFriendsSerializer

    def get(self):
        return Friends.objects.all()
