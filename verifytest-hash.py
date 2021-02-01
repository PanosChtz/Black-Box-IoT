import hashlib
from prettytable import PrettyTable
import time
import random
import json
import sys
import string

def h(preimage):
    return hashlib.sha256(preimage.encode('utf-8')).hexdigest()
    
def FindValue(pebbleList):
    for i in range(1,SIGMA):
        if pebbleList[i].position == pebbleList[0].position:
            return pebbleList[i].value

class Pebble:
  def __init__(pj, StartIncr, DestIncr, position, destination, value):
    pj.StartIncr = StartIncr
    pj.DestIncr = DestIncr
    pj.position = position
    pj.destination = destination
    pj.value = value

def printpebbles():
    x = PrettyTable()
    x.field_names = ["j","StartIncr","DestIncr","position","destination","value"]
    i=0
    for i in range (i,SIGMA):
        x.add_row([i,pebbles[i].StartIncr,pebbles[i].DestIncr,pebbles[i].position,pebbles[i].destination,pebbles[i].value])
    print(x)
    

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

DEBUG = False
SIGMA = int(sys.argv[1])
MESSAGELENGTH = 100
TESTLENGTH = int(10e+2)
f = open( "pebblelist"+str(SIGMA)+".txt", 'r' )
alldata = json.loads(f.read())
f.close()

#hashvalues = ["fd69733596022455b2828a11683ee10431258502f4ae99947f2537e8a79857b5","254395d0e357906b5eb521f090f65546ad1499c840c7736f26aa6a5930f9f6db","96c8d33adbf453c5e9f951992ed6ee9820e1546c10d02bc11ce934bf4092dd15","32def3a2cc50510ca4e036072355e9e46fb1e93dff9f9c49888c09e3d6b7b2e0","78de2e7e1e79b3082fcecfdda9c127eacf4bd64de3b8a92153de20de61c704ba","1a54abaf007bb42e4e2d6c2fad0cf8452c199b816bf070410ceeea184a248bb3","f21d07732c54b1807a4fecec00f1a0c4fd63d586d7e3db250208e8e03de5cf85","f6979be79997418151b219947ddfbf607c31aa981388bc068210a353ba64fbff","a3b5bcb0ab6c405abb151aada473d5cecdf272c5af83a3cf3e3d4e7b0ef812ce","91f833decc38c2dc2b0cebb8d9e6b0cc846dd41bdee5db2c0a27fc04400ec2f7","f03d1dd012c20af9db0be1b5273141af6874a11c49551fa0b5c29bfcc72e1f70","25ac586f0628c52c89f5d7acfe66e1787b8c0335aed202d6b00cda00e80bfc06","15626519a1bef1fa8088a847024c3ef4d872b55d6d396d002d7b84bc57d49ab1","4ff0c1481dce16c1d53df9419176cde9ea2a3ee8974a43d54129fa5e4691b078","20e6ed7e10c3b7111773b4a78ef227c1f52e8c3a69bcd3fc76912002ba0038b5","bc8367f61af060b100302304c8e06ef3f3147f248b8016f52042a59e137966fd","f7628284312b61fa9f37f74c13c86cfcd1a17bb9d573c8c670a9032818cdb419","2da3b7b242931d8c2857612e17f93b16a97abd9fe823038998b481a78dade5e5","cec7f3d20951ed832d5a6ec67852a645f910d2ac42d2fa1882535c089abde65d","52d53aca907590b844a632aa5a1f1342a7caf5ae1e4f45fbeb4bef558033d5e4","7a45009d2269cbe74e997158af46b7dd86a62efe7c93b4d4fb718ba2e13eae55","fb6893bbdf51fb3bfa85972931f71309b26c9afd57b644c4335bfa22c79ea188","18b2e2565091aa6b8ccaf6ae4ca9e8306da3629b106d94cf425b7899d46f0930","50668745e0f0e7526c699ff55358feeccf91b66f6fd64237a7c203e3754e7021","a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"]

SIGMA = len(alldata)
pebbles = []
for p in range (0,SIGMA):
    initval = alldata[str(p+1)]
    pebbles.append(Pebble(3*pow(2,p+1), pow(2,p+2),pow(2,p+1), pow(2,p+1), initval))

pos = 0

def computeValue():
    global pos
    #global val
    global pebbles
    if DEBUG: printpebbles()
    #1
    if (pos>=pow(2,SIGMA)):
        return None
    else:
        pos+=1
    #2
    for j in range (0,SIGMA):
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
        if (pebbles[0].destination > pow(2,SIGMA)):
            if DEBUG: print("Pebble redundant,retire pebble")
            pebbles[0].destination = float("inf")
            pebbles[0].position = float("inf")
        else:
            if DEBUG: print("Call to set value")
            pebbles[0].value = FindValue(pebbles)
        pebbles.sort(key=lambda x: x.destination, reverse=False)
    return output

randomstr = randomString(MESSAGELENGTH-len(str(TESTLENGTH)))
counter = TESTLENGTH
signeddata = []

sk = computeValue()
pk = sk
for k in range (0,TESTLENGTH):
    message = randomstr + str(counter)
    sk = computeValue()
    signature = [h(message+pk), sk]
    signeddata.insert(0,[message,signature])
    counter +=1
    pk = sk

check = True
timers = []
for k in range (0,TESTLENGTH-1):
    message = signeddata[k][0]
    sk = signeddata[k][1][1]
    start = time.time()
    pk = h(sk)
    check = check and (h(message+pk) == signeddata[k][1][0])
    end = time.time()
    timers.append(end-start)
if check:
    print("Average verifying time: " + str(sum(timers)/len(timers)))