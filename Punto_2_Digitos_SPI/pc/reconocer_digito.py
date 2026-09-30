import argparse, cv2, numpy as np, serial, time
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument("--port",default="COM5")
parser.add_argument("--sin-esp",action="store_true")
parser.add_argument("--model",default="modelo_mnist_cnn.h5")
args=parser.parse_args()
esp=None if args.sin_esp else serial.Serial(args.port,115200,timeout=.1)
modelo=None
try:
    from tensorflow.keras.models import load_model
    if Path(args.model).exists(): modelo=load_model(args.model)
except Exception: pass

cam=cv2.VideoCapture(0)
ultimo=None
print("q: salir. Si no hay modelo, teclas 0-9 permiten probar el enlace.")
while True:
    ok,frame=cam.read()
    if not ok: break
    h,w=frame.shape[:2]; s=min(h,w)//2
    x1=w//2-s//2; y1=h//2-s//2
    roi=frame[y1:y1+s,x1:x1+s]
    gris=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
    blur=cv2.GaussianBlur(gris,(5,5),0)
    bw=cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,11,4)
    cont,_=cv2.findContours(bw,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    pred=None; conf=0
    if cont:
        c=max(cont,key=cv2.contourArea)
        if cv2.contourArea(c)>500:
            x,y,ww,hh=cv2.boundingRect(c); dig=bw[y:y+hh,x:x+ww]
            lado=max(ww,hh)+20; sq=np.zeros((lado,lado),np.uint8)
            ox=(lado-ww)//2; oy=(lado-hh)//2; sq[oy:oy+hh,ox:ox+ww]=dig
            img=cv2.resize(sq,(28,28),interpolation=cv2.INTER_AREA)
            if modelo is not None:
                pr=modelo.predict(img.reshape(1,28,28,1)/255.0,verbose=0)[0]
                pred=int(np.argmax(pr)); conf=float(np.max(pr))
                cv2.putText(frame,f"Numero: {pred} ({conf*100:.1f}%)",(20,35),0,1,(0,255,0),2)
                if conf>.80 and pred!=ultimo and esp:
                    esp.write(f"DIG:{pred}\n".encode()); ultimo=pred
    cv2.rectangle(frame,(x1,y1),(x1+s,y1+s),(0,255,0),2)
    cv2.imshow("Reconocimiento de digitos",frame)
    k=cv2.waitKey(1)&0xff
    if k==ord('q'): break
    if ord('0')<=k<=ord('9') and esp:
        d=k-ord('0'); esp.write(f"DIG:{d}\n".encode()); ultimo=d
cam.release(); cv2.destroyAllWindows()
