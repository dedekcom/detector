import numpy as np
import json

class Neuron:
	def __init__(self,ntype = 1):
		self.nvalue = 0.0
		self.synapses = []
		self.activation_func = ntype
	
	def activate_func(self,x):
		if self.activation_func == 1:
			return 1.0/(1.0+np.exp(-x))
		elif self.activation_func == 2:
			return np.tanh(x)
		else:
			return float(x)
	
	def drv_activate_func(self,x):
		if self.activation_func == 1:
			return x*(1.0-x)
		elif self.activation_func == 2:
			return 1 - x*x
		else:
			return 1.0
	
	def forward(self):
		v = 0.0
		for x in self.synapses:
			v += x.calc()
		self.nvalue = self.activate_func(v)
	
	def backward(self,err):
		delta = err * self.drv_activate_func(self.nvalue)
		for x in self.synapses:
			x.neuron.backward(delta * x.svalue)
			x.update(delta)
	
	def set_prev_layer(self,l):
		for x in l:
			self.synapses.append(Synapse(x))
	
	def synapses_to_list(self):
		s = []
		for x in self.synapses:
			s.append(x.svalue)
		return s
	
	def set_synapses(self,l):
		l.reverse()
		for x in self.synapses:
			x.svalue = l.pop()


class Synapse:
	def __init__(self,n):
		self.neuron = n
		self.svalue = 2.0 * np.random.random() - 1.0
	
	def calc(self):
		return self.neuron.nvalue * self.svalue
	
	def update(self, delta):
		self.svalue += delta * self.neuron.nvalue


class Net:
	def __init__(self,sizes = [],activ_func = 1, v_input = [], v_output = []):
		if len(v_input) > 0:
			sizes = [len(v_input[0])] + sizes
		if len(v_output) > 0:
			sizes = sizes + [len(v_output[0])]
		self.dim_neurons = []
		self.l_neurons = []
		self.build(sizes, activ_func)
	
	def build(self, sizes, activ_func):
		self.activation_func = activ_func
		self.dim_neurons = sizes
		prev = []
		i = 0
		for s in sizes:
			ls = []
			self.l_neurons.append([])
			for x in range(s):
				n = Neuron(activ_func)
				n.set_prev_layer(prev)
				self.l_neurons[i].append(n)
			prev = self.l_neurons[i]
			i += 1
	
	
	def set_input(self,xlist):
		i = 0
		for x in xlist:
			self.l_neurons[0][i].nvalue = x
			i += 1
	
	def calc(self,x):
		self.set_input(x)
		for neurons in self.l_neurons[1:]:
			for n in neurons:
				n.forward()
	
	def neurons_to_list(self,neurons):
		l = []
		for x in neurons:
			l.append(x.nvalue)
		return l
	
	def predict(self,x):
		self.calc(x)
		return self.neurons_to_list(self.l_neurons[-1])
	
	def learn(self,xarray, output, times):
		eps = 0.1
		for n in xrange(times):
			i = 0
			sumerr = 0.0
			for x in xarray:
				self.calc(x)
				j = 0
				for o in self.l_neurons[-1]:
					err = output[i][j]-o.nvalue
					o.backward(err)
					sumerr += abs(err)
					j += 1
				i += 1
			if n % 1000 == 0:
				print 'iteration : '+str(n)
			if sumerr < eps:
				print 'error',sumerr,'<',eps,'i =',n
				break
	
	def to_dic(self):
		o = {'dim:': self.dim_neurons, 'func:': self.activation_func}
		i = 0
		for neurons in self.l_neurons:
			n = []
			for x in neurons:
				n.append(x.synapses_to_list())
			o['layer'+str(i)] = n
			i += 1
		return o
	
	def from_dict(self,dic):
		self.build(dic['dim:'],dic['func:'])
		i = 1
		for neurons in self.l_neurons[1:]:
			s = dic['layer'+str(i)]
			s.reverse()
			for n in neurons:
				n.set_synapses(s.pop())
			i += 1
	
	def save(self, filename):
		d = self.to_dic()
		json.dump(d, open(filename,'w'))
	
	def load(self, filename):
		d = json.load(open(filename))
		self.from_dict(d)

def test1():
	X = np.array([[0,0,1],
		[0,1,1],
		[1,0,1],
		[1,1,1]])
	Y = np.array([[0],
		[1],
		[1],
		[0]])

	net = Net([4],1,X,Y)
	net.learn(X,Y,60000)
	
	print str(net.predict([0,0,1]))
	print str(net.predict([0,1,1]))
	print str(net.predict([1,0,1]))
	print str(net.predict([1,1,1]))
	print net.to_dic()
	
	dic_net2 = net.to_dic()
	net2 = Net()
	net2.from_dict(dic_net2)
	
	print ''
	print str(net2.predict([0,0,1]))
	print str(net2.predict([0,1,1]))
	print str(net2.predict([1,0,1]))
	print str(net2.predict([1,1,1]))
	
	net2.save('net2.json')


def test2():
	X = np.array([[0,0],
		[0,1],
		[1,0],
		[1,1]])
	Y = np.array([[0],
		[0],
		[0],
		[1]])

	net = Net([2, 4, 1],2)
	net.learn(X,Y,60000)
	print str(net.predict([0,0]))
	print str(net.predict([0,1]))
	print str(net.predict([1,0]))
	print str(net.predict([1,1]))

def test3():
	net3 = Net()
	net3.load('net2.json')
	print ''
	print str(net3.predict([0,0,1]))
	print str(net3.predict([0,1,1]))
	print str(net3.predict([1,0,1]))
	print str(net3.predict([1,1,1]))
	print net3.to_dic()

#test3()
