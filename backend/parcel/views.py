from django.shortcuts import render

from .models import Category, Parcel
from .serializers import CategorySerializer, ParcelSerializer
from .paginations import ParcelPagination

from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action

from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend


class ParcelViewSet(viewsets.ModelViewSet):
    """
    Набор представлений для обработки объектов модели Parcel.
    Фильтрация по полям price[null оно или нет], category[по ключу].
	Выборка модели идет по полю created_at и переворачивается.
	Доступные методы GET и POST.
    """
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {'price':['isnull'], 'category':['exact']}
    queryset = Parcel.objects.all().order_by('created_at').reverse()
    serializer_class = ParcelSerializer
    pagination_class = ParcelPagination
    http_method_names = ['get', 'post']

    def list(self, request):
        """
        Получинение списка посылок, связанных с текущим сеансом.
        """
        # Сохранение сессии если ее нет
        if not request.session.session_key:
            request.session.save()

        # Фильтрация посылок, которые связаны с текущим сеансом
        parcels = self.filter_queryset(self.get_queryset())
        parcel_ids = request.session.get('parcel_id', [])
        parcels = parcels.filter(id__in=parcel_ids)

        # Пагинация
        page = self.paginate_queryset(parcels)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)    
        serializer = self.get_serializer(parcels, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Создание новой посылки и связывание её с текущим сеансом.
        """
        # Сохранение сессии если ее нет
        if not request.session.session_key:
            request.session.save()

        # Создание посыли с вылидацией и сохранение идентификатор сеанса
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        parcel_ids = request.session.get('parcel_id', [])
        parcel_ids.append(serializer.data['id'])
        request.session['parcel_id'] = parcel_ids

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Набор представлений для обработки объектов модели Category.
	Выборка модели идет по полю id.
	Доступные методы GET.
    """
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    http_method_names = ['get']

