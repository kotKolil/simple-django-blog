from django.contrib.auth.models import *
from rest_framework import serializers
from .models import *

class comment_api_ser(serializers.ModelSerializer):

	class Meta:
		model = comments 
		fields = ['user', 'date', 'text', 'state_id']
