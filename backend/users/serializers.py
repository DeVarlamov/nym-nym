from api.v1.serializers import RecipeSerializer
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from .models import User


class UserRegistrationSerializer(UserCreateSerializer):
    """Сереалайзер регистрации."""

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'password',
                  )


class UserSerializer(serializers.ModelSerializer):
    """Сереалайзер данных юзера."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return bool(
            user.is_authenticated
            and obj.subscribing.filter(user=user).exists()
        )


class SubscribedSerializer(serializers.ModelSerializer):
    """Список обьектов на которые подписан юзер."""
    recipes = serializers.SerializerMethodField(method_name='get_recipes')
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count')

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, object):
        limit = int(self.context['request'].query_params.get(
            'recipes_limit', default=0)
        )
        author_recipes = object.recipes.all()[:limit]
        return RecipeSerializer(
            author_recipes, many=True
        ).data


class SubscribeAuthorSerializer(SubscribedSerializer):
    """Подписка на автора и отписка."""

    def validate(self, obj):
        if self.context['request'].user == obj:
            raise serializers.ValidationError(
                {'errors': 'Нельзя подписаться на себя.'})
        return obj
