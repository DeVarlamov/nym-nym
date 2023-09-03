# Generated by Django 3.2.20 on 2023-09-03 17:42

import colorfield.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
                'ordering': ('id',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ImportIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csv_file', models.FileField(upload_to='uploads/')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, error_messages={'unique': 'Такой ингредиент уже есть.'}, max_length=200, verbose_name='Название')),
                ('measurement_unit', models.CharField(choices=[('г', 'граммы'), ('стакан', 'стакан'), ('по вкусу', 'по вкусу'), ('ст. л.', 'столовая ложка'), ('шт.', 'штука'), ('мл', 'миллилитры'), ('кг', 'килограммы'), ('л', 'литры'), ('ч. л.', 'чайная ложка'), ('банка', 'банка'), ('пакетик', 'пакетик'), ('пучок', 'пучок'), ('лист', 'лист'), ('зубчик', 'зубчик'), ('бутылка', 'бутылка'), ('пакет', 'пакет'), ('головка', 'головка'), ('корень', 'корень'), ('брусок', 'брусок'), ('кусочек', 'кусочек'), ('щепотка', 'щепотка'), ('брусочек', 'брусочек'), ('долька', 'долька'), ('чашка', 'чашка'), ('стебель', 'стебель'), ('пластинка', 'пластинка'), ('крошка', 'крошка'), ('кисточка', 'кисточка')], max_length=200, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'ингредиент',
                'verbose_name_plural': 'ингредиенты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='recipe_img/', verbose_name='Изображение блюда')),
                ('name', models.CharField(max_length=200, verbose_name='Название блюда')),
                ('text', models.TextField(verbose_name='Описание')),
                ('cooking_time', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, message='Время приготовления не может быть меньше 1'), django.core.validators.MaxValueValidator(360, message='Время приготовления не может быть больше 360')], verbose_name='Время приготовления, мин')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1, message='Количество ингредиента не может быть нулевым'), django.core.validators.MaxValueValidator(1000, message='Количество ингредиента не может быть больше тысячи')], verbose_name='Количество')),
            ],
            options={
                'verbose_name': 'Ингредиенты в рецепте',
                'verbose_name_plural': 'Ингредиенты в рецептах',
                'ordering': ('recipe',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(error_messages={'unique': 'Тег с таким названием уже существует.'}, max_length=200, unique=True, verbose_name='Название Тега')),
                ('color', colorfield.fields.ColorField(blank=True, default='#ffd057', error_messages={'unique': 'Такой цвет уже существует.'}, image_field=None, max_length=7, null=True, samples=None, unique=True, verbose_name='Цвет в HeX')),
                ('slug', models.SlugField(error_messages={'unique': 'Такой Slug уже существует.'}, max_length=200, unique=True, verbose_name='Уникальный Тег')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ShoppingСart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shoppingсarts', related_query_name='shoppingсarts', to='recipes.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзина',
                'ordering': ('id',),
                'abstract': False,
            },
        ),
    ]
