from autoslug import AutoSlugField
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    title = models.CharField('Название ингредиента', max_length=55,
                             db_index=True)
    unit = models.CharField('Единица измерения', max_length=10)

    class Meta:
        ordering = ('title',)
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return {self.title}


class Tag(models.Model):
    title = models.CharField('Имя тега', max_length=50, db_index=True)
    display_name = models.CharField('Имя тега для шаблона', max_length=50)
    color = models.CharField('Цвет тега', max_length=50)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_recipes',
                               verbose_name='Автор рецепта')
    title = models.CharField('Название ингредиента', max_length=55,
                             db_index=True)
    image = models.ImageField('Изображение', upload_to='recipes/')
    description = models.TextField('Описание')
    ingredients = models.ManyToManyField(Ingredient,
                                         through='RecipeIngredient',
                                         verbose_name='Ингредиент')
    tags = models.ManyToManyField(Tag, related_name='recipes',
                                  verbose_name='Теги')
    cooking_time = models.PositiveSmallIntegerField('Время приготовления')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True,
                                    db_index=True)
    slug = AutoSlugField(populate_from='title', allow_unicode=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='ingredients_amounts')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField('Количество', max_digits=5,
                                   decimal_places=1)

    class Meta:
        unique_together = ('ingredient', 'recipe')
