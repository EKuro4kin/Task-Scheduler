from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password



USER_MODEL = get_user_model() # return model User (/core/models.py)

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    def validate(self, attrs):
        password = attrs.get('password')
        password_repeat = attrs.pop('password_repeat')

        try:
            validate_password(password)
        except Exception as e:
            raise serializers.ValidationError({'password': e.messages})

        if password != password_repeat:
            raise serializers.DjangoValidationError('Passwords do non match')
        return attrs

    def create(self, validated_data): # validated_data - имеет тип dict{}
        password = validated_data.get('password')
        hashed_password = make_password(password)
        validated_data['password'] = hashed_password
        instance = super().create(validated_data)
        return instance



    class Meta:
        model = USER_MODEL
        fields = '__all__'
