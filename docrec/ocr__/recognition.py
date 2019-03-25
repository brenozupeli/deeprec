import numpy as np
from pytesseract import image_to_string
from PIL import Image
from ..text.textprocessing import text2words
# http://www.nltk.org/howto/portuguese_en.html
# http://stanford.edu/~rjweiss/public_html/IRiSS2013/text2/notebooks/cleaningtext.html
# Run OCR
def image2text(image, language='en_US'):
   
    lang = {'en_US': 'eng', 'pt_BR': 'por'}[language]
    text = image_to_string(
        Image.fromarray(image.astype(np.uint8)), lang=lang
    ).encode('utf-8', 'ignore')
    return text


def image2words(image, language='en_US', min_length=3):
    
    return text2words(
        image2text(image, language=language),
        min_length=min_length
    )


def number_of_words(image, language='en_US', min_length=3):
   
    return len(image2words(image, language=language, min_length=min_length))
