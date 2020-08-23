from kivymd.app import MDApp
from kivymd.uix.label import Label
from kivymd.uix.button import MDRectangleFlatButton, MDFloatingActionButtonSpeedDial
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.list import OneLineListItem, MDList
#from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder
from kivy.clock import Clock






class Main_info(Screen):
    #name = StringProperty("MainInfo")
    

    
    
    def __init__(self, **kwargs):
        super(Main_info,self).__init__(**kwargs)

        self.testdata = [dict() for x in range(4)]    
        self.testdata[0] = {"type":"programming","timeSpent":"", "date":"22/08/2020", "timeStart":"6:10", "timeEnd":"22:00", "project":""}
        self.testdata[1] =  {"type":"programming","timeSpent":"","date":"21/08/2020", "timeStart":"6:10", "timeEnd":"22:00", "project":""}
 
        Clock.schedule_once(self.update_Timeline,0.5)
    
    
    def uxids_dict_add(self,uxobjects):
        print (self.name + " uxObjects " + str(uxobjects))
        
        
    def update_Timeline(self,dt):
        print("updating timeline @ " + str(dt))

        self.ids.tester.text= "have i succeeded"
        self.listedItems = self.ids.past_items
        self.listedItems.add_widget(OneLineListItem(text="potato 101"))
    # def on_kv_post(self):
    #     super(Main_info,self).on_kv_post()
    #     for i in range(20):
    #         self.ids.floating.boxes.scrollingboxes.past_items.add_widget(OneLineListItem(text="potato" + i))




class sub_new_activity(Screen):

    def return_to_main(self):
        print("back")
        print("2current Screen: " + str(self.parent.current_screen) + " | has the next screen? " +str(self.parent.has_screen("subNewActivity")))
        self.parent.switch_to(screens[0])
        print("3current Screen: " + str(self.parent.current_screen) + " | has the next screen? " +str(self.parent.has_screen("subNewActivity")))
        
    def uxids_dict_add(self,uxobjects):
        print (self.name + " uxObjects " + str(uxobjects))



class Main(MDApp):

    data = {'timeline-plus-outline' : 'New activity',}


    def Add_callback(self,instance):
        print("\"Add to\" Screen")
        global screens
        
        self.sm.switch_to(screens[1])

    
    def build(self):
        global screens
        Builder.load_file("tmlayout.kv")
        self.sm = ScreenManager()
        screens = list()
        screens.append(Main_info(name="MainInfo"))
        screens.append(sub_new_activity(name="subNewActivity"))
        
        for i in range(len(screens)):
            self.sm.add_widget(screens[i])
            screens[i].uxids_dict_add(screens)
        print("potato" + str(screens))
        self.theme_cls.primary_palette = "Blue"

        print("0current Screen: " + str(self.sm.current_screen) + " | has the next screen? " +str(self.sm.has_screen("MainInfo")))
        self.sm.switch_to(screens[0])

        
        return self.sm




    
Main().run()

 
 