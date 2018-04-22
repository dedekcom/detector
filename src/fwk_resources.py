import urllib, os, glob, zipfile
from tool_logger import log
import tool_cfg as cfg

# public API


def download_tickers():
	path = cfg.getcfg("ticker_src")
	file_tickers = cfg.getcfg("ticker_gpw")
	try:
		file_name, msg = download_rsrc(path, file_tickers)
		lista = str(msg).split()
		content_type = "Content-Type:"
		app_zip = "application/zip"
		if lista.count(content_type)==0 or lista[lista.index(content_type)+1]!=app_zip:
			log("Downloaded file has Content-Type: "+lista[lista.index(content_type)+1]+" and is different than "+app_zip)
			return 0
		
		del_files_from_dir(cfg.dir_downloaded, "*.mst")
		unzip_file(cfg.dir_downloaded, file_tickers)
		del_files_from_dir(cfg.dir_tmp, file_tickers)
		return 1
	except Exception as e:
		log("downloading tickets FAILED: "+e.message)
		return 0

def get_tickers():
	return get_files(cfg.dir_downloaded, "*.mst")

def clean_dirs():
	del_files_from_dir(cfg.dir_downloaded, "*")
	del_files_from_dir(cfg.dir_tmp, "*")

# private 

def get_files(dir_name, files_pattern):
	return glob.glob(dir_name + "/" + files_pattern)

def download_rsrc(rsrc_address, file_name):
	log("downloading zip file")
	return urllib.urlretrieve(rsrc_address + "/" + file_name, cfg.dir_tmp + "/" + file_name)


def del_files_from_dir(dir_name, files_pattern):
	log("deleting " + files_pattern + " from "+dir_name)
	for f in get_files(dir_name, files_pattern):
		os.remove(f)
	
def unzip_file(dst_dir, file_name):
	log("unziping file "+file_name+" from "+cfg.dir_tmp+" to "+dst_dir)
	zfile = zipfile.ZipFile(cfg.dir_tmp + "/" + file_name)
	zfile.extractall(dst_dir)
	zfile.close()
