from kivymd.toast.kivytoast import toast
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.garden.mapview import MapView
import json
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.interactive import InteractiveLauncher
from kivy.uix.popup import Popup
from kivymd.theming import ThemeManager, ThemableBehavior
from kivy.properties import ObjectProperty, StringProperty, \
    BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import MDList, OneLineListItem, OneLineIconListItem,\
    TwoLineIconListItem, IconLeftWidget, ThreeLineListItem, IRightBodyTouch
from kivy.clock import Clock
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.card import MDCardPost
from kivymd.uix.backdrop import MDBackdrop
from kivymd.uix.label import MDLabel
from plyer import notification
from kivymd.uix.dialog import BaseDialog
from kivymd.uix.selectioncontrol import MDCheckbox

__version__ = "1.0.0"


class BackLayerItem(ThemableBehavior, BoxLayout):
    icon = StringProperty("android")
    text = StringProperty()
    # selected_item = BooleanProperty(False)

    # def on_touch_down(self, touch):
    #     if self.collide_point(touch.x, touch.y):
    #         for item in self.parent.children:
    #             if item.selected_item:
    #                 item.selected_item = False
    #         self.selected_item = True
    #     return super().on_touch_down(touch)


class MyCheckbox(IRightBodyTouch, MDCheckbox):
    pass


class DialogItem(BaseDialog):
    pass


class DialogDev(BaseDialog):
    pass


class Squire(ScreenManager):
    # darkswitch=ObjectProperty()
    mdlist = ObjectProperty()
    search = ObjectProperty()
    re = 0
    icons = {'hostels': 'home-circle',
             "lectures": 'teach',
             'religion': 'church',
             'faculty': 'office-building',
             'restaurants': 'food',
             'convocation': 'account-multiple',
             'fire': 'fire-truck',
             'gate': 'gate',
             'sports': 'soccer',
             'ict': 'desktop-tower-monitor',
             'library': 'library',
             'hospital': 'hospital-building',
             'post office': 'email',
             'radio': 'radio-fm',
             'toilets': 'toilet',
             'markets': 'shopping',
             'e-learning': 'laptop',
             'utility': 'bus',
             'senate': 'globe-model'
             }

    def alarm(self):
        Clock.schedule_once(lambda d: notification.notify("notification",
                                                          "notified"), 15)

    def free(self):
        if self.re % 2 == 1:
            SquireApp().theme_cls.primary_palette = "Teal"
            SquireApp().theme_cls.theme_style = "Light"
            self.darkswitch.active = False if self.darkswitch.active else True
        else:
            SquireApp().theme_cls.primary_palette = "BlueGray"
            SquireApp().theme_cls.theme_style = "Dark"
            self.darkswitch.active = False if self.darkswitch.active else True
        self.re += 1
        print(self.re)

    def locationSearch(self):
        # this is the main function for the searches. It is called anytime the
        # search is typed in.
        with open("locations.bdsm", "r") as f:
            der = json.load(f)
            derarr = sorted(zip(der.keys(), der.values()))
            # arranges the data in der alphabetically.
            der = {derarr[i][0]: derarr[i][1] for i in range(0, len(derarr))}
            if self.mdlist.children != 1:
                self.mdlist.clear_widgets()
            #childs=[x.text for x in self.mdlist.children]
            word = self.search.text.split(" ")

            for x in der:
                # wid is a template for all the list items that come out when searching
                wid = TwoLineIconListItem(
                    text=x,
                    secondary_text=der[x]["shortdesc"]
                )

                if len(word) > 1:
                    # this checks whether there is more than one word in the search bar
                    # so that if the user types space and doesn't know the exact
                    # name of the place, they can type something close.
                    if (word[0].lower() in x.lower() and
                        word[1].lower() in x.lower()) or \
                        (word[0] in der[x]['shortdesc'] or
                         word[1] in der[x]['shortdesc']) and \
                            "shortdesc" in der[x]:
                        # this checks if the entry has a short description
                        if self.mdlist.children == []:
                            self.mdlist.add_widget(wid)
                            wid.add_widget(IconLeftWidget(
                                icon=self.icons[der[x]["class"]]))
                        else:
                            if x in [x.text for x in self.mdlist.children]:
                                pass
                            else:
                                self.mdlist.add_widget(wid)
                                wid.add_widget(IconLeftWidget(
                                    icon=self.icons[der[x]["class"]]))

                elif len(word) == 1 and word != ['']:
                    # runs if there's only one word in the search bar
                    if word[0].lower() in x.lower() or (word[0] in
                                                        der[x]['shortdesc']) and "shortdesc" in der[x]:
                        if self.mdlist.children == []:
                            self.mdlist.add_widget(wid)
                            wid.add_widget(IconLeftWidget(
                                icon=self.icons[der[x]["class"]]))

                            def spawn(): self.spawn(wid.text)
                            wid.on_press = spawn
                        else:
                            if x in [x.text for x in self.mdlist.children]:
                                pass
                            else:
                                self.mdlist.add_widget(wid)
                                wid.add_widget(IconLeftWidget(
                                    icon=self.icons[der[x]["class"]]))

    def spawn(self, chief):
        with open("locations.bdsm", "r") as f:
            der = json.load(f)
            spawn = Screen(name=chief + 'screen')
            self.add_widget(spawn)
            layout = BoxLayout(orientation='vertical')
            tools = MDToolbar(
                title=chief,
            )  # TODO: change this to a user animation card after you get images
            spawn.add_widget(layout)
            labe = MDLabel(text=der[chief]['longdesc'])
            layout.add_widget(tools)
            layout.add_widget(labe)
        self.current = chief + 'screen'


class SquireApp(MDApp):
    kv_file = 'projectquiet.kv'

    def build(self):
        # self.theme_cls.theme_style="Dark"
        self.theme_cls.primary_palette = "Teal"
        return Squire()


SquireApp().run()
