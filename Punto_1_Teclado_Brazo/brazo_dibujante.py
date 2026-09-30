import argparse, time, math
import numpy as np
import cv2
import pybullet as p
import pybullet_data
import serial

parser=argparse.ArgumentParser()
parser.add_argument("--port",default="COM5")
parser.add_argument("--sin-serial",action="store_true")
args=parser.parse_args()

ser=None if args.sin_serial else serial.Serial(args.port,115200,timeout=.05)
p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.81)
p.loadURDF("plane.urdf")
robot=p.loadURDF("../../urdf/brazo.urdf",[0,0,0],useFixedBase=True)

lienzo=np.full((420,720,3),255,np.uint8)
font=cv2.FONT_HERSHEY_SIMPLEX

def dibujar(texto):
    global lienzo
    lienzo[:]=255
    cv2.putText(lienzo,texto,(60,260),font,5,(0,0,0),10,cv2.LINE_AA)
    # Movimiento visual de las articulaciones durante el "trazo"
    pasos=max(120,70*len(texto))
    for i in range(pasos):
        t=i/pasos
        q1=.75*math.sin(t*math.pi*2)
        q2=.55*math.sin(t*math.pi*4)
        q3=.05+.04*math.sin(t*math.pi*2)
        p.setJointMotorControl2(robot,0,p.POSITION_CONTROL,q1)
        p.setJointMotorControl2(robot,1,p.POSITION_CONTROL,q2)
        p.setJointMotorControl2(robot,2,p.POSITION_CONTROL,q3)
        p.stepSimulation()
        cv2.imshow("Pizarra",lienzo)
        cv2.waitKey(1)
        time.sleep(1/240)

print("Punto 1 listo. Teclado: escribe numero y #. Sin serial: escribe numero + Enter.")
while True:
    if ser:
        linea=ser.readline().decode(errors="ignore").strip()
        if linea.startswith("DRAW:"): dibujar(linea.split(":",1)[1])
        elif linea=="CLEAR": lienzo[:]=255
    else:
        texto=input("Numero (q sale): ").strip()
        if texto.lower()=="q": break
        if texto.isdigit(): dibujar(texto)
    cv2.imshow("Pizarra",lienzo)
    if cv2.waitKey(1)&0xFF==27: break
