import re
import curses

window = curses.initscr()

def curs_hide():
	curses.curs_set(0)

def curs_show():
	curses.curs_set(1)

def printxt(y,text):
	global window
	window.move(y,0)
	window.addstr(text)

class Bar:
	'''
	Progress Bar:
	:y: the line shows the progress bar
	:weight: length of the progress bar
	:totalvalues: total values
	:formats: how to show the progress:[FilledCharacter],$ReplaceValue$
		for example: 
		[[#]] $totalvalues$tasks
		[#########     ] 60tasks
	'''
	def __init__(self,y,effect,weight=20,totalvalues=100,formats="[[#]] $rate1$%\n"):
		self._weight = weight # length of the filled part
		self._totalvalues = totalvalues # totalvalues of the progress bar
		self._values = 0
		self._y = y # which line to show
		self._formats = formats
		self._effect = effect

		se = re.findall(r"^(.+)\[(.)\](.+)$",formats)
		if se:
			self._startwith,self._filled,self._endwith = se[0]
		else:
			formats = "$rate1$% [[#]]"
			self._startwith,self._filled,self._endwith = re.findall(
				r"^(.+)\[(.)\](.+)$",formats)[0]

		self.win = curses.initscr()

	def __add__(self,other):
		self._values += other
		if self._values > self._totalvalues:
			self._values = self._totalvalues

		index = round(self._weight*(self._values/self._totalvalues))

		# Content need to be replaced
		subcontent = {
			"rate":round((self._values/self._totalvalues)*100,1),
			"rate1":round((self._values/self._totalvalues)*100),
			"values":self._values,
			"totalvalues":self._totalvalues
		}

		# Startwith,endwith and replace
		startwith = self._startwith
		endwith = self._endwith
		for suba,subb in subcontent.items():
			startwith = re.sub(rf"\${suba}\$",str(subb),startwith)
			endwith = re.sub(rf"\${suba}\$",str(subb),endwith)

		# If length is over one,only the first character is used
		try:
			# When the progress bar is not filled.
			if index <= self._weight+1: 
				# Clear the whole line.
				self.win.move(self._y,0)
				self.win.clrtoeol()
				
				# Add the progress bar.
				self.win.addstr(self._y,0,startwith)
				self.win.addstr(self._y,len(startwith),self._filled*index,self._effect)
				self.win.addstr(self._y,self._weight+len(startwith),endwith)

				# Flash.
				self.win.refresh()
			else:
				# Raise if overflowed.
				raise IndexError("overflow")

		except curses.error:
			return None

		except IndexError:
			return None

	def __iter__(self):
		return iter([self.__add__ for i in range(self.totalvalues)])

	@property
	def weight(self):
		return self._weight

	@property
	def y(self):
		return self._y
	
	@property
	def totalvalues(self):
		return self._totalvalues
	
	@property
	def values(self):
		return self._values
	
	@property
	def formats(self):
		return self._formats


