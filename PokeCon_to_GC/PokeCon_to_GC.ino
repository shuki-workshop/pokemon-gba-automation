#include <avr/wdt.h>
#include <Gamecube.h>
#include <GamecubeAPI.h>
#include <GamecubeAPI.hpp>
#include <Gamecube_N64.h>
#include <N64.h>
#include <N64API.h>
#include <N64API.hpp>
#include <Nintendo.h>

#include "Nintendo.h"

// Define a Gamecube Console
//デジタル5,6番ピンを使う
CGamecubeConsole GamecubeConsole1(5);
Gamecube_Data_t d = defaultGamecubeData;

uint8_t pc_lx, pc_ly, pc_rx, pc_ry;

#define BUFFER_THRESHOLD 60

void ResetDirections()
{
  d.report.a = 0;
  d.report.b = 0;
  d.report.x = 0;
  d.report.y = 0;
  d.report.start = 0;
  d.report.dleft = 0;
  d.report.dright = 0;
  d.report.ddown = 0;
  d.report.dup = 0;
  d.report.z = 0;
  d.report.r = 0;
  d.report.l = 0;
  d.report.xAxis = 128;
  d.report.yAxis = 128;
  d.report.cxAxis = 128;
  d.report.cyAxis = 128;
  d.report.left = 0;
  d.report.right = 0;
}

void setup()
{

  ResetDirections();

  //コントローラーを認識させるおまじない
  d.report.start = 1;
  GamecubeConsole1.write(d);  //press start

  d.report.start = 0;
  GamecubeConsole1.write(d);  //release start

  // Start debug serial
  Serial.begin(9600);
  while( !Serial ) {
  }


}

void update_data(){
  if(!Serial.available()) return;

  String cmd_str = Serial.readStringUntil(0x0a);
  char cmd_char[32];
  cmd_str.toCharArray(cmd_char, sizeof(cmd_char));


  uint16_t p_btns;
  uint8_t hat;

  if (cmd_char[0] >= '0' && cmd_char[0] <= '9') {
    // format [button LeftStickX LeftStickY RightStickX RightStickY HAT]
    // button: Y | B | A | X | L | R | ZL | ZR | MINUS | PLUS | LCLICK | RCLICK | HOME | CAP
    // LeftStick : 0 to 255
    // RightStick: 0 to 255
    sscanf(cmd_char, "%hx %hhx %hhx %hhx %hhx %hhx", &p_btns, &hat,
          &pc_lx, &pc_ly, &pc_rx, &pc_ry);

    switch(hat){
      case 0:   // 上
        d.report.xAxis = 128;
        d.report.yAxis = 255;
        break;
      case 2:   // 右
        d.report.xAxis = 255;
        d.report.yAxis = 128;
        break;
      case 4:  // 下
        d.report.xAxis = 128;
        d.report.yAxis = 0;
        break;
      case 6:  // 左
        d.report.xAxis = 0;
        d.report.yAxis = 128;
        break;
      case 8:  // 移動しない
        d.report.xAxis = 128;
        d.report.yAxis = 128;
        break;
    }

    Serial.println(pc_lx);
    Serial.println(pc_ly);

    switch(pc_lx){
      case 0:
        d.report.dleft = 1;
        d.report.dright = 0;
        break;
      case 128:
        d.report.dleft = 0;
        d.report.dright = 0;
        break;
      case 255:
        d.report.dleft = 0;
        d.report.dright = 1;
        break;
    }  

    switch(pc_ly){
      case 0:
        d.report.dup = 1;
        d.report.ddown = 0;
        break;
      case 128:
        d.report.dup = 0;
        d.report.ddown = 0;
        break;
      case 255:
        d.report.dup = 0;
        d.report.ddown = 1;
        break;
    }

    p_btns >>= 2;
      
    d.report.y =       p_btns       & 1;
    d.report.b =      (p_btns >> 1) & 1;
    d.report.a =      (p_btns >> 2) & 1;
    d.report.x =      (p_btns >> 3) & 1;
    d.report.l =      (p_btns >> 4) & 1;
    d.report.r =      (p_btns >> 5) & 1;
    d.report.z =      (p_btns >> 7) & 1;
    d.report.start =  (p_btns >> 9) & 1;
  }
  else
    ResetDirections();  
}

void loop()
{
  if (Serial.available() > BUFFER_THRESHOLD) {
    wdt_enable(WDTO_15MS); 
    while (1) {}
  }
  else
    update_data();
  
  if(!GamecubeConsole1.write(d))
    Serial.println("GCが起動していないか、接続されていません。");

}
