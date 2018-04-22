import sys

is_debug = True

def log(msg):
	if is_debug:
		print msg

class Getch:
	def __init__(self):
		import tty

	def __call__(self):
		import tty, termios
		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())
			ch = sys.stdin.read(1)
		finally:
			termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
			if ch == '\x03':
				raise KeyboardInterrupt
			elif ch == '\x04':
				raise EOFError
			return ch

class Writer:
	def __init__(self):
		self.line = ''
		self.lline = []
		self.lenlline = 0
		
		self.idlastcmd = 0
		self.cntcmds = 1
		self.lencmds = 100
		self.lastcmds = map(lambda x: '',range(0, self.lencmds))
		self.setline('')
		
	
	def clrln(self):
		sys.stdout.write("\r"+ (' '*len(self.line)))
	
	def prln(self):
		sys.stdout.write("\r"+ self.line)
	
	def onenter(self):
		self.lline = self.line.split()
		self.lenlline = len(self.lline)
		#print 'enter: (cntcmds, idlast, lencmds)',str(self.cntcmds),str(self.idlastcmd),str(self.lencmds)
		if self.idlastcmd != self.cntcmds-1:
			self.lastcmds[self.cntcmds-1] = self.line
		self.cntcmds += 1
		if self.cntcmds > self.lencmds:
			self.cntcmds = self.lencmds
			self.lastcmds.pop(0)
			self.lastcmds[-1] = self.line
			self.lastcmds.append('')
		self.idlastcmd = self.cntcmds - 1
		self.setline('')
		print ''
		#print 'enter end: (cntcmds, idlast)',str(self.cntcmds),str(self.idlastcmd)
		#print self.lastcmds
		if self.lenlline > 0:
			return self.lline[0]
		else:
			return ''
	
	def onup(self):
		self.nextcmd(-1)
	
	def ondown(self):
		self.nextcmd(1)
	
	def nextcmd(self,i):
		self.idlastcmd += i
		if self.idlastcmd < 0:
			self.idlastcmd = self.cntcmds - 1
		elif self.idlastcmd >= self.cntcmds:
			self.idlastcmd = 0
		self.clrln()
		self.line = self.lastcmds[self.idlastcmd]
		self.prln()
	
	def setline(self,l):
		self.line = l
		self.lastcmds[self.idlastcmd] = self.line
	
	def onbackspace(self):
		self.clrln()
		self.setline(self.line[:-1])
		self.prln()
	
	def putchar(self,s):
		self.setline(self.line + s)
		self.prln()
	
	def getarg(self,arg,defval):
		if arg in self.lline and self.lline.index(arg) < self.lenlline-1:
			return self.lline[self.lline.index(arg)+1]
		else:
			return defval

	def igetarg(self,arg,defval):
		return int(self.getarg(arg,defval))
