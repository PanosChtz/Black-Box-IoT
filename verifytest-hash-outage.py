import hashlib
from prettytable import PrettyTable
import time
import random
import json
import sys
import string
from ecdsa import SECP256k1
from ecdsa import SigningKey
import matplotlib as mpl
#mpl.use('pgf')
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker

def h(preimage):
    return hashlib.sha256(preimage.encode('utf-8')).hexdigest()
    
def FindValue(pebbleList,sigma):
    for i in range(1,sigma):
        if pebbleList[i].position == pebbleList[0].position:
            return pebbleList[i].value

class Pebble:
  def __init__(pj, StartIncr, DestIncr, position, destination, value):
    pj.StartIncr = StartIncr
    pj.DestIncr = DestIncr
    pj.position = position
    pj.destination = destination
    pj.value = value

def printpebbles(sigma):
    x = PrettyTable()
    x.field_names = ["j","StartIncr","DestIncr","position","destination","value"]
    i=0
    for i in range (i,sigma):
        x.add_row([i,pebbles[i].StartIncr,pebbles[i].DestIncr,pebbles[i].position,pebbles[i].destination,pebbles[i].value])
    print(x)
    

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def computeValue(sigma):
    global pos
    global pebbles
    if DEBUG: printpebbles(sigma)
    #1
    if (pos>=pow(2,sigma)):
        return None
    else:
        pos+=1
    #2
    for j in range (0,sigma):
        if pebbles[j].position != pebbles[j].destination:
            pebbles[j].position = pebbles[j].position - 2
            pebbles[j].value = h(h(pebbles[j].value))
    #3
    if (pos % 2 == 1):
        if DEBUG: print("odd number")
        output =  h(pebbles[0].value)
        if DEBUG: print("output:"+str(output))
    else:
        output = pebbles[0].value
        if DEBUG: print("even number,output:"+str(output))
        pebbles[0].position = pebbles[0].position + pebbles[0].StartIncr
        if DEBUG: print("Reached: reassign")
        pebbles[0].destination = pebbles[0].destination + pebbles[0].DestIncr
        if DEBUG: print("and reassign")
        if (pebbles[0].destination > pow(2,sigma)):
            if DEBUG: print("Pebble redundant,retire pebble")
            pebbles[0].destination = float("inf")
            pebbles[0].position = float("inf")
        else:
            if DEBUG: print("Call to set value")
            pebbles[0].value = FindValue(pebbles,sigma)
        pebbles.sort(key=lambda x: x.destination, reverse=False)
    return output



DEBUG = False
sigmaarray = [20,22,24,26]
MESSAGELENGTH = 100
OUTAGEDEPTH = int(6*10e+2)

graphtimers=[]




randomstr = randomString(MESSAGELENGTH-len(str(OUTAGEDEPTH)))
counter = OUTAGEDEPTH




timers=[]
for s in sigmaarray:
    pos = 0
    pebbles = []
    f = open( "pebblelist"+str(s)+".txt", 'r' )
    alldata = json.loads(f.read())
    f.close()
    for p in range (0,s):
        initval = alldata[str(p+1)]
        pebbles.append(Pebble(3*pow(2,p+1), pow(2,p+2),pow(2,p+1), pow(2,p+1), initval))
    pkinit = computeValue(s)
    message = randomstr + str(counter)
    
    
    
    s = len(alldata)
    for k in range (0,OUTAGEDEPTH):
        pk = computeValue(s)

    sk = computeValue(s)
    signature = [h(message+pk), sk]

    check = True
    timers.append([])
    depths = []
    start = time.time()
    check = check and (signature[0] == h(message+pk))
    j = 0
    notfound = True
    while ((j < OUTAGEDEPTH+1) and notfound):
        sk = h(sk)
        if (j % 500 == 0):
            timers[sigmaarray.index(s)].append(time.time() - start)
            depths.append(j)
        if pkinit == sk:
            notfound = False
            print("OK")
        j +=1
    end = time.time()
    print("Verifying time: " + str(end - start))

sk = SigningKey.generate(curve=SECP256k1)
pk = sk.verifying_key
MESSAGELENGTH = 100
TESTLENGTH = int(10e+2)
randomstr = randomString(MESSAGELENGTH-len(str(TESTLENGTH)))
counter = TESTLENGTH
signeddata = []


sk = SigningKey.generate(curve=SECP256k1)
pk = sk.verifying_key
for k in range (0,TESTLENGTH):
    message = randomstr + str(counter)
    signature = sk.sign(message.encode())
    signeddata.insert(0,[message,signature])
    counter +=1

ecdsatimers = []
for k in range (0,TESTLENGTH):
    message = signeddata[k][0]
    signature = signeddata[k][1]
    start = time.time()
    assert pk.verify(signature,message.encode())
    end = time.time()
    ecdsatimers.append(end-start)

ecdsagraphtime = sum(ecdsatimers)/len(ecdsatimers)

print("Average verifying time: " + str(ecdsagraphtime))


for k in range(0,len(timers[0])):
    graphtimers.append([timers[0][k],timers[1][k],timers[2][k],timers[3][k],ecdsagraphtime])

labelList = [] #initialize list for legend names
labelList.append(r"Hash-based signatures, $n$ = 20")
labelList.append(r"Hash-based signatures, $n$ = 22")
labelList.append(r"Hash-based signatures, $n$ = 24")
labelList.append(r"Hash-based signatures, $n$ = 26")
labelList.append("ECDSA")


plt.rc('text', usetex=True)
plt.rc('font', family='serif', size='10')
fig, ax1 = plt.subplots(figsize=(4.4, 2.4))
ax1.plot(depths,graphtimers,linewidth=1)
ax1.set_xlabel('Outage depth')
ax1.set_ylabel('Time to verify')
#ax1.set_xscale('log')
#ax1.set_yscale('log')
plt.legend(labelList,bbox_to_anchor=(0.86,0.99), loc=1,fancybox=True, framealpha=0.0)
plt.tight_layout() #prevent cut-off labels
plt.show()
#plt.savefig('hash-vs-ecdsa-outage.pgf')