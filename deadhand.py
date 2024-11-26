import RPi.GPIO as GPIO
import time
import threading
import pygame
import math
import random
from texts import create_code, send_message

# GPIO setup
GPIO.setmode(GPIO.BCM)
NUKE = 6
BUZZER = 22
IR = 5

GPIO.setup(NUKE, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(IR, GPIO.IN)

GPIO.output(NUKE, GPIO.LOW)
GPIO.output(BUZZER, GPIO.LOW)

# Radar UI setup
pygame.init()
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("180° Radar Simulation")

black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
center_x, center_y = width // 2, height // 2 + 150
radius = 300
angle = 0
direction = 1

def radar_ui():
    global angle, direction
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(black)

        # Draw radar semi-circle and concentric circles
        for r in range(50, radius + 1, 50):
            pygame.draw.arc(screen, green, (center_x - r, center_y - r, 2 * r, 2 * r), 
                            math.radians(0), math.radians(180), 1)
        
        pygame.draw.line(screen, green, (center_x - radius, center_y), (center_x + radius, center_y), 2)
        
        # Draw radar sweep line
        x = center_x + radius * math.cos(math.radians(angle))
        y = center_y - radius * math.sin(math.radians(angle))
        pygame.draw.line(screen, green, (center_x, center_y), (x, y), 2)

        # Draw simulated blips
        detected_objects = [(random.randint(50, radius), random.randint(0, 180)) for _ in range(5)]
        for dist, ang in detected_objects:
            rad_x = center_x + dist * math.cos(math.radians(ang))
            rad_y = center_y - dist * math.sin(math.radians(ang))
            pygame.draw.circle(screen, red, (int(rad_x), int(rad_y)), 5)

        angle += direction
        if angle >= 180 or angle <= 0:
            direction *= -1

        pygame.display.flip()
        pygame.time.delay(20)

    pygame.quit()

def request_permission():
    print("Requesting permission from Nuclear Command.")
    code = create_code()
    send_message("Code to abort launch sequence: " + code)

    user_input = {'code': None}
    
    def get_user_input():
        ans = input("Enter abort code: ")
        user_input['code'] = ans
    
    input_thread = threading.Thread(target=get_user_input)
    input_thread.start()
    input_thread.join(timeout=5)
    
    if user_input['code'] == code:
        print("Launch sequence aborted.")
        GPIO.output(NUKE, GPIO.LOW)
        GPIO.output(BUZZER, GPIO.LOW)
    else:
        print("No valid code entered. Launching missiles!")
        GPIO.output(NUKE, GPIO.HIGH)
        GPIO.output(BUZZER, GPIO.HIGH)

def launch_control():
    try:
        while True:
            if GPIO.input(IR) == 0:
                request_permission()
                time.sleep(2)
    except KeyboardInterrupt:
        print("Exiting program")
    finally:
        GPIO.cleanup()

# Run radar UI and launch control concurrently
radar_thread = threading.Thread(target=radar_ui)
control_thread = threading.Thread(target=launch_control)

radar_thread.start()
control_thread.start()

radar_thread.join()
control_thread.join()


