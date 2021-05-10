import PyPDF2
import fitz
from PIL import Image
import os
import time

performanceData : dict = {0:1, 1:5}

def pixelCheck(img, width : int, height : int, step : int, maxPixels : int):
    pixelCounter : int = 0
    deletePage : bool = True
    for x in range (0,width,step):
        for y in range (0,height,step):
            r,g,b = img.getpixel((x,y))
            if (not((abs(r-b) <= 5) and (abs(r-g) <= 5) and (abs(b-g) <=5) and (min(r,g,b) > 235))):
                pixelCounter +=1
                if pixelCounter > maxPixels:
                    deletePage = False
    return deletePage

def process(fileName : str, uploadPath : str, downloadPath : str, imagePath : str, threshold : float, performance : int):
    startTime : float = time.time()
    stats : dict = {
        "removed": 0,
        "ttime": 0,
        "oldfsize": 0,
        "newfsize": 0
        }

    dirname = os.path.dirname(__file__)
    file = open(os.path.join(dirname, uploadPath + fileName), 'rb')
    reader = PyPDF2.PdfFileReader(file)

    n : int = reader.numPages
    step : int = performanceData[performance]
    doc = fitz.open(uploadPath + fileName)
    pagesToKeep : list = list(range(n))

    for i in range (n):
        page = doc.loadPage(i)
        pix = page.getPixmap()
        output = imagePath + "img%d.png" % (i) 
        pix.writePNG(output)
        img = Image.open(imagePath + "img%d.png" % (i)) 
        size = img.size
        width, height = size
        totalPixels = width * height
        
        maxPixels = (threshold * totalPixels) / step

        if pixelCheck(img, width, height, step, maxPixels):
            pagesToKeep.remove(i)
            stats["removed"]+=1
        os.remove(imagePath + "img%d.png" % (i))     
                        
    if len(pagesToKeep) == 0:
        return -1
    else:
        writer1 = PyPDF2.PdfFileWriter()
        
        for i in pagesToKeep:
            x = reader.getPage(i)
            writer1.addPage(x)

        with open (downloadPath + 'fixed_' + fileName, 'wb') as f:
            writer1.write(f)

    endTime = time.time()
    
    stats["ttime"] = round(endTime - startTime, 2)
    stats["oldfsize"] = round((os.stat(uploadPath + fileName).st_size) / 1000000, 3)
    stats["newfsize"] = round((os.stat(downloadPath + 'fixed_' + fileName).st_size) / 1000000, 3)
    return stats
    
    

    
    

    















