from kivy.lang import Builder
from kivymd.app import MDApp
import threading
from kivy.core.window import Window
from kivy.utils import platform



from pytube import YouTube
from moviepy.editor import *

from kivy.clock import mainthread

from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp,sp

from kivymd.uix.behaviors import (
 RoundedRectangularElevationBehavior,
 FakeRectangularElevationBehavior,
 
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
        #self.w=Window.size=350, 650
        self.w= Window.size
        self.theme_cls.primary_palette = "DeepOrange"
        self.theme_cls.primary_hue = "A400"
        # self.theme_cls.theme_style = "Light"
        self.theme_cls.theme_style = "Dark"
        self.bg_color = self.theme_cls.bg_normal

        
        # self.path = os.getcwd()
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
            self.path = 'sdcard/Downlaod'
        else:
            self.path = os.path.join(os.getcwd(),'data')
            
        self.type='Video'
        self.selected_qulity = ''


        # text_file = open('hotreloader.kv','r')
        # KV= text_file.read()
        # self.builder = Builder.load_string(KV)
        self.builder = Builder.load_file('kv_file.kv')
        return self.builder

    def update_kv_files(self,text):
        with open(self.path_to_kv_file,"w+") as kv_file:
            kv_file.write(text)
  
    #Get video
    def get_video(self,url,image,spinner,quality_btn,download_btn):
        if url  =='':
            self.show_dialog('Error','Please enter url')
            return
        elif 'www.youtube.com' not in url:
            self.show_dialog('Error','Please enter correct url')
            return

        quality_btn.text="Getting Data"
        download_btn.disabled=True
        self.yt = YouTube(url)
        image.source = self.yt.thumbnail_url
        self.spinner_on(spinner,quality_btn)
        # time.sleep(1)
        threading.Thread(target=self.get_video_types,args=(spinner,quality_btn,download_btn),daemon=True).start()
        
       
    
    def get_video_types(self,spinner,quality_btn,download_btn):
            self.video_types=self.yt.streams.filter(progressive=True)
            quality_btn.text='Select Quality'

            @mainthread
            def add_menu():
                menu_items = [
                    {
                        "text":str(i.resolution),
                        "viewclass": "OneLineListItem",
                        "height": dp(56),
                        "on_release": lambda itag = str(i.itag),quality_btn=quality_btn,download_btn=download_btn, res=str(i.resolution): self.set_quality(itag,quality_btn,download_btn,res)
                    } for i in self.video_types
                        ]
                self.menu = MDDropdownMenu(
                    items=menu_items,
                    width_mult=4,
                )
                self.spinner_off(spinner,quality_btn)
                
            add_menu()
            
            
    def set_quality(self,tag,quality_btn,download_btn,res):
        print(tag)
        self.selected_qulity= tag
        quality_btn.text=res
        download_btn.disabled= False
        self.menu.dismiss()
        
    def select_quality(self,type,quality_btn,download_button,spinner):
            self.new_thread = threading.Thread(target = self.select_quality_T , args=(type,quality_btn,download_button,spinner),daemon=True) # Now call that function from this a new thread.
            self.new_thread.start()

    def select_quality_T(self,type,quality_btn,download_button,spinner):
        self.type = type
        self.spinner_on(spinner)
        
        if self.type =='Audio':
          download_button.disabled= False
          quality_btn.disabled= True
        elif self.type =='Video':
            threading.Thread(target=self.get_video_types,args=(spinner,quality_btn,download_button),daemon=True).start()
            quality_btn.disabled= False
            download_button.disabled-= False
          
        self.spinner_off(spinner)
        

    def Download(self,spinner):
        if self.type =='Video':
            self.spinner_on(spinner)
            threading.Thread(target=self.download_video,daemon=True).start()
        else:
            pass
            threading.Thread(target=self.download_audio,daemon=True).start()
        
    def download_video(self):
        video = self.yt.streams.get_by_itag(self.selected_qulity)
        name_old = video.title[:round(len(video.title)/2)]
        name = os.path.join(self.path,name_old)
        video.download(filename=f'{name}.mp4')
        
        clip = VideoFileClip(f'{name}.mp4')
        clip.write_videofile(f'{name}_.mp4')
        clip.close()
        os.remove(f'{name}.mp4')
        
    def download_audio(self):
        video = self.yt.streams.get_audio_only()
        name_old = video.title[:round(len(video.title)/2)]
        name = os.path.join(self.path,name_old)
        
        try:
            video.download(filename=f'{name}.mp4')
            mp4_without_frames = AudioFileClip(f'{name}.mp4')
            mp4_without_frames.write_audiofile(f'{name}__.mp3')
            mp4_without_frames.close() # function call mp4_to_mp3("my_mp4_path.mp4", "audio.mp3")
            os.remove(f'{name}.mp4')
            print('done==========')
            
        except Exception as e:
            print(e)

        # @mainthread
        # def off():
        #     self.spinner_off(spinner)
        # off()
   
            
   
    # ----------------------Spinner Function 
    @mainthread
    def spinner_on(self,spinner,btn=None):
        spinner.active=True
        if btn ==None:
            return
        btn.disabled= True
        
    @mainthread
    def spinner_off(self,spinner,btn=None):
        spinner.active=False
        if btn ==None:
            return
        btn.disabled= False
        
    # ----------------------MEnu Function 
    #Menu Funtion
    def quality_popUp(self,item):
        self.menu.caller=item
        self.menu.open()
    
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
            self.menu.dismiss()
        
if __name__=='__main__':
    Main().run()