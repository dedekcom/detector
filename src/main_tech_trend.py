
import sys
import fwk_resources as rsrc
import fwk_ticker as fwktc
import tool_logger as log

argc = len(sys.argv)
log.is_debug = False

def getarg(arg,defval):
	if arg in sys.argv and sys.argv.index(arg) < argc-1:
		return sys.argv[sys.argv.index(arg)+1]
	else:
		return defval

def isarg(arg):
	return arg in sys.argv


def dvsmas(tck, smas):
	r = []
	for sm in smas:
		s1 = tck.sma(sm)
		s2 = tck.sma(sm,1)
		if s2 < 0:
			return []
		r.append((s1-s2)/s1)
	return r

def prog():
	go = 1
	if isarg("-u"):
		go = rsrc.download_tickers()
	if go == 0:
		return
	mode = getarg("-m",0)
	if mode == "1":
		smas = [23,90,180,270,360,500]
	elif mode == "2":
		print 'strong bulls:'
		smas = [23,45,90,180,270,360]
	
	
	tck = rsrc.get_tickers()
	
	tcwig = fwktc.Ticker('wig')
	lastdate = tcwig.getdate()
	
	result = []
	for tfile in tck:
		t = fwktc.Ticker()
		t.loadfull(tfile)
		if t.getdate() == lastdate:
			if mode == "1":
				d = dvsmas(t,smas)
				if len(d) > 0 and d[0] > 0 and d[1] >= 0 and d[2] <= 0 and d[3] <= 0 and d[4] <= 0 and d[5] <= 0:
					print t.ticker,'early up trend'
			elif mode == "2":
				d = dvsmas(t,smas)
				if len(d) > 0 and d[0] > 0 and d[1] >= 0 and d[2] >= 0 and d[3] >= 0 and d[4] >= 0 and d[5] >= 0:
					# print t.ticker,'strong bull',str(sum(d))
					result.append(str(sum(d)) + ' ' + t.ticker)
	result = sorted(result)
	for r in result:
		print r

prog()

