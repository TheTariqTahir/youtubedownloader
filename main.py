import webbrowser
from kivy.lang import Builder
from kivymd.app import MDApp
import threading
from kivy.core.window import Window
from kivy.utils import platform


import os
os.environ["IMAGEIO_FFMPEG_EXE"] = "/usr/bin/ffmpeg"

from pytube import YouTube
from moviepy.editor import AudioFileClip

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


class Main(MDApp):
    path_to_kv_file = 'kv_file.kv'

    def build(self):
        self.w=Window.size=350, 750
        # self.w= Window.size
        # print(self.w)
        self.theme_cls.primary_palette = "DeepOrange"
        self.theme_cls.primary_hue = "A400"
        # self.theme_cls.theme_style = "Light"
        self.theme_cls.theme_style = "Dark"
        self.bg_color = self.theme_cls.bg_normal

        
        #=============================Platform
        if platform == 'win':
            self.path = os.path.join(os.getcwd(), 'Download')
        elif platform == 'linux':
            self.path = os.path.join(os.getcwd(), 'Download')
        else:
            self.path = os.path.join(os.getenv('EXTERNAL_STORAGE'), ('Download'))
        try:
            os.mkdir(self.path)
        except:
            pass
        
        #--------------------- video Download
        self.type = 'Video'
        self.selected_qulity = ''
        self.qulity_available = False
        
        #============================ adding data to download

        self.downlaoad_screen = None

        self.builder = Builder.load_file('kv_file.kv')
        # text_file = open('hotreloader.kv','r')
        # KV= text_file.read()
        # self.builder = Builder.load_string(KV)

        return self.builder

    def update_kv_files(self, text):
        with open(self.path_to_kv_file, "w+") as kv_file:
            kv_file.write(text)

    # ==========================   Get video
    def get_video(self, url, image, spinner, quality_btn, download_btn):
        # print(os.getenv('EXTERNAL_STORAGE'))
        self.url = url
        if self.url == '':
            self.show_dialog('Error', 'Please enter url')
            return
        elif 'youtu' not in self.url:
            self.show_dialog('Error', 'Please enter correct url')
            return

        quality_btn.text = "Getting Data"
        download_btn.disabled = True
        self.yt = YouTube(self.url,on_progress_callback=self.on_progress, on_complete_callback=self.on_complete)
        image.source = self.yt.thumbnail_url
        
        self.spinner_on(spinner, quality_btn)
        threading.Thread(target=self.get_video_types, args=(
            spinner, quality_btn, download_btn), daemon=True).start()

    def test(self):
        webbrowser.open("https://www.instagram.com/mr_meemer.69/")

    def get_video_types(self, spinner, quality_btn, download_btn):
        # self.qulity_available=False
        self.video_types = self.yt.streaming_data
        quality_btn.text = 'Select Quality'

        @mainthread
        def add_menu():
            menu_items = [
                {
                    "text": str(i['qualityLabel']),
                    "viewclass": "OneLineListItem",
                    "height": dp(56),
                    "on_release": lambda itag=str(i['itag']), quality_btn=quality_btn, download_btn=download_btn, res=str(i['qualityLabel']): self.set_quality(itag, quality_btn, download_btn, res)
                } for i in self.video_types['formats']
            ]
            self.menu = MDDropdownMenu(
                items=menu_items,
                width_mult=4,
            )
            self.spinner_off(spinner, quality_btn)

        add_menu()

    def set_quality(self, tag, quality_btn, download_btn, res):
        self.selected_qulity = tag
        quality_btn.text = res
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
        name=name
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

    def Download(self, spinner,root):
        self.spinner = spinner

        self.screen_manager = root.manager
        # self.add_to_download_page()

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
            name_old = video.title[:round(
                len(video.title)*.6)].replace('|', '').replace('/', '').replace("\\", '').replace(":", '').replace("?", '').replace("*", '').replace("<", '').replace(">", '').strip()
            self.add_to_download_page(name_old,thumbnail)
            name = os.path.join(self.path, name_old)
            video.download(filename=f'{name}.mp4')
            self.screen_manager.current = 'Downloaded'

            self.spinner_off(spinner)
        except Exception as e:
            self.spinner_off(spinner)
            self.show_dialog('Error',str(e))

    def download_audio(self, spinner):
        print('Downloading Audio')
        video = self.yt.streams.get_audio_only()
        name_old = video.title.replace('|', '').replace('/', '').replace("\\", '').replace(":", '').replace("?", '').replace("*", '').replace("<", '').replace(">", '').strip()

        name = os.path.join(self.path, name_old)
        try:
            self.add_to_download_page(name_old)
            video.download(filename=f'{name}_audio.mp4')
            self.show_snakbar('Converting to Audio!')
            mp4_without_frames = AudioFileClip(f'{name}_audio.mp4')
            mp4_without_frames.write_audiofile(f'{name}.mp3')
            mp4_without_frames.close()  # function call mp4_to_mp3("my_mp4_path.mp4", "audio.mp3")
            os.remove(f'{name}_audio.mp4')
            self.show_snakbar('Audio file downloaded!',.2)
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


if __name__ == '__main__':
    Main().run()
