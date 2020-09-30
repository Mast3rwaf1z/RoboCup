#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from threading import Thread

ev3 = EV3Brick()

rMotor = Motor(Port.A, positive_direction=Direction.COUNTERCLOCKWISE)
lMotor = Motor(Port.D, positive_direction=Direction.COUNTERCLOCKWISE)
cMotor = Motor(Port.C)
colorS = ColorSensor(Port.S3)
ultraS = UltrasonicSensor(Port.S4)

ev3.speaker.set_volume(100)                                 #Set volume to 100%
Lydeffekt=0                                                 #Variable for at start en lyd
Section_number=1                                            #Variable for hvilket sektion af sangen der skal spilles
opgavenr =  0                                               #Variable for hvilken opgave der skal køres
active = 1                                                  #Variable der viser om robotten skal kører
glCount = 0                                                 #Grey line count. Bruges til opgave 4 med de parallele linjer

#Hver procentdel afvigelse af lys fra 'threshold' , 
#sætter turn_rate i drivebase 1.5 grader i sekundet
#fx hvis lyset afviger 10 fra 'threshold', så drejer 10*x grader pr. sekund

proportionalGain = 1.5


#Drive base
robot = DriveBase(lMotor, rMotor, wheel_diameter=50, axle_track=172) 

def Play_Music():                                           #Musikfunktion
    global Tokyo_Drift_Done
    global USSR_Done
    global Lydeffekt
    global Section_number                                        
    Tokyo_Drift_Done=1
    Rick_Roll_Done=0
    ev3.speaker.play_file("Pornhub-30.rsf")                 #Spil intro musik
    wait(3000)
    
    while opgavenr<3:                                       #Spil musik for opgaver 1-2
        if Lydeffekt==1:
            ev3.speaker.play_file("Tank1.rsf")
            ev3.speaker.play_file("Tank2.rsf")
        else:
            wait(200)
    while opgavenr==3:                                      #Spil musik for opgave 3
        if Lydeffekt==1:
            ev3.speaker.play_file("Naruto.rsf")
        else:
            wait(200)
    while opgavenr==4:                                      #Spil musik for opgave 4
        if Rick_Roll_Done==0:
            ev3.speaker.play_file("Rick1.rsf")
            ev3.speaker.play_file("Rick2.rsf")
            Rick_Roll_Done=1
        else:
            wait(200)
    while opgavenr==5:                                      #Spil Lydeffekter for opgave 5
        if Lydeffekt==1:
            ev3.speaker.play_file("Bomb_Plant.rsf")
            Lydeffekt=0
        elif Lydeffekt==2:
            ev3.speaker.play_file("Get_Out.rsf")
            ev3.speaker.play_file("C4-30.rsf")
            ev3.speaker.play_file("Terrorists_Win.rsf")
            Lydeffekt=0
        else:
            wait(100)
    while opgavenr>5 and opgavenr<9:                        #Spil musik for opgave 6-7-8
        if Section_number<8:
            Tokyo_Drift_Done=0
            Section_to_play="Tokyo_Drift"+str(Section_number)+".rsf"
            ev3.speaker.play_file(Section_to_play)
            Section_number+=1
            Tokyo_Drift_Done=1
            if opgavenr==9:
                wait(2000)
        else:
            break
    Section_number=1
    while opgavenr==9:                                      #Spil musik for opgave 9
        ev3.light.on(Color.RED)
        if Section_number<11:
            USSR_Done=0
            Section_to_play="USSR"+str(Section_number)+".rsf"
            ev3.speaker.play_file(Section_to_play)
            Section_number+=1
        else:
            USSR_Done=1
            break

Music_Thread=Thread(target=Play_Music)                      #Tilføje musikfunktionen til en anden thread
Music_Thread.start()                                        #Start musikfunktionen i en anden thread
cMotor.run_until_stalled(-100)                              #Sæt gripperen til at være helt åben

#Tjek farver
greyLine = colorS.reflection()                              # Definer farven grå
robot.turn(-45)                                             # Drej -45 grader
white = colorS.reflection()                                 # Definer farven hvid     
robot.turn(45)                                              # Drej 45 grader
threshold = (greyLine + white) / 2                          # Definer threshhold hvor sensor skal skifte imellem grå og hvid
blackLines = greyLine / 3                                   # Definer sort streg
    
def drive(x):                                               # Definerer en general drive funktion
    deviation = colorS.reflection() - threshold             

    turnRate = proportionalGain * deviation

    robot.drive(x, turnRate)

    wait(10)    


def Opgaver():                                              # Definer opgaverne der skal løses
    global Lydeffekt
    global opgavenr
    opgavenr += 1
    if opgavenr == 1:                                       # Brudt streg - Tobias
        while colorS.reflection() > blackLines:             # Så længe overfladen er sort skal den følge den grå linje
            drive(100)
        Lydeffekt=1                                         # Start Lyd (Tank Engine)
        robot.drive(100, 0)
        wait(300)
        robot.stop()
        robot.turn(45)                                      # Robotten skal dreje 45 grader

        while colorS.reflection() > greyLine:               # Kør ligeud indtil sensoren registrerer grå overflade
            robot.drive(100, 0)                             

        robot.straight(50)
        robot.stop()
        robot.turn(-45)                                     # Drej -45 grader
                                
        while colorS.reflection() > blackLines:             # Følg den grå linje så længe overfladen er over sort
            drive(100)                                      # Og så skal den stoppe når overfladen er sort
        
        robot.turn(-45)                                     # Robotten skal dreje -45 grader

        while colorS.reflection() > greyLine:               # Kør ligeud indtil sensoren registrerer grå overflade
            robot.drive(100, 0)
        wait(750)
        robot.stop()                                        
        robot.turn(45)                                      # Robotten skal dreje 45 grader og være lige på linjen
              
    elif opgavenr == 2:                                     # Flyt flaske - Mikkel
        speed = 400
        robot.drive(100,0)
        wait(1000)
        flaskTime = 0
        while flaskTime < 50:                               # Drive i given tid
            drive(50)
            flaskTime += 1
        robot.drive(50,90)
        wait(1000)                                          # Drejetid
        while ultraS.distance() > 100 :                     # Få længde på ultrasonic sensor
            drive(100)
        robot.straight(50)
        robot.stop()
        cMotor.run_until_stalled(150)                       # Løft klo / flaske
        seeBlack = 0
        robot.drive(100,2)
        wait(1500)
        robot.stop()
        while seeBlack == 0:                                # Fang i while loop indtil den ser sort
            if colorS.reflection() > blackLines:
                robot.drive(20, 2)
            else:
                seeBlack += 1
        robot.stop()
        cMotor.run_until_stalled(-150)                      # Sænk klo / flaske
        robot.drive(50, 0)                                  # Giv flaske et lille kærligt skub for at rette den op
        wait(400)
        Lydeffekt=0                                         # Stop Lyd (Tank Engine)
        robot.stop()
        cMotor.run(0)
        lMotor.run(-speed)
        rMotor.run(-speed)
        wait(2500)
        rMotor.run(50)
        wait(1500)
        lMotor.run(0)
        rMotor.run(0)
        



    elif opgavenr == 3:                                     # Vippe - David
        robot.straight(150)                                 # Robotten kører 150 mm frem
        robot.turn(-90)                                     # Den drejer til venstre
        Lydeffekt=1
        while colorS.reflection() > blackLines:
            drive(100)                                      # Robotten kører indtil den ser en sort streg
        robot.straight(400)                                 # Den kører ligeud henover vippen
        vippeTime = 0                                       # Definerer tiden den skal være på vippen
        while vippeTime < 500:                              # Så længe at robotten er på vippen
            drive(100)                                      # Skal den følge linjen ned af vippen 
            vippeTime += 1
        Lydeffekt=0
        robot.straight(600)
        robot.turn(-90)                                     # Defefter drejer den til venstre efter vippen
        
        #########################
        ###    SAFETYCODE!    ###
        ###robot.straight(150)###
        #########################
    elif opgavenr == 4:                                     # Parallele Streger - Rasmus
        glCount=0                                           # Definerer glCount variable
        if glCount == 0:                                    # Checker om glCount er lig med 0
            robot.straight(300)                             # Kører 300mm lige frem
            robot.turn(-30)                                 # Drejer 30 grader til venstre
            robot.drive(100, 0)                             # Robotten begynder at køre lige fremad
            glCount += 1                                    # Lægger 1 til glCount
        while glCount < 3:                                  # Loop der kører mens glCount er mindre end 3
            if colorS.reflection() > threshold:             # Checker om farvesensorerens reflection er højere end threshold
                glCount += 1                                # Lægger 1 til glCount
                wait(1500)                                  # Venter i 1500ms
        robot.straight(20)                                  # Kører 20mm lige frem
        robot.turn(30)                                      # Drejer 30 grader til højre
    
    elif opgavenr == 5:                                     # Målskive - Simon
        robot.straight(170)                                 # Kører 170 mm frem
        robot.turn(-90)                                     # Drejer til venstre

        while colorS.reflection() > blackLines:             # Kører indtil den ser en sort streg
            drive(50)
        robot.straight(500)                                 # Kører 500 mm frem
        robot.turn(-32)                                     # Drejer 32 grader til venstre

        cMotor_Stalled=0                                    # definerer variabel
        robot.reset()                                       # Reset distancen til målskive og måler ny distance fra målskive til flaske
        while cMotor_Stalled != 1:                          # Starter loop
            if ultraS.distance() < 80:                      # Hvis distancen mellem ultraS er 80 mm stopper robot
                robot.stop()
                Distance_to_bottle=robot.distance()         # Afstanden som den har målt fra måleskive til flaske
                cMotor.run_until_stalled(150)               # Kører motoren indtil den griber flasken
                cMotor_Stalled = 1                          # Variabel til at stoppe loop

            else:                                           # Robotten fortsætter med at køre indtil den ser flasken
                robot.drive(100,0)

        robot.straight(-Distance_to_bottle-170)             # Robotten bakker tilbage til midten af målskiven
        cMotor.run_until_stalled(-150)                      # Sætter flasken ned
        Lydeffekt=1                                         # Spil Lydeffekt 1 (Bomb has been planted)
        robot.straight(20)                                  # Skubber flasken
        robot.straight(-280)                                # Bakker 280 mm 
        robot.turn(-140)                                    # Drejer 140 grader til venstre
        cMotor.run_until_stalled(150)                       # sluk klogen
        Lydeffekt=2                                         # Spil Lydeffekt 2 (It's gonna blow)

        while True:                                         # Starter loop
            if colorS.reflection() > threshold:             # Fortsætter med at køre ligeud indtil den finder gråstreg
                robot.drive(100,0)
            else:                                           
                robot.straight(100)                         # Kører en smule frem, drejer til venstre og følger linjen
                robot.turn(-90)
                break

    elif opgavenr == 6:                                     #Undvig flaske 1 - Mohamad
        robot.stop()                                        #Stop drivebase
        lMotor.run(-200)                                    #Kør venstre moter med hastighed på -200 grader per sekund
        rMotor.run(200)                                     #Kør højer moter med hastighed på 200 grader per sekund
        wait(881)                                           #Vent 881 millisekunder
        lMotor.run(298.08)                                  #Kør venstre moter med hastighed på 298.08 grader per sekund
        rMotor.run(200)                                     #Kør højer moter med hastighed på 200 grader per sekund
        wait(7168)                                          #Vent 7168 millisekunder

    elif opgavenr == 7:                                     # Murparkour skrrrt - Faur
        robot.stop()                                        # Stop drivebase
        lMotor.run(200)                                     # Kør venstre motor med drivespeed
        rMotor.run(200)                                     # Kør højre motor med drivespeed
        wait(4523.89)                                       # Vent indtil sving 1
        lMotor.run(200*0.03)                                # Sæt venstre motor til ratio 1
        wait(1735.67)                                       # Vent indtil sving 2
        lMotor.run(200*1.97)                                # Sæt venstre motor til ratio 2
        wait(3471.33)                                       # Vent indtil sving 3
        lMotor.run(200*0.03)                                # Sæt venstre motor tilbage til ratio 1
        wait(1735.67)                                       # Vent indtil sving er færdig
        lMotor.run(200)                                     # Sæt venstre motor drivespeed = højre motor
        wait(2500)                                          # Kør ligeud indtil robotten når den grå streg

    elif opgavenr == 8:                                     #Undvig flaske 2 - Mohamad
        robot.stop()                                        #Stop Drivebase
        lMotor.run(-200)                                    #Kør venstre moter med hastighed på -200 grader per sekund
        rMotor.run(200)                                     #Kør højer moter med hastighed på 200 grader per sekund
        wait(881)                                           #Vent 881 millisekunder
        lMotor.run(298.08)                                  #Kør venstre moter med hastighed på 298.08 grader per sekund    
        rMotor.run(200)                                     #Kør højer moter med hastighed på 200 grader per sekund
        wait(7168)                                          #Vent 7168 millisekunder
        lMotor.run(200)                                     #Kør venstre moter med hastighed på 200 grader per sekund
        rMotor.run(200)                                     #Kør højer moter med hastighed på 200 grader per sekund
        #wait(400)                                           #Vent 700 millisekunder
        lMotor.run(-200)                                    #Kør venstre moter med hastighed på -200 grader per sekund    
        rMotor.run(200)                                     #Kør højer moter med hastighed på 200 grader per sekund
        wait(1581)                                          #Vent 1581 millisekunder

    elif opgavenr == 9:                                     #Landingsbane - Thomas
        global active
        Section_number=1
        while active==1:    
            if Tokyo_Drift_Done==1:    
                wait(6000)
                lbane = 0
                robot.straight(15)
                while(lbane<200):
                    drive(20)
                    wait(1)
                    lbane += 1
                robot.stop()
                cMotor.run_until_stalled(-150)
                robot.settings(60)                          #Gør robbotens hastighed mindre
                robot.straight((300/2) * 10)                #kører udregnet distance og stop programmet
                robot.stop()
                rMotor.run(50)
                lMotor.run(-50)
                while USSR_Done==0:
                    cMotor.run(300)
                    wait(1500)
                    cMotor.run(-300)
                    wait(1500)
                cMotor.stop()
                rMotor.stop()
                lMotor.stop()
                ev3.speaker.play_file("Shutdown.rsf")
                active = 2
            else:
                robot.stop()


while active == 1:
    drive(100)
    if colorS.reflection() < blackLines:
        Opgaver()
    