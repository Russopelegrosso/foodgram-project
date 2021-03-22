import pdfkit

from decimal import Decimal

from django.db import transaction, IntegrityError
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.template.loader import get_template

from .models import Ingredient, RecipeIngredient, Tag, Recipe


def get_tags():
    return Tag.objects.all()


def get_recipes(tags, recipe_favorites_user=None):
    if recipe_favorites_user:
        filter_param = {
            'recipe_favorites__user': recipe_favorites_user,
            'tags__title__in': tags
        }
    else:
        filter_param = {
            'tags__title__in': tags
        }
    recipes = Recipe.objects.filter(
        **filter_param
    ).select_related(
        'author'
    ).prefetch_related(
        'tags'
    ).distinct()
    return recipes


def get_ingredients(request):
    """
    Parse POST request body for ingredient names and their respective amounts.
    """
    ingredients = {}
    for key, name in request.POST.items():
        if key.startswith('nameIngredient'):
            num = key.split('_')[1]
            ingredients[name] = request.POST[
                f'valueIngredient_{num}'
            ]

    return ingredients


def save_recipe(request, form):

    try:
        with transaction.atomic():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()

            objs = []
            ingredients = get_ingredients(request)
            for name, quantity in ingredients.items():
                ingredient = get_object_or_404(Ingredient, title=name)
                objs.append(
                    RecipeIngredient(
                        recipe=recipe,
                        ingredient=ingredient,
                        quantity=Decimal(quantity.replace(',', '.'))
                    )
                )
            RecipeIngredient.objects.bulk_create(objs)

            form.save_m2m()
            return recipe
    except IntegrityError:
        raise HttpResponseBadRequest


def edit_recipe(request, form, instance):

    try:
        with transaction.atomic():
            RecipeIngredient.objects.filter(recipe=instance).delete()
            return save_recipe(request, form)
    except IntegrityError:
        raise HttpResponseBadRequest


def generate_pdf(template_name, context):

    pdf_options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None
    }
    html = get_template(template_name).render(context)
    return pdfkit.from_string(html, False, options=pdf_options)
