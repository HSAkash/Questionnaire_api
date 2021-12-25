from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    password2 = serializers.CharField(write_only=True,
                                      style={'input_type': 'password',
                                             'placeholder': 'Password'}
                                      )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', 'password2', 'image')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5,
                'style': {'input_type': 'password', 'placeholder': 'Password'}
            },
        }

    def create(self, validated_data):
        password2 = validated_data.pop('password2', None)
        if not validated_data['password'] == password2:
            raise serializers.ValidationError(
                {'password': 'Passwords must match'})
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        password2 = validated_data.pop('password2', None)
        if not instance.check_password(password) and password:
            raise serializers.ValidationError(
                {'password': 'Incorrect password'})
        if password and password2 and instance.check_password(password) and password == password2:
            raise serializers.ValidationError(
                {'password': 'New password must be different from old password'})
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password2)
            user.save()

        return user


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'is_admin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)
