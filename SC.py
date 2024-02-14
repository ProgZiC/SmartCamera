#!/usr/bin/python
import cv2
from deepface import DeepFace
import argparse 
import os
from imutils import paths
import time
models = [
  "VGG-Face", 
  "Facenet", 
  "Facenet512", 
  "OpenFace", 
  "DeepFace", 
  "DeepID", 
  "ArcFace", 
  "Dlib", 
  "SFace",
]

parser = argparse.ArgumentParser(description='options')
parser.add_argument(
    '-k',
    type=int,
    default=20,
    help='provide an integer (default: 20)'
)
parser.add_argument('indir', type=str, help='Input dir for videos')
namespace = parser.parse_args()


#print(namespace.k)
#print(namespace.indir)
def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_64F).var()
def blur(img):
    image = cv2.imread(img,cv2.IMREAD_GRAYSCALE)
    #gray = cv2.cvtColor(image, cv2.IMREAD_GRAYSCALE)
    fm = variance_of_laplacian(image)
    text = "Not Blurry"
	# if the focus measure is less than the supplied threshold,
	# then the image should be considered "blurry"
    if fm < 500:
        text = "Blurry"
    return text
def delete():
    path=os.getcwd()
    os.chdir(path+'\\Saved_frames')
    names_picture=os.listdir()
    for n in names_picture:
        if blur(n) == "Blurry":
            os.remove(n)

def face_comparison(img_1,img_2):
    img1= cv2.imread(img_1)
    img2= cv2.imread(img_2)

    output = DeepFace.verify(img_1,img_2,model_name=models[1])
    #print(output)
    verification = output['verified']
    if verification:
       return 1
    else:
       return 0
def input_database_slow():
    db_dict={}
    path=os.getcwd()
    os.chdir(path+'\\Saved_frames')
    names_picture=os.listdir()
    i=0
    k=1
    for name in names_picture:
        db_dict[k]=[name]
        k+=1
        for name_2 in names_picture:
            try:
                if face_comparison(name,name_2)==1:
                    names_picture.remove(name_2)
                else:
                    pass
            except ValueError:
                names_picture.remove(name_2)
    print(db_dict)
def input_database():
    db_dict={}
    path=os.getcwd()
    os.chdir(path+'\\Saved_frames')
    names_picture=os.listdir()
    dfs = DeepFace.find(img_path = "02132024-195300_12.jpg", db_path = "C:/Users/user/Documents/SmartCamera")
    print(dfs)

def face_capture_with_s(k,url):
    cascade_path = 'haarcascade_frontalface_default.xml' # датасет
    
    clf = cv2.CascadeClassifier(cascade_path) 
   
    camera = cv2.VideoCapture(0) # источник потока
    fps = 20.0
    camera.set(cv2.CAP_PROP_FPS, fps)
    i=0

    path=os.getcwd()

    if not os.path.isdir("Saved_frames"):
                os.mkdir("Saved_frames")
    while True:
        logic, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # // перевод картинки в серое 
        
        faces = clf.detectMultiScale(
            frame,
            scaleFactor=1.1,
            minNeighbors=k,
            minSize=(25, 25),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        for (x, y, width, height) in faces:
            cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 255, 0), 0)
            crop_img = frame[y:y+height, x:x+width]
            
            os.chdir(path+'\\Saved_frames')
            
            named_tuple = time.localtime() # получить struct_time
            time_string = time.strftime("%m%d%Y-%H%M%S", named_tuple)
            print(time_string)
            
            print(os.listdir())
            try:
                os.listdir()[-1]
            except IndexError:
                 cv2.imwrite( time_string +'.jpg', crop_img)
            else:
                    
                if time_string in os.listdir()[-1]:
                    i+=1
                    cv2.imwrite( time_string+'_'+ str(i) +'.jpg', crop_img)
                else:
                    i=0
                    cv2.imwrite( time_string +'.jpg', crop_img)
            #os.rename('1.jpg',time_string+'.jpg')
            #cv2.imshow("cropped", crop_img)
            cv2.imshow('Faces', frame)

           
           
            #cv2.imwrite(str(named_tuple) +".png", crop_img)
           

            
            #image = cv2.imread("time_string.png")
            #i+=1
            
        if cv2.waitKey(1) == ord('q'):
            break
        
    camera.release()
    cv2.destroyAllWindows()


def main():
    #input_database_slow()
    #print(face_comparison("2.jpg","1.jpg"))
    #input_database()
    #face_capture_with_s(namespace.k,namespace.indir)
    #blur('02132024-195301_3.jpg')
    #objs = DeepFace.analyze(img_path = "30.png", 
    #actions = ['age', 'gender', 'race', 'emotion'])
    #print(objs)
    delete()
if __name__ == '__main__':
    main()
