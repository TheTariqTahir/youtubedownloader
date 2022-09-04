from kivy.lang import Builder
from kivymd.app import MDApp

import threading
from pytube import YouTube
from moviepy.editor import *

from kivy.clock import Clock
from kivy.clock import Clock, mainthread
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp,sp

from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import (
    CommonElevationBehavior,
 RectangularElevationBehavior,
 CircularElevationBehavior,
 RoundedRectangularElevationBehavior,
 FakeRectangularElevationBehavior,
 FakeCircularElevationBehavior,
 
)

from kivy.core.window import Window
Window.size = 360,600

class MDCardElevation(MDCard, RoundedRectangularElevationBehavior,):
    pass
class MDCardButton(MDCard, FakeRectangularElevationBehavior,):
    pass



class Main(MDApp):
    path_to_kv_file='kv_file.kv'
       
    
    def build(self):
        self.theme_cls.primary_palette = "DeepOrange"
        self.theme_cls.primary_hue = "A400"
        # self.theme_cls.theme_style = "Light"
        self.theme_cls.theme_style = "Dark"
        self.bg_color = self.theme_cls.bg_normal

        
        # self.path = os.getcwd()
        self.path = os.path.join(os.getcwd(),'data')
     


        text_file = open('hotreloader.kv','r')
        KV= text_file.read()
        self.builder = Builder.load_string(KV)
        # self.builder = Builder.load_file('kv_file.kv')
        return self.builder

    def update_kv_files(self,text):
        with open(self.path_to_kv_file,"w+") as kv_file:
            kv_file.write(text)
  
    #Get video
    def get_video(self,url,image):
        if url  =='':
            self.show_dialog('Error','Please enter url')
            return
        elif 'www.youtube.com' not in url:
            self.show_dialog('Error','Please enter correct url')
            return
        
        self.yt = YouTube(url)
        image.source = self.yt.thumbnail_url
        # print(self.yt.thumbnail_url)
        # menu_items = [
        #     {
        #         "text": f"Item {i}",
        #         "viewclass": "OneLineListItem",
        #         "height": dp(56),
        #         "on_release": lambda a = 'test',b='working': self.show_dialog(a,b)
        #     } for i in range(5)
        # ]
        # self.menu = MDDropdownMenu(
        #     items=menu_items,
        #     width_mult=4,
        # )
        
    def select_quality(self,type,quality_btn,download_button,spinner):
            self.new_thread = threading.Thread(target = self.select_quality_T , args=(type,quality_btn,download_button,spinner)) # Now call that function from this a new thread.
            self.new_thread.start()

       
    def select_quality_T(self,type,quality_btn,download_button,spinner):
        spinner.active = True
        quality_btn.disabled= True
        
        
        

        Clock.schedule_once(lambda x : self.select_quality_(type,quality_btn,download_button,spinner),.5)

    @mainthread
    def select_quality_(self,type,quality_btn,download_button,spinner):
            name = os.path.join(self.path,self.yt.title[:round(len(self.yt.title)/2)])
            if type =='Audio':
                try:
                    self.yt.streams.get_audio_only().download(self.path,filename=f'{name}.mp4')
                    mp4_without_frames = AudioFileClip(f'{name}.mp4')
                    mp4_without_frames.write_audiofile(f'{name}__.mp3')
                    mp4_without_frames.close() # function call mp4_to_mp3("my_mp4_path.mp4", "audio.mp3")
                    os.remove(os.path.join(self.path,f'{name}.mp4'))
                    print('done==========')
                    
                except Exception as e:
                    self.show_dialog('Error',"Some Error Occurend")
            
            quality_btn.disabled= False
            spinner.active = False
        
    def quality_popUp(self,item):
        
        self.menu.caller=item
        self.menu.open()
        
    
        # v = yt.streams.
        # try:
        #     # v.streams.get_audio_only().download(filename=f'{name}.mp4')
        #     mp4_without_frames = AudioFileClip(f'{name}.mp4')
        #     mp4_without_frames.write_audiofile(f'{name}__.mp3')
        #     mp4_without_frames.close() # function call mp4_to_mp3("my_mp4_path.mp4", "audio.mp3")
        #     os.remove(os.path.join(path,f'{name}.mp4'))
        #     print('done==========')
            
        # except Exception as e:
        #     self.show_dialog('Error',"Some Error Occurend")
            
        
    # Navigation Button Function
    
    
    
    #Menu Funtion
    
    #  Dialog functions
    def show_dialog(self, title, text):
        title=title
        text=text
        cancel_btn_username_dialouge=MDFlatButton(
            text="Okay", on_release=self.close_dialog)
        self.dialog=MDDialog(title=title, text=text, size_hint=(
            0.7, 0.2), buttons=[cancel_btn_username_dialouge])
        self.dialog.open()

    def close_dialog(self, obj):
            self.dialog.dismiss()
        
        
if __name__=='__main__':
    Main().run()