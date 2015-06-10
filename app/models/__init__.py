from flask import Blueprint

models = Blueprint('models', __name__)

from .shopping_list import ShoppingList
