import asyncio
import collections
import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.message import ContentType
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery, ParseMode
from aiogram.utils import executor
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import threading
import psycopg2
from itertools import groupby


CREDENTIALS_FILE = 'provinciabottestproject-1d4b7c3d0c96.json'
credentials = Credentials.from_service_account_file('provinciabottestproject-1d4b7c3d0c96.json', scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
service = build('sheets', 'v4', credentials=credentials)
spreadsheetId = '1XbHmp2M04M2bsIaIRO1c7rxw-paDOct9B5-GahE7RWI'
bot = Bot(token='5474610554:AAFIsFI6ArPJmptuufE0kSSEGfnt4dfl1wI', parse_mode=types.ParseMode.MARKDOWN_V2)
PAYMENT_TOKEN = '410182388:LIVE:8ce102a6-6eb4-44e2-9cac-f84cfa5d77e0'
# live token -> 410182388:LIVE:74cc3263-ef7f-4d39-9053-4264397a4e38
# test token -> 401643678:TEST:875c0804-9a8e-46ba-925b-f99a2e12b398
# live work token -> 410182388:LIVE:8ce102a6-6eb4-44e2-9cac-f84cfa5d77e0
# test юкасса -> 381764678:TEST:43602
# bot token -> 5474610554:AAFIsFI6ArPJmptuufE0kSSEGfnt4dfl1wI
bot.parse_mode = 'HTML'
loop = asyncio.new_event_loop()
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
connect = psycopg2.connect(dbname='usersdb', user='postgres',
                           password='123321', host='localhost')
cursor = connect.cursor()
this_month = datetime.today().date().month - 1
this_year = 2022
this_day = datetime.today().date().day - 1
work_shift = True
months = {"1": "Январь-Февраль", "2": "Февраль-Март", "3": "Март-Апрель", "4": "Апрель-Май", "5": "Май-Июнь", "6": "Июнь-Июль", "7": "Июль-Август", "8": "Август-Сентябрь", "9": "Сентябрь-Октябрь", "10": "Октябрь-Ноябрь", "11": "Ноябрь-Декабрь", "12": "Декабрь-Январь"}
list_name = f'Статистика BurgerTek Полярный {months[f"{this_month}"]}'
cursor.execute("SELECT deliveryprice FROM tech_info")
delivery_price = cursor.fetchone()[0]
cursor.execute("SELECT interval FROM tech_info")
interval_time = cursor.fetchone()[0]
fifteenPercent = 0


class AddToMenu(StatesGroup):
    name = State()
    type = State()
    price = State()
    description = State()
    photo = State()


class ChangeDeliveryPrice(StatesGroup):
    newprice = State()


class Iamboss(StatesGroup):
    password = State()


class ChangeIntervalTime(StatesGroup):
    newinterval = State()


class ProfileInfo(StatesGroup):
    people = State()


class Decline(StatesGroup):
    reason = State()


class Help(StatesGroup):
    text = State()


class UserAddress(StatesGroup):
    text = State()


class Ivent(StatesGroup):
    format = State()
    amount = State()
    date = State()


class Time(StatesGroup):
    text = State()


class Comment(StatesGroup):
    text = State()


class Form(StatesGroup):
    name = State()
    phone = State()
    address = State()
    mail = State()


class Deletedata(StatesGroup):
    password = State()


class Review(StatesGroup):
    text = State()


def setInterval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()
            def loop(): # executed in another thread
                while not stopped.wait(interval): # until stopped
                    function(*args, **kwargs)
            t = threading.Thread(target=loop)
            t.daemon = True # stop if the program exits
            t.start()
            return stopped
        return wrapper
    return decorator


@setInterval(60)
def printer():
    cursor.execute(f"SELECT ID FROM orders WHERE StartCooking='{datetime.now().strftime('%H:%M')}' AND deliveryType=0")
    users_orders = cursor.fetchall()
    if len(users_orders) > 0:
        for i in range(len(users_orders)):
            cursor.execute(f"UPDATE orders SET deliveryType='1' WHERE ID={users_orders[i][0]}")
            connect.commit()


stop = printer()


@dp.message_handler(chat_type='private', commands=['start'])
async def start(message: types.Message):
    await message.answer(
        f"Добрый день! Я - Бот для заказа в “BurgerTek”. Я помогу Вам заказать любимую еду, корпоратив,"
        f" оставить отзыв и многое другое.", parse_mode=ParseMode.HTML)
    cursor.execute(f"SELECT * FROM login_id WHERE ID={message.chat.id}")
    temp = cursor.fetchone()
    if temp:
        await hello_menu(message)
    else:
        await Form.name.set()
        await message.answer("Для начала работы нужно пройти простую регистрацию. Как к Вам можно обращаться?⬇")


@dp.message_handler(chat_type='private', commands='Iambosshere')
async def Iambosshere(message: types.Message):
    await Iamboss.password.set()
    await message.answer('Введите пароль.')


@dp.message_handler(state=Iamboss.password)
async def bosspassword(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pass'] = message.text
    await state.finish()
    if data['pass'] == '177355':
        cursor.execute(f"UPDATE login_id SET Role=4 WHERE ID={message.chat.id}")
        connect.commit()
        await message.answer('Теперь Вы тут Big Boss')
        await boss_menu(message)
    else:
        await message.answer('Неверный пароль(')


@dp.message_handler(state=Form.name)
async def reg_ph(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Form.next()
    await message.answer(f"Укажите свой номер телефона. Это нужно нашим курьерам.⬇", parse_mode=ParseMode.HTML)


@dp.message_handler(lambda message: message.text, state=Form.phone)
async def process_age(message: types.Message, state: FSMContext):
    await Form.next()
    await state.update_data(phone=message.text)
    await message.answer("Отлично! Укажите свой адрес для доставки⬇")


@dp.message_handler(state=Form.address)
async def process_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['addres'] = message.text
    await Form.next()
    await message.answer("Супер! И последнее, Ваш адрес электронной почты. Это не обязательно, можете ввести любой символ⬇", parse_mode=ParseMode.HTML)


@dp.message_handler(state=Form.mail)
async def enter_mail(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['mail'] = message.text
        cursor.execute(f"INSERT INTO login_id (ID, Имя, Телефон, Адрес, role, Почта) VALUES ({message.chat.id},'{data['name']}','{data['phone']}','{data['addres']}',0,'{data['mail']}')")
        connect.commit()
        cursor.execute(f"INSERT INTO cart_data VALUES({message.chat.id},'отсутствует','отсутствует','отсутствует','отсутствует','отсутствует','отсутствует','отсутствует',0)")
        connect.commit()
    await state.finish()
    await hello_menu(message)


@dp.message_handler(Text(equals='В предыдущее меню↩'), chat_type='private')
async def hello_menu(message: types.Message):
    cursor.execute(f"SELECT menuStatus FROM login_id WHERE ID='{message.chat.id}'")
    if cursor.fetchone()[0] == '1':
        cursor.execute(f"SELECT menuMessage FROM login_id WHERE ID='{message.chat.id}'")
        user_message = cursor.fetchone()[0].split(',')
        for i in range(len(user_message)):
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=int(user_message[i]))
            except:
                pass
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('Заказать корпоратив 🎉', callback_data='order_ivent'))
    keyboard.add(types.InlineKeyboardButton('Наши отзывы 📝', callback_data=f'our_reviews'))
    keyboard.add(types.InlineKeyboardButton('Перейти в главное меню📍', callback_data='main__menu'))
    keyboard.add(types.InlineKeyboardButton('Скачать меню в pdf 📥', callback_data='download_pdf'))
    sended_message = await message.answer("Мы рады видеть Вас в нашем боте.\nНаш телефон: 89318010002\nНаше местоположение: г. Полярный, ул. Гаджиева, 11,возле ТЦ Коровник."
                                          "\nПриятного аппетита 😋", reply_markup=keyboard)
    cursor.execute(
        f"UPDATE login_id SET menuStatus='1', menuMessage='{sended_message.message_id}' WHERE ID='{message.chat.id}'")
    connect.commit()


@dp.callback_query_handler(Text(equals='download_pdf'))
async def down_pdf(callback: types.CallbackQuery):
    doc = open('photo_5257953780887043451_y.pdf', 'rb')
    await bot.send_document(chat_id=callback.message.chat.id, document=doc)


@dp.callback_query_handler(Text(equals='order_ivent'))
async def order__ivent(callback: types.CallbackQuery):
    global work_shift
    cursor.execute(f"SELECT Имя FROM login_id WHERE ID={callback.message.chat.id}")
    ban_or_not = cursor.fetchone()
    if ban_or_not[0] == 'Banned':
        await callback.message.answer('Вы были забанены')
    else:
        await callback.message.delete()
        await Ivent.format.set()
        await callback.message.answer('Наш ресторан занимается организацией кейтеринга для Ваших мероприятий и праздников. Если Вы хотите воспользоваться этой услугой, укажите формат мероприятия⬇')


@dp.message_handler(state=Ivent.format)
async def give_format(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['format'] = message.text
    await Ivent.next()
    await message.answer('Какое количество людей ожидается?⬇')


@dp.message_handler(state=Ivent.amount)
async def give_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
    await Ivent.next()
    await message.answer('На какую дату планируете мероприятие?⬇')


@dp.message_handler(state=Ivent.date)
async def give_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['date'] = message.text
    await state.finish()
    cursor.execute(f"SELECT Телефон FROM login_id WHERE ID={message.chat.id}")
    tmp = cursor.fetchone()
    await bot.send_message(-1001547432335, f"Был заказан корпоратив.\nФормат: {data['format']}\n"
                                       f"Количество человек: {data['amount']}\nДата: {data['date']}\nНомер: {tmp[0]}")
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('Заказать корпоратив 🎉', callback_data='order_ivent'))
    keyboard.add(types.InlineKeyboardButton('Наши отзывы 📝', callback_data=f'our_reviews'))
    keyboard.add(types.InlineKeyboardButton('Перейти в главное меню📍', callback_data='main__menu'))
    keyboard.add(types.InlineKeyboardButton('Скачать меню в pdf 📥', callback_data='download_pdf'))
    sended_message = await message.answer('Отлично! Наш менеджер @ник, скоро с Вами свяжется для уточнения деталей.', reply_markup=keyboard)
    cursor.execute(
        f"UPDATE login_id SET menuStatus='1', menuMessage='{sended_message.message_id}' WHERE ID='{message.chat.id}'")
    connect.commit()


@dp.callback_query_handler(Text(equals='main__menu'))
async def to_main_menu(callback: types.CallbackQuery):
    await callback.message.delete()
    cursor.execute(
        f"UPDATE login_id SET menuMessage='NULL', menuStatus='NULL' WHERE ID='{callback.message.chat.id}'")
    connect.commit()
    await main_menu(callback.message)


@dp.message_handler(Text(equals='Тех. Поддержка🆘'), chat_type='private')
async def support(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('Позвоню', callback_data='calltosupport'))
    keyboard.add(types.InlineKeyboardButton('Напишу текстом', callback_data='texttosupport'))
    await message.answer('Мы сожалеем о том, что Вам пришлось столкнуться с трудностями.'
                         ' Вы можете позвонить по телефону 89318010002 или описать проблему текстом, нажав на соответствующие кнопки.', reply_markup=keyboard)


@dp.callback_query_handler(Text(equals='calltosupport'))
async def calltosupport(callback: types.CallbackQuery):
    await callback.message.answer('Будем ждать ваш звонок.')
    await asyncio.sleep(1.5)
    await callback.message.edit_text('Перенаправляю вас в главное меню. 3')
    await asyncio.sleep(1)
    await callback.message.edit_text('Перенаправляю вас в главное меню. 2')
    await asyncio.sleep(1)
    await callback.message.edit_text('Перенаправляю вас в главное меню. 1')
    await asyncio.sleep(1)
    await callback.message.delete()
    await main_menu(callback.message)


@dp.callback_query_handler(Text(equals='texttosupport'))
async def texttosupport(callback: types.CallbackQuery):
    await Help.text.set()
    await asyncio.sleep(0.5)
    await callback.message.answer('Опишите свою проблему ниже⬇')


@dp.message_handler(state=Help.text)
async def after_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await asyncio.sleep(0.5)
    await state.finish()
    async with state.proxy() as tekst:
        tekst['ttt'] = data['text']
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('По телефону', callback_data=f"support_conn Телефон"))
    keyboard.add(types.InlineKeyboardButton('По почте', callback_data=f"support_conn Почта"))
    await message.answer('Выберите как с вами лучше связаться: ', reply_markup=keyboard)
    cursor.execute(
        f"UPDATE login_id SET menuStatus='1', menuMessage='{message.message_id + 1}' WHERE ID='{message.chat.id}'")
    connect.commit()


@dp.callback_query_handler(Text(startswith='support_conn'))
async def send_to_chat(callback: types.CallbackQuery, state: FSMContext):
    cursor.execute(
        f"UPDATE login_id SET menuMessage='NULL', menuStatus='NULL' WHERE ID='{callback.message.chat.id}'")
    connect.commit()
    async with state.proxy() as tekst:
        text = tekst['ttt']
    temp = callback.data.split(' ')[1]
    cursor.execute(f"SELECT {temp}, Имя FROM login_id WHERE ID={callback.message.chat.id}")
    tmp = cursor.fetchone()
    await bot.send_message(-1001547432335, f'Пришёл запрос в тех. поддержку от пользователя:'
                                      f'{callback.message.chat.id}\nИмя: {tmp[1]}\nТекст:\n' + text +
                           '\nПользователь попросил связаться с ним с помощью: \n' + temp +
                           f"\n{tmp[0]}")
    await state.finish()
    await asyncio.sleep(0.5)
    await callback.message.edit_text('В течение нескольких минут с Вами свяжутся.  В ином случае, можете обратиться к менеджеру @ник напрямую. Спасибо за понимание!')
    await main_menu(callback.message)


@dp.callback_query_handler(Text(startswith='info_changer'))
async def process_callback_add(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await ProfileInfo.people.set()
    if callback.data.split(' ')[1] != 'Почта':
        await callback.message.answer(f"Введите {callback.data.split(' ')[1]}")
        await callback.answer()
    else:
        await callback.message.answer("Введите Почту")
        await callback.answer()
    async with state.proxy() as parametr:
        parametr['change'] = callback.data.split(' ')[1]


@dp.message_handler(Text(equals='Редактировать профиль✏'), chat_type='private')
async def change_profile(message: types.Message):
    cursor.execute(f"SELECT menuStatus FROM login_id WHERE ID='{message.chat.id}'")
    if cursor.fetchone()[0] == '1' and message.text == 'Редактировать профиль✏':
        cursor.execute(f"SELECT menuMessage FROM login_id WHERE ID='{message.chat.id}'")
        user_message = cursor.fetchone()[0].split(',')
        for i in range(len(user_message)):
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=int(user_message[i]))
            except:
                pass
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    info = ['Имя', 'Телефон', 'Адрес', 'Почта']
    buttons = []
    cursor.execute(f"SELECT Имя, Телефон, Адрес, Почта FROM login_id WHERE ID={message.chat.id}")
    tmp = cursor.fetchone()
    for i in range(len(tmp)):
        buttons.append(types.InlineKeyboardButton(f"{info[i]}: {tmp[i]}",
                                                  callback_data=f"info_changer {info[i]} {message.chat.id}"))
    buttons.append(types.InlineKeyboardButton("Вернуться в меню", callback_data="info_back"))
    keyboard.add(*buttons)
    sended_message = await message.answer(f"Выберите тип данных для изменения", reply_markup=keyboard)
    cursor.execute(
        f"UPDATE login_id SET menuStatus='1', menuMessage='{sended_message.message_id}' WHERE ID='{message.chat.id}'")
    connect.commit()


@dp.callback_query_handler(Text(equals="info_back"))
async def process_callback_result(callback: types.CallbackQuery):
    cursor.execute(
        f"UPDATE login_id SET menuMessage='NULL', menuStatus='NULL' WHERE ID='{callback.message.chat.id}'")
    connect.commit()
    await callback.message.delete()
    await main_menu(callback.message)
    await callback.answer()


@dp.message_handler(state=ProfileInfo.people)
async def info_changer(message: types.Message, state: FSMContext):
    async with state.proxy() as parametr:
        text = parametr['change']
    await state.finish()
    async with state.proxy() as data:
        data['text'] = message.text
    cursor.execute(f"UPDATE login_id SET {text}='{data['text']}' WHERE ID='{message.chat.id}'")
    connect.commit()
    await state.finish()
    await message.answer('Данные успешно изменены')


@dp.message_handler(Text(equals='Статус заказа🔍'), chat_type='private')
async def check_status(message: types.Message):
    cursor.execute(f"SELECT ID, Status, List FROM orders WHERE User_ID={message.chat.id} AND Status!='Завершён' AND Status!='Отменён'")
    orders = cursor.fetchall()
    if orders:
        temp = []
        stroka = ''
        for j in range(len(orders)):
            temp.append(orders[j][2])
        spisok = [el for el, _ in groupby(temp)]
        for z in range (len(spisok)):
            stroka = stroka + '\n' + f'{z}. ' + str(spisok[z]) + ' - ' + str(collections.Counter(spisok)[f'{spisok[z]}']) + ' шт.'
        for i in range(len(orders)):
            text = interval_time
            await asyncio.sleep(0.5)
            await message.answer(f'Номер заказа: {orders[i][0]}\nЗаказ: {stroka}\nСтатус: {orders[i][1]}\nПримерное время ожидания заказа {text} минут')
    else:
        await message.answer('У вас сейчас нет активных заказов')


@dp.message_handler(chat_type='private', commands='givemerole')
async def give_role(message: types.Message):
    cursor.execute(f"UPDATE login_id SET Role=-1 WHERE ID={message.chat.id}")
    connect.commit()
    await message.answer("Вы успешно подали заявку на вступление в персонал.")


@dp.callback_query_handler(Text(equals='add_to_menu'))
async def add_to_menu(callback: types.CallbackQuery):
    await callback.message.delete()
    cursor.execute(f"SELECT Role FROM login_id WHERE ID={callback.message.chat.id}")
    role = cursor.fetchone()
    if role[0] == 4:
        await AddToMenu.name.set()
        await callback.message.answer('Введите название добавляемого блюда')
    else:
        await callback.message.answer("К сожалению, у вас недостаточно прав для команды администратора(")


@dp.message_handler(state=AddToMenu.name)
async def take_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await AddToMenu.next()
    await message.answer('Введите тип блюда.')


@dp.message_handler(state=AddToMenu.type)
async def take_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = message.text
    await AddToMenu.next()
    await message.answer('Введите цену блюда.')


@dp.message_handler(state=AddToMenu.price)
async def take_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)
    await AddToMenu.next()
    await message.answer('Пришлите описание блюда')


@dp.message_handler(state=AddToMenu.description)
async def take_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['desc'] = message.text
    await AddToMenu.next()
    await message.answer('Пришлите фотографию блюда')


@dp.message_handler(state=AddToMenu.photo, content_types='photo')
async def take_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        photo_id = message.photo[0].file_id
        data['photo'] = photo_id
    await state.finish()
    cursor.execute(f"INSERT INTO menu (Name, Price, Type, Photo, Description) VALUES ('{data['name']}','{data['price']}','{data['type']}','{data['photo']}','{data['desc']}')")
    connect.commit()
    await message.answer('Блюдо успешно добавлено')
    cursor.execute(
        f"UPDATE login_id SET menuMessage='NULL', menuStatus='NULL' WHERE ID='{message.chat.id}'")
    connect.commit()
    await boss_menu(message)


@dp.callback_query_handler(Text(equals='delete__from_menu'))
async def delete_from_menu_types(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass
    cursor.execute(f"SELECT menuStatus FROM login_id WHERE ID='{callback.message.chat.id}'")
    status = cursor.fetchone()[0]
    cursor.execute("SELECT DISTINCT Type FROM menu")
    tmp = cursor.fetchall()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for i in range(len(tmp)):
        keyboard.add(types.InlineKeyboardButton(tmp[i][0], callback_data=f"delete_from_menu_types {tmp[i][0]}"))
    keyboard.add(types.InlineKeyboardButton('Назад ↩', callback_data='back_to_boss'))
    await callback.message.answer('Выберите категорию:', reply_markup=keyboard)
    if status == '1' and callback.message.text == 'Меню🍽':
        cursor.execute(f"SELECT menuMessage FROM login_id WHERE ID='{callback.message.chat.id}'")
        user_message = cursor.fetchone()[0].split(',')
        for i in range(len(user_message)):
            try:
                await bot.delete_message(chat_id=callback.message.chat.id, message_id=int(user_message[i]))
            except:
                pass
    cursor.execute(
        f"UPDATE login_id SET menuStatus='1', menuMessage='{callback.message.message_id + 1}' WHERE ID='{callback.message.chat.id}'")
    connect.commit()


@dp.callback_query_handler(Text(startswith='delete_from_menu_types'))
async def delete_from_menu_choise(callback: types.CallbackQuery, state: FSMContext):
    name = callback.data.split(' ')[1]
    cursor.execute(f"SELECT Name,ID FROM menu WHERE Type='{name}'")
    tmp = cursor.fetchall()
    async with state.proxy() as data:
        data['type'] = name
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for i in range(len(tmp)):
        keyboard.add(types.InlineKeyboardButton(tmp[i][0], callback_data=f"delete_item {tmp[i][1]}"))
    keyboard.add(types.InlineKeyboardButton('Назад ↩', callback_data="types_to_delete_return"))
    await callback.message.edit_text(text='Выберите какое блюдо хотите удалить.', reply_markup=keyboard)
    cursor.execute(f"UPDATE login_id SET menuMessage='{callback.message.message_id}' WHERE ID='{callback.message.chat.id}'")
    connect.commit()
    await callback.answer()


@dp.callback_query_handler(Text(startswith='types_to_delete_return'))
async def go_back_to_delete(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy():
        await state.finish()
    await callback.answer('Вы были перемещены назад.')
    await callback.message.delete()
    await delete_from_menu_types(callback)


@dp.message_handler(chat_type='private', commands='Bossmenu')
async def boss_menu(message: types.Message):
    cursor.execute(f"SELECT Role FROM login_id WHERE ID={message.chat.id}")
    role = cursor.fetchone()
    if role[0] == 4:
        cursor.execute(f"SELECT menuStatus FROM login_id WHERE ID='{message.chat.id}'")
        status = cursor.fetchone()[0]
        if status == '1' and message.text.lower() == '/bossmenu':
            cursor.execute(f"SELECT menuMessage FROM login_id WHERE ID='{message.chat.id}'")
            user_message = cursor.fetchone()[0].split(',')
            for i in range(len(user_message)):
                try:
                    await bot.delete_message(chat_id=message.chat.id, message_id=int(user_message[i]))
                except:
                    pass
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton('Удалить блюдо из меню', callback_data='delete__from_menu'))
        keyboard.add(types.InlineKeyboardButton('Добавить блюдо в меню', callback_data='add_to_menu'))
        keyboard.add(types.InlineKeyboardButton('Отменить заказ', callback_data='cancel_order'))
        keyboard.add(types.InlineKeyboardButton('Изменить роль среди персонала', callback_data='take_user'))
        keyboard.add(types.InlineKeyboardButton('Забанить пользователя', callback_data='ban_user'))
        keyboard.add(types.InlineKeyboardButton('Краткая статистика', callback_data='shortstat'))
        keyboard.add(types.InlineKeyboardButton('Изменить сумму доставки', callback_data='change_delivery_price'))
        keyboard.add(types.InlineKeyboardButton('Управление оплатой', callback_data='ban_payment_type'))
        keyboard.add(types.InlineKeyboardButton('Промоакции', callback_data='promo_list'))
        keyboard.add(types.InlineKeyboardButton('Изменить интервал доставки', callback_data='change_interval'))
        sended_message = await message.answer('Выберите опцию.', reply_markup=keyboard)
        cursor.execute(
            f"UPDATE login_id SET menuStatus='1', menuMessage='{sended_message.message_id}' WHERE ID='{message.chat.id}'")
        connect.commit()
    else:
        await message.answer('у вас недостаточно прав')


@dp.callback_query_handler(Text(equals='change_interval'))
async def change_interval(callback: types.CallbackQuery):
    await callback.message.delete()
    await ChangeIntervalTime.newinterval.set()
    await callback.message.answer('Введите новый интервал минутах в формате xx-xx (без указания минут)')


@dp.message_handler(state=ChangeIntervalTime.newinterval)
async def new_interval_time(message: types.Message, state: FSMContext):
    global interval_time
    async with state.proxy() as data:
        data['newinterval'] = message.text
    cursor.execute(f"UPDATE tech_info SET interval='{data['newinterval']}' WHERE interval='{interval_time}'")
    connect.commit()
    interval_time = str(data['newinterval'])
    await state.finish()
    await message.answer('Интервал успешно изменён')


@dp.callback_query_handler(Text(startswith='ban_type '))
async def ban_type(callback: types.CallbackQuery):
    banType = callback.data.split(' ')[1]
    cursor.execute(f"SELECT available FROM payments WHERE name='{banType}'")
    access = cursor.fetchone()[0]
    if access is False:
        cursor.execute(f"UPDATE payments SET available={True} WHERE name='{banType}'")
    else:
        cursor.execute(f"UPDATE payments SET available={False} WHERE name='{banType}'")
    connect.commit()
    await callback.answer('Операция успешно выполнена')
    await callback.message.delete()
    await boss_menu(callback.message)


@dp.callback_query_handler(Text(equals='ban_payment_type'))
async def ban_payment_type(callback: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('Картой на месте', callback_data='ban_type cardonplace'))
    keyboard.add(types.InlineKeyboardButton('Наличными курьеру', callback_data='ban_type cashoncurier'))
    keyboard.add(types.InlineKeyboardButton('Картой курьеру', callback_data='ban_type cardoncurier'))
    keyboard.add(types.InlineKeyboardButton('Наличными на месте', callback_data='ban_type cashonplace'))
    keyboard.add(types.InlineKeyboardButton('Перевод на карту', callback_data='ban_type cardtransfer'))
    keyboard.add(types.InlineKeyboardButton('Картой в телеграме', callback_data='ban_type cardintelegram'))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data="promo_list_back"))
    await callback.message.edit_text(text='Выберите тип оплаты для блокировки/разблокировки', reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(Text(equals='promo_list'))
async def promo_list(callback: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('Скидка 15% на сумму заказа', callback_data="promo_list 1"))
    keyboard.add(types.InlineKeyboardButton('Назад', callback_data="promo_list_back"))
    await callback.message.edit_text(text='Выберите промоакцию для активации/отмены', reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(Text(startswith='promo_list '))
async def promo_list_activate(callback: types.CallbackQuery):
    promo_num = callback.data.split(' ')[1]
    global fifteenPercent
    if promo_num == '1':
        fifteenPercent = 1 if fifteenPercent == 0 else 0
    await callback.answer('Операция выполнена успешно')
    await callback.message.delete()
    await boss_menu(callback.message)


@dp.callback_query_handler(Text(equals='promo_list_back'))
async def promo_list_back(callback: types.CallbackQuery):
    await callback.message.delete()
    await boss_menu(callback.message)


@dp.callback_query_handler(Text(equals='change_delivery_price'))
async def change_delivery_price(callback: types.CallbackQuery):
    try:
        await callback.message.delete()
    except:
        pass
    await ChangeDeliveryPrice.newprice.set()
    await callback.message.answer('Введите новую цену доставки.')


@dp.message_handler(state=ChangeDeliveryPrice.newprice)
async def take_new_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['newprice'] = message.text
    global delivery_price
    cursor.execute(f"UPDATE tech_info SET deliveryprice={int(data['newprice'])} WHERE deliveryprice={delivery_price}")
    connect.commit()
    delivery_price = int(data['newprice'])
    await state.finish()
    await message.answer('Сумма доставки успешно изменена')
    cursor.execute(
        f"UPDATE login_id SET menuMessage='NULL', menuStatus='NULL' WHERE ID='{message.chat.id}'")
    connect.commit()


@dp.callback_query_handler(Text(equals='shortstat'))
async def show_short_stat(callback: types.CallbackQuery):
    cursor.execute(f"SELECT Price, Status, Статус_Оплаты FROM orders")
    info = cursor.fetchall()
    cancels_amount = 0
    money = 0
    for i in range(len(info)):
        if info[i][1] == 'Отменён':
            cancels_amount += 1
        if info[i][2] == 'Оплачен' and info[i][1] != 'Отменён':
            money += info[i][0]
    await callback.message.edit_text(f'Количество заказов на данный момент: {len(info)}, Количество отменённых из них: {cancels_amount}, Выручка на данный момент: {money} рублей.')
    cursor.execute(
        f"UPDATE login_id SET menuMessage='NULL', menuStatus='NULL' WHERE ID='{callback.message.chat.id}'")
    connect.commit()
    await boss_menu(callback.message)


@dp.callback_query_handler(Text(equals='ban_user'))
async def choose_user_for_ban(callback: types.CallbackQuery):
    cursor.execute("SELECT ID, CancelOrders, Имя FROM login_id WHERE CancelOrders>4")
    abuser_info = cursor.fetchall()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for i in range(len(abuser_info)):
        keyboard.add(types.InlineKeyboardButton(f'ID: {abuser_info[i][0]}, Кол-во отмен: {abuser_info[i][1]}, Имя: {abuser_info[i][2]}', callback_data=f'to_black_list {abuser_info[i][0]}'))
    keyboard.add(types.InlineKeyboardButton('Назад ↩', callback_data='back_to_boss'))
    await callback.message.edit_text('Выберите пользователя, которого хотите забанить.', reply_markup=keyboard)


@dp.callback_query_handler(Text(equals='back_to_boss'))
async def back_to_boss(callback: types.CallbackQuery):
    await callback.message.delete()
    await boss_menu(callback.message)


@dp.callback_query_handler(Text(startswith='to_black_list'))
async def handle_ban_command(callback: types.CallbackQuery):
    abuser_id = callback.data.split(" ")[1]
    cursor.execute(f"UPDATE login_id SET Имя='Banned' WHERE ID={abuser_id}")
    connect.commit()
    await callback.message.edit_text(f"Пользователь {abuser_id} заблокирован.")
    await boss_menu(callback.message)


@dp.callback_query_handler(Text(equals='take_user'))
async def take__user(callback: types.CallbackQuery):
    cursor.execute(f"SELECT Role FROM login_id WHERE ID={callback.message.chat.id}")
    this_user_role = cursor.fetchone()
    if this_user_role[0] == 4:
        cursor.execute("SELECT ID, Имя, Role FROM login_id WHERE Role!=0")
    else:
        cursor.execute("SELECT ID, Имя, Role FROM login_id WHERE Role!=0 AND Role < 4")
    personal_info = cursor.fetchall()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for i in range(len(personal_info)):
        if personal_info[i][2] == 1:
            Role = 'Курьер'
        elif personal_info[i][2] == 2:
            Role = 'Повар'
        elif personal_info[i][2] == 4:
            Role = 'BIG BOSS'
        else:
            Role = 'Заявка на выдачу'
        keyboard.add(types.InlineKeyboardButton(f'Имя: {personal_info[i][1]}, Текущая роль: {Role}', callback_data=f'choose_user {personal_info[i][0]} {this_user_role[0]}'))
    keyboard.add(types.InlineKeyboardButton('Назад ↩', callback_data='back_to_boss'))
    await callback.message.edit_text('Выберите пользователя для изменения роли.', reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith='choose_user'))
async def take_role(callback: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('Пользователь.', callback_data=f'change_role {callback.data.split(" ")[1]} 0'))
    keyboard.add(types.InlineKeyboardButton('Курьер.', callback_data=f'change_role {callback.data.split(" ")[1]} 1'))
    keyboard.add(types.InlineKeyboardButton('Повар.', callback_data=f'change_role {callback.data.split(" ")[1]} 2'))
    keyboard.add(types.InlineKeyboardButton('BIG BOSS.', callback_data=f'change_role {callback.data.split(" ")[1]} 4'))
    keyboard.add(types.InlineKeyboardButton('Назад ↩', callback_data=f'back_to_change_user_for_roles'))
    await callback.message.edit_text('Выберите новую роль.', reply_markup=keyboard)


@dp.callback_query_handler(Text(equals='back_to_change_user_for_roles'))
async def back_to_boss_menu(callback: types.CallbackQuery):
    await take__user(callback)


@dp.callback_query_handler(Text(startswith='change_role'))
async def change__role(callback: types.CallbackQuery):
    cursor.execute(f"UPDATE login_ID SET Role={callback.data.split(' ')[2]} WHERE ID={callback.data.split(' ')[1]}")
    connect.commit()
    await callback.message.edit_text(f'Роль пользователя {callback.data.split(" ")[1]} была успешно изменена')
    await boss_menu(callback.message)


@dp.message_handler(chat_type='private', commands='Curier')
async def curier_panel(message: types.Message):
    cursor.execute(f"SELECT Role FROM login_id WHERE ID={message.chat.id}")
    role = cursor.fetchone()
    if role[0] > 0:
        cursor.execute(f"SELECT menuStatus FROM login_id WHERE ID='{message.chat.id}'")
        status = cursor.fetchone()[0]
        if status == '1' and message.text.lower() == '/curier':
            cursor.execute(f"SELECT menuMessage FROM login_id WHERE ID='{message.chat.id}'")
            user_message = cursor.fetchone()[0].split(',')
            for i in range(len(user_message)):
                try:
                    await bot.delete_message(chat_id=message.chat.id, message_id=int(user_message[i]))
                except:
                    pass
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton('Доступные заказы.', callback_data='all_orders'))
        keyboard.add(types.InlineKeyboardButton('Мои заказы.', callback_data='my_orders'))
        sended_message = await message.answer('Выберите нужную опцию.', reply_markup=keyboard)
        cursor.execute(
            f"UPDATE login_id SET menuStatus='1', menuMessage='{sended_message.message_id}' WHERE ID='{message.chat.id}'")
        connect.commit()
    else:
        await message.answer('У вас недостаточно прав')


@dp.callback_query_handler(Text(equals='all_orders'))
async def all__orders(callback: types.CallbackQuery):
    cursor.execute("SELECT Адрес, ID, Время_Доставки FROM orders WHERE CurierID is NULL AND Status!='Отменён' AND Status!='Завершён' AND deliveryType=1 AND Тип_Доставки!='Самовывоз'")
    orders = cursor.fetchall()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for i in range(len(orders)):
        keyboard.add(types.InlineKeyboardButton(f'ID заказа: {orders[i][1]}, Адрес: {orders[i][0]}\nВремя доставки: {orders[i][2]}', callback_data=f"check_info_about_active_order {orders[i][1]}"))
    keyboard.add(types.InlineKeyboardButton('Назад ↩.', callback_data='back_to_curier_panel'))
    await callback.message.edit_text('Выберите заказ чтобы посмотреть информацию о нём.', reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith='check_info_about_active_order'))
async def check_info_about_active_orders(callback: types.CallbackQuery):
    cursor.execute(f'SELECT User_ID, Status, List, Price, Способ_Оплаты, Адрес, Тип_Доставки, Время_Доставки,'
                   f' Комментарий, Статус_Оплаты, Data FROM orders WHERE ID={callback.data.split(" ")[1]}')
    info = cursor.fetchone()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('Принять заказ.', callback_data=f'accept_order {callback.data.split(" ")[1]}'))
    keyboard.add(types.InlineKeyboardButton('Назад ↩.', callback_data='back_to_all_orders'))
    await callback.message.edit_text(f'<b>Информация о заказе</b>\n<b>ID заказа</b>: {callback.data.split(" ")[1]}\n<b>ID пользователя</b>: {info[0]}\n'
                                     f'<b>Статус заказа</b>: {info[1]}\n<b>Корзина</b>: {info[2]}\n<b>Общая стоимость заказа</b>: {info[3]}\n<b>Способ оплаты</b>: {info[4]}\n'
                                     f'<b>Адрес</b>: {info[5]}\n<b>Тип Доставки</b>: {info[6]}\n<b>Время Доставки</b>: {info[7]}\n'
                                     f'<b>Комментарий к заказу</b>: {info[8]}\n<b>Статус Оплаты</b>: {info[9]}\n'
                                     f'<b>Дата</b>: {info[10]}', reply_markup=keyboard)


@dp.callback_query_handler(Text(equals='back_to_curier_panel'))
async def back_to_curier_panel(callback: types.CallbackQuery):
    await callback.message.delete()
    await curier_panel(callback.message)


@dp.callback_query_handler(Text(startswith="accept_order"))
async def accept__order(callback: types.CallbackQuery):
    cursor.execute(f"UPDATE orders SET CurierID={callback.message.chat.id} WHERE ID={callback.data.split(' ')[1]}")
    connect.commit()
    await callback.message.edit_text('Вы успешно приняли заказ.')
    cursor.execute(f"SELECT User_ID FROM orders WHERE ID={callback.data.split(' ')[1]}")
    userid = cursor.fetchone()
    cursor.execute(f"SELECT Телефон FROM login_id WHERE id={userid[0]}")
    await bot.send_message(userid[0], f"Курьер забрал Ваш заказ и спешит к Вам. Номер курьера для связи {cursor.fetchone()[0]}")


@dp.callback_query_handler(Text(equals='my_orders'))
async def check_my_orders(callback: types.CallbackQuery):
    cursor.execute(f"SELECT Адрес, ID, Время_Доставки FROM orders WHERE CurierID={callback.message.chat.id} AND Status!='Отменён' AND Status!='Завершён'")
    my_orders = cursor.fetchall()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('Назад ↩.', callback_data='back_to_curier_panel'))
    for i in range (len(my_orders)):
        keyboard.add(types.InlineKeyboardButton(f'ID заказа: {my_orders[i][1]}, Адрес: {my_orders[i][0]}\nВремя доставки: {my_orders[i][2]}', callback_data=f"check_info_about_my_order {my_orders[i][1]}"))
    await callback.message.edit_text('Выберите заказ чтобы посмотреть информацию о нём.', reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith='check_info_about_my_order'))
async def check_info_about_my_order(callback: types.CallbackQuery):
    cursor.execute(f'SELECT User_ID, Status, List, Price, Способ_Оплаты, Адрес, Тип_Доставки, Время_Доставки,'
                   f' Комментарий, Статус_Оплаты, Data FROM orders WHERE ID={callback.data.split(" ")[1]}')
    info = cursor.fetchone()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('Заказ доставлен (Завершить заказ)', callback_data=f'complete_order {callback.data.split(" ")[1]}'))
    keyboard.add(types.InlineKeyboardButton('Назад ↩.', callback_data='back_to_my_orders'))
    await callback.message.edit_text(f'<b>Информация о заказе</b>\n<b>ID заказа</b>: {callback.data.split(" ")[1]}\n<b>ID пользователя</b>: {info[0]}\n'
                                     f'<b>Статус заказа</b>: {info[1]}\n<b>Корзина</b>: {info[2]}\n<b>Общая стоимость заказа</b>: {info[3]}\n<b>Способ оплаты</b>: {info[4]}\n'
                                     f'<b>Адрес</b>: {info[5]}\n<b>Тип Доставки</b>: {info[6]}\n<b>Время Доставки</b>: {info[7]}\n'
                                     f'<b>Комментарий к заказу</b>: {info[8]}\n<b>Статус Оплаты</b>: {info[9]}\n'
                                     f'<b>Дата</b>: {info[10]}', reply_markup=keyboard)


@dp.callback_query_handler(Text(equals='back_to_all_orders'))
async def back_to_all_panel(callback: types.CallbackQuery):
    await all__orders(callback)


@dp.callback_query_handler(Text(equals='back_to_my_orders'))
async def back_to_my_orders(callback: types.CallbackQuery):
    await check_my_orders(callback)


@dp.callback_query_handler(Text(startswith="complete_order"))
async def complete_order(callback: types.CallbackQuery):
    cursor.execute(f"UPDATE orders SET status='Завершён',Статус_Оплаты='Оплачен' WHERE ID={callback.data.split(' ')[1]}")
    connect.commit()
    cursor.execute(f"SELECT User_ID FROM orders WHERE ID={callback.data.split(' ')[1]}")
    userid = cursor.fetchone()
    global this_day
    cursor.execute(
        f"SELECT ID, User_ID, Status, List, Price, Способ_Оплаты, Адрес, Тип_Доставки, Время_Доставки, Комментарий, Статус_Оплаты, Data, CurierID FROM orders")
    info = cursor.fetchall()
    cursor.execute(f'SELECT "Способ_Оплаты", SUM(price) FROM orders GROUP BY "Способ_Оплаты"')
    money_buy_type = cursor.fetchall()
    tmp = '"Статус_Оплаты"'
    cursor.execute(f"SELECT SUM(price) FROM orders WHERE status!='Отменён' AND {tmp}='Оплачен'")
    money = cursor.fetchone()[0]
    cursor.execute(f"SELECT COUNT(*) FROM orders WHERE status!='Отменён'")
    cancels_amount = cursor.fetchone()[0]
    array = [["" for j in range(1)] for i in range(len(info))]
    for i in range(len(info)):
        if info[i][2] == 'Завершён':
            array[i][0] = str(info[i][4])
    results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
        "valueInputOption": "RAW",
        "data": [
            {"range": f"{this_day}!A1", 'values': [
                ['Количество заказов', 'Количество отменённых заказов', 'Выручка за день'],
                [len(info), cancels_amount, money]
            ]},
            {"range": f"{this_day}!A3", 'values': money_buy_type},
            {"range": f"{this_day}!A5",
             "values": [
                 ['ID заказа', 'ID пользователя', 'Статус заказа', 'Позиции в заказе', 'Сумма заказа', 'Способ Оплаты',
                  'Адрес', 'Тип доставки', 'Время доставки', 'Комментарий', 'Статус оплаты', 'Дата заказа',
                  'ID курьера, доставившего заказ', 'ИТОГО'],
             ]},
            {"range": f"{this_day}!A6", 'values': info
             },
            {"range": f"{this_day}!N6", 'values': array}
        ]
    }).execute()
    await callback.message.edit_text('Вы успешно завершили заказ.')
    cursor.execute(f"SELECT Способ_Оплаты FROM orders WHERE ID={callback.data.split(' ')[1]}")
    temp = cursor.fetchone()
    if temp != 'Картой в телеграме' and temp != 'Перевод на карту':
        cursor.execute(f"SELECT User_ID, Price FROM orders WHERE ID={callback.data.split(' ')[1]}")
        userid = cursor.fetchone()
        cursor.execute(f"UPDATE login_id SET OrdersSum=OrdersSum+{userid[1]} WHERE ID={userid[0]}")
        connect.commit()
    await bot.send_message(userid[0], "Ваш заказ успешно завершен! Ждём Вас снова 🙂")
    await asyncio.sleep(600)
    await hello_menu(callback.message)


@dp.callback_query_handler(Text(equals='cancel_order'))
async def cancel__order(callback: types.CallbackQuery):
    cursor.execute("SELECT User_ID, Price, ID FROM orders WHERE status!='Отменён' AND status!='Завершён'")
    short_info = cursor.fetchall()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for i in range(len(short_info)):
        keyboard.add(types.InlineKeyboardButton(f'ID пользователя: {short_info[i][0]}\nЦена заказа: {short_info[i][1]}', callback_data=f'checkinfo {short_info[i][2]}'))
    keyboard.add(types.InlineKeyboardButton('Назад ↩', callback_data="back_to_boss"))
    await callback.message.edit_text('Выберите заказ для просмотра информации (и последующей отмены)', reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith='checkinfo'))
async def check_info_about_cancel_order(callback: types.CallbackQuery):
    cursor.execute(f'SELECT ID, User_ID, status, List, Price, Способ_Оплаты, Адрес, Тип_Доставки, Время_Доставки,'
                   f' Комментарий, Статус_Оплаты, Data FROM orders WHERE ID={callback.data.split(" ")[1]}')
    info = cursor.fetchone()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('Отменить заказ', callback_data=f'cancel_this_order {callback.data.split(" ")[1]} {info[1]}'))
    keyboard.add(types.InlineKeyboardButton('Назад ↩', callback_data=f'cancel_order'))
    await callback.message.edit_text(f'<b>Информация о заказе</b>\n<b>ID заказа</b>: {info[0]}\n<b>ID пользователя</b>: {info[1]}\n'
                                     f'<b>Статус заказа</b>: {info[2]}\n<b>Корзина</b>: {info[3]}\n<b>Общая стоимость заказа</b>: {info[4]}\n<b>Способ оплаты</b>: {info[5]}\n'
                                     f'<b>Адрес</b>: {info[6]}\n<b>Тип Доставки</b>: {info[7]}\n<b>Время Доставки</b>: {info[8]}\n'
                                     f'<b>Комментарий к заказу</b>: {info[9]}\n<b>Статус Оплаты</b>: {info[10]}\n'
                                     f'<b>Дата</b>: {info[11]}',
                                     reply_markup=keyboard, parse_mode=ParseMode.HTML)


@dp.callback_query_handler(Text(startswith='cancel_this_order'))
async def cancel__this_order(callback: types.CallbackQuery):
    cursor.execute(f"UPDATE orders SET status='Отменён',Статус_Оплаты='Отменён' WHERE ID={callback.data.split(' ')[1]}")
    connect.commit()
    cursor.execute(f"UPDATE login_id SET CancelOrders=CancelOrders+1 WHERE ID={callback.data.split(' ')[2]}")
    connect.commit()
    cursor.execute(f'SELECT User_ID, List FROM orders WHERE ID={callback.data.split(" ")[1]}')
    temp = cursor.fetchone()
    await callback.message.edit_text('Выбранное блюдо было удалено из меню.')
    await boss_menu(callback.message)
    global this_day
    cursor.execute(
        f"SELECT ID, User_ID, Status, List, Price, Способ_Оплаты, Адрес, Тип_Доставки, Время_Доставки, Комментарий, Статус_Оплаты, Data, CurierID FROM orders")
    info = cursor.fetchall()
    cursor.execute(f'SELECT "Способ_Оплаты", SUM(price) FROM orders GROUP BY "Способ_Оплаты"')
    money_buy_type = cursor.fetchall()
    tmp = '"Статус_Оплаты"'
    cursor.execute(f"SELECT SUM(price) FROM orders WHERE status!='Отменён' AND {tmp}='Оплачен'")
    money = cursor.fetchone()[0]
    cursor.execute(f"SELECT COUNT(*) FROM orders WHERE status!='Отменён'")
    cancels_amount = cursor.fetchone()[0]
    array = [["" for j in range(1)] for i in range(len(info))]
    for i in range(len(info)):
        if info[i][2] == 'Завершён':
            array[i][0] = str(info[i][4])
    results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
        "valueInputOption": "RAW",
        "data": [
            {"range": f"{this_day}!A1", 'values': [
                ['Количество заказов', 'Количество отменённых заказов', 'Выручка за день'],
                [len(info), cancels_amount, money]
            ]},
            {"range": f"{this_day}!A3", 'values': money_buy_type},
            {"range": f"{this_day}!A5",
             "values": [
                 ['ID заказа', 'ID пользователя', 'Статус заказа', 'Позиции в заказе', 'Сумма заказа', 'Способ Оплаты',
                  'Адрес', 'Тип доставки', 'Время доставки', 'Комментарий', 'Статус оплаты', 'Дата заказа',
                  'ID курьера, доставившего заказ', 'ИТОГО'],
             ]},
            {"range": f"{this_day}!A6", 'values': info
             },
            {"range": f"{this_day}!N6", 'values': array}
        ]
    }).execute()
    await callback.message.edit_text('Заказ был помечен как отменённый.')
    await bot.send_message(temp[0], f'Ваш заказ номер {callback.data.split(" ")[1]} с позициями {temp[1]} был отменён')


@dp.callback_query_handler(Text(startswith='delete_item'))
async def delete_from_menu(callback: types.CallbackQuery, state: FSMContext):
    temp = callback.data.split(' ')
    item_to_del = ''
    for i in range(1, len(temp)):
        item_to_del += str(temp[i])
    async with state.proxy() as data:
        cursor.execute(f"DELETE FROM cart WHERE name='{data['type']}'")
    await state.finish()
    cursor.execute(f"DELETE FROM menu WHERE ID={int(item_to_del)}")
    connect.commit()
    await callback.message.edit_text('Выбранное блюдо было удалено из меню.')
    await boss_menu(callback.message)



@dp.callback_query_handler(Text(equals='OpenShift'))
async def open_work_shift(callback: types.CallbackQuery):
    global stop
    global list_name
    global months
    stop = printer()
    global this_month
    global this_year
    global spreadsheetId
    global this_day
    global work_shift
    if datetime.today().date().month != this_month:
        this_month = datetime.today().date().month
        this_day = datetime.today().date().day
        list_name = f'Статистика BurgerTek Полярный {months[f"{this_month}"]}'
        spreadsheet = service.spreadsheets().create(body={
            'properties': {'title': f'{list_name}', 'locale': 'ru_RU'},
            'sheets': [{'properties': {'sheetType': 'GRID',
                                        'sheetId': 0,
                                        'title': f'{this_day}',
                                        'gridProperties': {'rowCount': 5000, 'columnCount': 30}}}]
        }).execute()
        driveService = build('drive', 'v3', credentials=credentials)
        driveService.permissions().create(
            fileId=spreadsheet['spreadsheetId'],
            body={'type': 'user', 'role': 'writer', 'emailAddress': 'borisovzd@gmail.com'},  # доступ
            fields='id',
        ).execute()
        driveService.permissions().create(
            fileId=spreadsheet['spreadsheetId'],
            body={'type': 'user', 'role': 'writer', 'emailAddress': 'ghostshadow4527@gmail.com'},  # доступ
            fields='id',
        ).execute()
        spreadsheetId = spreadsheet['spreadsheetId']
        await bot.send_message( 546186690, f'https://docs.google.com/spreadsheets/d/{spreadsheetId}')
    elif datetime.today().date().day != this_day:
        this_day = datetime.today().date().day
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheetId,
            body=
            {
                "requests": [
                    {
                        "addSheet": {
                            "properties": {
                                "title": f"{this_day}",
                                "gridProperties": {
                                    "rowCount": 5000,
                                    "columnCount": 30
                                }
                            }
                        }
                    }
                ]
            }).execute()
    work_shift = True
    await callback.answer('Смена успешно открыта')


@dp.callback_query_handler(Text(equals='CloseShift'))
async def close_work_shift(callback: types.CallbackQuery):
    global work_shift
    work_shift = False
    global stop
    stop.set()
    await callback.answer('Смена успешно закрыта')
    global this_day
    cursor.execute(
        f"SELECT ID, User_ID, Status, List, Price, Способ_Оплаты, Адрес, Тип_Доставки, Время_Доставки, Комментарий, Статус_Оплаты, Data, CurierID FROM orders")
    info = cursor.fetchall()
    cursor.execute(f'SELECT "Способ_Оплаты", SUM(price) FROM orders GROUP BY "Способ_Оплаты"')
    money_buy_type = cursor.fetchall()
    tmp = '"Статус_Оплаты"'
    cursor.execute(f"SELECT SUM(price) FROM orders WHERE status!='Отменён' AND {tmp}='Оплачен'")
    money = cursor.fetchone()[0]
    cursor.execute(f"SELECT COUNT(*) FROM orders WHERE status!='Отменён'")
    cancels_amount = cursor.fetchone()[0]
    array = [["" for j in range(1)] for i in range(len(info))]
    for i in range(len(info)):
        if info[i][2] == 'Завершён':
            array[i][0] = str(info[i][4])
    results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
        "valueInputOption": "RAW",
        "data": [
            {"range": f"{this_day}!A1", 'values': [
                ['Количество заказов', 'Количество отменённых заказов', 'Выручка за день'],
                [len(info), cancels_amount, money]
            ]},
            {"range": f"{this_day}!A3", 'values': money_buy_type},
            {"range": f"{this_day}!A5",
             "values": [
                 ['ID заказа', 'ID пользователя', 'Статус заказа', 'Позиции в заказе', 'Сумма заказа', 'Способ Оплаты',
                  'Адрес', 'Тип доставки', 'Время доставки', 'Комментарий', 'Статус оплаты', 'Дата заказа',
                  'ID курьера, доставившего заказ', 'ИТОГО'],
             ]},
            {"range": f"{this_day}!A6", 'values': info
             },
            {"range": f"{this_day}!N6", 'values': array}
        ]
    }).execute()


async def main_menu(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Оставить отзыв🖌', 'Меню🍽', 'Тех. Поддержка🆘', 'Статус заказа🔍', 'Корзина🛒',
               'Редактировать профиль✏', 'В предыдущее меню↩']
    keyboard.add(*buttons)
    await message.answer('Добро пожаловать в <b>главное меню</b> Burgertek!'
                         ' Показать Вам меню? Или же Вы хотели бы оставить отзыв? Написать в тех. поддержку?'
                         ' В любом случае я помогу Вам!♥️', reply_markup=keyboard, parse_mode=ParseMode.HTML)
    if fifteenPercent == 1:
        await message.answer("В данный момент проходит акция на 15% от общей суммы заказа!")


@dp.message_handler(chat_type='private', commands='povar')
async def povar(message: types.Message):
    cursor.execute(f"SELECT Role FROM login_id WHERE ID={message.chat.id}")
    if cursor.fetchone()[0] < 2:
        await message.answer('у вас недостаточно прав')
        return
    cursor.execute(f"SELECT menuStatus FROM login_id WHERE ID='{message.chat.id}'")
    status = cursor.fetchone()[0]
    if message.text is None:
        message.text = 'text'
    if status == '1' and message.text.lower() == '/povar':
        cursor.execute(f"SELECT menuMessage FROM login_id WHERE ID={message.chat.id}")
        user_message = cursor.fetchone()[0].split(',')
        for i in range(len(user_message)):
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=int(user_message[i]))
            except:
                pass
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('Активные заказы', callback_data='active_orders'))
    keyboard.add(types.InlineKeyboardButton('Заблокировать блюдо', callback_data='block_position'))
    keyboard.add(types.InlineKeyboardButton('Открыть смену', callback_data='OpenShift'))
    keyboard.add(types.InlineKeyboardButton('Закрыть смену', callback_data='CloseShift'))
    sended_message = await message.answer('Выберите нужную опцию.', reply_markup=keyboard)
    cursor.execute(
        f"UPDATE login_id SET menuStatus='1', menuMessage='{sended_message.message_id}' WHERE ID='{message.chat.id}'")
    connect.commit()


@dp.callback_query_handler(Text(startswith='block_position'))
async def block_position(callback: types.CallbackQuery):
        cursor.execute("SELECT DISTINCT Type FROM menu")
        tmp = cursor.fetchall()
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        for i in range(len(tmp)):
            keyboard.add(types.InlineKeyboardButton(tmp[i][0], callback_data=f"povar_menu_type {tmp[i][0]}"))
        keyboard.add(types.InlineKeyboardButton("Назад ↩", callback_data="povar_menu_back"))
        await callback.message.edit_text('Выберите категорию:', reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith='povar_menu_type'))
async def povar_menu_type(callback: types.CallbackQuery, state: FSMContext):
    name = callback.data.split(' ')[1]
    cursor.execute(f"SELECT Name,ID FROM menu WHERE Type='{name}'")
    tmp = cursor.fetchall()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for i in range(len(tmp)):
        keyboard.add(types.InlineKeyboardButton(tmp[i][0], callback_data=f"povar_menu_item {tmp[i][1]}"))
    keyboard.add(types.InlineKeyboardButton('Назад ↩', callback_data="povar_menu_return"))
    async with state.proxy() as data:
        data['type'] = name
    await callback.message.delete()
    sended_message = await bot.send_message(callback.message.chat.id, text='Сделайте выбор', reply_markup=keyboard)
    cursor.execute(f"UPDATE login_id SET menuMessage='{sended_message.message_id}' WHERE ID='{callback.message.chat.id}'")
    connect.commit()
    await callback.answer()


@dp.callback_query_handler(Text(startswith='povar_menu_item'))
async def povar_menu_item(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    item_id = callback.data.split('povar_menu_item ')[1]
    async with state.proxy() as data:
        data['id'] = item_id
        data['amount'] = 1
        data['item_id'] = item_id
    cursor.execute(f"SELECT Available FROM menu WHERE ID='{item_id}'")
    available = cursor.fetchone()[0]
    if available == 0:
        keyboard.add(types.InlineKeyboardButton('Разблокировать позицию', callback_data=f"povar_item_block;{available};{item_id}"))
    else:
        keyboard.add(types.InlineKeyboardButton('Заблокировать позицию', callback_data=f"povar_item_block;{available};{item_id}"))
    keyboard.add(types.InlineKeyboardButton('Назад ↩', callback_data="povar_menu__item_back"))
    cursor.execute(f"SELECT Photo,Description,Price FROM menu WHERE ID='{item_id}'")
    tmp = cursor.fetchone()
    message_text = await callback.message.answer_photo(photo=str(tmp[0]), reply_markup=keyboard,
                                                       caption=f"Описание: {tmp[1]}"
                                                               f"\nЦена: {tmp[2]} ₽")
    cursor.execute(
        f"UPDATE login_id SET menuMessage='{message_text.message_id}' WHERE ID='{callback.message.chat.id}'")
    connect.commit()


@dp.callback_query_handler(Text(startswith='povar_item_block'))
async def povar_item_block(callback: types.CallbackQuery, state: FSMContext):
    item_id = callback.data.split(';')[2]
    item_available = callback.data.split(';')[1]
    if item_available == '1':
        cursor.execute(f"SELECT name FROM menu WHERE ID='{item_id}'")
        item_name = cursor.fetchone()[0]
        cursor.execute(f"UPDATE menu SET Available=0 WHERE ID='{item_id}'")
        cursor.execute(f"DELETE FROM cart WHERE name='{item_name}'")
    else:
        cursor.execute(f"UPDATE menu SET Available=1 WHERE ID='{item_id}'")
    connect.commit()
    await callback.message.delete()
    cursor.execute(
        f"UPDATE login_id SET menuMessage='' WHERE ID='{callback.message.chat.id}'")
    await state.finish()
    await povar(callback.message)


@dp.callback_query_handler(Text(equals='povar_menu__item_back'))
async def menu_item_back(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        name = data['type']
    cursor.execute(f"SELECT Name,ID FROM menu WHERE Type='{name}'")
    tmp = cursor.fetchall()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for i in range(len(tmp)):
        keyboard.add(types.InlineKeyboardButton(tmp[i][0], callback_data=f"povar_menu_item {tmp[i][1]}"))
    keyboard.add(types.InlineKeyboardButton('Назад ↩', callback_data="povar_menu_return"))
    async with state.proxy() as data:
        data['type'] = name
    await callback.message.delete()
    sended_message = await bot.send_message(callback.message.chat.id, text='Сделайте выбор', reply_markup=keyboard)
    cursor.execute(f"UPDATE login_id SET menuMessage='{sended_message.message_id}' WHERE ID='{callback.message.chat.id}'")
    connect.commit()
    await callback.answer()


@dp.callback_query_handler(Text(startswith='povar_menu_return'))
async def povar_menu_return(callback: types.CallbackQuery):
    await callback.answer()
    await block_position(callback)


@dp.callback_query_handler(Text(equals='povar_menu_back'))
async def menu_type_back(callback: types.CallbackQuery):
    await callback.answer('Вы были перемещены в меню повара')
    cursor.execute(
        f"UPDATE login_id SET menuMessage='NULL', menuStatus='NULL' WHERE ID='{callback.message.chat.id}'")
    connect.commit()
    await callback.message.delete()
    await povar(callback.message)


@dp.callback_query_handler(Text(equals='active_orders'))
async def active_orders(callback: types.CallbackQuery):
    cursor.execute(
        "SELECT Адрес, ID, Время_Доставки FROM orders WHERE (Status='Готовится' OR Status='Готов') AND deliveryType=1")
    orders = cursor.fetchall()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for i in range(len(orders)):
        keyboard.add(types.InlineKeyboardButton(
            f'ID заказа: {orders[i][1]}, Адрес: {orders[i][0]}\nВремя доставки: {orders[i][2]}',
            callback_data=f"check_active_order {orders[i][1]}"))
    keyboard.add(types.InlineKeyboardButton('Назад ↩', callback_data='back_to_povar_menu'))
    await callback.message.edit_text('Выберите заказ чтобы посмотреть информацию о нём', reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(Text(startswith='check_active_order'))
async def check_active_order(callback: types.CallbackQuery):
    cursor.execute(f'SELECT User_ID, Status, List, Price, Способ_Оплаты, Адрес, Тип_Доставки, Время_Доставки,'
                   f' Комментарий, Статус_Оплаты, Data FROM orders WHERE ID={callback.data.split(" ")[1]}')
    info = cursor.fetchone()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    if info[6] == 'Самовывоз':
        if info[1] != 'Готов':
            keyboard.add(types.InlineKeyboardButton('Отметить как приготовленный',
                                                    callback_data=f'povar_order_accept {callback.data.split(" ")[1]}'))
        keyboard.add(types.InlineKeyboardButton('Завершить заказ', callback_data=f'povar_finish_order {callback.data.split(" ")[1]}'))
    else:
        keyboard.add(
            types.InlineKeyboardButton('Отметить как приготовленный',
                                       callback_data=f'povar_accept_order {callback.data.split(" ")[1]}'))
    keyboard.add(types.InlineKeyboardButton('Назад ↩', callback_data='back_to_povar_orders'))
    await callback.message.edit_text(
        f'<b>Информация о заказе</b>\n<b>ID заказа</b>: {callback.data.split(" ")[1]}\n<b>ID пользователя</b>: {info[0]}\n'
        f'<b>Статус заказа</b>: {info[1]}\n<b>Корзина</b>: {info[2]}\n<b>Общая стоимость заказа</b>: {info[3]}\n<b>Способ оплаты</b>: {info[4]}\n'
        f'<b>Адрес</b>: {info[5]}\n<b>Тип Доставки</b>: {info[6]}\n<b>Время Доставки</b>: {info[7]}\n'
        f'<b>Комментарий к заказу</b>: {info[8]}\n<b>Статус Оплаты</b>: {info[9]}\n'
        f'<b>Дата</b>: {info[10]}', reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(Text(startswith="povar_finish_order"))
async def povar_finish_order(callback: types.CallbackQuery):
    cursor.execute(f"UPDATE orders SET Статус_Оплаты ='Оплачен', Status='Завершён' WHERE ID={callback.data.split(' ')[1]}")
    connect.commit()
    cursor.execute(f"SELECT Способ_Оплаты FROM orders WHERE ID={callback.data.split(' ')[1]}")
    temp = cursor.fetchone()
    if temp != 'Картой в телеграме' and temp != 'Перевод на карту':
        cursor.execute(f"SELECT User_ID, Price FROM orders WHERE ID={callback.data.split(' ')[1]}")
        userid = cursor.fetchone()
        cursor.execute(f"UPDATE login_id SET OrdersSum=OrdersSum+{userid[1]} WHERE ID={userid[0]}")
        connect.commit()
    await callback.answer('Статус заказа успешно изменён')
    global this_day
    cursor.execute(
        f"SELECT ID, User_ID, Status, List, Price, Способ_Оплаты, Адрес, Тип_Доставки, Время_Доставки, Комментарий, Статус_Оплаты, Data, CurierID FROM orders")
    info = cursor.fetchall()
    cursor.execute(f'SELECT "Способ_Оплаты", SUM(price) FROM orders GROUP BY "Способ_Оплаты"')
    money_buy_type = cursor.fetchall()
    tmp = '"Статус_Оплаты"'
    cursor.execute(f"SELECT SUM(price) FROM orders WHERE status!='Отменён' AND {tmp}='Оплачен'")
    money = cursor.fetchone()[0]
    cursor.execute(f"SELECT COUNT(*) FROM orders WHERE status!='Отменён'")
    cancels_amount = cursor.fetchone()[0]
    array = [["" for j in range(1)] for i in range(len(info))]
    for i in range(len(info)):
        if info[i][2] == 'Завершён':
            array[i][0] = str(info[i][4])
    results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
        "valueInputOption": "RAW",
        "data": [
            {"range": f"{this_day}!A1", 'values': [
                ['Количество заказов', 'Количество отменённых заказов', 'Выручка за день'],
                [len(info), cancels_amount, money]
            ]},
            {"range": f"{this_day}!A3", 'values': money_buy_type},
            {"range": f"{this_day}!A5",
             "values": [
                 ['ID заказа', 'ID пользователя', 'Статус заказа', 'Позиции в заказе', 'Сумма заказа', 'Способ Оплаты',
                  'Адрес', 'Тип доставки', 'Время доставки', 'Комментарий', 'Статус оплаты', 'Дата заказа',
                  'ID курьера, доставившего заказ', 'ИТОГО'],
             ]},
            {"range": f"{this_day}!A6", 'values': info
             },
            {"range": f"{this_day}!N6", 'values': array}
        ]
    }).execute()
    cursor.execute(f"SELECT User_ID, Price FROM orders WHERE ID={callback.data.split(' ')[1]}")
    userid = cursor.fetchone()
    cursor.execute(f"UPDATE login_id SET OrdersSum=OrdersSum+{userid[1]} WHERE ID={userid[0]}")
    connect.commit()
    await callback.message.delete()
    await povar(callback.message)
    await callback.answer()


@dp.callback_query_handler(Text(startswith='povar_order_accept'))
async def povar_order_accept(callback: types.CallbackQuery):
    cursor.execute(f"UPDATE orders SET Status='Готов' WHERE ID={callback.data.split(' ')[1]}")
    connect.commit()
    await callback.answer('Статус заказа успешно изменён')
    await callback.message.delete()
    cursor.execute(
        f"UPDATE login_id SET menuMessage='NULL', menuStatus='NULL' WHERE ID='{callback.message.chat.id}'")
    connect.commit()
    await povar(callback.message)


@dp.callback_query_handler(Text(startswith="povar_accept_order"))
async def povar_accept_order(callback: types.CallbackQuery):
    cursor.execute(f"SELECT CurierID,List FROM orders WHERE ID={callback.data.split(' ')[1]}")
    courierStatus = cursor.fetchone()
    if courierStatus[0] is not None:
        cursor.execute(f"UPDATE orders SET Status='В пути' WHERE ID={callback.data.split(' ')[1]}")
    else:
        cursor.execute(f"UPDATE orders SET Status='Ожидание курьера' WHERE ID={callback.data.split(' ')[1]}")
    connect.commit()
    await callback.answer('Статус заказа успешно изменён')
    cursor.execute(
        f"UPDATE login_id SET menuMessage='NULL', menuStatus='NULL' WHERE ID='{callback.message.chat.id}'")
    connect.commit()
    await callback.message.delete()
    await povar(callback.message)


@dp.callback_query_handler(Text(equals='back_to_povar_orders'))
async def back_to_povar_orders(callback: types.CallbackQuery):
    await active_orders(callback)
    await callback.answer()


@dp.callback_query_handler(Text(equals='back_to_povar_menu'))
async def back_to_povar_menu(callback: types.CallbackQuery):
    await callback.answer()
    cursor.execute(
        f"UPDATE login_id SET menuMessage='NULL', menuStatus='NULL' WHERE ID='{callback.message.chat.id}'")
    connect.commit()
    await callback.message.delete()
    await povar(callback.message)


@dp.callback_query_handler(Text(equals='our_reviews'))
async def our_reviews(callback: types.CallbackQuery):
    await callback.message.delete()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('Заказать корпоратив 🎉', callback_data='order_ivent'))
    keyboard.add(types.InlineKeyboardButton('Наши отзывы 📝', callback_data=f'our_reviews'))
    keyboard.add(types.InlineKeyboardButton('Перейти в главное меню📍', callback_data='main__menu'))
    keyboard.add(types.InlineKeyboardButton('Скачать меню в pdf 📥', callback_data='download_pdf'))
    await asyncio.sleep(0.5)
    await callback.message.answer(
        "Имя: Олег\n Оценка:  🌟🌟🌟🌟🌟 \n Отзыв: Самая лучшая шава, которую я когда-либо пробовал."
        "Особенно советую BBQ с двойным мясом. Однозначно 5/5")
    await asyncio.sleep(0.5)
    await callback.message.answer(
        "Имя: Егор\n Оценка:  🌟🌟🌟🌟🌟 \n Отзыв: Заказывал шаверму самовывозом, остался доволен."
        " Очень много мяса,"
        "соуса. Получилось очень вкусно.")
    await asyncio.sleep(0.5)
    await callback.message.answer("Имя: Александра\n Оценка:  🌟🌟🌟🌟🌟 \n Отзыв: бургеры и хот доги достаточно хороши."
                                  " Еда сытная и вкусная, брали на 6 человек, всем хватило, все остались довольны")
    await asyncio.sleep(0.5)
    await callback.message.answer(
        "Имя: Мурад\n Оценка:  🌟🌟🌟🌟🌟 \n Отзыв: Повару от души за шаверму, просто царская!", reply_markup=keyboard)


@dp.message_handler(Text(equals='Оставить отзыв🖌'), chat_type='private')
async def review(message: types.Message):
    cursor.execute(f"SELECT menuStatus FROM login_id WHERE ID='{message.chat.id}'")
    if cursor.fetchone()[0] == '1':
        cursor.execute(f"SELECT menuMessage FROM login_id WHERE ID='{message.chat.id}'")
        user_message = cursor.fetchone()[0].split(',')
        for i in range(len(user_message)):
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=int(user_message[i]))
            except:
                pass
    cursor.execute(
        f"UPDATE login_id SET menuStatus='1', menuMessage='{message.message_id + 1}' WHERE ID='{message.chat.id}'")
    connect.commit()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    stars = ""
    for i in range(5):
        stars += '🌟'
        keyboard.add(types.InlineKeyboardButton(stars, callback_data=f'review_stars {i + 1}'))
    keyboard.add(types.InlineKeyboardButton("Главное меню", callback_data='review_return'))
    sended_message = await message.answer('Выберите вашу оценку', reply_markup=keyboard)
    cursor.execute(
        f"UPDATE login_id SET menuStatus='1', menuMessage='{sended_message.message_id}' WHERE ID='{message.chat.id}'")
    connect.commit()


@dp.callback_query_handler(Text(equals='review_return'))
async def review_return(callback: types.CallbackQuery):
    cursor.execute(
        f"UPDATE login_id SET menuMessage='NULL', menuStatus='NULL' WHERE ID='{callback.message.chat.id}'")
    connect.commit()
    await callback.answer('Вы были перемещены в главное меню')
    await callback.message.delete()
    await main_menu(callback.message)


@dp.callback_query_handler(Text(startswith='review_stars'))
async def review_stars(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['stars'] = callback.data.split(' ')[1]
    await callback.message.edit_text(text='Опишите почему вы выбрали именно эту оценку:')
    await Review.text.set()


@dp.message_handler(state=Review.text)
async def review_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await state.finish()
    cursor.execute(
        f"UPDATE login_id SET menuMessage='NULL', menuStatus='NULL' WHERE ID='{message.chat.id}'")
    connect.commit()
    cursor.execute(f"SELECT Имя, Телефон FROM login_id WHERE ID={message.chat.id}")
    info = cursor.fetchone()
    await bot.send_message(-1001547432335,
                           "Имя: " + info[0] + "\nТелефон: " + info[1] + "\nОценка: " + data['stars'] + "\nОтзыв: " +
                           data['text'])
    await message.answer('Спасибо за ваш отзыв♥')
    await main_menu(message)


@dp.message_handler(Text(equals='Меню🍽'), chat_type='private')
async def menu(message: types.Message):
    cursor.execute(f"SELECT menuStatus FROM login_id WHERE ID={message.chat.id}")
    status = cursor.fetchone()[0]
    cursor.execute("SELECT DISTINCT Type FROM menu")
    tmp = cursor.fetchall()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for i in range(len(tmp)):
        withsmile = tmp[i][0]
        if withsmile == 'Бургер':
            withsmile += '🍔'
        elif withsmile == 'Картошка-фри':
            withsmile += '🍟'
        elif withsmile == 'Хот-дог':
            withsmile += '🌭'
        elif withsmile == 'Шаверма':
            withsmile += '🌯'
        elif withsmile == 'Блины':
            withsmile += '🥞'
        elif withsmile == 'Напитки':
            withsmile += '☕'
        keyboard.add(types.InlineKeyboardButton(withsmile, callback_data=f"menu_type {tmp[i][0]}"))
    keyboard.add(types.InlineKeyboardButton("Главное меню ↩", callback_data="menu_back"))
    await message.answer('Выберите категорию:', reply_markup=keyboard)
    if status == '1' and message.text == 'Меню🍽':
        cursor.execute(f"SELECT menuMessage FROM login_id WHERE ID='{message.chat.id}'")
        user_message = cursor.fetchone()[0].split(',')
        for i in range(len(user_message)):
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=int(user_message[i]))
            except:
                pass
    cursor.execute(
        f"UPDATE login_id SET menuStatus='1', menuMessage='{message.message_id + 1}' WHERE ID='{message.chat.id}'")
    connect.commit()


@dp.callback_query_handler(Text(startswith='menu_type'))
async def menu_type(callback: types.CallbackQuery, state: FSMContext):
    try:
        await callback.message.delete()
    except:
        pass
    name = callback.data.split(' ')[1]
    cursor.execute(f"SELECT Name,ID FROM menu WHERE Type='{name}'")
    tmp = cursor.fetchall()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    item_id = []
    for i in range(len(tmp)):
        cursor.execute(f"SELECT Photo,Description,Price,Name FROM menu WHERE ID='{tmp[i][1]}'")
        position = cursor.fetchone()
        await asyncio.sleep(0.55)
        if position[1] != "отсутствует":
            message = await callback.message.answer_photo(photo=str(position[0]), caption=f"Название: {position[3]}"
                                                                                          f"\nОписание: {position[1]}"
                                                                                          f"\nЦена: {position[2]} ₽")
        else:
            message = await callback.message.answer_photo(photo=str(position[0]), caption=f"Название: {position[3]}"
                                                                                          f"\nЦена: {position[2]} ₽")
        message_id = message.message_id
        item_id.append(message_id)
        keyboard.add(types.InlineKeyboardButton(tmp[i][0], callback_data=f"menu_item {tmp[i][1]}"))
    keyboard.add(types.InlineKeyboardButton('Назад ↩', callback_data="menu_return"))
    async with state.proxy() as data:
        data['type'] = name
    sended_message = await bot.send_message(callback.message.chat.id, text='Сделайте выбор', reply_markup=keyboard)
    text = f"{sended_message.message_id},{','.join(map(str, item_id))}"
    cursor.execute(f"UPDATE login_id SET menuMessage='{text}' WHERE ID='{callback.message.chat.id}'")
    connect.commit()
    await callback.answer()


@dp.callback_query_handler(Text(equals='menu_back'))
async def menu_type_back(callback: types.CallbackQuery):
    await callback.answer('Вы были перемещены в главное меню')
    await main_menu(callback.message)
    await callback.message.delete()
    cursor.execute(
        f"UPDATE login_id SET menuMessage='NULL', menuStatus='NULL' WHERE ID='{callback.message.chat.id}'")
    connect.commit()


@dp.callback_query_handler(Text(startswith='menu_item'))
async def menu_item(callback: types.CallbackQuery, state: FSMContext):
    item_id = callback.data.split('menu_item ')[1]
    cursor.execute(f"SELECT Available FROM menu WHERE ID='{item_id}'")
    if cursor.fetchone()[0] == 0:
        await callback.answer('Данная позиция в текущий момент недоступна')
        return
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    async with state.proxy() as data:
        cursor.execute(f"SELECT menuMessage FROM login_id WHERE ID='{callback.message.chat.id}'")
        message = cursor.fetchone()[0].split(',')
        for i in range(len(message)):
            try:
                await bot.delete_message(chat_id=callback.message.chat.id, message_id=int(message[i]))
            except:
                pass
        data['id'] = item_id
        data['amount'] = 1
        data['size'] = 'Empty'
        data['item_id'] = item_id
    cursor.execute(f"SELECT Name FROM menu WHERE ID='{item_id}'")
    size = cursor.fetchone()[0]
    cursor.execute(f"SELECT size,price FROM item_size WHERE Type='{data['type']}' AND Pos_Name='{size}'")
    positions = cursor.fetchall()
    if len(positions) > 0:
        async with state.proxy() as data:
            data['size'] = None
        keyboard.add(types.InlineKeyboardButton('Выбрать размер', callback_data=f"menu_adds_size"))
    cursor.execute(f"SELECT * FROM adds WHERE Permission like '%{data['type']}%'")
    if len(cursor.fetchall()) > 0:
        keyboard.add(types.InlineKeyboardButton('Добавить ингредиенты', callback_data=f"menu_adds_item {item_id}"))
    keyboard.row(types.InlineKeyboardButton('➖', callback_data='data_downgrade'),
                 types.InlineKeyboardButton(f"{data['amount']} шт.", callback_data=f"nothing"),
                 types.InlineKeyboardButton('➕', callback_data='data_increase'))
    keyboard.add(types.InlineKeyboardButton('В корзину', callback_data=f"menu_send_cart"))
    keyboard.add(types.InlineKeyboardButton('Назад ↩', callback_data="menu__item_back"))
    cursor.execute(f"SELECT Photo,Description,Price FROM menu WHERE ID='{item_id}'")
    tmp = cursor.fetchone()
    text = ''
    if tmp[1] != "отсутствует":
        text += f"Описание: {tmp[1]}"
    if data['size'] is None:
        for i in range(len(positions)):
            text += f"\n{positions[i][0]} - {positions[i][1]} ₽"
    else:
        text += f"\nЦена: {tmp[2]} ₽"
    message_text = await callback.message.answer_photo(photo=str(tmp[0]), reply_markup=keyboard,
                                                       caption=text)
    cursor.execute(
        f"UPDATE login_id SET menuMessage='{message_text.message_id}' WHERE ID='{callback.message.chat.id}'")
    connect.commit()


@dp.callback_query_handler(Text(equals='menu_adds_size'))
async def menu_adds_size(callback: types.CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    async with state.proxy() as data:
        cursor.execute(f"SELECT Name FROM menu WHERE ID='{data['item_id']}'")
        size = cursor.fetchone()[0]
    cursor.execute(f"SELECT size,price FROM item_size WHERE Type='{data['type']}' AND Pos_Name='{size}'")
    sizes = cursor.fetchall()
    for i in range(len(sizes)):
        keyboard.add(types.InlineKeyboardButton(f"{sizes[i][0]} {sizes[i][1]} ₽",
                                                callback_data=f"menu_sizes {sizes[i][0]}"))
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(Text(startswith='menu_sizes'))
async def menu_item_size(callback: types.CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    async with state.proxy() as data:
        data['size'] = callback.data.split("menu_sizes ")[1]
        cursor.execute(f"SELECT * FROM adds WHERE Permission like '%{data['type']}%'")
    keyboard.add(types.InlineKeyboardButton(f'Выбранный размер: {callback.data.split("menu_sizes ")[1]}',
                                            callback_data=f"menu_adds_size"))
    if len(cursor.fetchall()) > 0:
        keyboard.add(
            types.InlineKeyboardButton('Добавить ингредиенты', callback_data=f"menu_adds_item {data['item_id']}"))
    keyboard.row(types.InlineKeyboardButton('➖', callback_data='data_downgrade'),
                 types.InlineKeyboardButton(f"{data['amount']} шт.", callback_data=f"nothing"),
                 types.InlineKeyboardButton('➕', callback_data='data_increase'))
    keyboard.add(types.InlineKeyboardButton('В корзину', callback_data=f"menu_send_cart"))
    keyboard.add(types.InlineKeyboardButton('Назад ↩', callback_data="menu__item_back"))
    await callback.message.edit_reply_markup(reply_markup=keyboard)


@dp.callback_query_handler(Text(equals='data_downgrade'))
async def data_downgrade(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data['amount'] == 1:
            await callback.answer()
            return
        else:
            data['amount'] -= 1
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    cursor.execute(f"SELECT size,price FROM item_size WHERE Type='{data['type']}'")
    if len(cursor.fetchall()) > 0:
        if data['size'] is None:
            keyboard.add(types.InlineKeyboardButton('Выбрать размер', callback_data=f"menu_adds_size"))
        else:
            keyboard.add(types.InlineKeyboardButton(f"Выбранный размер: {data['size']}",
                                                    callback_data=f"menu_adds_size"))
    cursor.execute(f"SELECT * FROM adds WHERE Permission like '%{data['type']}%'")
    if len(cursor.fetchall()) > 0:
        keyboard.add(
            types.InlineKeyboardButton('Добавить ингредиенты', callback_data=f"menu_adds_item {data['item_id']}"))
    keyboard.row(types.InlineKeyboardButton('➖', callback_data='data_downgrade'),
                 types.InlineKeyboardButton(f"{data['amount']} шт.", callback_data=f"nothing"),
                 types.InlineKeyboardButton('➕', callback_data='data_increase'))
    keyboard.add(types.InlineKeyboardButton('В корзину', callback_data=f"menu_send_cart"))
    keyboard.add(types.InlineKeyboardButton('Назад ↩', callback_data="menu__item_back"))
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(Text(equals='data_increase'))
async def data_increase(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] += 1
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    cursor.execute(f"SELECT size,price FROM item_size WHERE Type='{data['type']}'")
    if len(cursor.fetchall()) > 0:
        if data['size'] is None:
            keyboard.add(types.InlineKeyboardButton('Выбрать размер', callback_data=f"menu_adds_size"))
        else:
            keyboard.add(types.InlineKeyboardButton(f"Выбранный размер: {data['size']}",
                                                    callback_data=f"menu_adds_size"))
    cursor.execute(f"SELECT * FROM adds WHERE Permission like '%{data['type']}%'")
    if len(cursor.fetchall()) > 0:
        keyboard.add(
            types.InlineKeyboardButton('Добавить ингредиенты', callback_data=f"menu_adds_item {data['item_id']}"))
    keyboard.row(types.InlineKeyboardButton('➖', callback_data='data_downgrade'),
                 types.InlineKeyboardButton(f"{data['amount']} шт.", callback_data=f"nothing"),
                 types.InlineKeyboardButton('➕', callback_data='data_increase'))
    keyboard.add(types.InlineKeyboardButton('В корзину', callback_data=f"menu_send_cart"))
    keyboard.add(types.InlineKeyboardButton('Назад ↩', callback_data="menu__item_back"))
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(Text(startswith='menu_adds_item'))
async def menu_adds_item(callback: types.CallbackQuery, state: FSMContext):
    cursor.execute(f"SELECT Name FROM menu WHERE ID='{callback.data.split('menu_adds_item ')[1]}'")
    name = cursor.fetchone()[0]
    async with state.proxy() as data:
        if data['size'] is None:
            await callback.answer('Выберите размер')
            return
        cursor.execute(f"SELECT Name,Price FROM adds WHERE Permission like '%{data['type']}%'")
        data['adds'] = []
    adds = cursor.fetchall()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for i in range(len(adds)):
        keyboard.add(types.InlineKeyboardButton(f"{adds[i][0]} {adds[i][1]} ₽",
                                                callback_data=f"menu_adds {adds[i][0]}"))
    keyboard.add(types.InlineKeyboardButton("В корзину", callback_data="menu_cart_send"))
    await callback.answer()
    try:
        await callback.message.delete()
    except:
        pass
    await callback.message.answer(text=f'Выберите ингредиенты для добавки в {name}', reply_markup=keyboard)
    cursor.execute(
        f"UPDATE login_id SET menuMessage='{callback.message.message_id + 1}' WHERE ID='{callback.message.chat.id}'")
    connect.commit()


@dp.callback_query_handler(Text(startswith='menu_adds'))
async def menu_adds(callback: types.CallbackQuery, state: FSMContext):
    add_name = callback.data.split('menu_adds ')[1]
    async with state.proxy() as data:
        data['adds'].append(add_name)
    await callback.answer(f'{add_name} успешно добавлен')


@dp.callback_query_handler(Text(equals='menu_cart_send'))
async def menu_cart_send(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        cursor.execute(f"SELECT Name FROM menu WHERE ID='{data['id']}'")
    name = cursor.fetchone()[0]
    cursor.execute(f"SELECT price FROM item_size WHERE Type='{data['type']}' AND size='{data['size']}'")
    price = cursor.fetchone()
    if not data['adds']:
        if price:
            cursor.execute(f"INSERT INTO cart(user_ID,Name,Size) VALUES({callback.message.chat.id},'{name}','{data['size']}')")
        else:
            cursor.execute(f"INSERT INTO cart(user_ID,Name) VALUES({callback.message.chat.id},'{name}')")
    else:
        if price:
            cursor.execute(f"INSERT INTO cart(user_ID,Name,Adds,Size) VALUES({callback.message.chat.id},'{name}','{','.join(data['adds'])}','{data['size']}')")
        else:
            cursor.execute(f"INSERT INTO cart(user_ID,Name,Adds) VALUES({callback.message.chat.id},'{name}','{','.join(data['adds'])}')")
    cursor.execute(
        f"UPDATE login_id SET menuMessage='NULL', menuStatus='NULL' WHERE ID='{callback.message.chat.id}'")
    connect.commit()
    await state.finish()
    await callback.answer('Товар успешно добавлен в корзину!')
    await callback.message.delete()
    await menu(callback.message)


@dp.callback_query_handler(Text(startswith='menu_send_cart'))
async def menu_send_cart(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data['size'] is None:
            await callback.answer('Выберите размер')
            return
        cursor.execute(f"SELECT Name FROM menu WHERE ID='{data['id']}'")
        name = cursor.fetchone()[0]
        cursor.execute(f"SELECT price FROM item_size WHERE Type='{data['type']}' AND size='{data['size']}'")
        price = cursor.fetchone()
        if price:
            for i in range(data['amount']):
                cursor.execute(f"INSERT INTO cart(user_ID,Name,Size) VALUES({callback.message.chat.id},'{name}','{data['size']}')")
                connect.commit()
        else:
            for i in range(data['amount']):
                cursor.execute(f"INSERT INTO cart(user_ID,Name)"
                               f" VALUES({callback.message.chat.id}, '{name}')")
                connect.commit()
    await state.finish()
    await callback.answer('Ваш товар был успешно добавлен в корзину')
    cursor.execute(
        f"UPDATE login_id SET menuMessage='NULL', menuStatus='NULL' WHERE ID='{callback.message.chat.id}'")
    connect.commit()
    await callback.message.delete()
    await menu(callback.message)


@dp.callback_query_handler(Text(equals='menu__item_back'))
async def menu_item_back(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        name = data['type']
    cursor.execute(f"SELECT Name,ID FROM menu WHERE Type='{name}'")
    tmp = cursor.fetchall()
    item_id = []
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for i in range(len(tmp)):
        cursor.execute(f"SELECT Photo,Description,Price,Name FROM menu WHERE ID='{tmp[i][1]}'")
        position = cursor.fetchone()
        if position[1] != "отсутствует":
            message = await callback.message.answer_photo(photo=str(position[0]), caption=f"Название: {position[3]}"
                                                                                          f"\nОписание: {position[1]}"
                                                                                          f"\nЦена: {position[2]} ₽")
        else:
            message = await callback.message.answer_photo(photo=str(position[0]), caption=f"Название: {position[3]}"
                                                                                          f"\nЦена: {position[2]} ₽")
        message_id = message.message_id
        item_id.append(message_id)
        keyboard.add(types.InlineKeyboardButton(tmp[i][0], callback_data=f"menu_item {tmp[i][1]}"))
    keyboard.add(types.InlineKeyboardButton('Назад ↩', callback_data="menu_return"))
    sended_message = await bot.send_message(callback.message.chat.id, text='Сделайте выбор', reply_markup=keyboard)
    text = f"{sended_message.message_id},{','.join(map(str, item_id))}"
    cursor.execute(f"UPDATE login_id SET menuMessage='{text}' WHERE ID='{callback.message.chat.id}'")
    await callback.message.delete()
    connect.commit()


@dp.callback_query_handler(Text(startswith='menu_return'))
async def menu_return(callback: types.CallbackQuery):
    await callback.answer()
    cursor.execute(f"SELECT menuMessage FROM login_id WHERE ID='{callback.message.chat.id}'")
    message = cursor.fetchone()[0].split(',')
    for i in range(len(message)):
        try:
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=int(message[i]))
        except:
            pass
    await menu(callback.message)


@dp.message_handler(Text(equals='Корзина🛒'), chat_type='private')
async def cart(message: types.Message):
    cursor.execute(f"SELECT Name,Adds,Size FROM cart WHERE user_ID='{message.chat.id}'")
    items = cursor.fetchall()
    cart_price = 0
    cursor.execute(f"SELECT menuStatus FROM login_id WHERE ID='{message.chat.id}'")
    status = cursor.fetchone()
    if status[0] == '1' and message.text == 'Корзина🛒':
        cursor.execute(f"SELECT menuMessage FROM login_id WHERE ID='{message.chat.id}'")
        user_message = cursor.fetchone()[0].split(',')
        for i in range(len(user_message)):
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=int(user_message[i]))
            except:
                pass
    if len(items) > 0:
        await message.answer('Список товаров в корзине')
        for i in range(len(items)):
            item_adds_price = 0
            if items[i][2] is not None:
                cursor.execute(f"SELECT Price FROM item_size WHERE Pos_Name='{items[i][0]}' AND size='{items[i][2]}'")
                size = 1
            else:
                cursor.execute(f"SELECT Price FROM menu WHERE Name='{items[i][0]}'")
                size = 0
            item_price = cursor.fetchone()[0]
            if items[i][1]:
                item_adds = items[i][1].split(',')
                for j in range(len(item_adds)):
                    cursor.execute(f"SELECT Price from adds where Name='{item_adds[j]}'")
                    item_adds_price += cursor.fetchone()[0]
                if size == 0:
                    await message.answer(
                        f"{i + 1}. {items[i][0]}\nДобавки: {items[i][1]}\nСумма: {item_adds_price + item_price} ₽")
                else:
                    await message.answer(
                        f"{i + 1}. {items[i][0]} {items[i][2]}\nДобавки: {items[i][1]}\nСумма: {item_adds_price + item_price} ₽")
            else:
                item_adds_price = 0
                if size == 0:
                    await message.answer(f"{i + 1}. {items[i][0]}\nСумма: {item_price} ₽")
                else:
                    await message.answer(f"{i + 1}. {items[i][0]} {items[i][2]}\nСумма: {item_price} ₽")
            cart_price += item_adds_price + item_price
        if fifteenPercent == 1:
            cart_price = round(cart_price * 0.85)
            await message.answer(f"Промоакция снизила общую сумму заказа на 15%")
        cursor.execute(f"SELECT OrdersSum FROM login_id WHERE ID={message.chat.id}")
        orderssum = cursor.fetchone()
        if orderssum[0] >= 5000:
            cart_price = round(cart_price * 0.9)
            await message.answer(f"На ваш заказ действует скидка 10% за сумму заказов свыше 5000.")
        else:
            if 5000 - (orderssum[0] + cart_price) > 0:
                await message.answer(f"Накапливаете заказы на сумму 5000 ₽ и получайте СКИДКУ 10% на следующий заказ. Вам осталось {5000 - (orderssum[0] + cart_price)}₽")
            elif 5000 - (orderssum[0] + cart_price) < 0:
                await message.answer(f"С учётом суммы текущего заказа, на следующий заказ будет действовать скидка 10%!")
        if fifteenPercent == 1:
            cart_price *= 0.85
            await message.answer(f"Промоакция снизила общую сумму заказа на 15%")
        await message.answer(f'Общая сумма c доставкой {cart_price + delivery_price} ₽'
                             f'\nОбщая сумма при самовывозе {cart_price} ₽')
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton('Да', callback_data=f"cart_payment_menu {cart_price}"))
        keyboard.add(types.InlineKeyboardButton('Удалить позицию', callback_data='cart_position_delete'))
        keyboard.add(types.InlineKeyboardButton('Очистить корзину', callback_data='cart_clear'))
        keyboard.add(types.InlineKeyboardButton('Вернуться в главное меню', callback_data='cart_return'))
        sended_message = await message.answer('Продолжить?', reply_markup=keyboard)
        cursor.execute(
            f"UPDATE login_id SET menuStatus='1', menuMessage='{sended_message.message_id}' WHERE ID='{message.chat.id}'")
        connect.commit()
    else:
        cursor.execute(
            f"UPDATE login_id SET menuMessage='NULL', menuStatus='NULL' WHERE ID='{message.chat.id}'")
        connect.commit()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        buttons = ['Оставить отзыв🖌', 'Меню🍽', 'Тех. Поддержка🆘', 'Статус заказа🔍', 'Корзина🛒',
                   'Редактировать профиль✏', 'В предыдущее меню↩']
        keyboard.add(*buttons)
        await message.answer('Корзина пуста', reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith='cart_payment_menu'))
async def cart_payment_menu(callback: types.CallbackQuery):
    if datetime.now().hour < 10 or datetime.now().hour > 22 and datetime.now().minute != 0:
        await callback.answer('Мы с удовольствием приготовим Ваш заказ в рабочее время с 10:00 до 22:00. С Уважением, Ваш Burgertek!',show_alert=True)
        return
    cursor.execute(f"SELECT Имя FROM login_id WHERE ID={callback.message.chat.id}")
    ban_or_not = cursor.fetchone()
    if ban_or_not[0] == 'Banned':
        await callback.message.answer("Вы были забанены.")
    else:
        if not work_shift:
            await callback.answer('Мы с удовольствием приготовим Ваш заказ в рабочее время с 10:00 до 22:00. С Уважением, Ваш Burgertek!', show_alert=True)
            return
        cursor.execute(
            f"UPDATE cart_data SET Комментарий='отсутствует',Время_Доставки='отсутствует',Способ_Оплаты='отсутствует',Сумма_Заказа='{callback.data.split('cart_payment_menu ')[1]}',Difference='0' WHERE ID='{callback.message.chat.id}'")
        connect.commit()
        await callback.message.delete()
        await cart__payment_menu(callback.message)


@dp.message_handler(chat_type='private', commands='givechatid')
async def givechatid(message: types.Message):
    await message.answer(message.chat.id)


async def cart__payment_menu(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    cursor.execute(
        f"SELECT Комментарий,Адрес,Тип_Доставки,Время_Доставки,Адрес,Способ_Оплаты FROM cart_data where ID='{message.chat.id}'")
    user = cursor.fetchone()
    keyboard.add(types.InlineKeyboardButton('Изменить тип доставки', callback_data='cart_payment_delivery'))
    keyboard.add(types.InlineKeyboardButton('Изменить время доставки', callback_data='cart_payment_delivery_time'))
    keyboard.add(types.InlineKeyboardButton('Изменить тип оплаты', callback_data='cart_payment_type'))
    if user[0] == 'отсутствует':
        keyboard.add(types.InlineKeyboardButton('Добавить комментарий к заказу', callback_data='cart_payment_comment'))
    else:
        keyboard.add(types.InlineKeyboardButton('Изменить комментарий', callback_data='cart_payment_comment'))
    keyboard.add(types.InlineKeyboardButton('Перейти к оплате', callback_data='cart_payment_confirming'))
    if user[2] == 'Самовывоз':
        await message.answer(f"Ваши данные\n"
                             f"Тип доставки: {user[2]}\n"
                             f"Время получения: {user[3]}\n"
                             f"Способ оплаты: {user[5]}\n"
                             f"Комментарий к заказу(не обязателен): {user[0]}", reply_markup=keyboard)
    else:
        await message.answer(f"Ваши данные\n"
                             f"Тип доставки: {user[2]}\n"
                             f"Адрес доставки: {user[4]}\n"
                             f"Время доставки: {user[3]}\n"
                             f"Способ оплаты: {user[5]}\n"
                             f"Комментарий к заказу(не обязателен): {user[0]}", reply_markup=keyboard)
    cursor.execute(
        f"UPDATE login_id SET menuMessage='{message.message_id + 1}' WHERE ID='{message.chat.id}'")
    connect.commit()


@dp.callback_query_handler(Text(equals='cart_payment_confirming'))
async def cart_payment_confirming(callback: types.CallbackQuery):
    if datetime.now().hour > 21:
        await callback.answer("Мы с удовольствием приготовим Ваш заказ в рабочее время с 10:00 до 22:00. С Уважением, Ваш Burgertek!", show_alert=True)
        return
    cursor.execute(
        f"SELECT Адрес,Тип_Доставки,Время_Доставки,Адрес,Способ_Оплаты FROM cart_data where ID='{callback.message.chat.id}'")
    user = cursor.fetchone()
    for i in range(len(user)):
        if user[i] == 'отсутствует':
            await callback.answer('Не все данные заполнены, проверьте корректность данных')
            return
    cursor.execute(
        f"UPDATE login_id SET menuMessage='NULL', menuStatus='NULL' WHERE ID='{callback.message.chat.id}'")
    connect.commit()
    await callback.message.edit_text('Ваш заказ был передан персоналу.\n'
                                     'Ожидайте подтверждения заказа в течение 2 минут ✉️')
    cursor.execute(f"SELECT Name,Adds,Size FROM cart WHERE user_ID='{callback.message.chat.id}'")
    items = cursor.fetchall()
    positions = []
    item_dict = {}
    text = 'Позиции в заказе\n'
    for i in range(len(items)):
        cursor.execute(f"SELECT Type FROM menu WHERE Name='{items[i][0]}'")
        item_type = cursor.fetchone()[0]
        if item_dict.get(f'{item_type}') is None:
            item_dict[f'{item_type}'] = 1
        else:
            item_dict[f'{item_type}'] += 1
        if items[i][1] is not None:
            if items[i][2] is not None:
                text += f"{i + 1}. {items[i][0]}_{items[i][2]}\nДобавки:{items[i][1]}\n"
                positions.append(f"{items[i][0]}_{items[i][2]} Добавки:{items[i][1]}")
            else:
                text += f"{i + 1}. {items[i][0]}\nДобавки:{items[i][1]}\n"
                positions.append(f"{items[i][0]} Добавки:{items[i][1]}")
        else:
            if items[i][2] is not None:
                text += f"{i + 1}. {items[i][0]}_{items[i][2]}\n"
                positions.append(f"{items[i][0]}_{items[i][2]}")
            else:
                text += f"{i + 1}. {items[i][0]}\n"
                positions.append(f"{items[i][0]}")
    keys = []
    for i in item_dict.keys():
        keys.append(i)
    cursor.execute(
        f"SELECT Сумма_Заказа,Адрес,Время_Доставки,Способ_Оплаты,Тип_Доставки,Комментарий,Difference FROM cart_data WHERE ID='{callback.message.chat.id}'")
    user = cursor.fetchall()[0]
    if user[4] != 'Самовывоз':
        user = list(user)
        user[0] = int(float(user[0])) + 150
        user = tuple(user)
    text += f"Общая стоимость заказа: {user[0]} ₽\nСпособ оплаты: {user[3]}\n"
    if user[4] != 'Самовывоз':
        text += f"Тип Доставки: {user[4]}\nАдрес: {user[1]}"
    else:
        text += f"Тип Доставки: {user[4]}"
    if user[5] != 'отсутствует':
        text += f"\nКомментарий к заказу: {user[5]}"
    cursor.execute(f"UPDATE cart_data SET Callback='{callback.message.chat.id};{user[0]};{user[2]};{user[3]};{user[6]}' WHERE ID='{callback.message.chat.id}'")
    connect.commit()
    cursor.execute(f"SELECT Имя,Телефон FROM login_id WHERE ID={callback.message.chat.id}")
    _user = cursor.fetchone()
    cursor.execute(
        f"INSERT INTO orders (User_ID, Status, List, Price,Способ_Оплаты, Адрес, Тип_Доставки, Время_Доставки, Комментарий, Data, Текст) VALUES ({callback.message.chat.id}, 'в обработке', '{';'.join(positions)}', '{user[0]}', '{user[3]}', '{user[1]}', '{user[4]}', '{user[2]}', '{user[5]}', '{datetime.today().date()}', 'Поступил заказ от: {callback.message.chat.id}\nИмя пользователя: {_user[0]}\nТелефон для связи: {_user[1]}\n{text}')")
    connect.commit()
    cursor.execute("SELECT ID FROM orders ORDER BY id DESC LIMIT 1")
    order_id = cursor.fetchone()[0]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton("Принять заказ", callback_data=f"order_accept {callback.message.chat.id} {order_id}"))
    keyboard.add(
        types.InlineKeyboardButton("Откорректировать/отменить заказ", callback_data=f"order_decline {callback.message.chat.id} {order_id}"))
    message_obj = await bot.send_message(chat_id=-1001590114672, text=f"Поступил заказ от: {callback.message.chat.id}\nИмя пользователя: {_user[0]}\nТелефон для связи: {_user[1]}\n{text}\nВремя доставки: {user[2]}",
                                         reply_markup=keyboard)
    cursor.execute(f"UPDATE orders SET messageid = {message_obj.message_id}, callback = '{callback.message.chat.id};{user[0]};{user[2]};{user[3]};{user[6]}' WHERE ID={order_id}")
    connect.commit()
    cursor.execute(f"DELETE FROM cart WHERE user_ID='{callback.message.chat.id}'")
    connect.commit()


@dp.callback_query_handler(Text(startswith='order_accept '))
async def order_accept(callback: types.CallbackQuery, state: FSMContext):
    order_id = callback.data.split(' ')[2]
    cursor.execute(f"SELECT callback FROM orders WHERE id={order_id}")
    user_info = cursor.fetchone()[0].split(';')
    async with state.proxy() as data:
        data['user_time'] = user_info[2]
    if user_info[2] == 'Как можно быстрее':
        delivery_type = 1
        current_time = 'отсутствует'
        cursor.execute(
            f"UPDATE orders SET Status='Готовится',Статус_Оплаты='ожидается',deliveryType='{delivery_type}',startCooking='отсутствует' WHERE ID={order_id}")
        connect.commit()
    else:
        delivery_type = 0
        current_time = user_info[2]
        cursor.execute(
            f"UPDATE orders SET Status='Готовится',Статус_Оплаты='ожидается',deliveryType='{delivery_type}',startCooking='{current_time}' WHERE id={order_id}")
        connect.commit()
    cursor.execute(f"SELECT Тип_Доставки FROM cart_data WHERE ID='{callback.data.split(' ')[1]}'")
    user_delivery_type = cursor.fetchone()[0]
    cursor.execute(f"SELECT Текст FROM orders WHERE id={order_id}")
    user_text = cursor.fetchone()[0]
    cursor.execute(f"SELECT OrdersSum FROM login_id WHERE ID={user_info[0]}")
    z = cursor.fetchone()
    if z[0] >= 5000:
        cursor.execute(f"UPDATE login_id SET OrdersSum=0 WHERE ID={user_info[0]}")
        connect.commit()
    if user_info[3] == 'Картой в телеграме' or user_info[3] == 'Перевод на карту':
        text = f"Номер заказа: {order_id}\n{user_text}\nВремя Доставки: {user_info[2]}"
        await callback.message.edit_text(f"{text}\nСтатус оплаты: ожидается")
    else:
        text = f"Номер заказа: {order_id}\n{user_text}\nВремя Доставки: {user_info[2]}"
        await callback.message.edit_text(text)
    cursor.execute(f"UPDATE orders SET Текст='{text}' WHERE id={order_id}")
    connect.commit()
    if user_info[3] == 'Перевод на карту':
        await bot.send_message(chat_id=user_info[0], text=f"Ваш заказ был успешно принят :)\n"
                                                          f"Вы выбрали способ оплаты переводом.\n"
                                                          f"Отправьте {user_info[1]} ₽ по следующим реквизитам 89118059320, Держатель Зиновий Дмитриевич Б.\n"
                                                          f"Через 30 секунд появится сообщение для подтверждения оплаты")
        await asyncio.sleep(30)
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton('Подтвердить оплату', callback_data=f"order_transfer_accept {order_id}"))
        await bot.send_message(chat_id=user_info[0], text='Нажмите кнопку ниже, если вы уверены в оплате',
                               reply_markup=keyboard)
    elif user_info[3] == 'Картой в телеграме':
        prices = []
        cursor.execute(f"SELECT List FROM orders WHERE id={order_id}")
        user_list = cursor.fetchone()[0].split(';')
        for i in range(len(user_list)):
            if len(user_list[i].split(' Добавки:')) > 1:
                temp = user_list[i].split(' Добавки:')
                if len(temp[0].split('_')) > 1:
                    cursor.execute(f"SELECT Price FROM item_size WHERE size='{temp[0].split('_')[1]}'")
                else:
                    cursor.execute(f"SELECT Price FROM menu WHERE Name='{temp[0]}'")
                local_price = int(cursor.fetchone()[0])
                adds = temp[1].split(',')
                for j in range(len(adds)):
                    cursor.execute(f"SELECT Price FROM adds WHERE Name='{adds[j]}'")
                    local_price += int(cursor.fetchone()[0])
                    cursor.execute(f"SELECT OrdersSum FROM login_id WHERE ID={user_info[0]}")
                    orderssum = cursor.fetchone()
                    if orderssum[0] >= 5000:
                        local_price = round(int(local_price * 0.9))
                prices.append(LabeledPrice(label=f"{temp[0]}\nДобавки: {temp[1]}", amount=int(local_price * 100)))
            else:
                if len(user_list[i].split('_')) > 1:
                    item = user_list[i].split('_')
                    cursor.execute(f"SELECT Price FROM item_size WHERE Pos_Name='{item[0]}' AND size='{item[1]}'")
                else:
                    cursor.execute(f"SELECT Price FROM menu WHERE Name='{user_list[i]}'")
                price = cursor.fetchone()
                cursor.execute(f"SELECT OrdersSum FROM login_id WHERE ID={user_info[0]}")
                orderssum = cursor.fetchone()
                if orderssum[0] >= 5000:
                    price[0] = round(price[0] * 0.9)
                if fifteenPercent == 1:
                    price[0] = round(price[0] * 0.85)
                if len(user_list[i].split('_')) > 1:
                    prices.append(LabeledPrice(label=f"{' '.join(user_list[i].split('_'))}", amount=int(price[0] * 100)))
                else:
                    prices.append(LabeledPrice(label=f"{user_list[i]}", amount=int(price[0] * 100)))
        if user_delivery_type != 'Самовывоз':
            prices.append(LabeledPrice(label='Доставка', amount=delivery_price*100))
        await bot.send_message(chat_id=user_info[0], text=f"Ваш заказ был успешно принят :)\n"
                                                          f"Вы выбрали способ оплаты картой в телеграме.\n"
                                                          f"Воспользуйтесь сообщением ниже для оплаты заказа.")
        async with state.proxy() as data:
            data['user_id'] = user_info[0]
            data['user_delivery_type'] = user_delivery_type
            data['current_time'] = current_time
        await bot.send_invoice(chat_id=str(user_info[0]),
                               title='Заказ',
                               description='Описание',
                               provider_token=PAYMENT_TOKEN,
                               currency='rub',
                               photo_url="https://i.postimg.cc/htbGdDRz/2022-09-19-12-37-22.jpg",
                               photo_height=256,
                               photo_width=256,
                               photo_size=256,
                               is_flexible=False,
                               prices=prices,
                               start_parameter='Enable',
                               payload=f"{order_id};{data['current_time']};{data['user_id']};{data['user_delivery_type']};{data['user_time']}")
    else:
        if user_delivery_type == 'Самовывоз':
            if data['user_time'] == 'Как можно быстрее':
                await bot.send_message(chat_id=user_info[0],
                                       text=f"Спасибо за Ваш заказ! Ждём Вас в течение {interval_time} минут по адресу г.Полярный,ул.Гаджиева 11 ")
            else:
                await bot.send_message(chat_id=user_info[0],text=f"Спасибо за Ваш заказ! Ждём вас в {current_time} по адресу г.Полярный,ул.Гаджиева 11.")
        else:
            if data['user_time'] == 'Как можно быстрее':
                await bot.send_message(chat_id=user_info[0],
                                       text=f"Ваш заказ был передан персоналу. Среднее время доставки {interval_time} минут.")
            else:
                await bot.send_message(chat_id=user_info[0],
                                       text=f"Спасибо за Ваш заказ! Он будет доставлен к {current_time}.")


@dp.pre_checkout_query_handler(lambda q: True)
async def checkout_process(pre_checkout_query: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message):
    user_info = message.successful_payment.invoice_payload.split(';')
    print(user_info)
    cursor.execute(f"UPDATE orders SET Статус_Оплаты='Оплачен' WHERE ID={user_info[0]}")
    connect.commit()
    cursor.execute(f"SELECT messageID,Текст,Тип_Доставки FROM orders WHERE ID='{user_info[0]}'")
    user = cursor.fetchone()
    messageID = user[1] + '\nСтатус оплаты: Оплачен'
    await bot.edit_message_text(chat_id=-1001590114672, message_id=user[0], text=messageID)
    chat_id = user_info[2]
    current_time = user_info[1]
    user_time = user_info[4]
    if user_info[3] == 'Самовывоз':
        if user_time == 'Как можно быстрее':
            await bot.send_message(chat_id=chat_id,
                                   text=f"Спасибо за Ваш заказ! Ждём Вас в течение {interval_time} минут по адресу г.Полярный,ул.Гаджиева 11 ")
        else:
            await bot.send_message(chat_id=chat_id,
                                   text=f"Спасибо за Ваш заказ! Ждём вас в {current_time} по адресу г.Полярный,ул.Гаджиева 11.")
    else:
        if user_time == 'Как можно быстрее':
            await bot.send_message(chat_id=chat_id,
                                   text=f"Спасибо за Ваш заказ! Время доставки заказа {interval_time} минут\n"
                                        "Мы сообщим Вам как только курьер заберет заказ.")
        else:
            await bot.send_message(chat_id=chat_id,
                                   text=f"Спасибо за Ваш заказ! Заказ будет доставлен к {current_time}\n"
                                        "Мы сообщим Вам как только курьер заберет заказ.")
    global this_day
    cursor.execute(
        f"SELECT ID, User_ID, Status, List, Price, Способ_Оплаты, Адрес, Тип_Доставки, Время_Доставки, Комментарий, Статус_Оплаты, Data, CurierID FROM orders")
    info = cursor.fetchall()
    cursor.execute(f'SELECT "Способ_Оплаты", SUM(price) FROM orders GROUP BY "Способ_Оплаты"')
    money_buy_type = cursor.fetchall()
    tmp = '"Статус_Оплаты"'
    cursor.execute(f"SELECT SUM(price) FROM orders WHERE status!='Отменён' AND {tmp}='Оплачен'")
    money = cursor.fetchone()[0]
    cursor.execute(f"SELECT COUNT(*) FROM orders WHERE status!='Отменён'")
    cancels_amount = cursor.fetchone()[0]
    array = [["" for j in range(1)] for i in range(len(info))]
    for i in range(len(info)):
        if info[i][2] == 'Завершён':
            array[i][0] = str(info[i][4])
    results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
        "valueInputOption": "RAW",
        "data": [
            {"range": f"{this_day}!A1", 'values': [
                ['Количество заказов', 'Количество отменённых заказов', 'Выручка за день'],
                [len(info), cancels_amount, money]
            ]},
            {"range": f"{this_day}!A3", 'values': money_buy_type},
            {"range": f"{this_day}!A5",
             "values": [
                 ['ID заказа', 'ID пользователя', 'Статус заказа', 'Позиции в заказе', 'Сумма заказа', 'Способ Оплаты',
                  'Адрес', 'Тип доставки', 'Время доставки', 'Комментарий', 'Статус оплаты', 'Дата заказа',
                  'ID курьера, доставившего заказ', 'ИТОГО'],
             ]},
            {"range": f"{this_day}!A6", 'values': info
             },
            {"range": f"{this_day}!N6", 'values': array}
        ]
    }).execute()
    cursor.execute(f"SELECT User_ID, Price FROM orders WHERE ID={user_info[0]}")
    userid = cursor.fetchone()
    cursor.execute(f"SELECT OrdersSum FROM login_id WHERE ID={userid[0]}")
    z = cursor.fetchone()
    if z[0] >= 5000:
        cursor.execute(f"UPDATE login_id SET OrdersSum=0 WHERE ID={userid[0]}")
        connect.commit()


@dp.callback_query_handler(Text(startswith='order_transfer_accept '))
async def order_transfer_accept(callback: types.CallbackQuery):
    order_id = callback.data.split('order_transfer_accept ')[1]
    cursor.execute(
        f"UPDATE orders SET Статус_Оплаты='Оплачен' WHERE ID={order_id}")
    connect.commit()
    cursor.execute(f"SELECT messageID,Текст FROM orders WHERE ID='{order_id}'")
    user = cursor.fetchone()
    messageID = user[1] + '\nСтатус оплаты: Оплачен'
    await bot.edit_message_text(chat_id=-723156318, message_id=user[0], text=messageID)
    await callback.message.delete()
    cursor.execute(f"SELECT User_ID, Price FROM orders WHERE ID={order_id}")
    userid = cursor.fetchone()
    cursor.execute(f"SELECT OrdersSum FROM login_id WHERE ID={userid[0]}")
    z = cursor.fetchone()
    if z[0] >= 5000:
        cursor.execute(f"UPDATE login_id SET OrdersSum=0 WHERE ID={userid[0]}")
        connect.commit()
    cursor.execute(f"UPDATE login_id SET OrdersSum=OrdersSum+{userid[1]} WHERE ID={userid[0]}")
    connect.commit()
    cursor.execute(f"SELECT Тип_Доставки,Время_Доставки FROM orders WHERE ID='{order_id}'")
    delivery_info = cursor.fetchone()
    if delivery_info[0] == 'Самовывоз':
        if delivery_info[1] == 'Как можно быстрее':
            await bot.send_message(chat_id=callback.message.chat.id,
                                   text=f"Спасибо за Ваш заказ! Ждём Вас в течение {interval_time} минут по адресу г.Полярный,ул.Гаджиева 11 ")
        else:
            await bot.send_message(chat_id=callback.message.chat.id,
                                   text=f"Спасибо за Ваш заказ! Ждём вас в {delivery_info[1]} по адресу г.Полярный,ул.Гаджиева 11.")
    else:
        if delivery_info[1] == 'Как можно быстрее':
            await bot.send_message(chat_id=callback.message.chat.id,
                                   text=f"Ваш заказ был передан персоналу. Среднее время доставки {interval_time} минут.")
        else:
            await bot.send_message(chat_id=callback.message.chat.id,
                                   text=f"Спасибо за Ваш заказ! Он будет доставлен к {delivery_info[1]}")


@dp.callback_query_handler(Text(startswith='order_decline'))
async def order_decline(callback: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    call_info = callback.data.split('order_decline ')[1]
    user_info = call_info.split(' ')[1]
    keyboard.add(types.InlineKeyboardButton('Отсутствие позиции в наличии', callback_data=f"order_absent {user_info}"))
    await callback.message.edit_text(text='Укажите причину отмены заказа', reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(Text(startswith='order_absent'))
async def order_decline_absent(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['absent'] = []
    order_id = callback.data.split('order_absent ')[1]
    cursor.execute(f"SELECT List FROM orders WHERE ID='{order_id}'")
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    positions = cursor.fetchone()[0].split(';')
    for i in range(len(positions)):
        keyboard.add(types.InlineKeyboardButton(f"{positions[i]}", callback_data=f"absent_position;{i};{order_id}"))
    keyboard.add(
        types.InlineKeyboardButton('Продолжить', callback_data=f"order_end;{order_id};"))
    await callback.message.edit_text('Выберите позиции, которые недоступны в данный момент', reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(Text(startswith="absent_position;"))
async def absent_position(callback: types.CallbackQuery, state: FSMContext):
    user_info = callback.data.split(';')
    cursor.execute(f"SELECT List FROM orders WHERE ID='{user_info[2]}'")
    user_list = cursor.fetchone()[0].split(';')
    for i in range(len(user_list)):
        if i == int(user_info[1]):
            async with state.proxy() as data:
                data['absent'].append(user_list[i])
            user_list.pop(i)
            break
    cursor.execute(f"UPDATE orders SET List='{';'.join(user_list)}' WHERE ID={user_info[2]}")
    connect.commit()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for i in range(len(user_list)):
        keyboard.add(
            types.InlineKeyboardButton(f"{user_list[i]}", callback_data=f"absent_position;{i};{user_info[2]}"))
    keyboard.add(types.InlineKeyboardButton('Продолжить', callback_data=f"order_end;{user_info[2]}"))
    await callback.message.edit_reply_markup(reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(Text(startswith='order_end;'))
async def order_end(callback: types.CallbackQuery, state: FSMContext):
    order_id = callback.data.split('order_end;')[1]
    cursor.execute(f"SELECT List FROM orders WHERE ID={order_id}")
    user_list = cursor.fetchone()[0].split(';')
    cursor.execute(f"SELECT User_ID FROM orders WHERE ID={order_id}")
    user_id = cursor.fetchone()[0]
    cursor.execute(f"DELETE FROM cart WHERE user_ID='{user_id}'")
    connect.commit()
    for i in range(len(user_list)):
        item = user_list[i].split(' Добавки:')
        if item[0] == '':
            break
        if len(item) > 1:
            item_size = None
            item_adds = item[1]
            if len(item[0].split('_')) > 1:
                item = item[0].split('_')
                item_size = item[1]
            item_name = item[0]
            if item_size is None:
                cursor.execute(
                    f"INSERT INTO cart(user_ID,Name,Adds) VALUES({user_id},'{item_name}','{item_adds}')")
            else:
                cursor.execute(
                    f"INSERT INTO cart(user_ID,Name,Adds,Size) VALUES({user_id},'{item_name}','{item_adds}','{item_size}')")
            connect.commit()
        else:
            if len(item[0].split('_')) > 1:
                item = item[0].split('_')
                cursor.execute(f"INSERT INTO cart(user_ID,Name,Size) VALUES({user_id},'{item[0]}','{item[1]}')")
            else:
                cursor.execute(f"INSERT INTO cart(user_ID,Name) VALUES({user_id},'{item[0]}')")
            connect.commit()
    cursor.execute(f"DELETE FROM orders WHERE ID={order_id}")
    connect.commit()
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('Перейти в меню', callback_data='cart_end_menu'))
    keyboard.add(types.InlineKeyboardButton('Перейти в корзину', callback_data='cart_end_cart'))
    text = ''
    async with state.proxy() as data:
        for i in range(len(data['absent'])):
            text += f"{i + 1}.{data['absent'][i]} \n"
        await bot.send_message(user_id, f"К сожалению, в данный момент мы не можем приготовить:"
                                        f"\n{text}Вы можете выбрать что-то на замену или заказать без этих позиций. Спасибо за понимание.",
                               reply_markup=keyboard)
    await state.finish()
    await callback.answer('Заказ успешно отменён')
    await callback.message.delete()


@dp.callback_query_handler(Text(equals='cart_end_cart'))
async def cart_end_menu(callback: types.CallbackQuery):
    await callback.answer('Вы были перемещены в корзину')
    await callback.message.delete()
    await cart(callback.message)


@dp.callback_query_handler(Text(equals='cart_end_menu'))
async def cart_end_menu(callback: types.CallbackQuery):
    await callback.answer('Вы были перемещены в меню')
    await callback.message.delete()
    await menu(callback.message)


@dp.callback_query_handler(Text(equals='cart_payment_type'))
async def cart_payment_type(callback: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    cursor.execute(f"SELECT Тип_Доставки FROM cart_data WHERE ID='{callback.message.chat.id}'")
    if cursor.fetchone()[0] == 'Самовывоз':
        keyboard.add(types.InlineKeyboardButton('Картой на месте', callback_data='cart__payment_type Картой на месте'))
        keyboard.add(
            types.InlineKeyboardButton('Наличными на месте', callback_data='cart__payment_type Наличными на месте'))
    else:
        keyboard.add(
            types.InlineKeyboardButton('Наличными курьеру', callback_data='cart__payment_type Наличными курьеру'))
        keyboard.add(types.InlineKeyboardButton('Картой курьеру', callback_data='cart__payment_type Картой курьеру'))
    keyboard.add(types.InlineKeyboardButton('Онлайн', callback_data='cart__payment_type Онлайн'))
    keyboard.add(types.InlineKeyboardButton('Назад ↩', callback_data='cart__payment_back'))
    await callback.message.edit_text('Выберите тип оплаты', reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(Text(equals='cart__payment_back'))
async def cart__payment_back(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await cart__payment_menu(callback.message)


@dp.callback_query_handler(Text(startswith='cart__payment_type'))
async def cart__payment_type(callback: types.CallbackQuery):
    payment_type = callback.data.split('cart__payment_type ')[1]
    if payment_type != 'Онлайн':
        if payment_type == "Картой в телеграме":
            payment_type = "cashoncurier"
        elif payment_type == "Перевод на карту":
            payment_type = "cardtransfer"
        elif payment_type == "Наличными на месте":
            payment_type = "cashonplace"
        elif payment_type == "Наличными курьеру":
            payment_type = "cashoncurier"
        elif payment_type == "Картой курьеру":
            payment_type = "cardoncurier"
        elif payment_type == "Картой на месте":
            payment_type = "cardonplace"
        cursor.execute(f"SELECT available FROM payments WHERE name='{payment_type}'")
        if cursor.fetchone()[0] is False:
            await callback.answer('Извините, данный способ оплаты недоступен', show_alert=True)
            return
        cursor.execute(f"UPDATE cart_data SET Способ_Оплаты='{callback.data.split('cart__payment_type ')[1]}'")
        connect.commit()
        await callback.answer('Способ оплаты успешно изменён')
        await callback.message.delete()
        await cart__payment_menu(callback.message)
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(
            types.InlineKeyboardButton('Картой в телеграме', callback_data='cart___payment_type Картой в телеграме'))
        keyboard.add(
            types.InlineKeyboardButton('Перевод на карту', callback_data='cart___payment_type Перевод на карту'))
        keyboard.add(types.InlineKeyboardButton('Назад ↩', callback_data='cart___payment_back'))
        await callback.message.edit_text(text='Выберите способ онлайн оплаты', reply_markup=keyboard)


@dp.callback_query_handler(Text(equals='cart___payment_back'))
async def cart___payment_back(callback: types.CallbackQuery):
    await cart_payment_type(callback)
    await callback.answer()


@dp.callback_query_handler(Text(startswith='cart___payment_type'))
async def cart___payment_type(callback: types.CallbackQuery):
    paymenttype = callback.data.split('cart___payment_type ')[1]
    cursor.execute(f"UPDATE cart_data SET Способ_Оплаты='{paymenttype}'")
    if paymenttype == "Картой в телеграме":
        paymenttype = "cashoncurier"
    elif paymenttype == "Перевод на карту":
        paymenttype = "cardtransfer"
    elif paymenttype == "Наличными на месте":
        paymenttype = "cashonplace"
    elif paymenttype == "Наличными курьеру":
        paymenttype = "cashoncurier"
    elif paymenttype == "Картой на месте":
        paymenttype = "cardonplace"
    cursor.execute(f"SELECT available FROM payments WHERE name='{paymenttype}'")
    if cursor.fetchone()[0] is False:
        await callback.answer('Извините, данный способ оплаты недоступен', show_alert=True)
        return
    paymenttype = callback.data.split('cart___payment_type ')[1]
    cursor.execute(f"UPDATE cart_data SET Способ_Оплаты='{callback.data.split('cart___payment_type ')[1]}'")
    connect.commit()
    await callback.answer('Способ оплаты успешно изменён')
    await callback.message.delete()
    await cart__payment_menu(callback.message)


@dp.callback_query_handler(Text(equals='cart_payment_delivery_time'))
async def cart_payment_delivery_time(callback: types.CallbackQuery):
    if datetime.now().hour > 21:
        await callback.answer(
            "Мы с удовольствием приготовим Ваш заказ в рабочее время с 10:00 до 22:00. С Уважением, Ваш Burgertek!",
            show_alert=True)
        return
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('Как можно быстрее', callback_data='cart_delivery_time_fast'))
    keyboard.add(types.InlineKeyboardButton('Указать время доставки', callback_data='cart_delivery_time_pick'))
    await callback.message.edit_text(text='Сделайте выбор', reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(Text(equals='cart_delivery_time_fast'))
async def cart_delivery_time_fast(callback: types.CallbackQuery):
    cursor.execute(f"SELECT Тип_Доставки FROM cart_data WHERE ID='{callback.message.chat.id}'")
    cursor.execute(f"UPDATE cart_data SET Время_Доставки='Как можно быстрее',Difference='0' WHERE ID='{callback.message.chat.id}'")
    connect.commit()
    await callback.answer()
    await callback.message.delete()
    await cart__payment_menu(callback.message)


@dp.callback_query_handler(Text(equals='cart_delivery_time_pick'))
async def cart_delivery_time_pick(callback: types.CallbackQuery, state: FSMContext):
    current_time = datetime.now() + timedelta(minutes=45)
    if current_time.hour >= 22 and current_time.minute != 0:
        await callback.answer(f'К сожалению мы не сможем приготовить вам заказ, так как минимально доступное время выходит за наше время работы\nРабочее время 10.00-22.00', show_alert=True)
        return
    await callback.message.edit_text(
        text=f"Введите время в формате **:**\nБлижайшее доступное время {current_time.strftime('%H:%M')}")
    await Time.text.set()
    await callback.answer()


@dp.message_handler(state=Time.text)
async def time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text
        current_time = datetime.now() + timedelta(minutes=45)
    if len(data['time']) == 5 and data['time'][0].isdigit() and data['time'][1].isdigit() and data['time'][2] == ':' and \
            data['time'][3].isdigit() and data['time'][4].isdigit():
        hour = int(data['time'][0] + data['time'][1])
        minute = int(data['time'][3] + data['time'][4])
        if current_time.hour <= hour < 24:
            if hour >= 22 and minute != 0:
                await message.answer("Рабочее время 10.00-22.00")
                return
            if current_time.minute <= minute < 60 or (hour > current_time.hour and minute < 60):
                choosing_time = datetime(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day, hour=hour, minute=minute)
                cursor.execute(
                    f"UPDATE cart_data SET Время_Доставки='{choosing_time.strftime('%H:%M')}' WHERE ID='{message.chat.id}'")
                connect.commit()
                await state.finish()
                await cart__payment_menu(message)
            else:
                await message.answer('Неверный ввод времени, попробуйте ещё раз')
        else:
            await message.answer('Неверный ввод времени, попробуйте ещё раз')
    else:
        await message.answer('Неверный ввод времени, попробуйте ещё раз')


@dp.callback_query_handler(Text(equals='cart_payment_delivery'))
async def cart_payment_delivery(callback: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton('Самовывоз', callback_data='cart__payment_delivery Самовывоз'))
    keyboard.add(types.InlineKeyboardButton('Доставить на мой адрес',
                                            callback_data='cart__payment_delivery Доставить на мой адрес'))
    keyboard.add(
        types.InlineKeyboardButton('Доставка на указанный адрес', callback_data='cart__payment_delivery Указать адрес'))
    keyboard.add(
        types.InlineKeyboardButton('Назад ↩', callback_data='cart__payment_back'))
    await callback.message.edit_text(text='Выберите тип доставки', reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(Text(startswith='cart__payment_delivery'))
async def cart__payment_delivery(callback: types.CallbackQuery):
    delivery_type = callback.data.split('cart__payment_delivery ')[1]
    cursor.execute(
        f"UPDATE cart_data SET Тип_Доставки='{delivery_type}',Способ_Оплаты='отсутствует',Difference=NULL WHERE ID='{callback.message.chat.id}'")
    connect.commit()
    if delivery_type == 'Доставить на мой адрес':
        cursor.execute(f"SELECT Адрес FROM login_id WHERE ID='{callback.message.chat.id}'")
        address = cursor.fetchone()[0]
        cursor.execute(
            f"UPDATE cart_data SET Адрес='{address}', Время_Доставки='отсутствует' WHERE ID='{callback.message.chat.id}'")
        connect.commit()
        await callback.answer('Тип доставки успешно изменён!')
        await callback.message.delete()
        await cart__payment_menu(callback.message)
    elif delivery_type == 'Указать адрес':
        await callback.message.edit_text(text='Введите адрес, на который будет осуществлена доставка')
        await UserAddress.text.set()
        await callback.answer()
    elif delivery_type == 'Самовывоз':
        cursor.execute(
            f"UPDATE cart_data SET Адрес='Недоступно', Время_Доставки='отсутствует' WHERE ID='{callback.message.chat.id}'")
        connect.commit()
        await callback.message.delete()
        await cart__payment_menu(callback.message)


@dp.message_handler(state=UserAddress.text)
async def user_address(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text
    await state.finish()
    cursor.execute(
        f"UPDATE cart_data SET Адрес='{data['address']}', Время_Доставки='отсутствует' WHERE ID='{message.chat.id}'")
    connect.commit()
    await message.answer('Адрес для доставки успешно изменён!')
    await cart__payment_menu(message)


@dp.callback_query_handler(Text(equals='cart_payment_comment'))
async def cart_payment_comment(callback: types.CallbackQuery):
    await callback.message.edit_text(text='Оставьте комментарий к заказу:')
    await Comment.text.set()
    await callback.answer()


@dp.message_handler(state=Comment.text)
async def comment(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['comment'] = message.text
    await state.finish()
    cursor.execute(f"UPDATE cart_data SET Комментарий='{data['comment']}' WHERE ID='{message.chat.id}'")
    connect.commit()
    await cart__payment_menu(message)


@dp.callback_query_handler(Text(equals='cart_return'))
async def cart_return(callback: types.CallbackQuery):
    await callback.answer('Вы были перемещены в главное меню')
    await callback.message.delete()
    cursor.execute(
        f"UPDATE login_id SET menuMessage='NULL', menuStatus='NULL' WHERE ID='{callback.message.chat.id}'")
    connect.commit()
    await main_menu(callback.message)


@dp.callback_query_handler(Text(equals='cart_position_delete'))
async def cart_position_delete(callback: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    cursor.execute(f"SELECT Name,Adds,ID FROM cart WHERE user_ID='{callback.message.chat.id}'")
    items = cursor.fetchall()
    for i in range(len(items)):
        if items[i][1] is not None:
            keyboard.add(types.InlineKeyboardButton(f"{items[i][0]} Добавки: {items[i][1]}",
                                                    callback_data=f"cart_del_pos {items[i][2]}"))
        else:
            keyboard.add(types.InlineKeyboardButton(f"{items[i][0]}", callback_data=f"cart_del_pos {items[i][2]}"))
    keyboard.add(types.InlineKeyboardButton("Вернуться в корзину", callback_data="back_to_cart_list"))
    await callback.message.edit_text('Выберите позицию для удаления', reply_markup=keyboard)
    await callback.answer()


@dp.callback_query_handler(Text(equals='back_to_cart_list'))
async def back_to_cart_list(callback: types.CallbackQuery):
    await callback.answer("Вы были перемещены в корзину")
    await callback.message.delete()
    await cart(callback.message)


@dp.callback_query_handler(Text(startswith='cart_del_pos'))
async def cart_del_pos(callback: types.CallbackQuery):
    cursor.execute(f"SELECT Name,Adds,ID FROM cart WHERE user_ID='{callback.message.chat.id}'")
    if len(cursor.fetchall()) == 1:
        cursor.execute(
            f"UPDATE login_id SET menuMessage='NULL', menuStatus='NULL' WHERE ID='{callback.message.chat.id}'")
        connect.commit()
    cursor.execute(f"DELETE FROM cart WHERE ID='{callback.data.split('cart_del_pos ')[1]}'")
    connect.commit()
    await callback.answer('Позиция успешно удалена')
    await cart_position_delete(callback)


@dp.callback_query_handler(Text(equals='cart_clear'))
async def cart_clear(callback: types.CallbackQuery):
    cursor.execute(f"DELETE FROM cart WHERE user_ID='{callback.message.chat.id}'")
    connect.commit()
    await callback.answer('Корзина успешно очищена!')
    await callback.message.delete()
    await main_menu(callback.message)
    cursor.execute(
        f"UPDATE login_id SET menuMessage='NULL', menuStatus='NULL' WHERE ID='{callback.message.chat.id}'")
    connect.commit()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
