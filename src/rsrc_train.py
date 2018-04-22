import fwk_ticker as tck
import fwk_neural as nn
import tool_cfg as cfg
from tool_logger import log
import numpy as np
from sklearn import svm
from sklearn import base

class TrainedNet:
	def __init__(self, filename=None):
		self.ticker = None
		
		self.neuralnet = None
		self.savednet = None
		
		self.clf_svc = None
		
		self.predicted = 3
		self.smas = cfg.igetcfgl('smas')
		self.prparts = cfg.fgetcfgl('out_class2')
		
		
		self.load(filename)
	
	def load(self, filename):
		self.ticker = tck.Ticker(filename)
		if not self.ticker.empty():
			self.savednet = cfg.dir_saved + '/' + filename.upper() + '_net.json'
	
	def setoutput(self,outputvec):
		self.prparts = outputvec
	
	def price_output(self, price, pricelater):
		diff = self.price_chg(price, pricelater)
		l = len(self.prparts)
		out = [0] * (l+1)
		if diff >= self.prparts[-1]:
			pos = l
		else:
			obj = next((x for x in self.prparts if diff < x), 0)
			pos = self.prparts.index(obj)
		out[pos] = 1
		return out
	
	def printable_output(self, net_out):
		# print net_out
		i = net_out.index(max(net_out))
		s = self.ticker.ticker + ' for ' + str(self.predicted) + ' ses: '
		if i == len(self.prparts):
			s += '> '+str(self.prparts[-1])
		elif i == 0:
			s += '< '+str(self.prparts[0])
		else:
			s += str(self.prparts[i-1]) + ':' + str(self.prparts[i])
		return s
	
	def print_output(self, net_out):
		print self.printable_output(net_out)
	
	def printable_from_sk(self, skout):
		y = [0] * (len(self.prparts)+1)
		y[skout[0]] = 1
		return self.printable_output(y)
	
	def price_chg(self, pricefrom, priceto):
		return (float(priceto) - float(pricefrom))/float(pricefrom) * 100.0
	
	def calcsmas(self, date):
		x = []
		price = self.ticker.getc(date)
		for sma in self.smas:
			sprice = self.ticker.sma(sma, date)
			x.append( self.price_chg(sprice, price) )
		return np.array(x)
	
	def predict(self):
		out = self.neuralnet.predict( self.calcsmas(0) )
		yl = []
		for y in out:
			yy = int(y*100)
			yl.append( float(yy)/100.0 )
		return yl
	
	def output_to_skl(self, Y):
		aY = []
		for y in Y:
			aY.append(y.index(1))
		return np.array(aY)
	
	def get_input_dates(self,deep=0,samples=0):
		if deep<=0 or deep > self.ticker.tcklen:
			deep = int(0.8 * self.ticker.tcklen)
		if samples==0:
			samples = deep/2
		last = self.smas[0]
		size = self.predicted + samples + last
		if size >= deep:
			log("history is too short: "+str(deep)+" for ticker "+self.ticker.ticker)
			return []
		return np.random.random_integers(self.predicted, deep - self.predicted - last, samples)
		
	
	def train(self, deep=0, predict_fut=3):
		if(self.savednet == None):
			log("no ticker")
			return []
		self.predicted = predict_fut
		dates = self.get_input_dates(deep)
		#log("dates to train: "+str(dates))
		X = []
		Y = []
		#log("building training set from smas: "+str(self.smas))
		for d in dates:
			X.append( self.calcsmas(d) )
			Y.append( self.calc_out(d) )
		aX = np.array(X)
		aY = self.output_to_skl(Y)
		
		self.clf_svc = svm.SVC(gamma=0.001, C=100.)
		self.clf_svc.fit(aX, aY)
		y = self.predict_svc(0)
		# print self.printable_from_sk(y)
		return y
	
		#self.neuralnet = nn.Net([len(Y[0])+2],1,X,Y)
		#self.neuralnet.learn(X,Y,5000)
		#self.neuralnet.save(self.savednet)
		#log("predicting future behaviour:")
		#self.printable_output( self.predict() )

	def clone_svc(self):
		return base.clone(self.clf_svc)

	def predict_svc(self,idate=0):
		return self.clf_svc.predict( np.array([self.calcsmas(idate)]) )
	
	def calc_out(self,idate):
		return self.price_output(self.ticker.getc(idate), self.ticker.getc(idate-self.predicted))

	def test(self,idate):
		real = self.output_to_skl([self.calc_out(idate)])
		pred = self.predict_svc(idate)
		return (real,pred)
	
	def sign(self,v):
		if v < 0:
			return -1
		elif v > 0:
			return 1
		else:
			return 0
	
	def testset(self, nofsamples, bonlydirect = False):
		dates = self.get_input_dates(samples = nofsamples)
		i = 0.0
		if bonlydirect:
			print 'up/down mode on'
		for d in dates:
			x = self.test(d)
			real = x[0].tolist()
			pred = x[1].tolist()
			x1 = self.printable_from_sk(real)
			x2 = self.printable_from_sk(pred)
			s = ''
			if real == pred or (bonlydirect and self.sign(self.prparts[real[0]-1])==self.sign(self.prparts[pred[0]-1])):
				i += 1.0
				s = 'ok'
			# print self.ticker.getdate(d),x1,x2,s
		acc = i/nofsamples*100.0
		print 'accuracy:',acc
		return acc
	