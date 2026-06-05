#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

// Inițializăm ecranul LCD. 
// 0x27 este adresa standard I2C pentru majoritatea ecranelor. 16 coloane, 2 rânduri.
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Definire pini
const int pinTrig = 9;
const int pinEcho = 10;
const int pinLED = 13;
const int pinBuzzer = 8;

const int limitaDistanta = 20; 

void setup() {
  // Inițializare LCD
  lcd.init();
  lcd.backlight(); // Aprinde lumina de fundal a ecranului
  
  // Mesaj de pornire
  lcd.setCursor(0, 0); // Pune cursorul pe prima coloană, primul rând
  lcd.print("Sistem Alarma");
  lcd.setCursor(0, 1); // Mută pe rândul 2
  lcd.print("Se incarca...");
  delay(2000); // Așteaptă 2 secunde ca să vedem mesajul
  lcd.clear(); // Șterge ecranul
  
  // Setare pini
  pinMode(pinTrig, OUTPUT);
  pinMode(pinEcho, INPUT);
  pinMode(pinLED, OUTPUT);
  pinMode(pinBuzzer, OUTPUT);
}

void loop() {
  // Măsurare distanță
  digitalWrite(pinTrig, LOW);
  delayMicroseconds(2);
  digitalWrite(pinTrig, HIGH);
  delayMicroseconds(10);
  digitalWrite(pinTrig, LOW);
  
  long durata = pulseIn(pinEcho, HIGH);
  int distanta = durata * 0.034 / 2;
  
  // --- AFIȘARE PE LCD ---
  lcd.setCursor(0, 0); // Rândul 1
  lcd.print("Distanta: ");
  lcd.print(distanta);
  lcd.print(" cm  "); // Spațiile goale șterg cifrele vechi dacă distanța scade (ex: de la 100 la 9)

  // Verificare limită alarmă
  if (distanta > 0 && distanta < limitaDistanta) {
    // Pornire Alarmă
    digitalWrite(pinLED, HIGH);
    tone(pinBuzzer, 1000);
    
    lcd.setCursor(0, 1); // Rândul 2
    lcd.print("STATUS: ALARMA! ");
  } else {
    // Oprire Alarmă
    digitalWrite(pinLED, LOW);
    noTone(pinBuzzer);
    
    lcd.setCursor(0, 1); // Rândul 2
    lcd.print("STATUS: OK      ");
  }
  
  delay(200); // Pauză scurtă pentru a nu licări ecranul prea rapid
}
