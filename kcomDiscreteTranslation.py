from PIL import Image
from kcom import ocr_space_file
import json
from googletrans import Translator
import kcomConfig


def cuttingBoard(imageName,area=(300,500,525,650)):
	#-crop image to text area
	#-sendImageforTextScanning
	#-SendtoTranslator
	img = Image.open(imageName)
	cropped_img = img.crop(area)
	croppedName = imageName.split("/")[0]+"/"+'trimmed'+imageName.split("/")[1]
	cropped_img.save(croppedName)
	
	ocrResponse = ocr_space_file(croppedName,False,kcomConfig.key,kcomConfig.lang)
	ocrJson = json.loads(ocrResponse)
	inputText = ocrJson['ParsedResults'][0]['ParsedText']
	
	translator = Translator()
	outputText = translator.translate(inputText,src=kcomConfig.src,dest=kcomConfig.dest)
	print(outputText.text)
	return outputText.text
		
