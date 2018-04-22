import tool_cfg as cfg
from tool_logger import log
import rsrc_train as tr

class Ticker:
	def __init__(self, ticker = None):
		self.tcklist = []
		self.lcloses = []
		self.tcklen = 0
		self.ticker = None
		if ticker != None:
			self.load(ticker)
	
	def load(self,ticker):
		self.loadfull(cfg.dir_downloaded + '/' + ticker.upper() + '.mst')
		
	def loadfull(self,tickerfull):
		try:
			tckfile = open(tickerfull)
			for line in tckfile.readlines():
				if line[0] != '<':
					x = line.rstrip().split(',')
					self.tcklist.append(x)
					self.lcloses.append(float(x[5]))
			tckfile.close()
			self.tcklist.reverse()
			self.tcklen = len(self.tcklist)
			self.lcloses.reverse()
			self.ticker = self.get(0)[0]
			log("ticker "+self.ticker+" successfuly loaded "+self.getdate(0))
		except Exception as e:
			log("opening ticker " + tickerfull +" FAILED: "+e.message)
	
	def empty(self):
		return self.tcklen == 0
	
	def get(self,i):
		return self.tcklist[i]
	
	def getc(self,i):
		return self.lcloses[i]
	
	def getdate(self,i=0):
		data = str(self.tcklist[i][1])
		return data[0:4]+'-'+data[4:6]+'-'+data[6:8]
	
	def sma(self,size,pos=0):
		if pos >= 0 and self.tcklen > pos+size:
			return sum(self.lcloses[pos:pos+size])/size
		else:
			return -1.0
	
	def dvc(self,i,val):
		return (self.lcloses[i]-val)/self.lcloses[i]
	

def print_answers(out,tn):
	n = len(out)
	prout = []
	print ''
	while len(out) > 0:
		y = out[0]
		ile = out.count(y)
		p = float(ile) / float(n) * 100.0
		pr = str(p) + '%' + ' ' + tn.printable_from_sk([y])
		print pr
		while ile > 0:
			out.remove(y)
			ile = out.count(y)

from sklearn.externals import joblib
def test_ticker(filename, deep, pr, noftests, nofchecks):
	cfg.is_debug = False
	try:
		tn = tr.TrainedNet(filename)
		out = []
		besty = 0
		bestn = None
		for i in range(noftests):
			y = tn.train(deep, pr)
			out.append(y[0])
			if nofchecks > 0:
				acc = tn.testset(nofchecks,True)
				if acc > besty:
					besty = acc
					bestn = i
					joblib.dump(tn.clf_svc, '../tmp/clf.pkl', compress=9)
		out.sort()
		print_answers(out,tn)
		if bestn != None:
			tn.clf_svc = joblib.load('../tmp/clf.pkl')
			y = tn.printable_from_sk(tn.predict_svc())
			print 'best predictor nr',str(bestn),':',y
	except Exception as e:
		print 'error',e.message 
	print ''

def test_tickers():
	tickers = ['08octava', 'agora', 'decora', 'wadex', 'swig80']
	for t in tickers:
		test_ticker(t,0, 50, 10)
