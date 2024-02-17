from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class loginser(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class registerser(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        
        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError("Username already taken !")
                    
        if data['email']:
            if User.objects.filter(username = data['email']).exists():
                raise serializers.ValidationError("Email already taken !")
            
        return data
    
    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'], email = validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        print("Done")
        return validated_data