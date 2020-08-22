from kivymd.app import MDApp
from kivymd.uix.label import Label
from kivymd.uix.button import MDRectangleFlatButton, MDFloatingActionButtonSpeedDial
from kivy.uix.screenmanager import Screen, ScreenManager
#from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder






class Main_info(Screen):
    #name = StringProperty("MainInfo")    
    pass





class sub_new_activity(Screen):

    def return_to_main(self):
        print("back")
        print("2current Screen: " + str(self.parent.current_screen) + " | has the next screen? " +str(self.parent.has_screen("subNewActivity")))
        self.parent.switch_to(screens[0])
        print("3current Screen: " + str(self.parent.current_screen) + " | has the next screen? " +str(self.parent.has_screen("subNewActivity")))
        


class Main(MDApp):

    data = {'timeline-plus-outline' : 'New activity',}


    def Add_callback(self,instance):
        print("\"Add to\" Screen")
        global screens
        
        self.sm.switch_to(screens[1])

    
    def build(self):
        global screens
        kv = Builder.load_file("tmlayout.kv")
        self.sm = ScreenManager()
        screens = list()
        screens.append(Main_info(name="MainInfo"))
        screens.append(sub_new_activity(name="subNewActivity"))

        for i in range(len(screens)):
            self.sm.add_widget(screens[i])
        print("potato" + str(screens))
        self.theme_cls.primary_palette = "Blue"

        print("0current Screen: " + str(self.sm.current_screen) + " | has the next screen? " +str(self.sm.has_screen("MainInfo")))
        self.sm.switch_to(screens[0])

        
        return self.sm
    
Main().run()

 
 