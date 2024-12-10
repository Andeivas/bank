import datetime
import glob
import json
import time
from datetime import date


import os

from aiogram import types, F, Router, Bot
from aiogram.client import bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.methods import send_document
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery, FSInputFile
from aiogram.filters import Command, state
import matplotlib.pyplot as plt
import requests
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()
TOKEN = "7294731861:AAFWSoNcHBM5n5H81pPopGEnEGGM128iEh8"

bot = Bot(token=TOKEN)


class Reg(StatesGroup):
    metal_id = State()
    startDate = State()
    endDate = State()


class Reg1(StatesGroup):
    metal = State()
    sum = State()


class Reg2(StatesGroup):
    metal = State()
    sum = State()


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет! Я могу помочь тебе узнать актуальную цену на дагоценные металлы и курсы валют")
    await msg.answer("Для информации о командах нажмите /info")


@router.message(Command("cod"))
async def cod(msg: Message):
    await msg.answer("456 российский рубль\n"
                     "431 доллар США\n"
                     "451 Евро\n"
                     "0 золото\n"
                     "1 серебро\n"
                     "2 платина\n"
                     "3 паладий\n")


@router.message(Command("info"))
async def info(msg: Message):
    await msg.reply("/cod коды валют \n"
                    "/rub 100 рублей россии\n"
                    "/usd доллар США \n"
                    "/euro Евро\n"
                    "/gold золото\n"
                    "/silver серебро\n"
                    "/platinum платина\n"
                    "/palladium палладий\n"
                    "/catalog памятные монеты\n"
                    "/metal_period_analytic анализ за период\n"
                    "/convert перевод в валюту\n"
                    "/convert1 перевод в белорусские рубли\n")


@router.message(Command("rub"))
async def rub(msg: Message):
    ADRESS = "https://api.nbrb.by/exrates/rates/456"
    response = requests.get(ADRESS).json()
    await msg.answer(str(response['Cur_OfficialRate']))


@router.message(Command("usd"))
async def usd(msg: Message):
    ADRESS = "https://api.nbrb.by/exrates/rates/431"
    response = requests.get(ADRESS).json()
    await msg.answer(str(response['Cur_OfficialRate']))


@router.message(Command("euro"))
async def euro(msg: Message):
    ADRESS = "https://api.nbrb.by/exrates/rates/451"
    response = requests.get(ADRESS).json()
    await msg.answer(str(response['Cur_OfficialRate']))


@router.message(Command("gold"))
async def gold(msg: Message):
    ADRESS = "https://api.nbrb.by/bankingots/prices/0"
    params = {"startDate": date.today(), "endDate": date.today()}
    response = requests.get(ADRESS, params=params).json()
    for item in response:
        await msg.answer("цена золота за грамм на сегодня: " + str(item['Value']))


@router.message(Command("silver"))
async def silver(msg: Message):
    ADRESS = "https://api.nbrb.by/bankingots/prices/1"
    params = {"startDate": date.today(), "endDate": date.today()}
    response = requests.get(ADRESS, params=params).json()
    for item in response:
        await msg.answer("цена серебра за грамм на сегодня: " + str(item['Value']))


@router.message(Command("platinum"))
async def platinum(msg: Message):
    ADRESS = "https://api.nbrb.by/bankingots/prices/2"
    params = {"startDate": date.today(), "endDate": date.today()}
    response = requests.get(ADRESS, params=params).json()
    for item in response:
        await msg.answer("цена платины за грамм на сегодня: " + str(item['Value']))


@router.message(Command("palladium"))
async def palladium(msg: Message):
    ADRESS = "https://api.nbrb.by/bankingots/prices/3"
    params = {"startDate": date.today(), "endDate": date.today()}
    response = requests.get(ADRESS, params=params).json()
    for item in response:
        await msg.answer("цена палладия за грамм на сегодня: " + str(item['Value']))


@router.message(Command("catalog"))
async def catalog(msg: Message):
    await msg.answer("каталог памятных монет: https://www.nbrb.by/today/services/coins/avail/1/print ")


@router.message(Command("metal_period_analytic"))
async def gold_period_analytic(msg: Message):
    main_kb = InlineKeyboardBuilder()
    gold = InlineKeyboardButton(text='💛золото', callback_data='https://api.nbrb.by/bankingots/prices/0')
    silver = InlineKeyboardButton(text='🤍серебро', callback_data='https://api.nbrb.by/bankingots/prices/1')
    platinum = InlineKeyboardButton(text='🩶платина', callback_data='https://api.nbrb.by/bankingots/prices/2')
    palladium = InlineKeyboardButton(text='💙палладий', callback_data='https://api.nbrb.by/bankingots/prices/3')
    main_kb.add(gold, silver, platinum, palladium)
    main_kb = main_kb.as_markup()
    await msg.answer("Выбирите металл для анализа:", reply_markup=main_kb)


@router.callback_query(F.data == 'https://api.nbrb.by/bankingots/prices/0')
async def gold(callback: CallbackQuery, state: FSMContext):
    global Adress1
    Adress1 = 'https://api.nbrb.by/bankingots/prices/0'
    await callback.answer('')
    await callback.message.delete()
    await callback.message.answer('Вы выбрали золото')
    await state.set_state(Reg.startDate)
    await callback.message.answer('Введите дату начала периода YYYY.DD.MM::')


@router.callback_query(F.data == 'https://api.nbrb.by/bankingots/prices/1')
async def gold(callback: CallbackQuery, state: FSMContext):
    global Adress1
    Adress1 = 'https://api.nbrb.by/bankingots/prices/1'
    await callback.answer('')
    await callback.message.delete()
    await callback.message.answer('Вы выбрали серебро')
    await state.set_state(Reg.startDate)
    await callback.message.answer('Введите дату начала периода YYYY.DD.MM::')


@router.callback_query(F.data == 'https://api.nbrb.by/bankingots/prices/2')
async def gold(callback: CallbackQuery, state: FSMContext):
    global Adress1
    Adress1 = 'https://api.nbrb.by/bankingots/prices/2'
    await callback.answer('')
    await callback.message.delete()
    await callback.message.answer('Вы выбрали платину')
    await state.set_state(Reg.startDate)
    await callback.message.answer('Введите дату начала периода YYYY.DD.MM:')


@router.callback_query(F.data == 'https://api.nbrb.by/bankingots/prices/3')
async def gold(callback: CallbackQuery, state: FSMContext):
    global Adress1
    Adress1 = "https://api.nbrb.by/bankingots/prices/3"
    await callback.answer('')
    await callback.message.delete()
    await callback.message.answer('Вы выбрали паладий')
    await state.set_state(Reg.startDate)
    await callback.message.answer('Введите дату начала периода YYYY.DD.MM:')


@router.message(Reg.startDate)
async def reg(msg: Message, state: FSMContext):
    await state.update_data(startDate=msg.text)
    await state.set_state(Reg.endDate)
    await msg.answer("Введите дату окончания периода YYYY.DD.MM: ")


@router.message(Reg.endDate)
async def reg2(msg: Message, state: FSMContext):
    await state.update_data(endDate=msg.text)
    data = await state.get_data()
    date_obj = datetime.datetime.strptime(data["startDate"], '%Y.%m.%d')
    date_obj1 = datetime.datetime.strptime(data["endDate"], '%Y.%m.%d')
    print(date_obj)
    params = {"startDate": date_obj, "endDate": date_obj1}
    response = requests.get(Adress1, params=params).json()

    match Adress1:
        case "https://api.nbrb.by/bankingots/prices/0":
            name = "Золота"

        case "https://api.nbrb.by/bankingots/prices/1":
            name = "серебра"

        case "https://api.nbrb.by/bankingots/prices/2":
            name = "платины"

        case "https://api.nbrb.by/bankingots/prices/3":
            name = "палладия"
    value = []
    Date = []
    count = 0
    for item in response:
        Date.insert(count, item['Date'])
        value.insert(count, item['Value'])
        t = str(item['Date'])
        t = t.replace("T00:00:00", " ")
        await msg.answer("цена " + name + " за грамм на " + t + " составляет : " + str(item['Value']))
        count = count + 1
    print(Date)
    print(value)
    plt.plot(Date, value)
    # plt.show()
    plt.savefig('Figure_1.png')
    chat_id = msg.chat.id
    print(chat_id)
    photo = open('Figure_1.png', 'rb')
    if os.path.isfile('Figure_1.png'):
        print("существует")
    else:
        print("нет")
    await bot.send_document(chat_id, photo)
    # with open(f"Figure_1.png", "rb") as photo_file:
    #    await bot.send_photo(chat_id, photo=photo_file)
    await state.clear()


@router.message(Command("convert"))
async def gold(msg: Message, state: FSMContext):
    await msg.answer('Введите валюту rub, usd, euro')
    await state.set_state(Reg1.metal)


@router.message(Reg1.metal)
async def reg(msg: Message, state: FSMContext):
    await state.update_data(metal=msg.text)
    await state.set_state(Reg1.sum)
    await msg.answer("Введите сумму в беллорусских рублях: ")


@router.message(Reg1.sum)
async def reg(msg: Message, state: FSMContext):
    await state.update_data(sum=float(msg.text))
    await state.set_state(Reg1.sum)
    data = await state.get_data()
    match data["metal"]:
        case "usd":
            name = "https://api.nbrb.by/exrates/rates/431"

        case "euro":
            name = "https://api.nbrb.by/exrates/rates/451"

        case "rub":
            name = "https://api.nbrb.by/exrates/rates/456"
    response = requests.get(name).json()
    if (name == "https://api.nbrb.by/exrates/rates/456"):
        answer = str(round(data["sum"] / float(response['Cur_OfficialRate']) * 100, 3))
    else:
        answer = str(round(data["sum"] / float(response['Cur_OfficialRate']), 3))
    await msg.answer(
        "Сегодня на сумму " + str(data["sum"]) + " белорусских рублей вы можете купить : " + answer + data["metal"])


@router.message(Command("convert1"))
async def gold(msg: Message, state: FSMContext):
    await msg.answer('Введите валюту rub, usd, euro')
    await state.set_state(Reg2.metal)


@router.message(Reg2.metal)
async def reg(msg: Message, state: FSMContext):
    await state.update_data(metal=msg.text)
    await state.set_state(Reg2.sum)
    await msg.answer("Введите сумму в " + msg.text + ":")


@router.message(Reg2.sum)
async def reg(msg: Message, state: FSMContext):
    await state.update_data(sum=float(msg.text))
    await state.set_state(Reg2.sum)
    data = await state.get_data()
    match data["metal"]:
        case "usd":
            name = "https://api.nbrb.by/exrates/rates/431"

        case "euro":
            name = "https://api.nbrb.by/exrates/rates/451"

        case "rub":
            name = "https://api.nbrb.by/exrates/rates/456"
    response = requests.get(name).json()

    if (name == "https://api.nbrb.by/exrates/rates/456"):
        answer = str(round(data["sum"] * float(response['Cur_OfficialRate']) / 100, 3))
    else:
        answer = str(round(data["sum"] * float(response['Cur_OfficialRate']), 3))
    await msg.answer("Сегодня на сумму " + str(data["sum"]) + data[
        "metal"] + " Вы можете купить : " + answer + " Белорусских рублей")


@router.message(Command("Check_palladium"))
async def palladium(msg: Message):
    ADRESS = "https://api.nbrb.by/bankingots/prices/3"
    params = {"startDate": date.today(), "endDate": date.today()}
    response = requests.get(ADRESS, params=params).json()
    for item in response:
        await msg.answer("цена палладия за грамм на сегодня: " + str(item['Value']))


@router.message(Command("Check_gold"))
async def palladium(msg: Message):
    ADRESS = "https://api.nbrb.by/bankingots/prices/0"
    params = {"startDate": date.today(), "endDate": date.today()}
    response = requests.get(ADRESS, params=params).json()

    for item in response:
        await msg.answer("цена золота за грамм на сегодня: " + str(item['Value']))
