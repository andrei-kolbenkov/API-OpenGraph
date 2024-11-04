from rest_framework import serializers
from .models import User, Link, Collection
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'last_login')
        read_only_fields = ['date_joined', 'last_login']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('email','password', 'username')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'user']

    def validate_collections(self, value):
        user = self.context['request'].user
        for collection in value:
            if collection.user != user:
                raise serializers.ValidationError("У вас отсутствуют некоторые из указанных коллекций")
        return value

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        if self.instance is None:  # Создание
            extra_kwargs.update({
                'title': {'read_only': True},
                'description': {'read_only': True},
                'image_url': {'read_only': True},
                'link_type': {'read_only': True},
                'collections': {'read_only': True},
            })
        else:  # Обновление
            extra_kwargs.update({
                'title': {'read_only': False},
                'description': {'read_only': False},
                'image_url': {'read_only': False},
                'link_type': {'read_only': False},
                'collections': {'read_only': False},
            })
        return extra_kwargs



class CollectionSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ('__all__')
        read_only_fields = ['created_at', 'updated_at', 'user']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True, required=True)
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not check_password(value, user.password):
            raise serializers.ValidationError("Текущий пароль неверен.")
        return value

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Новый пароль должен содержать минимум 8 символов.")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()


