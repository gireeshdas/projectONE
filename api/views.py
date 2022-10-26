from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.

from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import authentication, permissions
from api.serializers import UserSerializer, CategorySerializer, ProductSerializer
from rest_framework.decorators import action
from owner.models import Categories, Products, Carts


class UserModelView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class CategoryView(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        cat = Categories.objects.all()
        serializer = CategorySerializer(cat, many=True)
        return Response(data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def retrive(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Categories.objects.get(id=id)
        serializer=CategorySerializer(qs)
        return Response(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        object = Categories.objects.get(id=id)
        object.delete()
        return Response({"message": "deleted"})

    def update(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        object = Categories.objects.get(id=id)
        serializer = CategorySerializer(instance=object, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class ProductView(ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def list(self, request, query_params=None, *args, **kwargs):
        if "category" in request.query_params:
            id = request.query_params.get("category")
            print(id)
            qs = Products.objects.filter(category_id=id)
            serializer = ProductSerializer(qs, many=True)
        else:
            qs = Products.objects.all()
            serializer = ProductSerializer(qs, many=True)
        return Response(data=serializer.data)

    def retrive(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Products.objects.get(id=id)
        serializer=ProductSerializer(qs)
        return Response(data=serializer.data)

    # product = Products.objects.filter(user=request.user)
        # serializer = ProductSerializer(product, many=True)
       # return Response(data=serializer.data)


    def update(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        object=Products.objects.get(id=id)
        serializer=ProductSerializer(instance=object,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


    def destroy(self, request, *args, **kwargs):
        id=kwargs.get("pk")
        instace=Products.objects.get(id=id)
        instace.delete()
        return Response({"message":"deleted"})






