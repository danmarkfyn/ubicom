import json
import random
from pydispatch import dispatcher

CHANGELOC = 0

random.seed = 123

locations = ["main room","playground","bathroom","location not available","not here"]
numKids = 10

def createTestData():    
    dictRes = {}
    for i in range(1,numKids):
        kid = {}
        kid["firstName"] = "kid" + str(i)
        kid["location"] = locations[random.randint(0,len(locations)-1)]
        kid["picture"] = "child" + str(i) + ".png"
        dictRes["child" + str(i)] = kid

    with open('child.json', 'w') as json_file:
        json.dump(dictRes, json_file,indent=4)


# Changes location of given ID to new location
# Params:
#   Sender:  ID of sender
#   message: Contains new location
def change_location_handler( sender, message ):
    if message in locations:
        with open('child.json', 'r+') as json_file:
            data = json.load(json_file)
            if sender in data.keys():
                #Modify Data
                #prevLocation = data.get(sender).get("location")
                data[sender]["location"] = message

                #Write data
                json_file.seek(0)
                json.dump(data, json_file, indent=4)
                json_file.truncate()
            else:
                #Child was not a key in file
                raise NameError("Child id not in database")
    else:
        #Location not in available locations
        raise ValueError("Location not in database")


dispatcher.connect(change_location_handler,signal=CHANGELOC,sender=dispatcher.Any)


#Infinite loop to modify locations in database
def modifyLoop():
    print("Enter \"exit\" at any time to exit\n")

    while True:
        print("Child ID (child1,child2...): ",end='')
        child = input()
        if "exit" == child:
            break;
        print("New Location (main room, bathroom, playground...): ",end='')
        location = input()
        if "exit" == location:
            break;
        try:
            dispatcher.send(signal=CHANGELOC,sender=child,message=location)
        except NameError as namErr:
            print("ERROR: " + str(namErr))
        except ValueError as valErr:
            print("ERROR: " + str(valErr))
        print("\n")

if __name__ == "__main__":
    try:
        f = open("child.json")
        print("Found file")
        f.close()
    except IOError:
        print("Generating json file")
        createTestData()
    finally:
        print()
    modifyLoop()