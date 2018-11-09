from PIL import Image
import face_recognition
import os
import numpy as np
import cv2 
import pickle

class Face_Recognition:
    def __init__(self,data_folder_path):
        self.data_folder_path = data_folder_path
        self.face_cascade = cv2.CascadeClassifier('opencv-files/lbpcascade_frontalface.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()

    
    def prepare_training_data(self):
        y_labels = []
        x_train = [] 
        labels_ids = {}
        image_names = os.listdir(self.data_folder_path)
        current_id = 0 

        for image_name in image_names:
            image_path = self.data_folder_path+ "/" + image_name
            if image_name in labels_ids:
                pass
            else:
                labels_ids[image_name] = current_id
                current_id += 1
            id_ = labels_ids[image_name]
            #print(image_name.split('.')[0],image_path)
            pil_image = Image.open(image_path).convert("L") #grayscale
            image_array = np.array(pil_image,"uint8") #convert to numpy array
            #print (image_array)
            faces = self.face_cascade.detectMultiScale(image_array, scaleFactor=1.2, minNeighbors=5)
            for (x,y,w,h) in faces:
                roi = image_array[y:y+h,x:x+w]
                x_train.append(roi)
                y_labels.append(id_)
        #print (labels_ids)

        with open("labels.pickle",'wb') as f:
            pickle.dump(labels_ids,f)
        self.recognizer.train(x_train,np.array(y_labels))
        self.recognizer.save("trainer.yml")
    
        
if __name__ == '__main__':
    faces = Face_Recognition("test-data")
    faces.prepare_training_data()