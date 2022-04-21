# This code matches a list of ingredients with ingredients in a recipe and tells you which ones you have to go buy
# still working on extending functionality search

import requests
import json
import urllib
from random import randint
from itertools import compress

# ID set is used to ensure all recipes have unique ID
IDS = {-1}
APP_ID = "a395a114"
API_KEY = "8a66976d95a0a0fe1b484360704840a6"
URL = f'https://api.edamam.com/search?/app_id=${APP_ID}&app_key=${API_KEY}'


def main():
    """
    This program allows the user to search for recipes online using the
    Edamam API.
    """

    command = ''
    fridge2 = input('Write a list of the food you have on your fridge here and separated by a coma and a space:')
    fridge_food = fridge2.split(', ')
    _from = 0
    to = 100

    while command.lower() != 'q':
        print("\n1) Find New Recipe based on a keyword\n\t1a) More Results (can only be selected after once selecting 1) \n2)Append the fridge list \n\n'q' to quit \n")
        command = input("\t>> ")
        print(f'You have following items in your fridge: {fridge_food}\n')
        if command == '1':
            _from = 0
            to = 100
            print("Please enter a keyword")
            global key_word
            key_word = input("\t>> ")
            query_recipes(key_word, _from, to, fridge_food)

        elif command == '1a':
            try:
                _from += 100
                to += 100
                query_recipes(key_word, _from, to, fridge_food)
            except NameError:
                print('Please first choose option 1 to enter a keyword.\n')
                continue

        elif command == '2':
            append_fridge_food(fridge_food)


def query_recipes(key_word, _from, to, fridge_food):
    response = None
    success = False
    index = 0
    while not success:
        data = make_request(get_url_q(key_word, _from, to))
        data = data['hits']
        if len(data) > 0:
            success = True
        else:
            print(f'0 results for "{key_word}"')
            input("")

        if len(sort_recipes(data, fridge_food)) <= 20:
            print('We run out of recipes.')
            continue
        n = 0
        for recipe_index in sort_recipes(data, fridge_food)[0:20]:
            n += 1
            recipe = data[recipe_index]
            # From here down, this is what is going to be printed for the recipies any addition to interface, please add below this line
            print(
                f'{n} {get_name(recipe)} you have {sum(food_match(fridge_food, recipe))}/{len(food_match(fridge_food, recipe))} of the ingredients for this recipe')
            print(shopping_list(fridge_food, recipe))
            print(get_url(recipe))
            print('---------------------------------------\n')

        # show specific information about a recipe
        more = 'yes'
        while more == 'yes' and index !='none' :
            index = input("which recipe do you want more information on (write none to continue)")
            if index == 'none':
                continue
            print(sort_recipes(data, fridge_food)[int(index)])
            recipe = data[sort_recipes(data, fridge_food)[int(index) - 1]]
            print(get_name(recipe), '\n')
            print(get_url(recipe), '\n')
            get_instructions(recipe)
            print(get_food_in_recipe_percetage(fridge_food, recipe), '\n')
            print(show_more(recipe), '\n')
            more = input('Do you want to change the recipe you see? enter yes or no')


def show_more(recipe):
    while True:
        n = 0
        for i in list(recipe["recipe"].keys())[6:]:
            n += 1
            print(n, i)
        index1 = input("\nplease select a number from the list above to see more information regarding the recipe, q to quit: ")
        if index1 not in str(list(range(1, 16))):
            break

        print('\n', list(recipe["recipe"].keys())[int(index1) + 5], ': ',
              recipe['recipe'][str(list(recipe["recipe"].keys())[int(index1) + 5])], "\n")


def shopping_list(fridge_food, recipe):
    food_in_recipe = food_match(fridge_food, recipe)
    shop_items = list(compress(get_food(recipe), [not elem for elem in food_in_recipe]))
    if len(shop_items) == 0:
        print("You have all the ingredients you need for this recipe")
        return shop_items
    return shop_items


def food_match(fridge_food, recipes):
    food_in_recipe = []
    for food in get_food(recipes):
        if " " in food:
            for i in food.split():
                if i in fridge_food:
                    food_in_recipe.append(True)
                    break
                elif i == food.split()[-1]:
                    food_in_recipe.append(False)

        else:
            food_in_recipe.append(food in fridge_food)

    return food_in_recipe


def get_url(recipe):
    return recipe['recipe']['url']


def get_name(recipe):
    return recipe['recipe']['label']


def get_food(recipes):
    ingredients_list = []
    for food in recipes["recipe"]["ingredients"]:
        ingredients_list.append(food["food"])
    return ingredients_list


def get_food_in_recipe_percetage(fridge_food, recipe):
    return sum(food_match(fridge_food, recipe)) / len(food_match(fridge_food, recipe))


def sort_recipes(data, fridge_food):
    sorted_recipes = {}
    n = 0
    for recipe in data:
        sorted_recipes[n] = [get_food_in_recipe_percetage(fridge_food, recipe) * 100]
        n += 1
    return list(dict(sorted(sorted_recipes.items(), key=lambda item: item[1], reverse=True)).keys())


def append_fridge_food(fridge_food):
    _input = ''
    while _input != 'end':
        _input = input('Add other item, if you want to delete the list type clear, if you are done with adding items type end: ')
        if _input == 'end':
            break
        elif _input == 'clear':
            fridge_food.clear()
            break
        fridge_food.append(_input)
    return fridge_food


def get_instructions(recipe):
    for instruction in recipe['recipe']['ingredientLines']:
        print(instruction)


"""-----------------------MAKE REQUESTS--------------------------"""


def make_request(url):
    """
    Returns a request response from a given URL.
    """
    response = requests.get(url)
    data = response.json()
    return data


def get_url_q(key_word, _from, to):
    url = URL + f'&q=${key_word}&to={to}&from={_from}'
    return url


def get_url_r(uri):
    return URL + f'&r={uri}'


main()