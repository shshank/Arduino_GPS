
#include <SoftwareSerial.h>
#include <TinyGPS.h>

#define RXPIN 2
#define TXPIN 3

#define short_interval 1

#define long_interval 20000

#define GPSBAUD 4800


TinyGPS gps;

SoftwareSerial uart_gps(RXPIN, TXPIN);

void getgps(TinyGPS &gps);

void setup()
{
  Serial.begin(4800);

  uart_gps.begin(GPSBAUD);

  //Serial.println("");
  //Serial.println("Trying to connect..");
  //Serial.println("       ...waiting for lock...           ");
  //Serial.println("");
}

void loop()
{
  while(uart_gps.available())   // While there is data on the RX pin.
  {    
    int c = uart_gps.read();    // load the data into a variable...
    if(gps.encode(c))      // if there is a new valid sentence...
    {
      getgps(gps);      // then grab the data.
      delay(long_interval);
    }
  }
}

// The getgps function will get and print the values
void getgps(TinyGPS &gps)
{
  float latitude, longitude;

  gps.f_get_position(&latitude, &longitude);

  Serial.print("lat:"); 
  Serial.println(latitude,5); 
  delay(short_interval);
  Serial.print("long:"); 
  Serial.println(longitude,5);
  delay(short_interval);

  int year;
  byte month, day, hour, minute, second, hundredths;
  gps.crack_datetime(&year,&month,&day,&hour,&minute,&second,&hundredths);
  // Print data and time

  Serial.print("datetime:");
  if(month==0)
    Serial.print(month+1, DEC); 
  else
    Serial.print(month, DEC); 
  Serial.print("/");
  if(day==0)
    Serial.print(day+1, DEC);
  else
    Serial.print(day, DEC); 
  Serial.print("/"); 
  Serial.print(year);
  Serial.print("-"); 
  Serial.print(hour, DEC); 
  Serial.print("/"); 
  Serial.print(minute, DEC); 
  Serial.print("/"); 
  Serial.print(second, DEC); 
  Serial.print("/"); 
  Serial.println(hundredths, DEC);
  delay(short_interval);
  //Since month, day, hour, minute, second, and hundr
  // there is only one value for the function
  Serial.print("alt:"); 
  Serial.println(gps.f_altitude());  
  delay(short_interval);
  // Same goes for course
  Serial.print("course:"); 
  Serial.println(gps.f_course()); 
  delay(short_interval);
  // And same goes for speed
  Serial.print("speed:"); 
  Serial.println(gps.f_speed_kmph());
  delay(short_interval);
  Serial.println("done:done");

  unsigned long chars;
  unsigned short sentences, failed_checksum;
  gps.stats(&chars, &sentences, &failed_checksum);
}




