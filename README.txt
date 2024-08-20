#Гуид

#Нажми Control + Shift + - (минус) для того, чтобы свернуть все функции

#Привествесвенная страница : 31-32 (основна в welcomePage.py)
#Страница входа : 35-102
#Страница регистрации : 107 - 182
#Домащнаяя страница : 186-193

#Пример добавления страницы

#Имя страницы, пример: /nameOfThePage

#elif page.route == "/ИМЯ СТРАНИЦЫ":            <-- ИМЯ СТРАНИЦЫ !!!!
#page.views.clear()
#page.views.append(
    #ft.View(
        #route='/ИМЯ СТРАНИЦЫ',                 <-- ИМЯ СТРАНИЦЫ !!!
        #controls=[ft.Text("Home page")]
    #)
#)

#Если будешь писать функции для изменения чего либо на странице, то добавляй await page.update_async()

#НЕ ЗАБЫВАЙ, ЧТО ПОЧТИ ВЕЗДЕ НУЖНО ИСПОЛЬЗОВАТЬ ASYNC !!!

#Полезные документации:

#How to add keys to dictionary
#https://stackoverflow.com/questions/1024847/how-can-i-add-new-keys-to-a-dictionary

#Flet documentation
#https://flet.dev/docs/

#aiofiles documentation
#https://github.com/Tinche/aiofiles