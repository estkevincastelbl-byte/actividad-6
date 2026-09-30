#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "driver/spi_slave.h"
Adafruit_SSD1306 display(128,64,&Wire,-1);
uint8_t rx[3],tx[3];
void mostrar(int d){
  display.clearDisplay(); display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1); display.setCursor(0,0); display.print("DIGITO RECIBIDO");
  display.setTextSize(5); display.setCursor(48,18); display.print(d);
  display.display();
}
void setup(){
  Serial.begin(115200); Wire.begin(21,22);
  display.begin(SSD1306_SWITCHCAPVCC,0x3C); display.clearDisplay(); display.display();
  spi_bus_config_t bus={}; bus.mosi_io_num=23; bus.miso_io_num=19; bus.sclk_io_num=18;
  spi_slave_interface_config_t slv={}; slv.spics_io_num=5; slv.mode=0; slv.queue_size=1;
  spi_slave_initialize(SPI3_HOST,&bus,&slv,SPI_DMA_DISABLED);
}
void loop(){
  memset(rx,0,3); spi_slave_transaction_t t={}; t.length=24; t.rx_buffer=rx; t.tx_buffer=tx;
  if(spi_slave_transmit(SPI3_HOST,&t,portMAX_DELAY)==ESP_OK){
    if(rx[0]==0xA5 && rx[2]==(uint8_t)(0xA5^rx[1]) && rx[1]<=9) mostrar(rx[1]);
  }
}