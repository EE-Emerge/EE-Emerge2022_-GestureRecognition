const int led = 2;
const int red_led = GREEN_LED;
const int buttonPin = PUSH2;
char data;

int buttonState = 0;

void setup() {
  // put your setup code here, to run once:
  pinMode(led, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly: 
  buttonState = digitalRead(buttonPin);
  
  if(Serial.available())
  {
    data = Serial.read();
  }

  if (data == 'o')
  {
    digitalWrite(led, HIGH);
  }
  else
  {
    digitalWrite(led, LOW);
  }

  if (buttonState == LOW)
  {
    Serial.print('r');
    digitalWrite(led, HIGH);
    delay(1000);
  }
  /*else
  {
    Serial.print('f');
    digitalWrite(led, LOW);
  }*/

  
}
