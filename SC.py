import cv2
from deepface import DeepFace


def face_comparison(img_1,img_2):
    
    result = DeepFace.verify(img1_path = img_1, img2_path = img_2, enforce_detection=False)
    
    if result.get('verified'):
        print(result)
        cv2.imwrite("q.png", img_1)
def face_capture():
    cascade_path = 'haarcascade_frontalface_default.xml'
    i=0
    clf = cv2.CascadeClassifier(cascade_path)
    camera = cv2.VideoCapture('V.mp4')
    
    while True:
        logic, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        faces = clf.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=10,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        for (x, y, width, height) in faces:
            cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 255, 0), 2)
            crop_img = frame[y:y+height, x:x+width]
            #cv2.imshow("cropped", crop_img)
            cv2.imshow('Faces', frame)
            #cv2.imwrite(str(i)+".png", crop_img)
            #image = cv2.imread("30.png")
            
            
        if cv2.waitKey(1) == ord('q'):
            break
        
    camera.release()
    cv2.destroyAllWindows()


def main():
    #face_comparison('w2.png',"w1.png")
    #face_capture()
    objs = DeepFace.analyze(img_path = "30.png", 
 actions = ['age', 'gender', 'race', 'emotion']
)
    print(objs)
    
if __name__ == '__main__':
    main()
