from rest_framework import serializers

class StringSerializer(serializers.StringRelatedField):
    def to_internal_value(self, value):
        return value