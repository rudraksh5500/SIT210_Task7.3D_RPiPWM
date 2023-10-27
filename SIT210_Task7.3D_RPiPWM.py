# Import the necessary libraries
import RPi.GPIO as GPIO
import time

# Setting the GPIO mode to BCM 
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin numbers for the components
LED = 26   # LED control pin
TRIG = 19  # Ultrasonic sensor trigger pin
ECHO = 13  # Ultrasonic sensor echo pin

# Set up the GPIO pins as input or output
GPIO.setup(TRIG, GPIO.OUT) 
GPIO.setup(ECHO, GPIO.IN)   
GPIO.setup(LED, GPIO.OUT)   

# Creating a PWM object for controlling the LED
pwm = GPIO.PWM(LED, 100)
pwm.start(0)

# Defining a function to measure distance using the ultrasonic sensor
def dist():
    startT = time.time()
    stopT = time.time()
    
    # Send a short pulse to trigger the ultrasonic sensor
    GPIO.output(TRIG, True)
    time.sleep(0.0001)
    GPIO.output(TRIG, False)
    
    # Measure the time it takes for the echo signal to return
    while GPIO.input(ECHO) == 0:
        startT = time.time()
    while GPIO.input(ECHO) == 1:
        stopT = time.time()
    
    # Calculate the distance based on the time and speed of sound
    totTime = stopT - startT
    dist = (totTime * 34300) / 2
    return dist

try:
    # Continuously measure and react to the distance
    while True:
        distance = dist()  
        print(distance)    

        # Control the LED based on the measured distance
        if (distance <= 50):
            pwm.ChangeFrequency(6 - distance/10) 
            pwm.ChangeDutyCycle(50)               
            time.sleep(0.5)                    
        else:
            pwm.ChangeDutyCycle(0)               
        time.sleep(1)                             

except KeyboardInterrupt:
    # Clean up GPIO settings when the program is terminated
    GPIO.cleanup()
