from .models import CarInfo, RefuelInfo, FuelInfo, ExpenditureInfo, RankingList, CarCareInfo
from rest_framework import serializers


class CarInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarInfo
        fields = '__all__'


class RefuelInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefuelInfo
        fields = '__all__'


class FuelInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelInfo
        fields = '__all__'


class ExpenditureInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenditureInfo
        fields = '__all__'


class RankingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RankingList
        fields = '__all__'


class CarCareInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarCareInfo
        fields = '__all__'
