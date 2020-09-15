from kivymd.app import MDApp
from kivymd.uix.label import Label
from kivymd.uix.button import MDRectangleFlatButton, MDFloatingActionButtonSpeedDial
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition,SwapTransition
from kivymd.uix.list import ThreeLineListItem, MDList
#from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder
from kivy.clock import Clock
import datetime
import sqlite3

DB_conn= sqlite3.connect("TimeStorage.db")


class Main_info(Screen):

    def __init__(self, **kwargs):
        super(Main_info,self).__init__(**kwargs)



    
    def uxids_dict_add(self,uxobjects):
        global DB_conn
        print (self.name + " uxObjects " + str(uxobjects))
        self.avalible_screens = uxobjects

        try:
            DB_conn= sqlite3.connect("TimeStorage.db")
        except:
            print("failed table creation")
        try:
            DB_conn.cursor().execute("""CREATE TABLE timetable (task_id INTEGER PRIMARY KEY  AUTOINCREMENT,task_name text , task_type text ,timeSpent text, date text, timeStart text, timeEnd text, project_name text, project_ID text)""")
        except:
            print("timetable already exists")

        Clock.schedule_once(self.Init_TimeLine,0.1)

    def Init_TimeLine(self, dt):
        global DB_conn
        print("init timeline @ " + str(dt))
        cu = DB_conn.cursor()
        cu.execute("""SELECT task_name, timeSpent, task_type, date, timeStart, project_name FROM timetable""")
        self.displayData = cu.fetchall()
        print(self.displayData)
        print()

        self.Update_Timeline(None)


    def Update_Timeline(self, new_data):
        global DB_conn

        #try:
        if new_data != None:
            timeEnd = datetime.datetime.now()
            timeEnd = timeEnd.strftime("%H:%M")
            print(str(self.displayData) + " | new data :"  + str(new_data))
            addingData = {"name" : new_data["name"], "type": new_data["type"],"project": new_data["project"],
                          "date":new_data["date"], "timeStart":new_data["timeStart"],
                          "timeEnd":timeEnd, "timeSpent":new_data["timeSpent"]}
            print(str(addingData) + " || added too"+str(self.displayData))
            self.displayData.append([addingData["name"],addingData["timeSpent"],
                                     addingData["type"],addingData["date"],
                                     addingData["timeStart"],addingData["project"]])
            sql = ("INSERT INTO timetable(task_name, task_type,project_name, date, timeStart, timeEnd, timeSpent) VALUES (")
            for i in addingData.keys():
                sql = sql +"'"+ str(addingData[i]) + "'"
                if i != list(addingData.keys())[-1]:
                    sql = sql + ", "
            sql = sql + ")"
            print(sql)
            DB_conn.cursor().execute(sql)
            DB_conn.commit()
        else:
            print("no new data")
        #if self.parent.parent.ids.get("past_items") == True:
        listedItems = self.ids.past_items
        listedItems.clear_widgets()
        for i in self.displayData:
            listedItems.add_widget(ThreeLineListItem(text=(str(i[0]) + " | timespent: " + str(i[1])),
                secondary_text=("type: "+ i[2]+" | date: "+ str(i[3]) + "| start time: " + i[4] ),
                tertiary_text=("Project: " + i[5])))
            print(i)

            #else: 
            #Clock.schedule_once(self.update_Timeline,5)
            #print("clockin")
        #except:
            #print("failed to load ids wtf")

    ##Button Definition
    data = {'timeline-plus-outline' : 'New activity',"timeline-clock-outline": "add past activity"}
    def Add_callback(self,instance):
        print(instance.icon)
        global screens
        
        if instance.icon == "timeline-plus-outline":
            self.parent.switch_to(screens[1])
        if instance.icon == "timeline-clock-outline":
            #self.parent.switch_to(screens[2])
            print("not implemeneted yet")


class sub_new_activity(Screen):
    def __init__(self, **kwargs):
        super(sub_new_activity,self).__init__(**kwargs)

    def return_to_main(self):
        print("back")
        print("2current Screen: " + str(self.parent.current_screen) + " | has the next screen? " +str(self.parent.has_screen("subNewActivity")))
        self.parent.switch_to(screens[0])
        print("3current Screen: " + str(self.parent.current_screen) + " | has the next screen? " +str(self.parent.has_screen("subNewActivity")))
        
    def uxids_dict_add(self,uxobjects):
        print (self.name + " uxObjects " + str(uxobjects))
        self.avalible_screens = uxobjects

    def start_timer(self):
        timeStart = datetime.datetime.now()
        dateStart = timeStart.strftime("%d/%m/%Y")
        timeStart = timeStart.strftime("%H:%M:%S")
        activityDict = {"name":self.ids.TF_Name.text,"project":self.ids.TF_ProjectName.text,"type":self.ids.TF_WorkType.text,"timeSpent" : "","timeStart":str(timeStart), "date": str(dateStart)}
        print("Start" + str(activityDict))
        self.parent.switch_to(screens[2],transition=SwapTransition(),direction="right")
        self.avalible_screens[2].Start_Timer(activityDict)
        


class activity_timer(Screen):
    curr_pauseState = True
    timer = 0
    def __init__(self, **kwargs):
        super(activity_timer,self).__init__(**kwargs)


    def return_to_main(self):
        print("back")
        print("2current Screen: " + str(self.parent.current_screen) + " | has the next screen? " +str(self.parent.has_screen("subNewActivity")))
        self.parent.switch_to(screens[0])
        print("3current Screen: " + str(self.parent.current_screen) + " | has the next screen? " +str(self.parent.has_screen("subNewActivity")))

    def uxids_dict_add(self,uxobjects):
        print (self.name + " uxObjects " + str(uxobjects))
        self.ids.pausePlay.icon = "pause-circle-outline"
        self.avalibleScreens = uxobjects


    def Start_Timer(self,activity_dict):
        self.timer = 0
        self.currPauseState = False
        self.clockEvent = Clock.schedule_interval(self.Run_Timer,0.25)
        self.activityDict = activity_dict

    def Run_Timer(self, dt):
        if self.currPauseState != True:
            self.timer += dt

            print(datetime.timedelta(0,self.timer))
            display = int(self.timer)
            self.ids.timer_Display.text = str(datetime.timedelta(0,display))
        else:
            print("paused")
        

    def toggle_Pause_State(self):
        if self.ids.pausePlay.icon == "pause-circle-outline":
            self.currPauseState = True
            self.ids.pausePlay.icon = "play-circle-outline"
            print("paused")
        elif self.ids.pausePlay.icon == "play-circle-outline":
            self.currPauseState = False
            self.ids.pausePlay.icon = "pause-circle-outline"
            print("playing")

    def save_activity(self):
        print("potato")
        self.currPauseState = True
        self.clockEvent.cancel()
        self.activityDict["timeSpent"] = str(datetime.timedelta(0,int(self.timer)))
        self.avalibleScreens[0].Update_Timeline(self.activityDict)

        self.parent.switch_to(screens[0])
        

class Main(MDApp):

    def build(self):
        global screens
        Builder.load_file("tmlayout.kv")
        self.sm = ScreenManager(transition=NoTransition())
        screens = list()
        screens.append(Main_info(name="MainInfo"))
        screens.append(sub_new_activity(name="subNewActivity"))
        screens.append(activity_timer(name="activitytimer"))
        for i in range(len(screens)):
            self.sm.add_widget(screens[i])
            screens[i].uxids_dict_add(screens)
        print("potato" + str(screens))
        self.theme_cls.primary_palette = "Blue"

        print("0current Screen: " + str(self.sm.current_screen) + " | has the next screen? " +str(self.sm.has_screen("MainInfo")))
        self.sm.switch_to(screens[0])

        
        return self.sm




    
Main().run()

 
 