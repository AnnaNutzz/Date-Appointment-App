"""
Application to help me get a date
Colab + Ubuntu fail counter: 49
"""

import os
os.environ['KIVY_VIDEO'] = 'ffpyplayer'


import webbrowser
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from PIL import Image as PILImage
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.video import Video
from urllib.parse import quote


class DateMeApp(MDApp):
    def build(self):
        self.no_count = 0 
        self.selected_idea = None

        self.theme_cls.primary_palette = "Pink"
        self.theme_cls.primary_hue = "200"
        self.theme_cls.theme_style = "Dark"

        screen = MDScreen()

        # Title
        title = MDLabel(
            text="Can we go on a date??", 
            theme_text_color="Custom", 
            pos_hint={"x": 0.3, "center_y": 0.8},
            text_color=(1, 0, 0.5)
        )

        # Animated GIF (make sure the path is relative or correct on your system)
        video = Video(
            source="D:\Coding\Python\Kivy\ddpool.gif",
            size_hint=(0.6, 0.6),
            pos_hint={"center_x": 0.5, "center_y": 0.6},
            state='play',
            options={'eos': 'loop'}
        )

        # Text input for user's name
        self.name_input = MDTextField(
            hint_text="enter a name",
            helper_text="the name you want to give me <3",
            helper_text_mode="persistent",
            icon_right="heart",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            size_hint=(0.5, 0.1)
        )

        # Buttons
        yess = MDRectangleFlatButton(
            text="Yes!", 
            pos_hint={"center_x": 0.3, "center_y": 0.4}, 
            on_release=self.yes_ans
        )
        noo = MDRectangleFlatButton(
            text="No!", 
            pos_hint={"center_x": 0.7, "center_y": 0.4}, 
            on_release=self.no_ans
        )

        # Add widgets to screen
        screen.add_widget(title)
        screen.add_widget(video)
        screen.add_widget(self.name_input)
        screen.add_widget(yess)
        screen.add_widget(noo)

        return screen

    def yes_ans(self, obj):
        name = self.name_input.text or "special one"
        check = f"Okay, I will be your {name}"

        self.dia = MDDialog(
            title="YAY!",
            text=check,
            buttons=[
                MDRectangleFlatButton(text="Date Ideas", on_release=self.show_date_ideas)
            ]
        )
        self.dia.open()

    def no_ans(self, obj):
        self.no_count += 1
        messages = [
            "Oh no! Why did you say no? :(",
            "Come on, give me a chance!",
            "Okay, let's talk about it...",
            "I won't give up!",
            "Okay, fine... I'll stop asking. :(",
            "You've already said no too many times..."
        ]
        msg = messages[min(self.no_count - 1, len(messages) - 1)]

        self.dia = MDDialog(
            title="Response",
            text=msg,
            size_hint=(0.8, None),
            height="200dp",
            buttons=[MDRectangleFlatButton(text="Close", on_release=lambda x: self.dia.dismiss())]
        )
        self.dia.open()

    def show_date_ideas(self, obj):
        self.root.clear_widgets()

        main_layout = MDBoxLayout(
            orientation='vertical',
            padding=10,
            spacing=10,
            pos_hint={"center_x": 0.5, "center_y": 0.38},
            size_hint=(0.8, 0.8)
        )

        scrollview = ScrollView(size_hint=(1, 0.5))
        button_layout = MDBoxLayout(
            orientation='vertical',
            spacing = 10, 
            size_hint_y=None)
        button_layout.bind(minimum_height=button_layout.setter('height'))

        date_ideas = [
            "Coffee at a cafe",
            "Dinner at a fancy restaurant",
            "Picnic in the park",
            "Movie night",
            "Go for a walk",
            "Visit a museum",
            "Watch the sunset"
        ]

        for idea in date_ideas:
            list_item = MDRectangleFlatButton(
                text=idea,
                size_hint=(1, None),
                height=50,
                on_release=lambda btn, idea=idea: self.select_date_idea(idea)
            )
            button_layout.add_widget(list_item)

        scrollview.add_widget(button_layout)
        main_layout.add_widget(scrollview)
        self.root.add_widget(main_layout)

    def select_date_idea(self, idea):
        self.selected_idea = idea
        self.dia = MDDialog(
            title="Selected Date Idea",
            text=f"{idea}, bet it's going to be a good one!",
            buttons=[
                MDRectangleFlatButton(text="When?", on_release=self.show_date_picker),
                MDRectangleFlatButton(text="Changed your mind?", on_release=lambda x: self.dia.dismiss())
            ]
        )
        self.dia.open()

    def on_save(self, instance, value, date_range):
        date = value.strftime("%A, %B %d, %Y")
        self.send_whatsapp_message(date, self.selected_idea)

    def on_cancel(self, instance, value):
        print("Canceled")

    def show_date_picker(self, *args):
        if not self.selected_idea:
            self.dia = MDDialog(
                title="Error",
                text="Please select a date idea before choosing the date.",
                size_hint=(0.8, None),
                height="200dp",
                buttons=[MDRectangleFlatButton(text="Close", on_release=lambda x: self.dia.dismiss())]
            )
            self.dia.open()
        else:
            date_dialog = MDDatePicker()
            date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
            date_dialog.open()

    def send_whatsapp_message(self, date, idea):
        name = self.name_input.text or "beautiful"
        message = f"Let's go on a date on {date}, {name}! \nPlan is: {idea}"
        url = f"https://wa.me/9679550477?text={quote(message)}"
        webbrowser.open(url)


if __name__ == "__main__":
    DateMeApp().run()
