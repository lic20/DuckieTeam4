// AUTHOR: Shinny Sun
// UPLOAD DATE: 12/15/2021

// PROGRAM DESCRIPTION: This code remote controls the Duckie Grabber of UberDuck. 
// The 'UP' button moves the grabber to the neutral position, 'DOWN' button moves
// it to the down position, and 'FAST FORWARD' button moves the grabber to the yeet
// position. 

// IRremote - Version: Latest 
#include <IRremote.h>
#include <IRremoteInt.h>

// Initialize motor pins
#define MOTOR_EN_1_2  10
#define MOTOR_IN1     9
#define MOTOR_IN2     8

int speed = 0;
int time = 0;
int receiver = 6; // Signal Pin of IR receiver to Arduino Digital Pin 6

/*-----( Declare objects )-----*/
IRrecv irrecv(receiver);     // create instance of 'irrecv'
decode_results results;      // create instance of 'decode_results'

void setup()   /*----( SETUP: RUNS ONCE )----*/
{
  Serial.begin(9600);
  Serial.println("IR Receiver Button Decode"); 
  irrecv.enableIRIn(); // Start the receiver
  pinMode(MOTOR_EN_1_2, OUTPUT);
  pinMode(MOTOR_IN1, OUTPUT);
  pinMode(MOTOR_IN2, OUTPUT);
  while (! Serial);
  Serial.println("Speed 0 to 255");
  digitalWrite(MOTOR_IN1, LOW);
  digitalWrite(MOTOR_IN2, LOW);
}/*--(end setup )---*/


void loop()   /*----( LOOP: RUNS CONSTANTLY )----*/
{
   analogWrite(MOTOR_EN_1_2, abs(speed));
   delay(time);
   digitalWrite(MOTOR_IN1, LOW);
   digitalWrite(MOTOR_IN2, LOW);
  if (irrecv.decode(&results)) // have we received an IR signal?

  {
    translateIR(); 
    irrecv.resume(); // receive the next value
  }  
}/* --(end main loop )-- */

/*-----( Function )-----*/
void translateIR() // takes action based on IR code received

// describing Remote IR codes 

{

  switch(results.value)
    
  {
    
  case 0xFFA25D: Serial.println("POWER"); // stops motor from running
    analogWrite(MOTOR_EN_1_2, 0);
    digitalWrite(MOTOR_IN1, LOW);
    digitalWrite(MOTOR_IN2, LOW);
    break;
  case 0xFF22DD: Serial.println("FAST BACK"); // moves claw down for pickup from yeet position
      speed = -150;
      time = 500;
      digitalWrite(MOTOR_IN1, LOW);
      digitalWrite(MOTOR_IN2, HIGH);
      break;
  case 0xFFC23D: Serial.println("FAST FORWARD"); // yeet duckie
      speed = 250;
      time = 1000;
      digitalWrite(MOTOR_IN1, HIGH);
      digitalWrite(MOTOR_IN2, LOW);break;
      
  case 0xFFE01F: Serial.println("DOWN"); // moves claw down for pickup
      speed = -100;
      time = 500;
      digitalWrite(MOTOR_IN1, LOW);
      digitalWrite(MOTOR_IN2, HIGH); break;
      
  case 0xFFA857: Serial.println("VOL-");    break;
  case 0xFF906F: Serial.println("UP"); // moves claw to neutral position
      speed =150;
      time = 1000;
      digitalWrite(MOTOR_IN1, HIGH);
      digitalWrite(MOTOR_IN2, LOW);break;

  default: 
    Serial.println(" other button   ");

  }// End Case

  delay(500); // Do not get immediate repeat


} //END translateIR
