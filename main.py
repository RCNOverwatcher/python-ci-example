from gpiozero import LightSensor
import time
import flet as ft
import yagmail

def main(page: ft.Page):
    
    def btnAreaClick(e):
        ldr = LightSensor(27)

        total = 0

        for i in range(1,10):
            total += (ldr.value * 1000000)
            lvLDR.controls.append(ft.Text(str(ldr.value)))
            time.sleep(1)
            
        current = 0.0000026455026
        resistance = 1000000 - (total / 10)
        power = current * current * resistance
        powerPerSqMetre = power / 0.00000012
        
        area = tbArea.value
        finalValue = int(area) * powerPerSqMetre
        finalValuekW = finalValue / 1000
        moneyGenerated = (finalValuekW * (10/(60*60))) * 16
        page.add(ft.Text(f"Money made in 10s: {str(moneyGenerated)} pence."))
        return moneyGenerated
    
    def btnEmailClick(e, moneyGenerated):
            yag = yagmail.SMTP(tbEmail.value, tbPassword.value)
            yag.send(tbRecipient.value, "SolarX Results", f"You will make {str(moneyGenerated)} pence every 10 seconds!.")
            page.add(ft.Text("Email sent!"))
            
    def themeToggle(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        page.update()
        
    page.title = "SolarX"
    page.window_width = 900
    page.window_height = 700
    page.window_resizable = False
    
    page.appbar = ft.AppBar(
        title=ft.Text("SolarX"),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(ft.icons.WB_SUNNY_OUTLINED, on_click=themeToggle),
        ],
    )
    
    img = ft.Image(
        src="assets\cover.png",
        width=900,
        fit=ft.ImageFit.CONTAIN,
    )
    
    images = ft.Row(
        expand=1, 
        wrap=False, 
        scroll="always"
    )
    
    tbArea = ft.TextField(
        label="Area of solar panels (m²): "
    )
    
    btnArea = ft.ElevatedButton(
        text="Calculate", 
        on_click=btnAreaClick
    )
    
    tbEmail = ft.TextField(
        label="Enter your gmail username: "
    )
    
    tbPassword = ft.TextField(
        label="Enter your password: ", 
        password=True, 
        can_reveal_password=True
    )
    
    tbRecipient = ft.TextField(
        label="Enter the recipient's email address: ",
        suffix_text="@gmail.com"
    )
    
    btnEmail = ft.ElevatedButton(
        text="Send Email", 
        on_click=btnEmailClick
    )
    
    lvLDR = ft.ListView( 
        spacing=10, 
        padding=20, 
        auto_scroll=True
    )
    
    page.add(
        img, 
        images,
        ft.Row(controls=[
            ft.Column(controls=[
                tbArea, 
                btnArea
            ]),
            ft.Column(controls=[
                tbEmail,
                tbPassword,
                tbRecipient,
                btnEmail
            ]),
            ft.Column(controls=[
                lvLDR
            ])
        ])
    )
    
    pass

ft.app(target=main)