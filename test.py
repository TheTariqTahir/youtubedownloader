from kivymd.app import MDApp
from kivy.clock import mainthread
from kivy.lang import Builder
KV = '''
BoxLayout:
    MDCard:
        MDLabel:
            id:text
            text:'asdfasdfasfsa'
        
        MDRaisedButton:
            text:'start'
            on_press:app.start_thread()
        MDRaisedButton:
            text:'Click'
            on_press:text.text='changed'


'''

import threading as th
from kivymd.uix.boxlayout import BoxLayout

class App(MDApp):
        
        
    def build(self):
        self.builder = Builder.load_string(KV)
        return self.builder
        
    def start_thread(self):
        th.Thread(target=self.start,daemon=True).start()
        
        
    def start(self):
        for i in range(13231231231):
            print(i)
            
    def actual(self):
        pass
        
# class Root(BoxLayout):
#     def __init__(self,**kwargs):
#         super().__init__(**kwargs)
        
        

    

if __name__=='__main__':
    App().run()
    
    
    