from rest_framework import serializers
from rest_framework.decorators import detail_route, list_route
from django.contrib.auth.hashers import make_password
from . import models


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serialize user profiles
    """

    # TODO: hyperlinks as sub-resource under each user
    # TODO: add extra user fields?
    # TODO: nullify fields that user is not allowed to see? (this may be
    # expensive in querysets)


    class Meta:
        model = models.Profile
        fields = (
        'gender','phone','date_of_birth'
        ,'website','about_me', 'visibility', 'user'
        )
        read_only = {'read_only': True}
        extra_kwargs = {
                'user':read_only
        }


class UserSerializer(serializers.ModelSerializer):
    """
    Serialize User objects.
    """

    role = serializers.SerializerMethodField()
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = ('alias', 'role','email', 'name', 'school_id', 'password', 'password_confirmation')
        write_only = {'write_only': True}
        extra_kwargs = {
                'email': write_only,
                'role': write_only,
                'name': write_only,
                'school_id': write_only,
                'password': write_only,
                'password_confirmation': write_only
	}

    def get_role(self, obj):
        if(obj.role == models.User.ROLE_STUDENT):
            return 'student'
        elif(obj.role == models.User.ROLE_TEACHER):
            return 'teacher'
        elif(obj.role == models.User.ROLE_STAFF):
            return 'staff'
        elif(obj.role == models.User.ROLE_ADMIN):
            return 'admin'


    def create(self, validated_data):
        password_confirmation = validated_data.pop('password_confirmation', None)
        if(password_confirmation == validated_data['password']):
            validated_data['password'] = make_password(validated_data['password'])
            return super(UserSerializer, self).create(validated_data)
        else:
            raise Exception()


class FullUserSerializer(serializers.ModelSerializer):
    """
    Serialize full User objects.
    """

    # TODO: extra_emails
    # TODO: create hyperlinks or make it role-based access?

    class Meta:
        model = models.User
        fields = ('url', 'alias', 'name', 'role', 'email', 'school_id')
