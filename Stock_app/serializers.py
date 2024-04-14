from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import Hub, Machine

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'

class HubSerializer(serializers.ModelSerializer):
    machines = MachineSerializer(many=True, read_only=True)

    class Meta:
        model = Hub
        fields = '__all__'

    def validate(self, data):
        # Get the service_provider from the validated data
        service_provider = data.get('service_provider')
        owner = data.get('owner')

        if not (User.objects.filter(username=service_provider, groups__name='technician').exists()):
            # print("Error")
            raise serializers.ValidationError("The service provider must be a technician")
        elif not (User.objects.filter(username=owner, groups__name='owner').exists()):
            raise serializers.ValidationError("The Owner must be a Owner")

        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class loginser(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class registerser(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    user_group = serializers.ChoiceField(choices=[('owner', 'Owner'), ('technician', 'Technician')])

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError("Username already taken !")

        if data['email']:
            if User.objects.filter(username=data['email']).exists():
                raise serializers.ValidationError("Email already taken !")

        return data

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'], email=validated_data['email'])
        user.set_password(validated_data['password'])
        
        # Assign user to selected group
        group_name = validated_data.get('user_group')
        if group_name:
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

        user.save()
        return validated_data
