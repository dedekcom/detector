import tool_cfg as cfg
import fwk_resources as rsrc
import tool_logger as lg
import fwk_ticker as tck

cfg.reloadcfg()
itf = cfg.loaditf()

def printcommands():
	cmnds = itf['commands']
	for cmd in cmnds:
		print '\t',cmd["cmd"],'\t\t',cmd["txt"]

getch = lg.Getch()

def main_loop():
	printcommands()
	go = True
	wr = lg.Writer()
	while go:
		s = ''
		print 'enter command:'
		loop = True
		cmd = ''
		while loop:
			s = getch()
			code = ord(s)
			rep = repr(s)
			#print rep
			if rep =="'\\r'":
				loop = False
				cmd = wr.onenter()
			#elif code == 8 or code == 127:
			elif rep == "'\\x7f'":
				wr.onbackspace()
			elif code == 27:
				c2 = repr(getch())
				if c2 == "'['":
					c2 = repr(getch())
					if c2 == "'A'":
						wr.onup()
					elif c2=="'B'":
						wr.ondown()
					elif c2=="'C'":
						print "right"
					elif c2=="'D'":
						print "left"
			else:
				wr.putchar(s)
		if cmd == 'cfg':
			cfg.reloadcfg()
		elif cmd == 'clear':
			rsrc.clean_dirs()
		elif cmd == 'download':
			rsrc.download_tickers()
		elif cmd == 'exit':
			go = False
		elif cmd == 'help':
			printcommands()
		elif cmd == 'pr':
			if  wr.lenlline > 1:
				nofsessions = wr.igetarg('-d',0)
				noffut = wr.igetarg('-p',3)
				noftests = wr.igetarg('-t',10)
				nofchecks = wr.igetarg('-c',0)
				tck.test_ticker(wr.lline[1], nofsessions, noffut, noftests, nofchecks)
			else:
				print 'missing ticker for pr command'
		else:
			print itf['unknown'], cmd

main_loop()


