from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN, admins
import keyboard as kb
import functions as func
import sqlite3
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import Throttled
from random import randint
import os, glob
from aiogram.utils.markdown import link


storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
connection = sqlite3.connect('data.db')
q = connection.cursor()

class st(StatesGroup):
	item = State()
	item2 = State()
	item3 = State()
	item4 = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	ID = message.chat.id
	if result[0] == 0:
		if ID in admins:
			await message.answer(f'Привіт, адмін {ID}.', reply_markup=kb.menu)
		else:
			await message.answer(f'Привіт, {message.chat.first_name}.\nТи можеш надіслати мені новину або запитання, за бажанням прикріпивши відео та фото.')
	else:
		await message.answer('Ви заблоковані!')


@dp.message_handler(content_types=['text'], text='Панель адміністратора 🛠')
async def handfler(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id in admins:
			await message.answer('Ви відкрили панель адміністратора', reply_markup=kb.adm)

@dp.message_handler(content_types=['text'], text='Назад ◀️')
async def handledr(message: types.Message, state: FSMContext):
	await message.answer('Ви повернулися назад', reply_markup=kb.menu)


@dp.message_handler(content_types=['text'], text='Адміністратори 📖')
async def admi(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	ID = message.chat.id
	if result[0] == 0:
		if ID in admins:
			await message.answer(f'Список Адміністраторів:')
			for i in admins:
				await message.answer(f'<a href="tg://user?id={i}">{i}</a>', parse_mode="HTML")



@dp.message_handler(content_types=['text'], text='Заблоковані користувачі 📋')
async def handlaer(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id in admins:
			q.execute(f"SELECT * FROM users WHERE block == 1")
			result = q.fetchall()
			sl = []
			for index in result:
				i = index[0]
				sl.append(i)

			ids = '\n'.join(map(str, sl))
			await message.answer(f'ID заблокованих користувачів:\n{ids}')


@dp.message_handler(commands=['admins'])
async def adm(message: types.Message):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	ID = message.chat.id
	if result[0] == 0:
		if ID in admins:
			await message.answer(f'Список Адміністраторів:')
			for i in admins:
				await message.answer(f'<a href="tg://user?id={i}">{i}</a>', parse_mode="HTML")





@dp.message_handler(content_types=['text'], text='Заблокувати 🚫')
async def hanadler(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id in admins:
			await message.answer('Введіть ID користувача, якого хочете заблокувати.', reply_markup=kb.back)
			await st.item3.set()


@dp.message_handler(content_types=['text'], text='Розблокувати ❎')
async def hfandler(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id in admins:
			await message.answer('Введіть ID користувача, якого хочете розблокувати.', reply_markup=kb.back)
			await st.item4.set()


@dp.message_handler(content_types=['text'], text='Розсилка 📨')
async def hangdler(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id in admins:
			await message.answer('Введіть текст розсилки:', reply_markup=kb.back)
			await st.item.set()

@dp.message_handler(content_types=['text'])
@dp.throttled(func.antiflood, rate=300)
async def h(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	if result[0] == 0:
		if message.chat.id in admins:
			pass
		else:
			await message.answer('Ваше повідомлення надіслано.')
			for i in admins:
				name = link(f'{message.from_user.first_name}', f'tg://user?id={message.chat.id}')
				await bot.send_message(i, f'*Отримано нове повідомлення від:* {name}\nID: `{message.chat.id}`\nПовідомлення: _{message.text}_', reply_markup=kb.fun(message.chat.id), parse_mode='Markdown')
	else:
		await message.answer('Ви заблоковані!')



@dp.message_handler(content_types=["photo", "text"])
@dp.throttled(func.antiflood, rate=0)
async def photo(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	id = message.chat.id
	text = message.caption
	name = randint(1, 1000000)
	if result[0] == 0:
		if message.chat.id in admins:
			pass
		else:
			await message.photo[-1].download(f'{id}/{name}.jpg')
			await message.answer('Ваше повідомлення надіслано.')
			for i in admins:
				photo = open(f'{id}/{name}.jpg', 'rb')
				name = link(f'{message.from_user.first_name}', f'tg://user?id={message.chat.id}')
				await bot.send_photo(i, photo, caption=f'*Отримано фото від:* {name}\nID: `{message.chat.id}`\nТекст: {text}', reply_markup=kb.fun(message.chat.id), parse_mode='Markdown')
			for file in glob.glob(f"{id}/*"):
				os.remove(file)
	else:
		await message.answer('Ви заблоковані!')


@dp.message_handler(content_types=["video", "text"])
@dp.throttled(func.antiflood, rate=0)
async def video(message: types.Message, state: FSMContext):
	func.join(chat_id=message.chat.id)
	q.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
	result = q.fetchone()
	id = message.chat.id
	text = message.caption
	name = randint(1, 1000000)
	if result[0] == 0:
		if message.chat.id in admins:
			pass
		else:
			file_id = message.video.file_id  # Get file id
			file = await bot.get_file(file_id)  # Get file path
			await bot.download_file(file.file_path, f"{id}/{name}.mp4")
			await message.answer('Ваше повідомлення надіслано.')
			for i in admins:
				video = open(f'{id}/{name}.mp4', 'rb')
				name = link(f'{message.from_user.first_name}', f'tg://user?id={message.chat.id}')
				await bot.send_video(i, video.read(), caption=f'*Отримано відео від:* {name}\nID: `{message.chat.id}`\nТекст: {text}',reply_markup=kb.fun(message.chat.id), parse_mode='Markdown')

			for file in glob.glob(f"{id}/*"):
				os.remove(file)
	else:
		await message.answer('Ви заблоковані!')




@dp.callback_query_handler(lambda call: True) # Inline
async def cal(call, state: FSMContext):
	if 'ans' in call.data:
		a = call.data.index('-ans')
		ids = call.data[:a]
		await call.message.answer('Введіть відповідь користувачу:', reply_markup=kb.back)
		await st.item2.set()
		await state.update_data(uid=ids)
	elif 'ignor' in call.data:
		await call.answer('Видалено')
		await bot.delete_message(call.message.chat.id, call.message.message_id)
		await state.finish()
	elif 'ban' in call.data:
		a = call.data.index('-ban')
		ids = call.data[:a]


		q.execute(f"SELECT block FROM users WHERE user_id = {ids}")
		result = q.fetchall()
		connection.commit()
		if len(result) == 0:
			await call.message.answer('Користувач не знайдений в базі даних.', reply_markup=kb.adm)
			await state.finish()
		else:
			a = result[0]
			id = a[0]

			if ids in map(str, admins):
				await bot.send_message(call.message.chat.id, 'Це адміністратор 😑')

			elif id == 0:
				q.execute(f"UPDATE users SET block = 1 WHERE user_id = {ids}")
				connection.commit()
				await call.message.answer('Користувача заблоковано.', reply_markup=kb.adm)
				await state.finish()

				for i in admins:
					await bot.send_message(i,
										   f'Адміністратор <a href="tg://user?id={call.message.chat.id}">{call.message.chat.id}</a> заблокував користувача <a href="tg://user?id={ids}">{ids}</a>',
										   parse_mode="HTML")

				await bot.send_message(ids, 'Вас було заблоковано адміністрацією.')
			else:
				await call.message.answer('Цей користувач вже заблокований.', reply_markup=kb.adm)
				await state.finish()





@dp.message_handler(state=st.item2)
async def proc(message: types.Message, state: FSMContext):
	if message.text == 'Скасування':
		await message.answer('Скасування! Повертаюсь назад.', reply_markup=kb.menu)
		await state.finish()
	else:
		await message.answer('Повідомлення надіслано.', reply_markup=kb.menu)
		data = await state.get_data()
		id = data.get("uid")
		await state.finish()
		await bot.send_message(id, '<b>Вам відповів адміністратор!</b>\n\n<b>Відповідь:</b> {}'.format(message.text), parse_mode='HTML')
		for i in admins:
			await bot.send_message(i, f'Адміністратор <a href="tg://user?id={message.chat.id}">{message.chat.id}</a> надіслав відповідь користувачу <a href="tg://user?id={id}">{id}</a>\n\nВідповідь: {message.text}',parse_mode="HTML")

@dp.message_handler(state=st.item)
async def process_name(message: types.Message, state: FSMContext):
	q.execute(f'SELECT user_id FROM users')
	row = q.fetchall()
	connection.commit()
	text = message.text
	if message.text == 'Скасування':
		await message.answer('Скасування! Повертаюсь назад.', reply_markup=kb.adm)
		await state.finish()
	else:
		info = row
		await message.answer('Починаю розсилку!', reply_markup=kb.adm)
		for i in admins:
			await bot.send_message(i,f'Адміністратор <a href="tg://user?id={message.chat.id}">{message.chat.id}</a> починає розсилку! \nТекст: {text}',parse_mode="HTML")

		for i in range(len(info)):
			try:
				await bot.send_message(info[i][0], str(text))
			except:
				pass
		await message.answer('Розсилку завершено.', reply_markup=kb.adm)
		await state.finish()


@dp.message_handler(state=st.item3)
async def proce(message: types.Message, state: FSMContext):

	if message.text == 'Скасування':
		await message.answer('Скасування! Повертаюсь назад.', reply_markup=kb.adm)
		await state.finish()
	else:
		if message.text.isdigit():
			q.execute(f"SELECT block FROM users WHERE user_id = {message.text}")
			result = q.fetchall()
			connection.commit()
			if len(result) == 0:
				await message.answer('Користувач не знайдений в базі даних.', reply_markup=kb.adm)
				await state.finish()
			else:
				a = result[0]
				id = a[0]

				if message.text in map(str, admins):
					await bot.send_message(message.chat.id, 'Це адміністратор 😑')

				elif id == 0:
					q.execute(f"UPDATE users SET block = 1 WHERE user_id = {message.text}")
					connection.commit()
					await message.answer('Користувача заблоковано.', reply_markup=kb.adm)
					await state.finish()


					for i in admins:
						await bot.send_message(i,f'Адміністратор <a href="tg://user?id={message.chat.id}">{message.chat.id}</a> заблокував користувача <a href="tg://user?id={message.text}">{message.text}</a>',parse_mode="HTML")

					await bot.send_message(message.text, 'Вас було заблоковано адміністрацією.')
				else:
					await message.answer('Цей користувач вже заблокований.', reply_markup=kb.adm)
					await state.finish()
		else:
			await message.answer('Введіть ID!')

@dp.message_handler(state=st.item4)
async def proc(message: types.Message, state: FSMContext):
	if message.text == 'Скасування':
		await message.answer('Скасування! Повертаюсь назад.', reply_markup=kb.adm)
		await state.finish()
	else:
		if message.text.isdigit():
			q.execute(f"SELECT block FROM users WHERE user_id = {message.text}")
			result = q.fetchall()
			connection.commit()
			if len(result) == 0:
				await message.answer('Користувач не знайдений в базі даних.', reply_markup=kb.adm)
				await state.finish()
			else:
				a = result[0]
				id = a[0]
				if id == 1:
					q.execute(f"UPDATE users SET block = 0 WHERE user_id = {message.text}")
					connection.commit()
					await message.answer('Користувача розблоковано.', reply_markup=kb.adm)
					await state.finish()

					for i in admins:
						await bot.send_message(i,f'Адміністратор <a href="tg://user?id={message.chat.id}">{message.chat.id}</a> розблокував користувача <a href="tg://user?id={message.text}">{message.text}</a>',parse_mode="HTML")

					await bot.send_message(message.text, 'Вас було розблоковано аміністрацією.')
				else:
					await message.answer('Користувач не заблокований.', reply_markup=kb.adm)
					await state.finish()
		else:
			await message.answer('Введіть ID!')

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)