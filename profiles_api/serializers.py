from rest_framework import serializers

from profiles_api import models

from django.contrib.auth import authenticate

class HelloSerializers(serializers.Serializer):
    """ Serializes a name field for testing our APIView"""

    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializer a user profile object """
    class Meta:
        model = models.UserProfile
        fields = ('id', 'email', 'name', 'password')
        extra_kwargs = {
            'password': {
                'write_only':True,
                'style': {'input_type': 'password'}
                }
        }

    def create(self, validated_data):
        """ Create and return a new user """
        user = models.UserProfile.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            password = validated_data['password']
        )

        return user

    def update(self, instance, validated_data):
        """ Handle updating user account """
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)

class LoginSerializer(serializers.Serializer):
    """ Handle User login with email """
    email = serializers.EmailField()
    password = serializers.CharField(
    style={'input_type': 'password'},
    trim_whitespace = False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # DRF's authenticate() still expects "username" map it to email
            user = authenticate(
            request = self.context.get('request'),
            username = email,
            password = password
            )

            if not user:
                raise serializers.ValidationError(
                'Unable to log in with provided credentials',
                code = 'authorization'
                )

        else:
            raise serializers.ValidationError(
            'Must include "email" and "password".',
            code = 'authorization'
            )
        attrs['user'] = user
        return attrs
