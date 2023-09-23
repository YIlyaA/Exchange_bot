import schedule
import requests
from bs4 import BeautifulSoup
from config import token, chat_id
from aiogram import Bot, Dispatcher, executor, types

usds = []
bot = Bot(token=token)
dp = Dispatcher(bot)


# Функция для получения курса валюты
def get_currency_rate():
    # Адрес сайта, с которого мы будем получать данные
    url = "https://www.google.com/search?q=%D0%BA%D1%83%D1%80%D1%81+" \
          "%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D0%B0+%D0%BA+%D0%B7%D0%BB%D0%BE%D1%82%D0%BE%D0%BC%D1%83"
    headers = {
        'User-Agent': 'Your User_AGENT'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    result = soup.find("span", {"class": "DFlfde SwHCTb", "data-precision": "2"})
    usd_pln = float(result.text)
    usds.append(usd_pln)

    print(usds)

    if check_changes(usds):
        num = str(usds[-1])

        message = 'Текущий курс доллара: ' + num + ' PLN'
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
        print(requests.get(url).json())  # Эта строка отсылает сообщение


def main():
    schedule.every(5).seconds.do(get_currency_rate)
    # schedule.every().day.at('21:41').do(get_currency_rate)

    while True:
        schedule.run_pending()


def check_changes(list):
    if len(list) == 1:
        return True
    elif len(list) == 3:
        list.pop(0)
    elif list[-1] != list[-2]:
        return True
    else:
        return False


# Основной код программы
if __name__ == "__main__":
    main()
    # executor.start_polling(dp)
