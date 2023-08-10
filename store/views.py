from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, OrderItem, Collection
from .serializers import ProductSerializer, CollectionSerializer


# Create your views here.
class ProductList(ListCreateAPIView):
    queryset = (
        Product.objects.select_related("collection")
        .prefetch_related("promotions")
        .all()
    )
    serializer_class = ProductSerializer

    # def get(self, _):
    #     queryset = (
    #         Product.objects.select_related("collection")
    #         .prefetch_related("promotions")
    #         .all()
    #     )
    #     serializer = ProductSerializer(queryset, many=True)
    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer = ProductSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def get(self, _, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, _, pk):
        product = get_object_or_404(Product, pk=pk)
        if OrderItem.objects.filter(product_id=pk).exists():
            return Response(
                {
                    "error": "Product can not be deleted because it is associated with an order item."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.prefetch_related("product_set").all()
    serializer_class = CollectionSerializer

    # def get(self, _):
    #     queryset = Collection.objects.prefetch_related("product_set").all()
    #     serializer = CollectionSerializer(queryset, many=True)
    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer = CollectionSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


class CollectionDetail(APIView):
    def get(self, _, pk):
        collection = get_object_or_404(Collection, pk=pk)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)

    def put(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        serializer = CollectionSerializer(collection, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, _, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if Product.objects.filter(collection=collection).exists():
            return Response(
                {
                    "error": "Collection can not be deleted because it is associated with one or more products."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
