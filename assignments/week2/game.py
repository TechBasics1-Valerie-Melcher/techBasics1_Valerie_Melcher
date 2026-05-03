# This is my Week2 assignment "Catch Charlie" The goal is to catch the imaginary chicken Charlie by choosing the right options.
print (' Hello there !')
import time
time.sleep(1)
print (' What is your name? ')
name = input (" Please enter your name: ")
time.sleep(1)
print (' Hello,', name)

time.sleep(2)
print (' I have a problem.')
time.sleep(1)

print (' My beloved chicken Charlie escaped the barn this morning. Can you help me,', name, ' ? ')
time.sleep(1)
print ( ' Please choose an option ')
time.sleep(1)
print (' 1. Of course! ')
print (' 2. Uh, sure? ')
print (" 3. Let's find Charlie! ")
time.sleep(1)
choice = input (" Enter choice 1-3: ")

valid = False
while not valid:


    if choice == "1":
        print (" Thank you! ")
        valid = True

    elif choice == "2":
        print (" I promise it won't take long ")
        valid = True
    elif choice == "3":
        print (" Let's go! ")
        valid = True
    else:
        choice = input ("Invalid choice, Try again: ")
        valid = False



time.sleep(2)
print (" He has to be either in the house, in the backyard, or by the frog pond")
time.sleep(1)
print ("Where should we look first?")

print ("Please choose an option")
time.sleep(1)
print (" 1. Let's start in the house! ")
print (" 2. Hmm, maybe in the backyard? ")
print (" 3. The frog pond sounds like a good starting point. ")

choice = input ("Enter choice 1-3: ")
if choice == "1":
    print (" Alright, let's start there. ")

    time.sleep(2)
    print (" We made it to the house. Let's try calling him. Can you please yell something to get his attention? ")
    command = input (" Say something to Charlie: ")

    time.sleep(2)
    print (" Hm, nothing. I guess he's not in here. ")
    time.sleep(1)
    print (" Where should we go next,", name, "? ")
    time.sleep(1)
    print(" 1. To the backyard then ")
    print(" 2. He must be at the frog pond! ")
    time.sleep(1)
    choice = input (" Please choose an option: ")

    valid = True

    while not valid:
        choice = input (" Please choose an option: ")

    if choice == "1":
        print (" Good idea! !")
        valid = True

        time.sleep(1)
        print (" Alright, let's try our luck here in the backyard. ")
        time.sleep(1)
        print (" Why don't you try calling Charlie again? ")
        time.sleep(1)

        choice = input (" Call Charlie: ")

        time.sleep(2)

        print (" Nothing again. Surely he must be at the frog pond then. Let's go! ")

        time.sleep(1)

        print (" Okay, this is our last hope. Let me try calling Charlie this time. ")
        time.sleep(1)
        print (" Charlieee?? Are you hereee? ")
        time.sleep (1)
        print (" Oh no, he's not here either! My poor Charlie, where could he be? ")
        time.sleep(1)
        print (" Wait, I here something! Don't you?" )
        time.sleep(1)
        choice = input (" Say something: ")
        time.sleep(1)
        print (" Over there by the barn! Let's go check! ")

        time.sleep(2)

        print (" I can't believe it! He was hiding behind the barn this whole time! ")
        time.sleep(1)
        print (" Oh I am so glad that he is safe, thank you for your help!")

        choice = input (" Say something: ")
        time.sleep (2)

        print (" You've reached the end of this short game I made! Thanks for playing! :) ")


    elif choice == "2":
        print (" You might be right. ")
        valid = True

        time.sleep(2)

        print (" Welcome to our little frog pond! It's not a great hiding spot, but it sure is pretty! ")
        time.sleep(1)
        print (" If Charlie is close, he will hear if you call him. Would you please try? ")
        time.sleep(1)
        choice = input (" Call Charlie: ")
        time.sleep(1)
        print (" Seems he's not close. Should we go back and see if he's in the backyard? ")
        time.sleep(1)

        print (" 1. Yes, let's go find him! ")
        print (" 2. Hm, I have to leave soon. ")

        choice = input (" Should we go?: ")

        valid = False
        while not valid:
            choice = input (" Option 1 or 2?: ")

            if choice == "1":
                print (" I really hope we'll find him there! ")
                valid = True

            elif choice == "2":
                print (" Let's hope he's there! ")
                valid = True

            else:
                choice = input ("Invalid choice, try again!: ")
                valid = False

        time.sleep(1)

        print (" Alright, this is our last option. Do you think we'll find Charlie here?" )
        choice = input (" Say something: ")
        time.sleep(1)

        print (" I can only hope he'll respond if I call him. ")
        time.sleep(1)
        print (" Charlie?! Where are youuuu? ")
        time.sleep(2)

        print (" BAWK-BaAaWwK ")
        time.sleep(1)
        print (" Charlie?!? Is that you? ")
        time.sleep (1)
        print (" Oh it's him, it's him! We finally found him! ")
        time.sleep(1)
        print (" Thank you so much for your help,", name, "! ")
        time.sleep(1)
        choice = input ("Say something: ")

        time.sleep (2)
        print ("You've reached the end of this short game I made! Thanks for playing! :)")


    else:
       choice = input (" Invalid choice, Try again: ")

    time.sleep(1)


elif choice == "2":
    print ("He might be there, let's go see!")
    time.sleep(1)

    print ("The backyard looks empty. Let's look around anyway.")
    time.sleep(1)

    print ("Could you please try calling Charlie?")
    time.sleep(2)
    choice = input ("Say something: ")

    print ("Hm, he doesn't seem to be here.")
    time.sleep(1)

    print ("We should look for him in the other spots. ")
    time.sleep(1)
    print ("Where should we go next?", name, "? ")
    time.sleep(1)
    print (" 1. The house ")
    print (" 2. The frog pond ")
    time.sleep(1)

    choice = input (" Please choose an option: ")

    valid = False
    while not valid:

        if choice == "1":
            print ("To the house then!")
            valid = True

            time.sleep(2)

            print (" We made it to the house. If Charlie is hiding here it will be hard to find him. ")
            time.sleep(1)

            time.sleep(1)
            print (" Charlie? Charlieeee?")
            time.sleep(1)

            print ("Would you try calling him, please?")
            time.sleep(1)

            choice = input ("Say something: ")

            print ("Oh man, he's not here..")
            time.sleep(1)

            print ("Seems like the frog pond is our last option.")
            time.sleep(1)

            print(" I can only hope he'll respond if I call him. ")
            time.sleep(1)
            print(" Charlie?! Where are youuuu? ")
            time.sleep(2)

            print(" BAWK-BaAaWwK ")
            time.sleep(1)
            print(" Charlie?!? Is that you? ")
            time.sleep(1)
            print(" Oh it's him, it's him! We finally found him! ")
            time.sleep(1)
            print(" Thank you so much for your help,", name, "! ")
            time.sleep(1)
            choice = input("Say something: ")

            time.sleep(2)
            print("You've reached the end of this short game I made! Thanks for playing! :)")

        elif choice == "2":
            print (" Okay, let's try the frog pond! ")
            valid = True

            print(" Welcome to our little frog pond! It's not a great hiding spot, but it sure is pretty! ")
            time.sleep(1)
            print(" If Charlie is close, he will hear if you call him. Would you please try? ")
            time.sleep(1)
            choice = input(" Call Charlie: ")
            time.sleep(1)
            print(" Seems he's not close. Should we go back and see if he's in the house? ")
            time.sleep(1)

            choice = input ("Say something: ")

            time.sleep(1)
            print ("The house is out last option, we should go check.")
            time.sleep(1)
            print(" We made it to the house. If Charlie is hiding here it will be hard to find him. ")
            time.sleep(1)

            time.sleep(1)
            print(" Charlie? Charlieeee?")
            time.sleep(1)

            print("Would you try calling him, please?")
            time.sleep(1)
            choice = input ("Call Charlie: ")
            time.sleep(1)
            print(" BAWK-BaAaWwK ")
            time.sleep(1)
            print(" Charlie?!? Is that you? ")
            time.sleep(1)
            print(" Oh it's him, it's him! We finally found him! ")
            time.sleep(1)
            print(" Thank you so much for your help,", name, "! ")
            time.sleep(1)
            choice = input("Say something: ")

            time.sleep(2)
            print("You've reached the end of this short game I made! Thanks for playing! :)")


        else:
            choice = input ("Invalid choice, Please try again: ")
            valid = False


elif choice == "3":

        print(" Welcome to our little frog pond! It's not a great hiding spot, but it sure is pretty! ")
        time.sleep(1)
        print(" If Charlie is close, he will hear if you call him. Would you please try? ")
        time.sleep(1)
        choice = input(" Call Charlie: ")
        time.sleep(1)
        print(" Seems he's not close. Where should we go next?")
        time.sleep(1)
        print (" 1. The house ")
        print (" 2. The backyard ")
        choice = input ("Enter choice: ")

        valid = False
        while not valid:
            if choice == "1":
                valid = True

                time.sleep(2)
                print(" We made it to the house. Let's try calling him. Can you please yell something to get his attention? ")
                choice = input(" Say something to Charlie: ")

                time.sleep(2)
                print(" Hm, nothing. I guess he's not in here. ")
                time.sleep(1)

                print (" I guess he has to be in the backyard then. Let's go! ")

                time.sleep (1)
                print(" Alright, this is our last option. Do you think we'll find Charlie here?")
                choice = input(" Say something: ")
                time.sleep(1)

                print(" I can only hope he'll respond if I call him. ")
                time.sleep(1)
                print(" Charlie?! Where are youuuu? ")
                time.sleep(2)

                print(" BAWK-BaAaWwK ")
                time.sleep(1)
                print(" Charlie?!? Is that you? ")
                time.sleep(1)
                print(" Oh it's him, it's him! We finally found him! ")
                time.sleep(1)
                print(" Thank you so much for your help,", name, "! ")
                time.sleep(1)
                choice = input("Say something: ")

                time.sleep(2)
                print("You've reached the end of this short game I made! Thanks for playing! :)")

            elif choice == "2":

                valid =True
                time.sleep(1)
                print(" Alright, let's try our luck here in the backyard. ")
                time.sleep(1)
                print(" Why don't you try calling Charlie again? ")
                time.sleep(1)

                choice = input(" Call Charlie: ")

                time.sleep(2)

                print(" Nothing again. Surely he must be in the house then. Let's go! ")
                time.sleep(1)
                print(" We made it to the house. If Charlie is hiding here it will be hard to find him. ")
                time.sleep(1)

                print(" Charlie? Charlieeee?")
                time.sleep(1)

                print("Would you try calling him, please?")
                time.sleep(1)
                choice = input("Call Charlie: ")
                time.sleep(1)
                print(" BAWK-BaAaWwK ")
                time.sleep(1)
                print(" Charlie?!? Is that you? ")
                time.sleep(1)
                print(" Oh it's him, it's him! We finally found him! ")
                time.sleep(1)
                print(" Thank you so much for your help,", name, "! ")
                time.sleep(1)
                choice = input("Say something: ")

                time.sleep(2)
                print("You've reached the end of this short game I made! Thanks for playing! :)")

            else:
                choice = input ("Invalid choice, try again: ")
                valid = False




else:
        choice = input ("Invalid choice, try again!: ")



time.sleep(2)

