from aiogram.fsm.state import StatesGroup, State


class Main(StatesGroup):
    MAIN = State()
    TOP_MONEY = State()


class WordleGameMenu(StatesGroup):
    MAIN = State()
    CHOOSE_CATEGORY = State()


class WordleGaming(StatesGroup):
    GAME = State()
    RESULT = State()


class AdminMenu(StatesGroup):
    MAIN = State()


class GuessHeroMenu(StatesGroup):
    GAME = State()
    RESULT = State()


class CategoriesMenu(StatesGroup):
    MAIN = State()
    CATEGORY_MENU = State()


class AddCategoryMenu(StatesGroup):
    INPUT_CATEGORY_NAME = State()
    CONFIRM = State()


class AddWordsInCategory(StatesGroup):
    INPUT_WORDS = State()
    CONFIRM = State()