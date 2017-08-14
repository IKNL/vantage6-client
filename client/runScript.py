import json
import requests
import time
import os

# connect to service
headerData = {
    'Content-Type': "application/json"
}

# Init configuration file
configFile = open("config.json")
clientData = json.load(configFile)
configFile.close()

if "id" not in clientData:
    # execute HTTP POST to try and authenticate
    resp = requests.post(clientData["masterUrl"] + "/client/add", data=json.dumps(clientData), headers=headerData)
    respObj = json.loads(resp.text)
    clientId = respObj.get('clientId', '')
    clientData["id"] = clientId
    configFile = open("config.json", "w")
    json.dump(clientData, configFile)
    configFile.close()

print("Starting with client ID " + str(clientData["id"]))

abort = 0

while abort == 0:
    taskList = list()

    # Connect to central host, if fails do nothing
    try:
        resp = requests.get(clientData["masterUrl"] + "/client/" + str(clientData["id"]) + "/task")
        taskList = json.loads(resp.text)
    except:
        print("Could not retrieve result from master.")

    # If no task retrieved (or central host down) wait again
    if len(taskList) == 0:
        print("Waiting....")
        time.sleep(clientData["interval"])

    # If there are tasks retrieved, proces task list
    iTask = 0
    while iTask < len(taskList):
        myTask = taskList[iTask]
        taskId = myTask.get('id')
        image = myTask.get('image')
        inputText = myTask.get("input")
        imageResponse = "output.txt"

        #create directory to put files into
        curFolder = os.getcwd()+"\\task"+str(taskId)
        os.mkdir(curFolder)

        #put the input arguments in a text file
        inputFilePath = curFolder+"\\input.txt"
        text_file = open(inputFilePath, "w")
        text_file.write(inputText)
        text_file.close()

        outputFilePath = curFolder+"\\output.txt"
        text_file = open(outputFilePath, "w")
        text_file.write(inputText)
        text_file.close()

        #pulling the image for updates or download
        os.system("docker pull " + image)

        #create the command line execution line
        dockerExecLine = "docker run -v " + inputFilePath + ":/input -v " + outputFilePath + ":/output " + image
        print("running: " + dockerExecLine)
        os.system(dockerExecLine)

        file = open(outputFilePath, 'r')
        responseText = file.read()
        file.close()

        responseData = {
            'response': str(responseText)
        }

        # execute HTTP POST to send back result (response)
        resp = requests.post(
            clientData["masterUrl"] + "/client/" + str(clientData["id"]) + "/task/" + str(taskId) + "/result/add",
            data=json.dumps(responseData), headers=headerData)
        respObjResult = json.loads(resp.text)
        print("resultId" + str(respObjResult["taskId"]))
        iTask += 1