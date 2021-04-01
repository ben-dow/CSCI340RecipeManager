from src.controllers.util import bcolors, command_input, pretty_print_recipe
from src.models import *
from sqlalchemy.sql import func


def search(app_session):
    print(bcolors.HEADER + "Search for Recipe" + bcolors.ENDC)
    command = ""

    while command != "Exit":
        search_type = command_input(bcolors.BOLD + "How would you like to search?" + bcolors.ENDC,
                                    ["By Ingredient", "By Name", "By Category", "Exit"])
        if search_type == "Exit":
            break

        sort_type = command_input(bcolors.BOLD + "How would you like to sort the search?" + bcolors.ENDC,
                                  ["Name", "Rating", "Recent", "Exit"])
        if sort_type == "Exit":
            break

        command = input("Search Now: ")
        if command == "Exit":
            break

        search_get_results(app_session, command, search_type, sort_type)

    print(bcolors.OKBLUE + "Exiting Recipe Search" + bcolors.ENDC)
    return


def search_get_results(app_session, command, search_type, sort_type):
    if sort_type == "Name":
        sort_order = Recipe.name.asc()
    elif sort_type == "Recent":
        sort_order = Recipe.creation_date.desc()

    if search_type == "By Ingredient":
        if (sort_type != "Rating"):
            # Query for the ingredient id being searched for
            try:
                ingredient_id = app_session.session.query(Ingredient.id).filter(Ingredient.name == command)[0].id
            except IndexError:
                print('It appears that ingredient doesn\'t exist. Try again now:')
                return

            results = app_session.session.query(Recipe) \
                .join(RecipeIngredients) \
                .filter(RecipeIngredients.ingredient_id == ingredient_id) \
                .order_by(sort_order)
        else:
            # Query for the ingredient id being searched for
            try:
                ingredient_id = app_session.session.query(Ingredient.id).filter(Ingredient.name == command)[0].id
            except IndexError:
                print('It appears that ingredient doesn\'t exist. Try again now:')
                return

            results = app_session.session.query(Recipe) \
                .join(RecipeIngredients) \
                .filter(RecipeIngredients.ingredient_id == ingredient_id) \
                .join(CookedBy) \
                .group_by(Recipe).order_by(func.avg(CookedBy.rating).desc())
    elif search_type == "By Name":
        if sort_type != "Rating":
            results = app_session.session.query(Recipe) \
                .filter(Recipe.name == command) \
                .order_by(sort_order)
        else:
            results = app_session.session.query(Recipe) \
                .filter(Recipe.name == command) \
                .join(CookedBy) \
                .group_by(Recipe).order_by(func.avg(CookedBy.rating).desc())
    elif search_type == "By Category":
        if sort_type != "Rating":
            results = app_session.session.query(Recipe) \
                .join(Category) \
                .filter(Category.category_type == command) \
                .order_by(sort_order)
        else:
            results = app_session.session.query(Recipe) \
                .join(Category) \
                .filter(Category.category_type == command) \
                .join(CookedBy) \
                .group_by(Recipe).order_by(func.avg(CookedBy.rating).desc())

    for row in results:
        pretty_print_recipe(row)

    return
