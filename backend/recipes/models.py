from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from foodgram.settings import (
    INGREDIENT_UNITS,
    LENGTH_FOR_COLOR,
    MAXIMUM_LENGTH,
    MINCOUNT,
)
from users.models import User


class Tag(models.Model):
    """Модель Тегов."""

    name = models.CharField(
        'Название Тега',
        max_length=MAXIMUM_LENGTH,
        unique=True,
        error_messages={
            'unique': 'Тег с таким названием уже существует.',
        },
    )
    color = ColorField(
        'Цвет в HeX',
        max_length=LENGTH_FOR_COLOR,
        unique=True,
        error_messages={
            'unique': 'Такой цвет уже существует.',
        },
        default='#ffd057',
        null=True,
    )
    slug = models.SlugField(
        'Уникальный Тег',
        max_length=MAXIMUM_LENGTH,
        unique=True,
        error_messages={
            'unique': 'Такой Slug уже существует.',
        },
    )

    class Meta:
        ordering = ('name',)
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиент"""
    name = models.CharField(
        'Название',
        max_length=MAXIMUM_LENGTH,
        db_index=True,
        error_messages={
            'unique': 'Такой ингредиент уже есть.',
        },
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=MAXIMUM_LENGTH,
        choices=INGREDIENT_UNITS,
    )

    class Meta:
        ordering = ['name']
        verbose_name = "ингредиент"
        verbose_name_plural = "ингредиенты"
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredients'
            )
        ]

    def __str__(self):
        return f'{self.name},в {self.measurement_unit}'


class ImportIngredient(models.Model):
    """Модель импорта ингридиентов."""

    csv_file = models.FileField(upload_to='uploads/')
    date_added = models.DateTimeField(auto_now_add=True)


class Recipe(models.Model):
    """Модель рецептов."""

    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
    )
    image = models.ImageField(
        'Изображение блюда',
        upload_to='recipe_img/',
    )
    name = models.CharField(
        'Название блюда',
        max_length=MAXIMUM_LENGTH,
    )
    text = models.TextField(
        'Описание',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления, мин',
        default=MINCOUNT,
        validators=[
            MinValueValidator(
                1,
                message='Время приготовления не может быть меньше 1'
            ),
            MaxValueValidator(
                360,
                message='Время приготовления не может быть больше 360'
            )
        ],
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """ Модель связывает Recipe и Ingredient с
    указанием количества ингредиентов.
    """
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Ингредиенты'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        default=MINCOUNT,
        validators=[
            MinValueValidator(
                1,
                message='Количество ингредиента не может быть нулевым'
            ),
            MaxValueValidator(
                1000,
                message='Количество ингредиента не может быть больше тысячи'
            )
        ],
    )

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Ингредиенты в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_combination'
            )
        ]

    def __str__(self):
        return f'{self.recipe} содержит ингредиент/ты {self.ingredient}'


class UserRelation(models.Model):
    """Связь подписок"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        related_query_name='%(class)ss',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        related_query_name='%(class)ss',
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ('id',)
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_%(class)s'
            )
        ]

    def __str__(self):
        return f'{self.user.username} - {self.recipe.id}'


class Favorite(UserRelation):
    """Подписка на избранное"""

    class Meta(UserRelation.Meta):
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingСart(UserRelation):
    """Рецепты в корзине покупок.
    Модель связывает Recipe и User.
    """

    class Meta(UserRelation.Meta):
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
