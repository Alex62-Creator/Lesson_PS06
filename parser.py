# Импортируем модуль со временем
import time
# Импортируем модуль csv
import csv
# Импортируем Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By

# Функция поиска необходимых данных со страницы и добавления их в список
def pars(url):
    # Открываем веб-страницу
    browser.get(url)
    print(f"=====Страница {url}")
    # Задаём 3 секунды ожидания, чтобы веб-страница успела прогрузиться
    time.sleep(10)

    # Находим все карточки светильников с помощью названия класса
    # Названия класса берём с кода сайта
    svets = browser.find_elements(By.CSS_SELECTOR, 'div.lsooF')
    print(f"===== {svets}")

    # Перебираем коллекцию светильников
    # Используем конструкцию try-except, чтобы "ловить" ошибки, как только они появляются
    for svet in svets:
        try:
            # Находим элементы внутри карточки по значению
            # Находим название
            name = svet.find_element(By.CSS_SELECTOR, 'span').text
            # Находим цену
            price = svet.find_element(By.CSS_SELECTOR, 'div.q5Uds').find_element(By.CSS_SELECTOR, 'span').text
            # Находим ссылку с помощью атрибута 'href'
            link = svet.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            print(f"=====Name {name}\nPrice {price}\nLink {link}")
        # Вставляем блок except на случай ошибки - в случае ошибки программа попытается продолжать
        except Exception as e:
            print(f"Произошла ошибка при парсинге: {e}")
            continue

        # Вносим найденную информацию в список
        data.append([name, price, link])
        print(f"=====Data {data}")

# Инициализируем браузер
browser = webdriver.Chrome()
# Указываем первую страницу, которую будем просматривать
url = "https://divan.ru/category/svet"

# Создаём список, в который потом всё будет сохраняться
data = []

# Парсим первую страницу
pars(url)

# Модифицируем шаблон страниц, которые будем просматривать
url += "/page-"

# Цикл для парсинга остальных страниц
for i in ['2', '3', '4', '5']:
    # Формируем адрес очередной страницы, которую будем просматривать
    url += i
    # Парсим очередную страницу
    pars(url)

# Закрываем подключение браузера
browser.quit()

# Прописываем открытие нового файла, задаём ему название и форматирование
# 'w' означает режим доступа, мы разрешаем вносить данные в таблицу
with open("svet.csv", 'w', newline='', encoding='utf-8') as file:
    # Используем модуль csv и настраиваем запись данных в виде таблицы
    # Создаём объект
    writer = csv.writer(file)
    # Создаём первый ряд
    writer.writerow(['Название светильника', 'Цена', 'Ссылка'])
    # Прописываем использование списка как источника для рядов таблицы
    writer.writerows(data)
