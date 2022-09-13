import webbrowser
from kivy.lang import Builder
from kivymd.app import MDApp
import threading
from kivy.core.window import Window
from kivy.utils import platform
from kivymd.uix.filemanager import MDFileManager
from kivy.uix.screenmanager import FadeTransition , SlideTransition
from kivy.uix.screenmanager import FadeTransition , SlideTransition

import sqlite3
import requests as r

from pytube import YouTube
import os

from kivy.clock import mainthread

from kivymd.uix.card import MDCard
from kivymd.uix.snackbar import Snackbar

from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.fitimage import FitImage
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar

from kivy.metrics import dp, sp

from kivymd.uix.behaviors import (
    RoundedRectangularElevationBehavior,
    FakeRectangularElevationBehavior,

)

from kivy.core.window import Window


class MDCardElevation(MDCard, RoundedRectangularElevationBehavior,):
    pass


class MDCardButton(MDCard, FakeRectangularElevationBehavior,):
    pass

import pyrebase
from kivy.clock import Clock



class Main(MDApp):
    path_to_kv_file = 'kv_file.kv'

    def build(self):
        # self.w= Window.size
        # print(self.w)
        self.theme_cls.primary_palette = "DeepOrange"
        self.theme_cls.primary_hue = "A400"
        # self.theme_cls.theme_style = "Light"
        self.theme_cls.theme_style = "Dark"
        self.bg_color = self.theme_cls.bg_normal

        
        #=============================Platform
        if platform == 'win':
            self.path = os.path.join(os.getcwd(), 'YoutubeDownloads')
        elif platform == 'linux':
            self.path = os.path.join(os.getcwd(), 'YoutubeDownloads')
        else:
            self.path = os.path.join(os.getenv('EXTERNAL_STORAGE'), ('YoutubeDownloads'))
        try:
            os.mkdir(self.path)
        except:
            pass
        
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
        
        
        
        
        #--------------------- video Download
        self.type = 'Video'
        self.selected_qulity = ''
        self.qulity_available = False
        
        #============================ File manager
        Window.bind(on_keyboard=self.onBackKey)

        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,  # function called when the user reaches directory tree root
            select_path=self.select_path,
            
        )   
        self.manager_open=False
        
        self.filename=''
        
        #============================ Builder
        self.builder = Builder.load_file('kv_file.kv')
        # text_file = open('hotreloader.kv','r')
        # KV= text_file.read()
        # self.builder = Builder.load_string(KV)
        self.w=Window.size=400, 800


        #----------------------------------  firebase

        
        self.config = {
                'apiKey': "AIzaSyAYaA6X_Yx5fr0tMmDzZiYIdjJL2LvOSNk",
                'authDomain': "downloader-97343.firebaseapp.com",
                'projectId': "downloader-97343",
                'storageBucket': "downloader-97343.appspot.com",
                'messagingSenderId': "213069231530",
                'appId': "1:213069231530:web:72891f5d9373e437b7a7d3",
                'measurementId': "G-HN4JYZ8P8Z",
                'databaseURL':'https://downloader-97343-default-rtdb.firebaseio.com/'
                }

        self.firebase = pyrebase.initialize_app(self.config)

        self.db = self.firebase.database()

        self.con = sqlite3.connect('offline.db')
        self.cur =self.con.cursor()
        
        self.cur.execute('SELECT * from login')
        res = self.cur.fetchone()
        if res[0]=='True':
            temp =self.db.child('data').child(res[1]).get()
            if temp.val()['active']=='True':
                self.builder.ids.screen_manager.current='Home'
                self.builder.ids.b_download.disabled=False
                self.builder.ids.b_home.disabled=False
        self.con.commit()
          
            

        return self.builder

    def test_con(self):
        try:
            x=r.get('https://www.google.com')
            if x.status_code=='200':
                return True
        except Exception as e:
            print('adfasdf')
            Clock.schedule_once(self.show_dialog('Error',str(e),2))


        

    def check_password(self,root,email_,password):
    
        if email_ =='':
            self.show_dialog('Error','Please enter email')
            return
        if password =='':
            self.show_dialog('Error','Please enter email')
            return
        try:
            email = email_.split('@')[0]
            data =self.db.child('data').child(email).get()
            self.online_allow = False
            self.offline_allow = False
            if data.val()['active'] == 'False':
                if email_ == (data.val()['email']) and password==data.val()['password']:
                    try:
                        self.db.child('data').child(email).update({"active":'True'})
                        self.online_allow = True
                    except Exception as e:
                        self.show_dialog('Online',str(e))
                    try:
                        self.cur.execute("UPDATE login set active='True',email='"+str(email_)+"'")
                        self.con.commit()
                        self.offline_allow = True
                    except Exception as e:
                        self.show_dialog('offline',str(e))
                    if self.online_allow and self.offline_allow:
                        root.manager.transition = FadeTransition()
                        root.manager.current='Home'
                        root.manager.transition = SlideTransition() 
                        self.builder.ids.b_download.disabled=False
                        self.builder.ids.b_home.disabled=False
                        return True
            else:
                self.show_dialog('Acces Denied','Account already registered')

        except Exception as e:
            self.show_dialog('Error',str(e))
            



    def update_kv_files(self, text):
        with open(self.path_to_kv_file, "w+") as kv_file:
            kv_file.write(text)

    # ==========================   file manager
    
    def file_manager_open(self,path):
        self.file_manager.show(self.path)
        self.path_field=path
        self.manager_open=True
        
    def exit_manager(self,*args):
        self.file_manager.close()
        self.manager_open=False
    
    def select_path(self,path):
        if '.' in path:
            self.path ,file = os.path.split(path)
        else:
            self.path= path
        self.path_field.text=self.path
        self.exit_manager()
    
    def onBackKey(self,window,key,*args):
        if key == 27 :
            if self.manager_open:
                self.file_manager.back()
                print('back')
                return True
    
    # ==========================   Get video
    def get_video(self, url, image, spinner, quality_btn,quality, download_btn,file_name):
        # print(os.getenv('EXTERNAL_STORAGE'))
        if self.test_con() ==False:
            return
        self.url = url
        if self.url == '':
            self.show_dialog('Error', 'Please enter url')
            return
        elif 'youtu' not in self.url:
            self.show_dialog('Error', 'Please enter correct url')
            return

        quality.text = "Getting Data"
        download_btn.disabled = True
        self.yt = YouTube(self.url,on_progress_callback=self.on_progress, on_complete_callback=self.on_complete)
        image.source = self.yt.thumbnail_url
        file_name.text=self.yt.title[:50]+'...'
        self.filename=self.yt.title
        
        self.spinner_on(spinner, quality_btn)
        threading.Thread(target=self.get_video_types, args=(
            spinner, quality_btn,quality, download_btn), daemon=True).start()

    def test(self):
        webbrowser.open("https://www.instagram.com/mr_meemer.69/")
        
    def change_to_home(self,screen_manager,b_home,l_home,b_download,l_download):
        b_home.md_bg_color=self.theme_cls.primary_color
        l_home.color=[1]*4
        b_download.md_bg_color=self.theme_cls.bg_normal
        l_download.color=self.theme_cls.primary_color
        screen_manager.transition.direction = 'right'
        screen_manager.current= 'Home'
        
    def change_to_downloading(self,screen_manager,b_download,l_download,b_home,l_home):
        b_download.md_bg_color=self.theme_cls.primary_color
        l_download.color=[1]*4
        b_home.md_bg_color=self.theme_cls.bg_normal
        l_home.color=self.theme_cls.primary_color

        screen_manager.transition.direction = 'left'
        screen_manager.current= 'Downloaded'

    def get_video_types(self, spinner, quality_btn,quality, download_btn):
        # self.qulity_available=False
        self.video_types = self.yt.streaming_data
        quality.text = 'Select Quality'

        @mainthread
        def add_menu():
            menu_items = [
                {
                    "text": str(i['qualityLabel']),
                    "viewclass": "OneLineListItem",
                    "height": dp(56),
                    "on_release": lambda itag=str(i['itag']), quality_btn=quality_btn, download_btn=download_btn, res=str(i['qualityLabel']): self.set_quality(itag, quality_btn,quality, download_btn, res)
                } for i in self.video_types['formats']
            ]
            self.menu = MDDropdownMenu(
                items=menu_items,
                width_mult=4,
            )
            self.spinner_off(spinner, quality_btn)

        add_menu()

    def set_quality(self, tag, quality_btn,quality, download_btn, res):
        self.selected_qulity = tag
        quality.text = res
        download_btn.disabled = False
        self.menu.dismiss()

    def select_quality(self, type, quality_btn, download_button, spinner, url):
        if url == '':
            self.show_dialog('Error', 'Please Enter URL')
            return
        self.type = type

#@----------------------------------     Download Video
    @mainthread
    def add_to_download_page(self,name,thumbnail):
        # name=round(name[:len(name/1.5)])
        name=name[:50]+'...'
        self.main_card = MDCard(
            size_hint_y=None,
            height=dp(70),
            radius=dp(8),
            md_bg_color=self.theme_cls.bg_light,
            line_color=self.theme_cls.primary_color,
            line_width=dp(1.3),
            padding=dp(10),
            spacing=dp(5),
        )
        #----------------  Download Image
        image_card=MDCard(
            size_hint=(None,None),
            height=dp(50),
            width=dp(50),
        )
        self.image= FitImage(
            source=thumbnail,
            radius=dp(8),
        )
        image_card.add_widget(self.image)
        self.main_card.add_widget(image_card)

        #---------------------------------------------- wrapper Card
        card_wrapper = MDCard(
            size_hint=(.8,1),
            orientation= 'vertical',
            spacing= '5dp',
        )
        #----------------  Name of File
        name_card = MDCard(
            padding= ('10dp', '0dp', '0dp', '0dp')
        )
        file_name=  MDLabel(
                        text=name,
                        font_color='Custom',
                        color='white',
        )
        file_name.font_size=dp(12)
        name_card.add_widget(file_name)


        #----------------  Progress Bar
        progress_card= MDCard(
            size_hint=(1,None),
            height=dp(6),
            padding=(dp(10),dp(10)),
        )
        self.progress_bar = MDProgressBar(
            value=0.0,
            size_hint=(1,None),
            height=dp(5),
            pos_hint={'center_y':.5},
        )
        progress_card.add_widget(self.progress_bar)

        #----------------  percentage text

        percentage_card = MDCard(
            padding= ('10dp', '0dp', '10dp', '0dp')
        )
        self.pending_percentage=MDLabel(
                        text='0.0%',
                        font_color='Custom',
                        halign='left',
                        color='white',
                        )
        self.pending_percentage.font_size=dp(12)
        total_percentage=MDLabel(
                        text='100.0%',
                        font_color='Custom',
                        halign='right',
                        color='white',
                        )
        total_percentage.font_size=dp(12)
        percentage_card.add_widget(self.pending_percentage)
        percentage_card.add_widget(total_percentage)

        #----------------- ADD to card


        card_wrapper.add_widget(name_card)
        card_wrapper.add_widget(progress_card)
        card_wrapper.add_widget(percentage_card)
        self.main_card.add_widget(card_wrapper)



        self.screen_manager.get_screen('Downloaded').ids.download_screen.add_widget(self.main_card)
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.current= 'Downloaded'

        return file_name,self.progress_bar,self.pending_percentage

  
    def Download(self, spinner,root,filename):
        self.spinner = spinner

        self.screen_manager = root.manager
        # self.add_to_download_page()
        self.filename=filename.text
        if self.type == 'Video':
            self.spinner_on(spinner)
            threading.Thread(target=self.download_video,args=(spinner,), daemon=True).start()
        else:
            self.spinner_on(spinner)
            threading.Thread(target=self.download_audio,args=(spinner,), daemon=True).start()



    def download_video(self, spinner):
        try:
            yt = YouTube(self.url,on_progress_callback=self.on_progress, on_complete_callback=self.on_complete)
            video = yt.streams.get_by_itag(self.selected_qulity)
            thumbnail = yt.thumbnail_url
            name_old = self.filename[:50].replace('|', '').replace('/', '').replace("\\", '').replace(":", '').replace("?", '').replace("*", '').replace("<", '').replace(">", '').strip()
            self.add_to_download_page(name_old,thumbnail)
            name = os.path.join(self.path, name_old)
            self.to_download_screen()
            video.download(filename=f'{name}.mp4')

            self.spinner_off(spinner)
        except Exception as e:
            self.spinner_off(spinner)
            self.show_dialog('Error',str(e))

    @mainthread
    def to_download_screen(self):
        print('running')
        print(self.screen_manager.ids)
        self.builder.ids.b_download.md_bg_color=self.theme_cls.primary_color
        self.builder.ids.l_download.color=[1]*4
        self.builder.ids.b_home.md_bg_color=self.theme_cls.bg_normal
        self.builder.ids.l_home.color=self.theme_cls.primary_color
        self.screen_manager.transition.direction = 'left'
        self.screen_manager.current = 'Downloaded'
        

    def download_audio(self, spinner):
        print('Downloading Audio')
        # video = self.yt.streams.get_audio_only()

        try:
            yt = YouTube(self.url,on_progress_callback=self.on_progress, on_complete_callback=self.on_complete)
            video = yt.streams.get_audio_only()
            print(video.title)
            thumbnail = yt.thumbnail_url
            name_old = self.filename[:50].replace('|', '').replace('/', '').replace("\\", '').replace(":", '').replace("?", '').replace("*", '').replace("<", '').replace(">", '').strip()
            self.add_to_download_page(name_old,thumbnail)

            name = os.path.join(self.path, name_old)
            video.download(filename=f'{name}_audio.mp4')
            self.to_download_screen()
            
            print('done==========')
            self.spinner_off(spinner)

        except Exception as e:
            self.show_snakbar('Audio Conversion failed',.3)
            print(e)


    @mainthread
    def on_complete(self, stream, path):
        self.show_dialog('Success', 'File downloaded in Download folder')

    def on_progress(self,stream, chunk, bytes_remaining):
        # print('running')
        self.spinner_off(self.spinner)
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        totalsz = (total_size/1024)/1024
        totalsz = round(totalsz,1)
        remain = (bytes_remaining / 1024) / 1024
        remain = round(remain, 1)
        dwnd = (bytes_downloaded / 1024) / 1024
        dwnd = round(dwnd, 1)
        percentage_of_completion = round(percentage_of_completion,2)

        self.progress_bar.value = percentage_of_completion
        self.pending_percentage.text=str(percentage_of_completion)+'%'



    # ----------------------Spinner Function

    @mainthread
    def show_snakbar(self, text,duration = None):
        if duration==None:
            Snackbar(
                text=f"{text}!",
                pos_hint= {"center_x": .5, "center_y": .15},
                size_hint_x= .8,
                    ).open()
        else:
            Snackbar(
                text=f"{text}!",
                pos_hint= {"center_x": .5, "center_y": .15},
                size_hint_x= .8,
                duration= duration,
                    ).open()
            

    @mainthread
    def spinner_on(self, spinner, quality_btn=None, download_button=None):
        spinner.active = True
        if quality_btn == None:
            return
        quality_btn.disabled = True
        if download_button == None:
            return
        download_button.disabled = True

    @mainthread
    def spinner_off(self, spinner, quality_btn=None, download_button=None):
        spinner.active = False
        if quality_btn == None:
            return
        quality_btn.disabled = False
        if download_button == None:
            return
        download_button.disabled = False

    # ----------------------MEnu Function
    # Menu Funtion
    def quality_popUp(self, item):
        self.menu.caller = item
        self.menu.open()

    #  Dialog functions
    def show_dialog(self, title, text):
        title = title
        text = text
        cancel_btn_username_dialouge = MDFlatButton(
            text="Okay", on_release=self.close_dialog)
        self.dialog = MDDialog(title=title, text=text, size_hint=(
            0.7, 0.2), buttons=[cancel_btn_username_dialouge])
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()
        
    def quit_show_dialog(self, title, text):
        title = title
        text = text
        
        yes_quit = MDFlatButton(text="Yes", on_release=self.close_dialog)
        no_quit = MDFlatButton(text="No", on_release=self.quit_dialog.dismiss())
        
        self.quit_dialog = MDDialog(title=title, text=text, size_hint=(0.7, 0.2), buttons=[yes_quit,no_quit])
        self.quit_dialog.open()

    def quit_close_dialog(self, obj):
        self.quit_dialog.dismiss()
        # self.quit=yes
        
    


if __name__ == '__main__':
    Main().run()
