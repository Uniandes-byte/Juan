#include <ros.h>
#include <std_msgs/Int8.h>
#include <geometry_msgs/Vector3.h>

ros::NodeHandle nh;

//motor 1
int ENA = 11; // Entrada a pin 11.
int IN1 = 5; // Entrada a pin 5.
int IN2 = 6; // Entrada a pin 6.

//motor 2
int IN3 = 7; // Entrada a pin 7.
int IN4 = 8; // Entrada a pin 8.
int ENB = 10; // Entrada a pin 10.

// Inicializa variables de velocidad.
int speed_lineal = 0; 
int speed_angular = 0; 

void locomotion(const geometry_msgs::Vector3 & dataFromRos)
{
  speed_lineal = round(4.875*abs(dataFromRos.x)-37.5); // Relación entre velocidad lineal y PWM.
  speed_angular = round(1.2188*abs(dataFromRos.y)+35.624); // Relación entre velocidad angular y PWM.

  if(dataFromRos.x > 0) // Si valor de velocidad lineal x mayor a 0.
  {
    adelante();
  }
  else if(dataFromRos.x < 0) // Si valor de velocidad lineal x menor a 0.
  {
    atras();
  }
   else if(dataFromRos.y > 0) // Si valor de velocidad angular y mayor a 0.
  {
    izquierda();
  }
   else if(dataFromRos.y < 0) // Si valor de velocidad angular y menor a 0.
  {
    derecha();
  }
   else if(dataFromRos.x ==0 && dataFromRos.y ==0) // Si valor de velocidad lineal y angular igual a 0.
  {
    detenido();
  }
}

ros::Subscriber<geometry_msgs::Vector3> sub("locomotion_arduino",locomotion); // Se subscribe al tópico locomotion_arduino.


void setup ()
{
  
  // Declaramos todos los pines como salidas.
  pinMode (IN1, OUTPUT);
  pinMode (IN2, OUTPUT);
  pinMode (ENA, OUTPUT);
  pinMode (IN3, OUTPUT);
  pinMode (IN4, OUTPUT);
  pinMode (ENB, OUTPUT);
  nh.initNode();
  nh.subscribe(sub);

}

void loop()
{
  nh.spinOnce();
  delay(3);

}

============================================
// Metodos de movimiento
============================================

void adelante() // Movimiento hacia adelante.
{
  digitalWrite(IN1, LOW); // Pin 1 en low.
  digitalWrite(IN2, HIGH); // Pin 2 en high.
  digitalWrite(IN3, LOW); // Pin 3 en low.
  digitalWrite(IN4, HIGH); // Pin 4 en high.
  analogWrite(ENA, speed_lineal); // Pin A en speed_lineal.
  analogWrite(ENB, speed_lineal); // Pin B en speed_lineal.
  delay(3);
}

void atras() // Movimiento hacia atrás.
{
  digitalWrite(IN1, HIGH); // Pin 1 en high.
  digitalWrite(IN2, LOW); // Pin 2 en low.
  digitalWrite(IN3, HIGH); // Pin 3 en high.
  digitalWrite(IN4, LOW); // Pin 4 en low.
  analogWrite(ENA, speed_lineal); // Pin A en speed_lineal.
  analogWrite(ENB, speed_lineal); // Pin B en speed_ lineal.
  delay(3);

}
void izquierda() // Movimiento hacia la izquierda.
{
  digitalWrite(IN1, HIGH); // Pin 1 en high.
  digitalWrite(IN2, LOW); // Pin 2 en low.
  digitalWrite(IN3, LOW); // Pin 3 en low.
  digitalWrite(IN4, HIGH); // Pin 4 en high.
  analogWrite(ENA, speed_angular); // Pin A en speed_lineal.
  analogWrite(ENB, speed_angular ); // Pin B en speed_lineal.
  delay(3);
}

void derecha() // Movimiento hacia la derecha.
{

  digitalWrite(IN1, LOW); // Pin 1 en low.
  digitalWrite(IN2, HIGH); // Pin 2 en high.
  digitalWrite(IN3, HIGH); // Pin 3 en high.
  digitalWrite(IN4, LOW); // Pin 4 en low.
  analogWrite(ENA, speed_angular); // Pin A en speed_lineal.
  analogWrite(ENB, speed_angular); // Pin B en speed_lineal.
  delay(3);
}

void detenido()
{

  digitalWrite(IN1, LOW); // Pin 1 en low.
  digitalWrite(IN2, LOW); // Pin 1 en low.
  digitalWrite(IN3, LOW); // Pin 1 en low.
  digitalWrite(IN4, LOW); // Pin 1 en low.
  analogWrite(ENA, 0); // Pin A en speed_lineal.
  analogWrite(ENB, 0); // Pin B en speed_lineal.
  delay(3);
}
