#include <SPI.h>
const int CS=5;
void setup(){
  Serial.begin(115200);
  SPI.begin(18,19,23,CS);
  pinMode(CS,OUTPUT); digitalWrite(CS,HIGH);
}
void enviar(byte d){
  SPI.beginTransaction(SPISettings(500000,MSBFIRST,SPI_MODE0));
  digitalWrite(CS,LOW);
  SPI.transfer(0xA5); SPI.transfer(d); SPI.transfer(0xA5^d);
  digitalWrite(CS,HIGH);
  SPI.endTransaction();
}
void loop(){
  if(Serial.available()){
    String s=Serial.readStringUntil('\n'); s.trim();
    if(s.startsWith("DIG:")){
      int d=s.substring(4).toInt();
      if(d>=0 && d<=9){ enviar((byte)d); Serial.printf("SPI:OK %d\n",d); }
    }
  }
}