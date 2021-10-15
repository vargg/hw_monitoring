from datetime import datetime

from rest_framework import serializers

from .utils import DATE_FORMAT


class GetAllUsageSerializer(serializers.Serializer):
    date = serializers.DateTimeField(
        required=False,
        read_only=True,
    )
    cpu = serializers.FloatField(required=False)
    gpu = serializers.FloatField(required=False)
    memory = serializers.FloatField(required=False)
    request_method = serializers.CharField(
        max_length=4,
        required=False,
        read_only=True,
    )

    def to_internal_value(self, data):
        for i in range(len(data)):
            try:
                data[i] = data[i].lower()
            except AttributeError:
                raise serializers.ValidationError(
                    {
                        data[i]: 'Ключи должны задаваться строкой'
                    }
                )
        return data

    def validate(self, data):
        options = [field.field_name for field in self._writable_fields]
        if len(data) < 1:
            raise serializers.ValidationError(
                'Требуется указать минимум один ключ. '
                f'Доступные варианты: {options}'
            )
        for item in data:
            if item not in options:
                raise serializers.ValidationError(
                    f'Ключ "{item}" не поддерживается. '
                    f'Доступные варианты: {options}'
                )
        return data


class DeleteUsageSerializer(serializers.Serializer):
    from_date = serializers.CharField(
        max_length=14,
        required=False,
    )
    until_date = serializers.CharField(
        max_length=14,
        required=False,
    )

    def validate(self, data):
        errors = []
        if len(data) == 1:
            errors.append(
                'При указании периода, требуется задавать обе '
                f'границы: {list(self.fields.keys())}; допускается выполнять '
                'запрос без указания периода.'
            )
        for field in data:
            try:
                datetime.strptime(data[field], DATE_FORMAT)
            except ValueError:
                errors.append(
                    f'Данные в поле {field} указаны неверно. '
                    'Требуемый формат: MM:DD:hh:mm:ss'
                )
        if errors:
            raise serializers.ValidationError(errors)
        return data
