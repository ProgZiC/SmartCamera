#!/usr/bin/python
import cv2
import dlib
import argparse 
import os
import face_recognition
import time
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



def face_comparison(img_1,img_2):
    
    known_image = face_recognition.load_image_file("img_1.jpg")
    unknown_image = face_recognition.load_image_file("img_2.jpg")

    biden_encoding = face_recognition.face_encodings(known_image)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

    results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
    return results
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
            if face_comparison(name,name_2)==1:
                names_picture.remove(name_2)
            else:
                pass
              
    print(db_dict)
             

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
            cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 255, 0), 2)
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
    input_database_slow()
    #print(face_comparison("2.jpg","1.jpg"))

    #face_capture_with_s(namespace.k,namespace.indir)

    #objs = DeepFace.analyze(img_path = "30.png", 
    #actions = ['age', 'gender', 'race', 'emotion'])
    #print(objs)
    
if __name__ == '__main__':
    main()
