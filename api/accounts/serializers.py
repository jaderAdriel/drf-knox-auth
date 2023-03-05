from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'role', 'gender', 'cpf')
        extra_kwargs = {
            'password' : {'required' : True}
        }


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
    def validate(self, attrs):
        cpf = attrs.get('cpf')
        if User.objects.filter(cpf=cpf).exists():
            raise serializers.ValidationError('User with this CPF already exists')
        
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password')

        if password:
            instance.set_password(password)

        instance = super().update(instance, validated_data)
        return instance
    
class LoginSerializer(serializers.Serializer):
    cpf = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        cpf = attrs.get('cpf')
        password = attrs.get('password')

        if not cpf or not password:
            raise serializers.ValidationError("Please give both cpf and password.")

        if not User.objects.filter(cpf=cpf).exists():
            raise serializers.ValidationError('Cpf does not exist.')

        user = authenticate(request=self.context.get('request'), cpf=cpf,
                            password=password)
        if not user:
            raise serializers.ValidationError("Wrong Credentials.")

        attrs['user'] = user
        
        return attrs