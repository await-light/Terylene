import time
import random
import json
from threading import Thread
from websocket import create_connection
from asciimatics.scene import Scene
from asciimatics.widgets import Frame,Layout,Button
from asciimatics.widgets import TextBox,Widget
from asciimatics.widgets.divider import Divider
from asciimatics.event import KeyboardEvent
from asciimatics.screen import ManagedScreen,Screen
from asciimatics.renderers.charts import BarChart
from asciimatics.renderers.plasma import Plasma
from asciimatics.renderers.images import ImageFile
from asciimatics.particles import StarFirework,Splash


def colorful_text(screen, text, x, y):
	for index,char in enumerate(text):
		screen.paint(text=char, x=x+index, y=y, colour=random.randint(0, 256))

class V(Frame):
	def __init__(self,screen):
		Frame.__init__(self,
			screen=screen,
			height=screen.height * 2 // 3,
			width=screen.width * 2 // 3)

		self.s = screen

		self.ws = create_connection("wss://hack.chat/chat-ws")
		self.join()

		self.set_theme("bright")

		layout = Layout([5,1])
		self.add_layout(layout)
		self.sendmessage = TextBox(1,name="text", as_string=True,
			line_wrap=True)
		layout.add_widget(self.sendmessage,0)
		layout.add_widget(Button("Send",self.send),1)

		layout1 = Layout([1])
		self.add_layout(layout1)
		layout.add_widget(Divider(),0)
		self.showmessage = TextBox(Widget.FILL_FRAME,name="message", 
			as_string=True,line_wrap=True,readonly=True)
		self.showmessage.hide_cursor = True
		self.showmessage.disabled = True
		layout1.add_widget(self.showmessage)

		self.layout = layout

		self.fix()

		listenfunc = Thread(target=self.listen).start()

	def listen(self):
		while True:
			r = json.loads(self.ws.recv())
			if r["cmd"] == "chat":
				self.showmessage.value += \
					f"{r['nick']}:{r['text']}\n"
			elif r["cmd"] == "warn":
				self.showmessage.value += \
					f"! {r['text']}\n"
			else:
				continue
			self.s.refresh()

	def join(self):
		self.ws.send(json.dumps({
			"cmd":"join",
			"nick":"Light",
			"channel":"your-channel"
			}))

	def send(self):
		self.ws.send(json.dumps({
			"cmd":"chat",
			"text":self.sendmessage.value
			}))
		self.sendmessage.value = ""
		

def demo(screen):
	scenes = [
    	Scene([V(screen)], -1, name="Main"),
		]
	screen.play(scenes)

Screen.wrapper(demo)
