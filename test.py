import json
import random

random.seed = 123
locations = ["main room","playground","bathroom","not here"]
numKids = 10

if __name__ == "__main__":
    dictRes = {}
    for i in range(1,numKids):
    	kid = {}
    	kid["firstName"] = "kid" + str(i)
    	kid["location"] = locations[random.randint(0,3)]
    	kid["picture"] = "child" + str(i) + ".png"
    	dictRes["child" + str(i)] = kid

    with open('child.txt', 'w') as json_file:
        json.dump(dictRes, json_file)


def detectKid(id,location):
    with open('child.json', 'r+') as json_file:
        data = json.loads(json.load(json_file))

        data[id,"location"] = location

        json.dump(data, json_file)