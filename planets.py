from kivy.config import Config
Config.set('graphics', 'fullscreen','auto')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from functools import partial
from numpy import round as npround
from time import time

class ImageButton(Image):

    # Function that implements a button based on the Image class.
    # Images for unpressed/pressed state should be en_name_up.JPG/en_name_down.JPG and es_name_up.JPG/es_name_down.JPG

    def __init__(self,  name='', on_release=None, *args, **kwargs):
        super(ImageButton, self).__init__(*args, **kwargs)
        
        self.name = name
        self.nocache = True
        
        self.source = 'button_images/en_' + name + '_up.JPG'
        
        if on_release is not None:
            self.press_action = on_release
        else:
            self.press_action = None
        
    def on_touch_down(self, touch, *args):
    
        # Function called when the user touches the button
        man = App.get_running_app().manager
        print(man.blockTouch)
        if self.collide_point(*touch.pos) and man.blockTouch is not True:
            lang = man.lang + '_'
            self.source = 'button_images/' + lang + self.name + '_down.JPG'
    
    def on_touch_up(self, touch, *args):
    
        # Function called when the user stops touching the button
        man = App.get_running_app().manager
        lang = man.lang + '_'
        self.source = 'button_images/' + lang + self.name + '_up.JPG'
        if self.press_action is not None and self.collide_point(*touch.pos) and man.blockTouch is not True:
            man.blockTouch = True
            self.press_action()
            Clock.schedule_once(man.unblock_touch, .5)
           
    def refresh(self):
        
        # This reloads the button's image. Called when we've changed languages.
        
        lang = App.get_running_app().manager.lang + '_'
        self.source = 'button_images/' + lang + self.name + '_up.JPG'

class AttractorWidget(Image):
    
    def on_touch_down(self, *args):
        
        app= App.get_running_app()
        
        app.manager.screen.last_interact = time()
        app.manager.current = 'scale'
    
    def __init__(self, *args, **kwargs):
        super(AttractorWidget, self).__init__(*args, **kwargs)
        self.size_hint = (1,1)
        self.nocache = True


class AttractorScreen(Screen):
        
    def __init__(self, *args, **kwargs):
        super(AttractorScreen, self).__init__(*args, **kwargs)

        self.add_widget(AttractorWidget(source='background_images/Attractor.JPG'))


class ScaleScreen(Screen):
    
    def select_world(self, world, *args):
        
        # function to set a specfic world 
        
        self.current_world = world
        self.background_image.source = 'background_images/'+world+'.JPG'
        
        if world != 'Moon':
            self.title.text = ''#'On ' + world + ', you would weigh:'
        else:
            self.title.text = ''#'On the Moon, you would weigh:'
    
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
            #self.kg_label.text = str(round(self.kg*factor[self.current_world])) + ' kg'
            self.lb_label.text = str(round(self.kg*factor[self.current_world]*2.20462)) + ' lbs'
        else:
            #self.kg_label.text = str(npround(self.kg*factor[self.current_world], 5)) + ' kg'
            self.lb_label.text = str(npround(self.kg*factor[self.current_world]*2.20462, 5)) + ' lbs'
           
    def toggle_language(self, *args):
        
        # When called, it toggles the language variable in the manager between en/es_name_down.
        # It then refreshes everything to reflect the new language.
        
        app = App.get_running_app()
        
        if app.manager.lang == 'en':
            app.manager.lang = 'es'
        else:
            app.manager.lang = 'en'
            
        for widget in self.button_box.children:
            widget.refresh()
        
        
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
        
        master_layout = BoxLayout(orientation='vertical', size_hint=(1,1))
        
        self.title = Label(text='',
                        font_size=100,
                        size_hint=(1,0.15))
        
        weight_box = BoxLayout(orientation='horizontal',
                                size_hint=(1,0.35))
        
        #self.kg_label = Label(text='0 kg',
        #                        font_size=200,
        #                        size_hint=(0.5,1))
        self.lb_label = Label(text='0 lbs',
                                font_size=200,
                                size_hint=(0.5,1))
        
        #weight_box.add_widget(self.kg_label)
        weight_box.add_widget(self.lb_label)
        
        self.button_box = GridLayout(cols=4, rows=2,
                                size_hint=(1,0.4))
        
        self.mercury = ImageButton(name='Mercury',
                                on_release=partial(self.select_world, 'Mercury'))
        self.venus = ImageButton(name='Venus',
                                on_release=partial(self.select_world, 'Venus'))
        self.moon = ImageButton(name='Moon',
                                on_release=partial(self.select_world, 'Moon'))
        self.mars = ImageButton(name='Mars',
                                on_release=partial(self.select_world, 'Mars'))
        self.ceres = ImageButton(name='Ceres',
                                on_release=partial(self.select_world, 'Ceres'))
        self.bennu = ImageButton(name='Bennu',
                                on_release=partial(self.select_world, 'Bennu'))
        self.titan = ImageButton(name='Titan',
                                on_release=partial(self.select_world, 'Titan'))
        self.pluto = ImageButton(name='Pluto',
                                on_release=partial(self.select_world, 'Pluto'))
                                
        self.button_box.add_widget(self.mercury)
        self.button_box.add_widget(self.venus)
        self.button_box.add_widget(self.moon)
        self.button_box.add_widget(self.mars)
        self.button_box.add_widget(self.ceres)
        self.button_box.add_widget(self.bennu)
        self.button_box.add_widget(self.titan)
        self.button_box.add_widget(self.pluto)
        
        
        lang_box = BoxLayout(orientation='horizontal',
                                size_hint=(1,0.1))
                                
        spacer2 = Label(size_hint=(0.45,1))
        spacer3 = Label(size_hint=(0.45,1))
        self.lang_switch = Button(text='Español',
                                    font_size=30,
                                    size_hint=(0.1, 1),
                                    on_release=self.toggle_language)
        
        lang_box.add_widget(spacer2)
        #lang_box.add_widget(self.lang_switch)
        lang_box.add_widget(spacer3)
        
        master_layout.add_widget(self.title)
        master_layout.add_widget(weight_box)
        master_layout.add_widget(self.button_box)
        master_layout.add_widget(lang_box)
        
        # Background image
        self.background_image = Image(source='background_images/Moon.JPG',
                                        size_hint=(1,1), nocache=True)
        
        background_container = FloatLayout()
        background_container.add_widget(self.background_image)
        background_container.add_widget(master_layout)
        
        self.add_widget(background_container)
        
        Clock.schedule_interval(self.update_weight, 0.25)


class ScreenManagement(ScreenManager):
    
    def unblock_touch(self, *args):
        
        # Function that sets self.blcokTouch = False
        
        self.blockTouch = False
    
    def __init__(self, *args, **kwargs):
        super(ScreenManagement, self).__init__(*args, **kwargs)
        
        self.screen = ScaleScreen(name='scale')
        self.attractor = AttractorScreen(name='attractor')
        
        self.blockTouch = False # We block touches while the world is being switched. Enabled/disabled by each button when pressed/
        
        self.add_widget(self.screen)
        self.add_widget(self.attractor)
        
        self.current = 'attractor'
        
        self.lang = 'en'

class MainApp(App):
    
    def build(self):
        self.manager = ScreenManagement(transition=NoTransition())
        return(self.manager)

# Start the app
MainApp().run()
