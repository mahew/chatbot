import tkinter as tk
from tkinter import filedialog
import tensorflow as tf
import tensorflow.keras as keras
import numpy as np

##############################################################################
img_height = 256
img_width = 256
cnn_model = tf.keras.models.load_model('chatbot_model.h5')
class_names = ['beer', 'cocktail', 'wine']
##############################################################################

def classify():
    root = tk.Tk()
    root.withdraw()        
    file_path = filedialog.askopenfilename()
    root.lift()
    
    img = keras.preprocessing.image.load_img(
        file_path, target_size=(img_height, img_width)
    )
    
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    
    predictions = cnn_model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    confidence = 100 * np.max(score)
    
    replys = []

    if confidence < 70:
        replys.append("I'm not very sure what this is, sorry! Try ask me what something else is")
    else:
        class_response = "This image is most likely a {} I have {:.2f} percent confidence in my predicion.".format(class_names[np.argmax(score)], confidence)
        replys.append(class_response)
    
    replys.append("Anything else you would like to know?")
    
    return replys