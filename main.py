import flet as ft
import json
import aiofiles
import os
import shutil
import random
import textwrap
from welcomePage import WelcomePage
import re

async def main(page: ft.Page):
    page.title = "Avito"
    page.theme_mode = "dark"
    page.window_width = 1024
    page.window_height = 1212
    page.window_reziable = False

    global local_username
    local_username = ""

    global logged_in
    logged_in = False

    async def route_change(route):
        page.views.clear()

        if page.route == "/":
            page.views.append(WelcomePage(page))

        elif page.route == "/logOrSignIn":
            username = ft.TextField(hint_text="Имя пользователя")
            password = ft.TextField(hint_text="Пароль", password=True)

            async def check_user(event):
                async with aiofiles.open("users_data.json", "r") as file:
                    data = json.loads(await file.read())
                if username.value in data:
                    temp_username_data = data[username.value]
                    if temp_username_data["password"] == password.value:
                        global local_username
                        local_username = username.value
                        global logged_in
                        logged_in = True
                        await page.go_async('/home')
                    else:
                        page.views.clear()
                        page.views.append(
                            ft.View(
                                route="/logOrSignIn",
                                controls=[
                                    ft.Text("Войдите в аккаунт", weight=ft.FontWeight.BOLD),
                                    username,
                                    password,
                                    ft.ElevatedButton("Войти", on_click=check_user),
                                    ft.Text("Неверное имя пользователя или пароль", weight=ft.FontWeight.BOLD,
                                            color=ft.colors.RED),
                                    ft.Text("Или", weight=ft.FontWeight.BOLD),
                                    ft.ElevatedButton("Создайте новый", on_click=lambda _: page.go("/signUp"))
                                ],
                                vertical_alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            )
                        )
                        await page.update_async()
                else:
                    page.views.clear()
                    page.views.append(
                        ft.View(
                            route="/logOrSignIn",
                            controls=[
                                ft.Text("Войдите в аккаунт", weight=ft.FontWeight.BOLD),
                                username,
                                password,
                                ft.ElevatedButton("Войти", on_click=check_user),
                                ft.Text("Неверное имя пользователя или пароль", weight=ft.FontWeight.BOLD,
                                        color=ft.colors.RED),
                                ft.Text("Или", weight=ft.FontWeight.BOLD),
                                ft.ElevatedButton("Создайте новый", on_click=lambda _: page.go("/signUp"))
                            ],
                            vertical_alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        )
                    )
                    await page.update_async()

            page.views.append(
                ft.View(
                    "/logOrSignIn",
                    [
                        ft.Text("Войдите в аккаунт", weight=ft.FontWeight.BOLD),
                        username,
                        password,
                        ft.ElevatedButton("Войти", on_click=check_user),
                        ft.Text("Или", weight=ft.FontWeight.BOLD),
                        ft.ElevatedButton("Создайте новый", on_click=lambda _: page.go("/signUp"))
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

        elif page.route == "/signUp":

            username = ft.TextField(hint_text="Имя пользователя")
            email_inpt = ft.TextField()

            def is_valid_email(email_inpt):

                email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

                if re.match(email_regex, email_inpt.value):
                    return True
                else:
                    return False
            password = ft.TextField(hint_text="Пароль", password=True)
            password_confirm = ft.TextField(hint_text="Подтвердите пароль", password=True)

            async def check_and_create(event):

                async with aiofiles.open("users_data.json", "r") as file:
                    data = json.loads(await file.read())

                if password.value != password_confirm.value:
                    page.views.clear()
                    page.views.append(
                        ft.View(
                            route='/signUp',
                            controls=[
                                ft.Text("Создайте аккаунт", weight=ft.FontWeight.BOLD),
                                username,
                                password,
                                password_confirm,
                                ft.Text("Пароли не совпадают", weight=ft.FontWeight.BOLD, color=ft.colors.RED),
                                ft.ElevatedButton("Создать аккаунт", on_click=check_and_create),
                            ]
                        )
                    )
                    await page.update_async()

                elif username.value in data:
                    page.views.clear()
                    page.views.append(
                        ft.View(
                            route='/signIn',
                            controls=[
                                ft.Text("Создайте аккаунт", weight=ft.FontWeight.BOLD),
                                username,
                                password,
                                password_confirm,
                                ft.Text("Имя пользователя занято", weight=ft.FontWeight.BOLD, color=ft.colors.RED),
                                ft.ElevatedButton("Создать аккаунт", on_click=check_and_create),
                            ]
                        )
                    )
                    await page.update_async()



                else:
                    with open(".venv/users_data.json", "r") as file:
                        data = json.load(file)

                    data[username.value] = {}
                    new_user = data[username.value]
                    new_user["username"] = username.value
                    new_user["password"] = password.value
                    new_user["sales"] = 0
                    new_user["purchases"] = 0

                    data[username.value] = new_user

                    global local_username
                    local_username = new_user["username"]

                    with open(".venv/users_data.json", "w") as file:
                        json.dump(data, file)

                    src_dir = f'assets/{username.value}'

                    # Destination directory
                    dst_dir = 'assets/defaults'

                    os.makedirs(src_dir, exist_ok=True)

                    shutil.copyfile(dst_dir + '/avatar.jpg', src_dir + '/avatar.jpg')

                    src_dir = f'assets/{username.value}/ads'
                    os.makedirs(src_dir, exist_ok=True)

                    src_dir = f'assets/{username.value}/savedAds'
                    os.makedirs(src_dir, exist_ok=True)

                    global logged_in
                    logged_in = True

                    await page.go_async('/home')

            async def go_back(event):
                await page.go_async('/logOrSignIn')

            page.views.clear()
            page.views.append(
                ft.View(
                    route='/signIn',
                    controls=[
                        ft.Text("Создайте аккаунт", weight=ft.FontWeight.BOLD),
                        username,
                        password,
                        password_confirm,
                        ft.ElevatedButton("Создать аккаунт", on_click=check_and_create),
                        ft.ElevatedButton("Назад к входу", on_click=go_back)
                    ]
                )
            )

        async def changetab(e):
            if e.control.data == 'home':
                await page.go_async('/home')
            elif e.control.data == 'saved':
                await page.go_async('/saved')
            elif e.control.data == 'account':
                await page.go_async('/account')

        nav = ft.Container(
            bgcolor=ft.colors.WHITE,
            width=page.window_width - 20,
            border_radius=30,
            content=ft.Row(controls=[
                ft.IconButton(icon='home',
                              icon_size=40,
                              data='home',
                              on_click=changetab),
                ft.IconButton(icon='bookmark',
                              icon_size=40,
                              data='saved',
                              on_click=changetab),
                ft.IconButton(icon='person',
                              icon_size=40,
                              data='account',
                              on_click=changetab)],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )

        async def go_to_publish_ad(e):
            await page.go_async("/publishAd")

        publish_ad_button = ft.ElevatedButton("Опубликовать объявление", bgcolor=ft.colors.LIGHT_BLUE, on_click=go_to_publish_ad)

        if page.route == "/home":

            async def more_about_ad(event):
                print(event.data)
                await page.go_async("/aboutAd:" + event.data)

            ads = ft.Column(
                spacing=10,
                height=page.height + 150,
                width=page.width,
                scroll=ft.ScrollMode.ALWAYS,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )

            with open("ads.json", "r") as file:
                data = json.load(file)

            row = None  # Variable to store current row
            for index, item in enumerate(data["ads"]):
                # Create a new row every 2 items
                if index % 2 == 0:
                    if row is not None:
                        ads.controls.append(row)  # Add previous row to Column
                    row = ft.Row(spacing=10)  # Create new row

                # Create Card for the current item
                card = ft.Card(
                    content=ft.Container(
                        content=ft.Column([
                            ft.Image(
                                src=item.get("image"),
                                width=350,
                                height=350,
                                fit=ft.ImageFit.COVER,
                                border_radius=10
                            ),
                            ft.ListTile(
                                title=ft.Text(item.get("name")),
                                subtitle=ft.Text(textwrap.shorten(item.get("description"), width=50, placeholder="...")),
                            ),
                            ft.Text(f"Цена: {item.get('cost')}", style=ft.TextThemeStyle.BODY_MEDIUM),
                            ft.ElevatedButton(text="Подробнее", on_click=more_about_ad, data=item.get("id")),
                            ft.TextButton("Связаться",
                                          url=item.get("chat_link"))
                        ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ),
                    color=ft.colors.BROWN_100,
                    width=420,
                    height=650
                )

                row.controls.append(card)

            ads.controls.append(row)

            page.views.clear()
            page.views.append(
                ft.View(
                    route='/home',
                    controls=[
                        ft.Text("Home page"),
                        nav,

                        publish_ad_button,
                        ft.Text(""),
                        ads
                    ],
                    vertical_alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

        elif page.route == "/saved":
            page.views.clear()
            page.views.append(
                ft.View(
                    route='/saved',
                    controls=[
                        ft.Text("Saved"),
                        nav,
                        publish_ad_button
                    ],
                    vertical_alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )


        elif page.route == "/account":
            page.views.clear()

            if(logged_in):
                with open('users_data.json', 'r') as file:
                    data = json.load(file)

                local_data = data[local_username]
                print(local_username)

                async def log_out(event):
                    global logged_in
                    logged_in = False
                    await page.go_async("/home")

                page.views.append(
                    ft.View(
                        route='/account',
                        controls=[
                            ft.Text('Account'),
                            nav,
                            publish_ad_button,
                            ft.Container(
                                width=200,
                                height=200,
                                border_radius=90,
                                content=ft.Image(src=f"/{local_username}/avatar.jpg")
                            ),
                            ft.Text("Количество продаж: " + str(local_data['sales'])),
                            ft.Text("Количество покупок: " + str(local_data["purchases"])),

                            ft.Text(" "),
                            ft.ElevatedButton("Выйти", on_click=log_out)
                        ],
                        vertical_alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )

            else:

                async def go_to_log_in_page(event):
                    await page.go_async("/")

                page.views.append(
                    ft.View(
                        route='/account',
                        controls=[
                            ft.Text('Account'),
                            nav,
                            ft.Text(" "),
                            ft.Text(" "),
                            ft.Text('Вы не вошли в аккаунт!'),
                            ft.ElevatedButton("Войти или создать сейчас", on_click=go_to_log_in_page)
                        ],
                        vertical_alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )

        elif page.route == "/publishAd":
            page.views.clear()
            if (logged_in):
                with open('users_data.json', 'r') as file:
                    data = json.load(file)

                local_data = data[local_username]

                with open("ads.json", "r") as file:
                    data = json.load(file)



                def check_id():
                    gen_id = str(random.randint(10000000, 99999999))
                    for i in data.get("ads"):
                        if(i.get("id") == gen_id):
                            check_id()
                    return gen_id

                async def pick_files_result(e: ft.FilePickerResultEvent):
                    ad_id = check_id()
                    print(ad_id)
                    ad_dir = f'ads/{ad_id}/'
                    os.makedirs(ad_dir, exist_ok=True)

                    for idx, file in enumerate(e.files):
                        destination = os.path.join(ad_dir, f'image{idx + 1}.png')
                        shutil.copy(file.path, destination)
                        selected_files.controls.append(ft.Image(src=destination, width=350, height=350, border_radius=10))
                    await page.update_async()

                selected_files = ft.Column(controls=[])
                pick_files_dialog = ft.FilePicker(on_result=pick_files_result, )

                page.overlay.append(pick_files_dialog)

                pick_files_button = ft.ElevatedButton(
                    "Выбрать файлы",
                    icon=ft.icons.UPLOAD_FILE,
                    width=200,
                    height=50,
                    on_click=lambda _: pick_files_dialog.pick_files(
                        allow_multiple=False
                    ),
                )



                ad_name = ft.TextField(label="Название")
                ad_description = ft.TextField(label="Описание")
                ad_cost = ft.TextField(label="Цена")

                async def add_category(e):
                    button_text = e.control.text
                    button_data = e.control.data

                    if button_text in categories.value:
                        categories.value = categories.value.replace(f' {button_text},', '')
                        e.control.bgcolor = ft.colors.GREY
                    else:
                        categories.value += f' {button_text},'
                        e.control.bgcolor = ft.colors.GREEN

                    await page.update_async()

                categories = ft.Text("Категории: ")

                categories_buttons = ft.Row(controls=[
                    ft.ElevatedButton("Мужчинам", color=ft.colors.WHITE, bgcolor=ft.colors.GREY, data="men", on_click=add_category),
                    ft.ElevatedButton("Женщинам", color=ft.colors.WHITE, data="women", bgcolor=ft.colors.GREY, on_click=add_category),
                    ft.ElevatedButton("Детям", color=ft.colors.WHITE, bgcolor=ft.colors.GREY, data="children", on_click=add_category),
                ])

                async def publish_ad(e):
                    ad_id = check_id()
                    print(ad_id)
                    ad_dir = f'ads/{ad_id}/'
                    os.makedirs(ad_dir, exist_ok=True)

                    image_src = selected_files.controls[0].src if selected_files.controls else None

                    ad_data = {
                        "id": ad_id,
                        "image": image_src,
                        "name": ad_name.value,
                        "description": ad_description.value,
                        "cost": ad_cost.value,
                        "author": local_username,
                        "chat_link": f"https://web.telegram.org/k/#@{local_username}"
                    }

                    with open("ads.json", "r") as file:
                        data = json.load(file)

                    data["ads"].append(ad_data)

                    with open("assets/ads.json", "w") as file:
                        json.dump(data, file)

                    await page.go_async('/home')

                page.views.append(
                    ft.View(
                        route='/publishAd',
                        controls=[
                            ft.Text('Опубликуйте объявление'),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        pick_files_button,
                                        selected_files,
                                        ad_name,
                                        ad_description,
                                        ad_cost,
                                        categories,
                                        categories_buttons,
                                        ft.ElevatedButton("Опубликовать", on_click=publish_ad)
                                    ],
                                    scroll=ft.ScrollMode.AUTO
                                ),
                                height=page.height * 0.8,  # Adjust height for scrolling area
                                width=page.width * 0.9,
                                border_radius=10,
                                padding=20,
                            )
                        ],
                        vertical_alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        scroll=ft.ScrollMode.AUTO  # Add scroll functionality to the entire view
                    )
                )
            else:
                async def go_to_log_in_page(event):
                    await page.go_async("/")

                page.views.append(
                    ft.View(
                        route='/publishAd',
                        controls=[
                            ft.Text('Публикация объявления'),
                            nav,
                            ft.Text(" "),
                            ft.Text(" "),
                            ft.Text('Вы не вошли в аккаунт!'),
                            ft.ElevatedButton("Войти или создать сейчас", on_click=go_to_log_in_page)
                        ],
                        vertical_alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )

        elif str(page.route).startswith(("/aboutAd:")):

            def remove_prefix(input_string, prefix):

                if input_string.startswith(prefix):
                    return input_string[len(prefix):]
                else:
                    return input_string

            id = remove_prefix(page.route, "/aboutAd:")

            ad = ft.Column(

            )

            with open("ads.json", "r") as file:
                data = json.load(file)

            for i in data["ads"]:
                try:
                    if(i.get("id") == id):
                        ad.controls.append(ft.Text(i.get("name")))
                except:
                    ad.controls.append(ft.Text("Товар не найден :("))



            page.views.clear()
            page.views.append(
                ft.View(
                    route='/aboutAd:',
                    controls=[
                        ft.Text("Подробнее"),
                        nav,
                        publish_ad_button,
                        ad
                    ],
                    vertical_alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

        await page.update_async()

    async def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        await page.go_async(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    await page.go_async('/')

ft.app(target=main, assets_dir='assets')
