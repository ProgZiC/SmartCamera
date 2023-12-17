import cv2
from deepface import DeepFace


def face_comparison(img_1,img_2):
    
    result = DeepFace.verify(img1_path = img_1, img2_path = img_2)
    
    if result.get('verified'):
        return 1
    else:
        return 0
        #cv2.imwrite("q.jpg", img_1) // запись изображения

def face_capture_with_s():
    cascade_path = 'haarcascade_frontalface_default.xml' # датасет
    clf = cv2.CascadeClassifier(cascade_path) 
    camera = cv2.VideoCapture('V.mp4') # источник потока
    
    i=0
    while True:
        logic, frame = camera.read()
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) // перевод картинки в серое 
        
        faces = clf.detectMultiScale(
            frame,
            scaleFactor=1.1,
            minNeighbors=20,
            minSize=(25, 25),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        for (x, y, width, height) in faces:
            cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 255, 0), 2)
            crop_img = frame[y:y+height, x:x+width]
            cv2.imshow("cropped", crop_img)
            #cv2.imshow('Faces', frame)

            cv2.imwrite(str(i)+".jpg", crop_img)
            #image = cv2.imread("30.png")
            i+=1
            
        if cv2.waitKey(1) == ord('q'):
            break
        
    camera.release()
    cv2.destroyAllWindows()


def main():
    #print(face_comparison("2.jpg","1.jpg"))
    face_capture_with_s()
    #objs = DeepFace.analyze(img_path = "30.png", 
    #actions = ['age', 'gender', 'race', 'emotion'])
    #print(objs)
    
if __name__ == '__main__':
    main()
