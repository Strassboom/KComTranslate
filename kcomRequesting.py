import requests
import kcomConfig
from bs4 import BeautifulSoup
import base64
import os
import googletrans

def downloadImages(masterUrl,srcList,destinationFolder):
	filenameList = []
	os.makedirs(destinationFolder,exist_ok=True)
	for image_link in srcList:
		image_content = requests.get(masterUrl+image_link).content
		filename = "{}/{}".format(destinationFolder,image_link.split("/")[-1])
		with open(filename,"wb+") as f:
			f.write(image_content)
		filenameList.append(filename)
	return filenameList

def getImage():
	response = requests.get("https://toonkor.moe/새디스틱_뷰티_50화.html")
	soup = BeautifulSoup(response.content,"html.parser")
	# Finds the script tag hodling the encoded comic image tags
	search = soup.find_all("script")
	for item in search:
		if "var toon_img = " in item.text[:26]:
			#print(item)
			image_string = item.text.split(";")[0].split('''var toon_img = ''')[1]
			break
	# Decodes and formats the string of image tags to be parsable by BeautifulSoup
	decoded_image_string = base64.b64decode(image_string).decode("utf8").replace('\'','\"')
	newSoup = BeautifulSoup(decoded_image_string,'html.parser')
	# Finds the source images for each comic page in the current webpage
	search = newSoup.find_all("img")
	srcList = []
	for item in search:
		srcList.append(item["src"])
	destinationFolder = googletrans.Translator().translate(soup.title.text).text.replace(" ","_")
	filetracks = downloadImages("https://toonkor.moe",srcList,destinationFolder)
	print(filetracks)

def ocr_space_file(filename, overlay=False, api_key="Hello", language="kor"):
	""" OCR.space API request with local file.
	Python3.5 - not tested on 2.7
	:param filename: Your file path & name.
	:param overlay: Is OCR.space overlay required in your response.
	Defaults to False.
	:param api_key: OCR.space API key.
	Defaults to 'helloworld'.
	:param language: Language code to be used in OCR.
	List of available language codes can be found on https://ocr.space/OCRAPI
	Defaults to 'en'.
	:return: Result in JSON format.
	"""
	
	payload = {'isOverlayRequired': overlay,
	'apikey': api_key,
	'language': language,
	}
	with open(filename, 'rb') as f:
		r = requests.post('https://api.ocr.space/parse/image',
		files={filename: f},
		data=payload,
		)
	return r.content.decode()
	
	
def ocr_space_url(url, overlay=False, api_key="Hello", language="kor"):
	""" OCR.space API request with remote file.
	Python3.5 - not tested on 2.7
	:param url: Image url.
	:param overlay: Is OCR.space overlay required in your response.
	Defaults to False.
	:param api_key: OCR.space API key.
	Defaults to 'helloworld'.
	:param language: Language code to be used in OCR.
	List of available language codes can be found on https://ocr.space/OCRAPI
	Defaults to 'en'.
	:return: Result in JSON format.
	"""
	
	payload = {'url': url,
	'isOverlayRequired': overlay,
	'apikey': api_key,
	'language': language,
	}
	r = requests.post('https://api.ocr.space/parse/image',
	data=payload,
	)
	return r.content.decode()
	
	
# Use examples:
# test_file = ocr_space_file(filename='example_image.png', language='pol')
# test_url = ocr_space_url(url='http://i.imgur.com/31d5L5y.jpg')

