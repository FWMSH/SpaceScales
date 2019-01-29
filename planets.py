from kivy.config import Config
Config.set('graphics', 'fullscreen','auto')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from functools import partial
from numpy import round as npround
from time import time

class AttractorWidget(Label):
    
    def on_touch_down(self, *args):
        
        app= App.get_running_app()
        
        app.manager.screen.last_interact = time()
        app.manager.current = 'scale'
    
    def __init__(self, *args, **kwargs):
        super(AttractorWidget, self).__init__(*args, **kwargs)


class AttractorScreen(Screen):
        
    def __init__(self, *args, **kwargs):
        super(AttractorScreen, self).__init__(*args, **kwargs)

        self.add_widget(AttractorWidget(text='How Much Would You\nWeigh on the Moon?\n[size=100]Step on the scale to find out!',
                                    markup=True,
                                    halign='center',
                                    font_size=150))


class ScaleScreen(Screen):
    
    def select_world(self, world, *args):
        
        # function to set a specfic world 
        
        self.current_world = world
        
        if world != 'Moon':
            self.title.text = 'On ' + world + ', you would weigh:'
        else:
            self.title.text = 'On the Moon, you would weigh:'
    
    def convert_weight(self, *args):
        
        # Function to take an input weight from the scale and convert
        # it for the selected planet
        
        factor = {'Mercury': 0.378,
                        'Venus': 0.91,
                        'Earth': 1,
                        'Moon': 0.1656,
                        'Mars': 0.379,
                        'Ryugu': 0.0000125,
                        'Bennu': 0.00000102,
                        'Ceres': 0.0284,
                        'Jupiter': 2.53,
                        'Saturn': 1.07,
                        'Titan': 0.1381,
                        'Uranus': 0.91,
                        'Neptune': 1.14,
                        'Pluto': 0.0635}
            
        if self.current_world != 'Bennu':    
            self.kg_label.text = str(round(self.kg*factor[self.current_world])) + ' kg'
            self.lb_label.text = str(round(self.kg*factor[self.current_world]*2.20462)) + ' lbs'
        else:
            self.kg_label.text = str(npround(self.kg*factor[self.current_world], 5)) + ' kg'
            self.lb_label.text = str(npround(self.kg*factor[self.current_world]*2.20462, 5)) + ' lbs'
           
            
        
        
    def update_weight(self, *args):
        
        # Function to open the weight.txt file, read the weight, and
        # trigger the widgets to update
        
        app = App.get_running_app()
        
        try:
            with open('/home/pi/planet_scale/weight.txt', 'r') as f:
                self.kg = int(float(f.read()))
            if (round(self.kg) > 5):
                self.last_interact = time()
                if (app.manager.current != 'scale'):
                    app.manager.current = 'scale'
            elif time() - self.last_interact > 60:
                self.select_world('Moon')
                app.manager.current = 'attractor'
            
            self.convert_weight()
            
        except:
            pass
    
    def __init__(self, *args, **kwargs):
        super(ScaleScreen, self).__init__(*args, **kwargs)
        
        self.current_world = 'Moon'
        self.last_interact = time()
        
        master_layout = BoxLayout(orientation='vertical')
        
        self.title = Label(text='On the Moon, you would weigh:',
                        font_size=100,
                        size_hint=(1,0.25))
        
        weight_box = BoxLayout(orientation='horizontal',
                                size_hint=(1,0.25))
        
        self.kg_label = Label(text='0 kg',
                                font_size=200,
                                size_hint=(0.5,1))
        self.lb_label = Label(text='0 lbs',
                                font_size=200,
                                size_hint=(0.5,1))
        
        #weight_box.add_widget(self.kg_label)
        weight_box.add_widget(self.lb_label)
        
        button_box = GridLayout(cols=4, rows=2,
                                size_hint=(1,0.4))
        
        self.mercury = Button(text='Mercury',
                                font_size=50,
                                on_release=partial(self.select_world, 'Mercury'))
        self.venus = Button(text='Venus',
                                font_size=50,
                                on_release=partial(self.select_world, 'Venus'))
        self.moon = Button(text='Moon',
                                font_size=50,
                                on_release=partial(self.select_world, 'Moon'))
        self.mars = Button(text='Mars',
                                font_size=50,
                                on_release=partial(self.select_world, 'Mars'))
        self.ceres = Button(text='Ceres',
                                font_size=50,
                                on_release=partial(self.select_world, 'Ceres'))
        self.bennu = Button(text='Bennu',
                                font_size=50,
                                on_release=partial(self.select_world, 'Bennu'))
        self.titan = Button(text='Titan',
                                font_size=50,
                                on_release=partial(self.select_world, 'Titan'))
        self.pluto = Button(text='Pluto',
                                font_size=50,
                                on_release=partial(self.select_world, 'Pluto'))
                                
        button_box.add_widget(self.mercury)
        button_box.add_widget(self.venus)
        button_box.add_widget(self.moon)
        button_box.add_widget(self.mars)
        button_box.add_widget(self.ceres)
        button_box.add_widget(self.bennu)
        button_box.add_widget(self.titan)
        button_box.add_widget(self.pluto)
        
        
        lang_box = BoxLayout(orientation='horizontal',
                                size_hint=(1,0.1))
                                
        spacer2 = Label(size_hint=(0.45,1))
        spacer3 = Label(size_hint=(0.45,1))
        self.lang_switch = Button(text='Español',
                                    font_size=30,
                                    size_hint=(0.1, 1))
        
        lang_box.add_widget(spacer2)
        lang_box.add_widget(self.lang_switch)
        lang_box.add_widget(spacer3)
        
        master_layout.add_widget(self.title)
        master_layout.add_widget(weight_box)
        master_layout.add_widget(button_box)
        master_layout.add_widget(lang_box)
        
        self.add_widget(master_layout)
        
        Clock.schedule_interval(self.update_weight, 0.25)


class ScreenManagement(ScreenManager):
    
    def __init__(self, *args, **kwargs):
        super(ScreenManagement, self).__init__(*args, **kwargs)
        
        self.screen = ScaleScreen(name='scale')
        self.attractor = AttractorScreen(name='attractor')
        
        self.add_widget(self.screen)
        self.add_widget(self.attractor)
        
        self.current = 'attractor'

class MainApp(App):
    
    def build(self):
        self.manager = ScreenManagement(transition=FadeTransition(duration=0.2))
        return(self.manager)

# Start the app
MainApp().run()
