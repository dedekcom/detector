import re
import json

dir_tmp = "../tmp"
dir_data = "../data"
dir_downloaded = dir_data + "/downloaded"
dir_saved = dir_data + "/saved"
dir_html = "../html"

config_path = "../rsrc/config.cfg"
cfgdic = {}

itf_path = "../rsrc/interface.json"

def reloadcfg():
	config_file = open(config_path)
	cfg_list = config_file.readlines()
	config_file.close()
	for line in cfg_list:
		if re.search("^[a-zA-Z0-9_]+:",line):
			l = line.split()
			if len(l[1:])>0:
				cfgdic[l[0][:-1]] = l[1:]

def getcfgl(key):
	if not cfgdic:
		reloadcfg()
	return cfgdic[key]

def igetcfgl(key):
	return map(lambda n: int(n), getcfgl(key))

def fgetcfgl(key):
	return map(lambda n: float(n), getcfgl(key))

def getcfg(key,pos=0):
	return list (getcfgl(key))[pos]

def loaditf():
	return json.load(open(itf_path))

