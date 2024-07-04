from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Функция запроса для поиска
def search_wikipedia(browser, query):
    search_box = browser.find_element(By.ID, "searchInput")
    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # Ждем загрузки результатов

def list_paragraphs(browser):
    paragraphs = browser.find_elements(By.TAG_NAME, "p")
    for paragraph in paragraphs:
        if paragraph.text.strip():
            print(paragraph.text)
            user_input = input("Нажмите Enter для продолжения или 'назад' для возврата: ")
            if user_input.lower() == 'назад':
                break

def list_internal_links(browser):
    links = browser.find_elements(By.XPATH, "//div[@id='bodyContent']//a[@href]")
    internal_links = [link for link in links if link.get_attribute('href').startswith('https://ru.wikipedia.org/wiki/')]
    for i, link in enumerate(internal_links):
        print(f"{i + 1}: {link.get_attribute('href')}")
    return internal_links

def main():
    browser = webdriver.Chrome()
    browser.get("https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")
    # Проверка по заголовку нужный ли сайт открылся
    assert "Википедия" in browser.title

    while True:
        query = input("Введите запрос для поиска на Википедии (или 'выход' для завершения): ")
        if query.lower() == 'выход':
            break

        search_wikipedia(browser, query)

        while True:
            action = input("Выберите действие: 1 - листать параграфы, 2 - перейти на связанную страницу, 3 - выйти: ")
            if action == "1":
                list_paragraphs(browser)
            elif action == "2":
                internal_links = list_internal_links(browser)
                while True:
                    link_choice = input("Введите номер ссылки для перехода или 'назад' для возврата: ")
                    if link_choice.lower() == 'назад':
                        continue
                    try:
                        link_index = int(link_choice) - 1
                        if 0 <= link_index < len(internal_links):
                            browser.get(internal_links[link_index].get_attribute('href'))
                            time.sleep(2)  # Ждем загрузки страницы
                        else:
                            print("Неверный номер ссылки. Попробуйте снова.")
                    except ValueError:
                        print("Неверный ввод. Пожалуйста, введите номер ссылки.")
            elif action == "3":
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

        # Спрашиваем пользователя, хочет ли он выполнить новый запрос
        new_search = input("Хотите выполнить новый запрос? (да/нет): ")
        if new_search.lower() != "да":
            break

    browser.quit()

if __name__ == "__main__":
    main()


