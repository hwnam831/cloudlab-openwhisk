import requests
import json
import os
import socket
import time
import threading
import sys
import signal
import subprocess
import re
import random
random.seed(time.time())

def signal_handler(sig, frame):
    serverSocket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def parse_lscpu():
    tpc = subprocess.check_output('lscpu | grep -i \"Thread(s) per core\"',shell=True).decode("utf-8")
    threadspercore = int(re.match(r".+\:\s+(\d+)\n",tpc).group(1))
    cps = subprocess.check_output('lscpu | grep -i \"Core(s) per socket\"',shell=True).decode("utf-8")
    corepersocket = int(re.match(r".+\:\s+(\d+)\n",cps).group(1))
    sck = subprocess.check_output('lscpu | grep -i \"Socket(s)\"',shell=True).decode("utf-8")
    sockets = int(re.match(r".+\:\s+(\d+)\n",sck).group(1))
    return threadspercore, corepersocket, sockets

threadspercore, corepersocket, num_socket = parse_lscpu() 

pkg_to_cpuset = [str(i*corepersocket)+'-'+str(i*corepersocket+corepersocket-1) for i in range(num_socket)]
pkg_funcs = [[] for _ in range(num_socket)]
func_to_pkg = {}


# Set bind address and port
myHost = '0.0.0.0'
myPort = 5656

# Create a socket for receiving connections
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serverSocket.bind((myHost, myPort))
serverSocket.listen(1)

# map functions to owning cores
mapFuncToSetCores = {}
# map function to container ids
mapFuncToContainers = {}
# map physical cores to function owners
mapCores = {}
# map functions to regions (safe to donate core, not safe to donate core)
mapFuncToRegions = {}
# set of free cores
setFreeCores = set()
# map functions to classes
mapFuncToClass = {}
mapFuncToSocket = {
    'matmul':0,
    'linpack':0,
    'primes':0,
    'ml_training':0,
    'video_processing':0,
    'cnn_serving':0,
    'lr_serving':0,
    'img-rotate':0,
    'base64':0,
    'rnn_serving':0,
    'matmul1':1,
    'linpack1':1,
    'primes1':1,
    'ml_training1':1,
    'video_processing1':1,
    'cnn_serving1':1,
    'lr_serving1':1,
    'img-rotate1':1,
    'base641':1,
    'rnn_serving1':1
}

lockStatus = threading.Lock()

# initialize mapCores and setFreeCores (FIXME: need to change to range according to number of cores)
for i in range(0, 20):
    mapCores[i] = "none"
    setFreeCores.add(i)


# docker command to check if container exists --> docker ps -q -f id=C_ID
# docker command to set cpus for a given container --> docker update --cpuset-cpus CPUS C_ID

# kn service update  hello --request cpu=2

# https://kubernetes.io/docs/tasks/administer-cluster/cpu-management-policies/

def delete_func(func):

    del mapFuncToSetCores[func]
    del mapFuncToContainers[func]
    #del mapFuncToRegions[func]
    pkg = func_to_pkg[func]
    del func_to_pkg[func]
    for core in mapCores:
        if mapCores[core] == func:
            mapCores[core] = "none"
            setFreeCores.add(core)
    pkg_funcs[pkg].remove(func)

def allocator(funcName):
    if funcName in mapFuncToSocket:
        return mapFuncToSocket[funcName]
    else:
        return random.randint(0,num_socket-1)

def checkThread():

    # init global variables
    global mapFuncToContainers
    global mapFuncToSetCores
    global mapCores
    global mapFuncToRegions
    global setFreeCores
    global mapFuncToClass
    global pkg_funcs

    while True:
        time.sleep(0.1)
        lockStatus.acquire()
        for func in list(mapFuncToSetCores):
            container = mapFuncToContainers[func]
            output = ((subprocess.check_output("docker ps -q -f id="+str(container), shell=True)).decode("utf-8"))[:-1]
            
            # The container has been deleted
            if output == "":
                delete_func(func)

            # The container is still running
            # To check if the container is safe to donate cores
            '''
            else:
                try:
                    configs = {"Q":"Safe?"}
                    cmdQA = "docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' " + str(container)
                    output = ((subprocess.check_output(cmdQA, shell=True)).decode("utf-8"))[:-1]
                    while True:
                        try:
                            rsp = requests.post('http://' + str(output) + ':1111', json=configs)
                            break
                        except:
                            pass
                    isSafe = (json.loads(rsp.text))["Response"]
                    mapFuncToRegions[func] = isSafe
                except:
                    pass
                '''
                
        lockStatus.release()



threadChecker = threading.Thread(target=checkThread)
threadChecker.start()

#TODO: use docker stat to balance?
def loadBalancer():

    # init global variables
    global mapFuncToContainers
    global mapFuncToSetCores
    global mapCores
    global mapFuncToRegions
    global setFreeCores
    global mapFuncToClass
    global pkg_funcs

    while True:
        time.sleep(1)
        pkgload = [len(funcs) for funcs in pkg_funcs]
        if  max(pkgload) - min(pkgload) <= 1:
            minpkg, maxpkg = random.sample(list(range(len(pkgload))),2)
            continue
        else:
            minpkg = pkgload.index(min(pkgload))
            maxpkg = pkgload.index(max(pkgload))
        lockStatus.acquire()
        maxlen = len(pkg_funcs[maxpkg])
        if maxlen < 1:
            lockStatus.release()
            continue
        funcName = pkg_funcs[maxpkg][random.randint(0,len(pkg_funcs[maxpkg])-1)]
        
        mapFuncToSetCores[funcName] = pkg_to_cpuset[minpkg]
        pkg_funcs[maxpkg].remove(funcName)
        pkg_funcs[minpkg].append(funcName)
        func_to_pkg[funcName] = minpkg
        lockStatus.release()
        cmdToExec = "docker update --cpuset-cpus " + mapFuncToSetCores[funcName] +\
                    " " + str(mapFuncToContainers[funcName])
        print(cmdToExec)
        try:
            subprocess.check_output(cmdToExec, shell=True)
        except:
            print("docker update failed?")
            pass
#balancer = threading.Thread(target=loadBalancer)
#balancer.start()
print("wait on requests")



while True:
    # Wait for a connection from a client
    (clientSocket, address) = serverSocket.accept()
    clientAddress = address[0]
    while True:
        try:
            data_ = clientSocket.recv(1024)
            dataStr = data_.decode('UTF-8')
            dataStrList = dataStr.splitlines()
            message = json.loads(dataStrList[-1])
            break
        except Exception as e:
            print("Error 1 == " + str(dataStr) + " == " + str(e))
            pass

    
    funcName = message["funcName"]
    containerName = message["containerName"]
    #containerName = funcName 
    numReqCores = int(message["numReqCores"])
    # funcClass = int(message["funcClass"])

    lockStatus.acquire()
    

    print(funcName)
    print(numReqCores)
    print(containerName)
    if funcName in mapFuncToSetCores:
        delete_func(funcName)
    #Naive algorithm: random distribution
    pkg_id = allocator(funcName)
    mapFuncToSetCores[funcName] = pkg_to_cpuset[pkg_id]
    mapFuncToContainers[funcName] = containerName
    func_to_pkg[funcName] = pkg_id
    pkg_funcs[pkg_id].append(funcName)

    lockStatus.release()
    result = {"Response": list(mapFuncToSetCores[funcName])}
    msg = json.dumps(result)
    clientSocket.send(msg.encode(encoding="utf-8"))
    clientSocket.close()
    cmdToExec = "docker update --cpuset-cpus " + mapFuncToSetCores[funcName] + " " + str(containerName)
    print(cmdToExec)
    try:
        subprocess.check_output(cmdToExec, shell=True)
    except:
        print("docker update failed?")
        pass

'''
    if numReqCores < 0:
        continue
        # If a function is deleted, free all cores
        # TODO: un implemented
        clientSocket.close()
        coresToFree = message["freeCores"]
        if len(mapFuncToSetCores[funcName]) == len(coresToFree):
            print("Free all cores :O " + funcName)
        for coreF in coresToFree:
            setFreeCores.add(coreF)
            try:
                mapFuncToSetCores[funcName].remove(coreF)
            except:
                print(str(funcName) + " " + str(containerName) + " " + str(coreF))
                pass
        cmdToExec = "docker update --cpuset-cpus " + (str(list(mapFuncToSetCores[funcName]))[1:-1]).replace(" ","") + " " + str(containerName)
        try:
            subprocess.check_output(cmdToExec, shell=True)
        except:
            pass
        strToPrint = ""
        for func in mapFuncToSetCores:
            strToPrint += " " + str(len(mapFuncToSetCores[func]))
        print(strToPrint)
        lockStatus.release()
    else:
        # If a function is request for more cores
        mapFuncToContainers[funcName] = containerName
        # mapFuncToClass[funcName] = funcClass
        result = {}
        donors = set()
        mapDonorToCore = {}
        if funcName not in mapFuncToRegions:
            mapFuncToRegions[funcName] = "non-safe"
        numCoresBefore = 0
        if funcName in mapFuncToSetCores:
            numCoresBefore = len(mapFuncToSetCores[funcName])
        numProvidedCores = 0
        for i in range(0, numReqCores):
            if len(setFreeCores) > 0:
                numProvidedCores += 1
                freeCore = setFreeCores.pop()
                mapCores[freeCore] = funcName
                if funcName not in mapFuncToSetCores:
                    mapFuncToSetCores[funcName] = set()
                mapFuncToSetCores[funcName].add(freeCore)
        safeFuncs = set()
        for funcSafe in mapFuncToRegions:
            if mapFuncToRegions[funcSafe] == "safe":
                safeFuncs.add(funcSafe)
        while numProvidedCores < numReqCores:
            potentialDonors = set()
            for funcDon in mapFuncToRegions:
                if ((funcDon!=funcName) and ((mapFuncToRegions[funcDon]) == "safe") and (len(mapFuncToSetCores[funcDon])>2) and (mapFuncToClass[funcName] < mapFuncToClass[funcDon])) or ((mapFuncToClass[funcName] < mapFuncToClass[funcDon]) and ((len(mapFuncToSetCores[funcDon])>1))):
                    potentialDonors.add(funcDon)
            maxNumCores = 0
            realFuncDon = ""
            for potDonor in potentialDonors:
                if len(mapFuncToSetCores[potDonor]) > maxNumCores:
                    maxNumCores = len(mapFuncToSetCores[potDonor])
                    realFuncDon = potDonor
            if realFuncDon != "":
                numProvidedCores += 1
                donors.add(realFuncDon)
                donatedCore = mapFuncToSetCores[realFuncDon].pop()
                mapCores[donatedCore] = funcName
                if funcName not in mapFuncToSetCores:
                    mapFuncToSetCores[funcName] = set()
                mapFuncToSetCores[funcName].add(donatedCore)
                mapDonorToCore[realFuncDon] = donatedCore
            else:
                break
        numCoresAfter = len(mapFuncToSetCores[funcName])
        lockStatus.release()
        if numCoresAfter < numCoresBefore + numReqCores:
            print("DID NOT PROVIDE ENOUGH CORES! " + funcName + " " + str(numCoresBefore)+  " " + str(numReqCores))
        result = {"Response": list(mapFuncToSetCores[funcName])}
        msg = json.dumps(result)
        clientSocket.send(msg.encode(encoding="utf-8"))
        clientSocket.close()
        try:
            cmdToExec = "docker update --cpuset-cpus " + (str(list(mapFuncToSetCores[funcName]))[1:-1]).replace(" ","") + " " + str(containerName)
            subprocess.check_output(cmdToExec, shell=True)
        except:
            pass
        strToPrint = ""
        for func in mapFuncToSetCores:
            strToPrint += " " + str(len(mapFuncToSetCores[func]))
        print(strToPrint)
        for donor in donors:
            try:
                cmdToExecDonor = "docker update --cpuset-cpus " + (str(list(mapFuncToSetCores[donor]))[1:-1]).replace(" ","") + " " + str(mapFuncToContainers[donor])
                subprocess.check_output(cmdToExecDonor, shell=True)
            except:
                pass
            configs = {"evictedCore":mapDonorToCore[donor]}
            cmdUpd = "docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' " + str(mapFuncToContainers[donor])
            output = ((subprocess.check_output(cmdUpd, shell=True)).decode("utf-8"))[:-1]
            while True:
                try:
                    requests.post('http://' + str(output) + ':5500', json=configs)
                    break
                except:
                    pass
'''
