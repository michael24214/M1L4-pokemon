from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

# Установите ваш токен Telegram-бота
TELEGRAM_BOT_TOKEN = 'Your token'

# URL для получения данных о покемонах
POKEMON_API_URL = "https://pokeapi.co/api/v2/pokemon/"

# Хранилище для отслеживания уже запрашиваемых покемонов
requested_pokemons = set()

# Получение имени покемона по его номеру
def get_name(pokemon_number):
    url = f'{POKEMON_API_URL}{pokemon_number}/'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['forms'][0]['name']
    return "Unknown"

# Получение URL изображения покемона по его номеру
def get_img(pokemon_number):
    url = f'{POKEMON_API_URL}{pokemon_number}/'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['sprites']['front_default']
    return None

# Обработчик команды /pokemon
def get_pokemon(update: Update, context: CallbackContext):
    pokemon_name = ' '.join(context.args).lower()
    pokemon_number = None

    # Поиск номера покемона по его имени
    url = f'https://pokeapi.co/api/v2/pokemon?limit=1000'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for pokemon in data['results']:
            if pokemon['name'] == pokemon_name:
                pokemon_number = pokemon['url'].split('/')[-2]
                break

    if pokemon_number:
        if pokemon_name in requested_pokemons:
            update.message.reply_text(f'Вы уже получили информацию о {pokemon_name}.')
        else:
            requested_pokemons.add(pokemon_name)
            name = get_name(pokemon_number)
            image_url = get_img(pokemon_number)
            if image_url:
                update.message.reply_text(f'Покемон: {name}\nНомер: {pokemon_number}\nФото: {image_url}')
            else:
                update.message.reply_text('Изображение не найдено.')
    else:
        update.message.reply_text('Покемон не найден. Попробуйте ещё раз.')

def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("pokemon", get_pokemon))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
