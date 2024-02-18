#!/usr/bin/python
import cv2
from deepface import DeepFace
import argparse 
import os
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
##############################################################################################
parser = argparse.ArgumentParser(description='options')
parser.add_argument(
    '-k',
    type=int,
    default=20,
    help='provide an integer (default: 20)'
)
parser.add_argument(
    '-s', action='store_true'
)
parser.add_argument(
    '-c', action='store_true'
)
#parser.add_argument('indir', type=str, help='Input dir for videos')
namespace = parser.parse_args()
#print(namespace.s)

###############################################################################################
def variance_of_laplacian(image):
    # Вычисление дисперсии Лапласа
	return cv2.Laplacian(image, cv2.CV_64F).var()
def blur(img):
    # Определение размытости изображения
    image = cv2.imread(img,cv2.IMREAD_GRAYSCALE)
    fm = variance_of_laplacian(image)
    text = "Not Blurry"
    if fm < 500:
        text = "Blurry"
    return text
def delete():
    # Удаление размытых изображений
    names_picture=os.listdir()
    for n in names_picture:
        if blur(n) == "Blurry":
            os.remove(n)

def face_comparison(img_1,img_2):
    img1= cv2.imread(img_1)
    img2= cv2.imread(img_2)

    output = DeepFace.verify(img_1,img_2,model_name=models[2])
    verification = output['verified']
    if verification:
       return 1
    else:
       return 0
    
def data_structure_slow():
    delete()
    db_dict={}
    names_picture=os.listdir()
    i=0
    k=0
    for name in names_picture:
        k+=1
        db_dict[k]=[name]
        for name_2 in names_picture:
            try:
                if face_comparison(name,name_2)==1:
                    names_picture.remove(name_2)
                    db_dict[k].append(name_2)
                else:
                    pass
            except ValueError:
                names_picture.remove(name_2)
    print(db_dict)
    return db_dict

def analyze_list(dict):
    genders=[]
    for key in dict.keys():
        w=0
        m=0
        for k in dict.get(key):
            objs = DeepFace.analyze(img_path = k, 
        actions = ['gender'])
            print(objs[0]["gender"])
            if objs[0]["gender"]["Woman"] > objs[0]["gender"]["Man"]:
                gender = 'Woman'
                w+=1
            else:
                gender = 'Man'
                m+=1
        if m > w:
            genders.append('Man')
        else:
            genders.append('Woman')
    return genders

def analyze_item(k):
    objs = DeepFace.analyze(img_path = k, 
        actions = ['gender'])
    if objs[0]["gender"]["Woman"] > objs[0]["gender"]["Man"]:
        gender = 'Woman'
    else:
        gender = 'Man'
    return gender

def input_database(gender,dict):
    m=0
    os.chdir('..')
    file = open("stat.txt", "w")
    for i in range(1,len(gender)+1):
        print(str(i)+':'+str(gender[i-1])+':'+str(dict[i]))
        if str(gender[i-1]) == "Man":
            m+=1
        file.write(str(i)+':'+str(gender[i-1])+':'+str(dict[i]))
    file.write( 'Man: '+str((m/len(gender)) * 100 )+'% Woman: '+str(((m-len(gender))/len(gender)) * 100 ) + '%')
    file.close()

def face_capture_with_s(k):
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
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #  перевод картинки в серое 
        faces = clf.detectMultiScale(                  # обнаружение лиц на фото
            frame,
            scaleFactor=1.1,
            minNeighbors=k,
            minSize=(50, 50),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        for (x, y, width, height) in faces:
            cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 255, 0), 0) # вырез прямоугольник лица
            crop_img = frame[y:y+height, x:x+width]
            
            os.chdir(path+'\\Saved_frames')
            
            named_tuple = time.localtime() # получить struct_time
            time_string = time.strftime("%m%d%Y-%H%M%S", named_tuple)

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
            #cv2.imshow("cropped", crop_img)
            cv2.imshow('Faces', frame) # вывод фрейма с прямоугольником
        if cv2.waitKey(1) == ord('q'):
            break    

    camera.release()
    cv2.destroyAllWindows()

def main():
    if namespace.c == True and namespace.s == False:
        face_capture_with_s(namespace.k)
    elif namespace.s == True and namespace.c == False:
        path=os.getcwd()
        os.chdir(path+'\\Saved_frames')
        data=data_structure_slow()
        input_database(analyze_list(data),data)
    elif namespace.s == True and namespace.c == True:
        face_capture_with_s(namespace.k)
        data=data_structure_slow()
        input_database(analyze_list(data),data)
if __name__ == '__main__':
    main()
