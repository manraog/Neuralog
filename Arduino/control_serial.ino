////////////// LIBRERIAS ///////////////
#include <OneWire.h>
#include <DallasTemperature.h>


////////////// PINES ////////////////
//ShiftRegister 74HC595
#define CLOCK 7
#define DATA 6 //Entrada de datos
#define LATCH 5 //Pasa el estado del registro a los latch de salida

//SensorTemp DS18B20
#define SENSOR 11 //OneWire Bus

//Habitaciones
#define SALA 4
#define COCINA 3
#define CUARTO 2

/////// CONFIGURA DS18B20 //////////
// Crea una instancia del sensor
OneWire oneWire(SENSOR);
// Pasamos la instancia al "manejador de sensores DS18B20"
DallasTemperature sensors(&oneWire);

/////// VARIABLES GLOBALES //////////
float temperatura;
byte posicion = 1;
byte comando;

////////////// SETUP ///////////////
void setup() {
  // Inicia Serial
  Serial.begin(9600);

  // Entradas
  pinMode(SALA, INPUT_PULLUP);
  pinMode(COCINA, INPUT_PULLUP);
  pinMode(CUARTO, INPUT_PULLUP);
  
  // Salidas
  pinMode(CLOCK, OUTPUT);
  pinMode(DATA, OUTPUT);
  pinMode(LATCH, OUTPUT);

  // Inicia sensores DS18B20
  sensors.begin();

  
}

void loop() {
  
  //Cuando no se recibe nada
  if(Serial.available() <= 0) {
    //Envia los datos de los sensores
    sensors.requestTemperatures();
    temperatura = sensors.getTempCByIndex(0);

    if (digitalRead(SALA) == LOW)
    {
      posicion = 1;
    }
    else if (digitalRead(COCINA) == LOW)
    {
      posicion = 2;
    }
    else if (digitalRead(CUARTO) == LOW)
    {
      posicion = 3;
    }
    else
    {
      posicion = 1;
    }
    
    Serial.print(posicion);
    Serial.print(',');
    Serial.println(temperatura);
    delay(500);
  }
  //Cuando se recibe algo
  //if (Serial.available() > 0) 
  else{
    //Lee el byte
    comando = Serial.read();
    digitalWrite(LATCH, LOW);
    shiftOut(DATA, CLOCK, MSBFIRST, comando);   
    digitalWrite(LATCH, HIGH);
  }
}
