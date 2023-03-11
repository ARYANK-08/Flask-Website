import cv2
import datetime
import imutils
import numpy as np
from centroidtracker import CentroidTracker





protopath="MobileNetSSD_deploy.prototxt"
modelpath="MobileNetSSD_deploy.caffemodel"
detector=cv2.dnn.readNetFromCaffe(prototxt=protopath,caffeModel=modelpath)


tracker=CentroidTracker(maxDisappeared=80,maxDistance=90)

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor"]

class Final(object):

    def non_max_supression_fast(self,boxes,overlapThresh):
        try:
            if len(boxes)==0:
                return[]
            if boxes.dtype.kind=="i":
                boxes=boxes.astype("float")

            pick=[]
            x1=boxes[:,0]
            y1=boxes[:,1]
            x2=boxes[:,2]
            y2=boxes[:,3]

            area=(x2-x1+1)*(y2-y1+1)
            idxs=np.argsort(y2)

            while len(idxs)>0:
                last=len(idxs)-1
                i=idxs[last]
                pick.append(i)
                xx1=np.maximum(x1[i],x1[idxs[:last]])
                yy1=np.maximum(y1[i],y1[idxs[:last]])
                xx2=np.minimum(x2[i],y2[idxs[:last]])
                yy2=np.minimum(y2[i],y2[idxs[:last]])

                w=np.maximum(0,xx2-xx1+1)
                h=np.maximum(0,yy2-yy1+1)

                overlap=(w*h)/area[idxs[:last]]
                idxs=np.delete(idxs,np.concatenate(([last],
                                                    np.where(overlap>overlapThresh)[0])))

            return boxes[pick].astype("int")
        except Exception as e:
            print("Exception occurred in non_max_suppression:{}".format(e))


    def main3(self) :
        cap=cv2.VideoCapture(0)
        fps_start=datetime.datetime.now()
        fps=0
        total_frame3s=0
        lpc_count=0
        opc_count=0
        object_id_list=[]

        while True:
            self.ret, frame3= cap.read()
            frame3=imutils.resize(frame3,width=600)
            total_frame3s=total_frame3s+1


            (H,W)=frame3.shape[:2]

            blob=cv2.dnn.blobFromImage(frame3,0.007843,(W,H),127.5)
            detector.setInput(blob)
            person_detections=detector.forward()


            rects=[]

            for i in np.arange(0,person_detections.shape[2]):
                confidence=person_detections[0,0,i,2]
                if confidence>0.5:
                    idx=int(person_detections[0,0,i,1])

                    if CLASSES[idx] !="person":
                        continue

                    person_box= person_detections[0,0,i,3:7] * np.array([W,H,W,H])
                    (startX,startY,endX,endY)=person_box.astype("int")
                    rects.append(person_box)
            boundingboxes=np.array(rects)
            boundingboxes=boundingboxes.astype(int)
            rects=self.non_max_supression_fast(boundingboxes,0.3)

            
            objects = tracker.update(rects)
            for (objectId,bbox) in objects.items():
                x1,y1,x2,y2=bbox
                x1=int(x1)
                y1=int(y1)
                x2=int(x2)
                y2=int(y2)


                cv2.rectangle(frame3,(x1,y1),(x2,y2),(0,255,0),2)
                text="ID:{}".format(objectId)
                cv2.putText(frame3,text,(x1,y1-5),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),1)
                
                if objectId not in object_id_list:
                    object_id_list.append(objectId)


            fps_and_time=datetime.datetime.now()
            time_diff=fps_and_time - fps_start
            if time_diff.seconds==0:
                fps=0.0
            else:
                fps=(total_frame3s/time_diff.seconds)

            fps_text="FPS:{:.2f}".format(fps)

            cv2.putText(frame3,fps_text,(5,30),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
            
            
            lpc_count=len(objects)
            opc_count=len(object_id_list)
            lpc_txt="LIVE COUNT: {}".format(lpc_count)
            opc_txt="TOTAL COUNT:{}".format(opc_count)
            cv2.putText(frame3,lpc_txt,(5,60),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
            cv2.putText(frame3,opc_txt,(5,90),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        
            self.ret, buffer = cv2.imencode('.jpg', frame3)
            final_frame3 = buffer.tobytes()
            return (final_frame3)
