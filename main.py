import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2

        self.add_widget(Label(text='Username:'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)

        self.add_widget(Label(text='Password:'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)

        self.login_button = Button(text='Login')
        self.login_button.bind(on_press=self.login)
        self.add_widget(self.login_button)

        self.register_button = Button(text='Register',font_size=40)
        self.register_button.bind(on_press=self.register)
        self.add_widget(self.register_button)

    def login(self, instance):
        # Implement login logic here
        pass

    def register(self, instance):
        # Implement registration logic here
        pass

class MyApp(App):

    def build(self):
        return LoginScreen()

if __name__ == '__main__':
    MyApp().run()
