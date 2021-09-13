import json
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from plyer import notification


Clock.schedule_once(lambda d:notification.notify("notification","notified"), 5)