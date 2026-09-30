#include <Wire.h>
#include <Keypad.h>
#include <LiquidCrystal_I2C.h>

const byte FILAS=4, COLS=4;
char teclas[FILAS][COLS]={{'1','2','3','A'},{'4','5','6','B'},{'7','8','9','C'},{'*','0','#','D'}};
byte pFilas[FILAS]={13,14,27,26};
byte pCols[COLS]={25,33,32,23};
Keypad teclado=Keypad(makeKeymap(teclas),pFilas,pCols,FILAS,COLS);
LiquidCrystal_I2C lcd(0x27,16,2);

String numero="";
void mostrar(){
  lcd.clear();
  lcd.setCursor(0,0); lcd.print("Numero:");
  lcd.setCursor(0,1); lcd.print(numero);
}
void setup(){
  Serial.begin(115200);
  Wire.begin(21,22);
  lcd.init(); lcd.backlight();
  mostrar();
}
void loop(){
  char k=teclado.getKey();
  if(!k) return;
  if(k>='0' && k<='9' && numero.length()<4){ numero+=k; mostrar(); }
  else if(k=='*' && numero.length()){ numero.remove(numero.length()-1); mostrar(); }
  else if(k=='B'){ numero=""; mostrar(); Serial.println("CLEAR"); }
  else if(k=='#' && numero.length()){
    Serial.println("DRAW:"+numero);
    lcd.clear(); lcd.print("Dibujando...");
    delay(300);
    mostrar();
  }
}