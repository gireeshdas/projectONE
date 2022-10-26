from rest_framework.serializers import ModelSerializer
from owner.models import Categories,Products
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=[
            "first_name",
            "last_name",
            "email",
            "username",
            "password",
        ]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CategorySerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)

    class Meta:
        model=Categories
        fields=[
            "id",
            "category_name",
            "is_active"
        ]


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)


    class Meta:
        model=Products
        fields="__all__"

    def create(self,validated_data):
        user=self.context.get("user")
        return Products.objects.create(**validated_data,user=user)