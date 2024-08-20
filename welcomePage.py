import flet as ft

def WelcomePage(page: ft.Page):
    return(
        ft.View(
            "/",
            [
                ft.Text("Здравствуйте!", weight=ft.FontWeight.BOLD),
                ft.ElevatedButton("Войти", on_click=lambda _: page.go("/logOrSignIn")),
            ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )