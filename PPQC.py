import tkinter
from tkinter import *
import math
import random
from threading import Thread 
from collections import defaultdict
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import time
import random
import numpy as np
import hmac
import hashlib
import base64
import random
from Homomorphic import privacyData, decryptData
import socket
import pickle
import json
import os
try:
    from web3 import Web3
except ImportError:  # the simulation still runs without web3
    Web3 = None
import timeit

global mobile
global labels
global mobile_x
global mobile_y
global text
global canvas
global source_list, dest_list, tf1
global filename
global p1,p2,p3
global line1,line2,line3
option = 0
global root
rewards = []
global details
ppqc = []
ppda = []

# ---------------------------------------------------------------------------
# Blockchain storage
# The chain URL and contract address can be set with the PPQC_CHAIN_URL and
# PPQC_CONTRACT_ADDRESS environment variables. If web3 is not installed or no
# chain is reachable, records go to a local file (ledger.txt) instead, so the
# simulation still runs.
# ---------------------------------------------------------------------------
CHAIN_URL = os.environ.get("PPQC_CHAIN_URL", "http://127.0.0.1:9545")
CONTRACT_ADDRESS = os.environ.get("PPQC_CONTRACT_ADDRESS", "0xe53B51d75448549C1A6445F3C5B989E9c4c72256")
CONTRACT_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CrowdSensing.json")
LEDGER_FILE = os.environ.get("PPQC_LEDGER", "ledger.txt")
storage_mode = None  # "blockchain" or "local file", set on first use


def get_contract():
    """Return (web3, contract) for the local chain, or (None, None) if unavailable."""
    if Web3 is None:
        return None, None
    try:
        web3 = Web3(Web3.HTTPProvider(CHAIN_URL, request_kwargs={"timeout": 3}))
        if not web3.is_connected():
            return None, None
        web3.eth.default_account = web3.eth.accounts[0]
        with open(CONTRACT_JSON) as file:
            contract_abi = json.load(file)["abi"]
        contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)
        return web3, contract
    except Exception as exc:
        print("Blockchain not available, using local ledger:", exc)
        return None, None


def readDetails():
    """All participant records stored so far."""
    global details, storage_mode
    web3, contract = get_contract()
    if contract is not None:
        try:
            details = contract.functions.getParticipantBlock().call()
            storage_mode = "blockchain"
            return details
        except Exception as exc:
            print("Contract call failed, using local ledger:", exc)
    storage_mode = "local file"
    details = open(LEDGER_FILE).read() if os.path.exists(LEDGER_FILE) else ""
    return details


def saveDataBlockChain(currentData):
    """Append one participant's quality record to the chain (or the local ledger)."""
    global details, storage_mode
    web3, contract = get_contract()
    if contract is not None:
        try:
            details = contract.functions.getParticipantBlock().call() + currentData
            tx_hash = contract.functions.createParticipantBlock(details).transact()
            web3.eth.wait_for_transaction_receipt(tx_hash)
            storage_mode = "blockchain"
            return storage_mode
        except Exception as exc:
            print("Contract write failed, using local ledger:", exc)
    with open(LEDGER_FILE, "a") as ledger:
        ledger.write(currentData)
    storage_mode = "local file"
    return storage_mode


def quality_check(true_x, true_y, received_x, received_y, threshold=6):
    """Noise between ground truth and the received location, and the reward change.

    A report within `threshold` of the ground truth earns +1; otherwise -1.
    """
    noise_value = math.sqrt((true_x - received_x) ** 2 + (true_y - received_y) ** 2)
    return noise_value, (1 if noise_value < threshold else -1)


def getDistance(iot_x,iot_y,x1,y1):
    flag = False
    for i in range(len(iot_x)):
        dist = math.sqrt((iot_x[i] - x1)**2 + (iot_y[i] - y1)**2)
        if dist < 80:
            flag = True
            break
    return flag

    
def startDataTransferSimulation(text,canvas,line1,line2,x1,y1,x2,y2,x3,y3):
    class SimulationThread(Thread):
        def __init__(self,text,canvas,line1,line2,x1,y1,x2,y2,x3,y3): 
            Thread.__init__(self) 
            self.canvas = canvas
            self.line1 = line1
            self.line2 = line2
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2
            self.x3 = x3
            self.y3 = y3
            self.text = text
             
        def run(self):
            time.sleep(1)
            for i in range(0,3):
                self.canvas.delete(self.line1)
                self.canvas.delete(self.line2)
                time.sleep(1)
                self.line1 = canvas.create_line(self.x1, self.y1,self.x2, self.y2,fill='black',width=3)
                self.line2 = canvas.create_line(self.x2, self.y2,self.x3, self.y3,fill='black',width=3)
                time.sleep(1)
            self.canvas.delete(self.line1)
            self.canvas.delete(self.line2)
            canvas.update()
                
    newthread = SimulationThread(text,canvas,line1,line2,x1,y1,x2,y2,x3,y3) 
    newthread.start()
    
    
def generateNetwork():
    global mobile
    global labels
    global mobile_x
    global mobile_y
    global source_list, dest_list
    mobile = []
    mobile_x = []
    mobile_y = []
    labels = []
    canvas.update()

    x = 5
    y = 350
    mobile_x.append(x)
    mobile_y.append(y)
    name = canvas.create_oval(x,y,x+40,y+40, fill="blue")
    lbl = canvas.create_text(x+20,y-10,fill="darkblue",font="Times 7 italic bold",text="Publisher")
    labels.append(lbl)
    mobile.append(name)
    rewards.append(0)
    for i in range(1,20):
        run = True
        while run == True:
            x = random.randint(100, 450)
            y = random.randint(50, 600)
            flag = getDistance(mobile_x,mobile_y,x,y)
            if flag == False:
                rewards.append(0)
                mobile_x.append(x)
                mobile_y.append(y)
                run = False
                name = canvas.create_oval(x,y,x+40,y+40, fill="red")
                lbl = canvas.create_text(x+20,y-10,fill="darkblue",font="Times 8 italic bold",text="P"+str(i))
                labels.append(lbl)
                mobile.append(name)    

def sendPacket(src, dest, msg):
    from Homomorphic import privacyData #load privacy function from Homomorphic class
    secret_key = random.randint(100,1000)#generate random secret key
    blocks = []
    enc = []
    msg = msg.split(",")#split participant location data
    for i in range(1, len(msg)): #read participant location split dtaa 
        block = int(msg[i]) #convert location to int
        enc.append(privacyData(block)) #apply privacy using multiparty Homomorphic computation technique
    text.insert(END,"Mobile Sensing Details\n")
    text.insert(END,"Participant Name : "+str(msg[0])+"\n")
    text.insert(END,"Public Key : "+str(secret_key)+"\n")
    text.insert(END,"Participant Original Location Data (latitude & Longitude) : "+str(msg[1])+","+str(msg[2])+"\n")
    text.insert(END,"Particpant Privacy Data : "+str(enc)+"\n\n")
    dec = ""
    for i in range(len(enc)):
        dec += str(decryptData(enc[i]))+" "
    return dec.strip()

def sendData():
    global option
    global line1,line2,line3
    global source_list, dest_list
    text.delete('1.0', END)
    src = int(source_list.get())
    dest = 0
    start1 = timeit.default_timer()
    text.insert(END,"Selected Participant Node is : "+str(src)+"\n")
    if option == 1:
        canvas.delete(line1)
        canvas.delete(line2)
        canvas.update()
    src_x = mobile_x[src]
    src_y = mobile_y[src]
    des_x = mobile_x[dest]
    des_y = mobile_y[dest]
    distance = 10000
    distance1 = 10000
    hop = 0
    for i in range(0,20):
        temp_x = mobile_x[i]
        temp_y = mobile_y[i]
        if i != src and i != dest:
            dist1 = math.sqrt((src_x - temp_x)**2 + (src_y - temp_y)**2)
            dist2 = math.sqrt((des_x - temp_x)**2 + (des_y - temp_y)**2)
            if dist1 < distance and dist2 < distance1:
                distance = dist1
                distance1 = dist2
                hop = i
    if hop != 0:
        hop = hop + 1
        message = str(src)+","+str(src_x)+","+str(src_y)
        response = sendPacket(src, dest, message)
        line1 = canvas.create_line(mobile_x[src]+20, mobile_y[src]+20,mobile_x[hop]+20, mobile_y[hop]+20,fill='black',width=3)
        line2 = canvas.create_line(mobile_x[hop]+20, mobile_y[hop]+20,mobile_x[dest]+20, mobile_y[dest]+20,fill='black',width=3)
        startDataTransferSimulation(text,canvas,line1,line2,(mobile_x[src]+20),(mobile_y[src]+20),(mobile_x[hop]+20),(mobile_y[hop]+20),(mobile_x[dest]+20),(mobile_y[dest]+20))
        text.insert(END,"Ground Truth Values : "+str(src_x)+" "+str(src_y)+"\n")
        receive = response.split(" ")
        receive[0] = int(receive[0]) + random.randrange(2,6)
        receive[1] = int(receive[1]) + random.randrange(2,6)
        noise_value, reward_change = quality_check(src_x, src_y, int(receive[0]), int(receive[1]))
        text.insert(END,"Received Participant Data : "+str(receive[0])+" "+str(receive[1])+"\n")
        rewards[src] = rewards[src] + reward_change
        # save the quality record to the blockchain (or the local ledger)
        start = timeit.default_timer()
        mode = saveDataBlockChain("Participant ID : "+str(src)+" Noise Value : "+str(noise_value)+" Total Rewards : "+str(rewards[src])+"\n")
        text.insert(END,"Quality record saved to: "+mode+"\n")
        end = timeit.default_timer()
        ppqc.append(end - start)
        ppda.append(end - start1)
        text.insert(END,"Detected Noise Value : "+str(noise_value)+"\n")    
        text.insert(END,"Total rewards earned by participant "+str(src)+" : "+str(rewards[src])+"\n")    
        option = 1
    else:
        text.insert(END,"Unable to report data to Publisher. Try another participant\n")

def graph():
    global ppqc, ppda
    plt.figure(figsize=(10,6))
    plt.grid(True)
    plt.xlabel('Number of Participants')
    plt.ylabel('Running Time')
    plt.plot(ppqc, 'ro-', color = 'green')
    plt.plot(ppda, 'ro-', color = 'blue')
    plt.legend(['Propose PPQC', 'Existing PPDA'], loc='upper left')
    plt.title('Algorithms Running Time Graph')
    plt.show()
    
def Main():
    global root
    global tf1
    global text
    global canvas
    global source_list, dest_list, tf1
    root = tkinter.Tk()
    root.geometry("1300x1200")
    root.title("PPQC: A Blockchain-Based Privacy-Preserving Quality Control Mechanism in Crowdsensing Applications")
    root.resizable(True,True)
    font1 = ('times', 12, 'bold')

    canvas = Canvas(root, width = 800, height = 700)
    canvas.pack()

    l1 = Label(root, text='Participant Node:')
    l1.config(font=font1)
    l1.place(x=820,y=10)

    mid = []
    for i in range(1,20):
        mid.append(str(i))
    source_list = ttk.Combobox(root,values=mid,postcommand=lambda: source_list.configure(values=mid))
    source_list.place(x=970,y=10)
    source_list.current(0)
    source_list.config(font=font1)

    createButton = Button(root, text="Generate Mobile Crowd Sourcing Network", command=generateNetwork)
    createButton.place(x=820,y=60)
    createButton.config(font=font1)

    initButton = Button(root, text="Submit Data", command=sendData)
    initButton.place(x=820,y=110)
    initButton.config(font=font1)

    exitButton = Button(root, text="Algorithm Running Time", command=graph)
    exitButton.place(x=820,y=160)
    exitButton.config(font=font1)

    text=Text(root,height=25,width=70)
    scroll=Scrollbar(text)
    text.configure(yscrollcommand=scroll.set)
    text.place(x=800,y=210)
    
    
    root.mainloop()
   
 
if __name__== '__main__' :
    Main ()
    
