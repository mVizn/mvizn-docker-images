import cv2
import os
import time

class YOLO:
    def __init__(self,weightsfile,cfgfile=None,namesfile=None,size=None):
        if cfgfile is None:
            cfgfile=weightsfile[:-len('.weights')]+'.cfg'
        if namesfile is None:
            namesfile=weightsfile[:-len('.weights')]+'.names'
        cfg=dict()
        for line in open(cfgfile):
            if '#' in line:continue
            try:
                k,v=line.strip().split('=')[:2]
                cfg[k]=v
            except:
                pass
        if size is None:
            size=(int(cfg['width']),int(cfg['height']))
        self.net=cv2.dnn.readNet(weightsfile, cfgfile)
        self.classes=open(namesfile).read().rstrip().split('\n')
        print("Classes..", self.classes)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        self.model = cv2.dnn_DetectionModel(self.net)
        self.model.setInputParams(size=size, scale=1/255)
    def infer(self, frame, CONFIDENCE_THRESHOLD=0.2, NMS_THRESHOLD=0.4):
        classes, scores, boxes = self.model.detect(frame, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)
        classes = list(self.classes[i] for i in classes)
        scores = list(score for score in scores)
        return classes, scores, boxes
    def inferold(self, frame, thresh=0.2):
        classes, scores, boxes = self.infer(frame, thresh)
        results = []
        for (classid, score, box) in zip(classes, scores, boxes):
            result=['',0,[0,0,0,0]]
            result[0]=classid
            result[1]=score
            box[0]=box[0]+box[2]/2
            box[1]=box[1]+box[3]/2
            result[2]=box
            results.append(result)
        return results


def yolodraw(im,yolo):
    res=yolo.infer(im)
    for label,prob,box in zip(*res):
        cv2.rectangle(im,box,color=rainbowbgr[yolo.classes.index(label)%7],thickness=2)
        #putText(im,f'{prob:0.2f}',(box[0],box[1]),shadow=True)
        cv2.putText(im,f'{label}',(box[0],box[1]),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1)
    return res

rainbowbgr=[(0, 0, 255),
 (0, 165, 255),
 (0, 255, 255),
 (0, 128, 0),
 (255, 0, 0),
 (130, 0, 75),
 (238, 130, 238),
 (128, 128, 128),
 (255, 255,255),
]
print("Loading weights...\n")
yolo=YOLO('/weights/QCgantry.weights')

def infer(imgpath):
    image = cv2.imread(imgpath)
    res = yolodraw(inimage, yolo)
    cv2.imwrite(image)

def main():

    in_dir = "/dev/shm/dockerinput"
    out_dir = "/dev/shm/dockeroutput"

    if not os.path.exists(in_dir):
        os.makedirs(in_dir)
        print(f"Created directory: {in_dir}")
    #os.chmod(in_dir, 0o777)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        print(f"Created directory: {out_dir}")
    #os.chmod(out_dir, 0o777)

    while True:
        # Iterate over the files in the input directory.
        for filename in os.listdir(in_dir):
            filepath = os.path.join(in_dir, filename)
            print("Found..", filepath, "\n")
            outfilepath = os.path.join(out_dir, filename)
            image = cv2.imread(filepath)
            res = yolodraw(image, yolo)
            print(res)
            print("Writing..", outfilepath, "\n")
            cv2.imwrite(outfilepath, image)
            os.remove(filepath)
            print("Deleted..", filepath, "\n")
        print("sleeping .. \n")
        time.sleep(1)


if __name__ == "__main__":
    main()
