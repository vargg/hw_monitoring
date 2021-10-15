import pickle

from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import DeleteUsageSerializer, GetAllUsageSerializer
from .utils import (get_current_cpu_usage, get_current_date,
                    get_current_gpu_usage, get_current_memory_usage)

utils = {
    'date': get_current_date,
    'cpu': get_current_cpu_usage,
    'gpu': get_current_gpu_usage,
    'memory': get_current_memory_usage,
}


class CurrentUsageView(APIView):
    def get(self, request):
        values = self.get_values(utils.keys())
        serializer = GetAllUsageSerializer(values)
        result = serializer.data

        self.redis_set_value(request, values)

        return Response(result, status=status.HTTP_201_CREATED)

    def post(self, request):
        serializer = GetAllUsageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        requierd_fields = ['date']
        requierd_fields.extend(serializer.validated_data)
        values = self.get_values(requierd_fields)

        serializer = GetAllUsageSerializer(values)
        result = serializer.data

        self.redis_set_value(request, values)

        return Response(result, status=status.HTTP_201_CREATED)

    def get_values(self, requierd_fields):
        values = dict()
        for item in requierd_fields:
            values[f'{item}'] = utils[f'{item}']()
        return values

    def redis_set_value(self, request, values):
        date = values.pop('date')
        values['request_method'] = request.method
        cache.set(date, pickle.dumps(values))


class UsageView(APIView):
    def get(self, request):
        values = list()
        for key in cache.keys('*'):
            values.append(
                {key: pickle.loads(cache.get(key))}
            )
        print(len(values))
        return Response(values, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DeleteUsageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data:
            keys_to_del = list(filter(
                lambda k: k >= serializer.validated_data['from_date']
                and k <= serializer.validated_data['until_date'],
                cache.keys('*')
            ))
            for key in keys_to_del:
                cache.delete(key)
        else:
            cache.clear()
        return Response(status=status.HTTP_204_NO_CONTENT)
