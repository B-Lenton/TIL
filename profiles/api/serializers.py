from django.contrib.auth.models import User
from rest_framework import serializers

from profiles.models import Profile

# TODO: Keep following this tutorial (https://www.django-rest-framework.org/tutorial/1-serialization/)
#       from "Writing regular Django views using our Serializer"...
# it should be able to update and create accounts now but check migration 4 in case the defaults 
# are doing something strange to the database...

class AccountSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Needed in normal .Serializer but not in ModelSerializer (hopefully)...
        username = serializers.CharField(max_length=200)
        image = serializers.ImageField()
        first_name = serializers.CharField(max_length=200)
        last_name = serializers.CharField(max_length=200)
        email = serializers.EmailField()
        password = serializers.CharField(
            write_only=True,
            required=True,
            help_text='Leave empty if no change needed',
            style={'input_type': 'password', 'placeholder': 'Password'}
        )
    '''

    class Meta:
        model = Profile
        fields = ('username', 'image', 'first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = Profile.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.image = validated_data.get('image', instance.image)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()

        def update(self, instance, validated_data):
            user = update(instance, validated_data)
            try:
                user.set_password(validated_data['password'])
            except KeyError:
                pass
            user.save()
            return user
        
        return instance
        
