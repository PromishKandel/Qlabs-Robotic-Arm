
#Imports giving in the template 
import sys
import random
import time
sys.path.append('../')

from Common_Libraries.p2_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim ():
    try:
        arm.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

arm = qarm()

update_thread = repeating_timer(2, update_sim)


#Moving arm to home position 
arm.home()
time.sleep(4)

    
#Field variables for flex are sensor  
Larm_intial = 0
Rarm_intial = 0
Larm_final = 0
Rarm_final = 0



"""
By: Promish
Function determines the change in flex position and runs the code if change
    is greater than 0.5 and assigns it to an int value.
    1 = Flex
    0 = No change
    -1 =  Unflex
"""
def Armcheck(data_arm):

    #Global variables used to hold arm flex dat
    global Larm_intial
    global Rarm_intial
    global Larm_final
    global Rarm_final
    Lflex = 0
    Rflex = 0

    #Setting the intial flex value to perivous final value 
    Larm_intial = Larm_final
    Rarm_intial = Rarm_final

    #Setting the final flex value to current flex position of both arms 
    Larm_final = data_arm[0]
    Rarm_final = data_arm[1]


    #Checking to see if left arm flex position change is greater than 0.5
    if Larm_final - Larm_intial > 0.5:
        Lflex = 1
        print("Left arm is flexed")

    
    elif Larm_final - Larm_intial < -0.5:
        Lflex = -1
        print("Left arm is extended")

    
    else:
        Lflex = 0
        print("No change has occured")


    #Checking to see if right arm flex position change is greater than 0.5
    if Rarm_final - Rarm_intial > 0.5:
        Rflex = 1
        print("Left arm is flexed")

  
    elif Rarm_final - Rarm_intial < -0.5:
        Rflex = -1
        print("Left arm is extended")

    
    else:
        Rflex = 0
        print("No change has occured")

    #Returns a list of 2 index containing a flex in int value eg [1,-1]
    return (Lflex, Rflex)



"""
By:Promish
Function returns a list [x,y,z] of the dropoff location of the spawned cage
by referencing  the binID
"""
def dropoff(num):

#Dropoff location for small red bin
    if num == 1:
        droplocation = [-0.5959, 0.2408, 0.4576]

    #Dropoff location for small green bin
    elif num == 2:
        droplocation = [0.0, -0.656, 0.4446]

    #Dropoff location for small blue bin        
    elif num == 3:
        droplocation = [0.0, 0.656, 0.4446]

    #Dropoff location for big red bin        
    elif num == 4:
        droplocation = [-0.4, 0.1657, 0.1999]

    #Dropoff location for big green bin        
    elif num == 5:
        droplocation = [0.0, -0.4329, 0.1999]

    #Dropoff location for big blue bin        
    elif num == 6:
        droplocation = [0.0, 0.4329, 0.1999]
   
    return droplocation



"""
By: Promish and Hunter
Function checks to see if binID corresponds to a big cage
and opens correct drawer by referencing the BinID
"""
def Open_AutoClave_BinDrawer (binID, arm_threshold):
    
    #EmG value being evaluted for left flex and right no change
    if arm_threshold[0] == 1 and arm_threshold[1] == 0:
        #Opens reds BinDrawer if BinID is 4
        if binID == 4:
            arm.open_red_autoclave(True)
            return print ("Opening Red Drawer")

        #Opens green BinDrawer if BinID is 5
        elif binID == 5:
            arm.open_green_autoclave(True)
            return print ("Opening green Drawer")
    
        #Opens blue BinDrawer if BinID is 5
        elif binID == 6:
            arm.open_blue_autoclave(True)
            return print ("Opening blue Drawer")


"""
By:Promish and Hunter
Function Checks to see if binID corresponds to a big cage
and closes correct drawer by referencing the BinID
"""
def Close_AutoClave_BinDrawer (binID, arm_threshold):
    
    #EmG value being evaluted for left unflex and right no change
    if arm_threshold[0] == -1 and arm_threshold[1] == 0:
        #Closes reds BinDrawer if BinID is 4
        if binID == 4:
            arm.open_red_autoclave(False)
            return print ("Closing Red Drawer")

        #Closes green BinDrawer if BinID is 5
        elif binID == 5:
            arm.open_green_autoclave(False)
            return print ("Closing green Drawer")

        #Closes blue BinDrawer if BinID is 6
        elif binID == 6:
            arm.open_blue_autoclave(False)
            return print ("Closing blue Drawer")






"""
By: Promish
Function picks up the bin that was spawned in the following the steps
    -bending down
    -closing the gripper
    -opening the gripper
    -closing the gripper
    -bending back to home position
"""
def Control_Gripper(arm_threshold):
    
    #EmG value being evaluted for right flex and left no change
    if arm_threshold[1] == 1 and arm_threshold[0] == 0:
        arm.rotate_shoulder(50)
        time.sleep(2)

        #Gripper opens and closes twice to center the cage properly 
        arm.control_gripper(45)
        time.sleep(2)

        arm.rotate_shoulder(-50)
        return print("Gripping Complete")

    #EmG value being evaluted for right unflex and left no change
    elif arm_threshold[1] == -1 and arm_threshold[0] == 0:
        arm.control_gripper(-45)




"""
By: Promish and Hunter
Function moves the arm to the correct dropoff location that is optained
from the dropoff function in the form of a list
"""
def Move_EndEffector (drop_off_location, arm_threshold):
    
    #EmG value being evaluted for right flex and left flex
    if arm_threshold[0] == 1 and arm_threshold[1] == 1:
        time.sleep(1.5)
        arm.move_arm (drop_off_location[0], drop_off_location[1], drop_off_location[2])
        return print ("Moving to AutoClave")

    #EmG value being evaluted for left unflex and right unflex
    elif arm_threshold[0] == -1 and arm_threshold[1] == -1:
        arm.move_arm(0.4064, 0.0, 0.4826)
        return print ("Moving to home position")




"""
By Promish
Function identifies which cage was spanwed using the binID that is passed
down as a parameter in the function
"""
def Identify_Autoclave_Bin(binID):

    if binID == 1:
        print("Small Red cage was spawned")

    elif binID == 2:
        print("Small Red cage was spawned")

    elif binID == 3:
        print("Small Red cage was spawned")

    elif binID == 4:
        print("Big Red cage was spawned")

    elif binID == 5:
        print("Big Green cage was spawned")

    elif binID == 6:
        print("Big Blue cage was spawned")

        
"""
By: Promish 
Driver function that runs the code
"""
def main():

    #This is only for the interview to make things for efficient when demoing program
    #binID = 5

    
    #Random cage is spawed using a random number generator     
    #In a real world application this would be the code to spawn random cages
    binID = random.randint(1,6)


    arm.spawn_cage(binID)

    #Calling Identify_Autoclave_Bin function
    Identify_Autoclave_Bin(binID)

    
    #Correct dropoff location is optained from dropoff() function
    drop_off_location = dropoff(binID)

    #Variable for running terminate condition is created
    terminate = True

    #Infinte loop in order for the program to keep checking flex position
    while (terminate):

        """
        List that stores the initial flex data for both arms
        and is passed down to Armcheck which the value is stored in
        list arm_threshold
        """
        data_arm = [arm.emg_left(), arm.emg_right()]
        arm_threshold = Armcheck(data_arm)


        #Calling Move_EndEffector function
        Move_EndEffector(drop_off_location, arm_threshold)

        #Calling Control_Gripper function
        Control_Gripper(arm_threshold)
        

        """
        Checking to see if a Drawer needs to be opened based on the
        binID (4,5 and 6 are big cages)
        """
        if binID == 4:
            Open_AutoClave_BinDrawer (binID, arm_threshold)
            Close_AutoClave_BinDrawer (binID, arm_threshold)

            
        elif binID == 5:
            Open_AutoClave_BinDrawer (binID, arm_threshold)
            Close_AutoClave_BinDrawer (binID, arm_threshold)
            

            
        elif binID == 6:
            Open_AutoClave_BinDrawer (binID, arm_threshold)
            Close_AutoClave_BinDrawer (binID, arm_threshold)

        else:
            print("NO Drawers need to be open for small cages")


        #EmG value being evaluted for left unflex and right no change
        if arm_threshold[0] == -1 and arm_threshold[1] == 0:
            arm.home()
            time.sleep(2)
            #Ask user if they want program to terminate using True and False input
            condition = input("Terminate program(run or end)?")
            if condition == "run":
                terminate = True

                #This is only for the interview to make things for efficient when demoing program
                #binID = 1 
                #In a real world application this would be the code to spawn random cages
                #binID = random.randint(1,6)
                #arm.spawn_cage(binID)
                #Identify_Autoclave_Bin(binID)
                
            else:
                terminate = False

      

        #Checks sensor data every 2 seconds 
        time.sleep(2)
        print(" ")
        print(" ")
        print(" ")


main()
print("Program has been terminated by user")
    
      
    

    
    

    
    









    


