import hashlib
from prettytable import PrettyTable
import time
import random
import json
import sys
import string
from ecdsa import SECP256k1
from ecdsa import SigningKey

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

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

timers = []
for k in range (0,TESTLENGTH):
    message = signeddata[k][0]
    signature = signeddata[k][1]
    start = time.time()
    assert pk.verify(signature,message.encode())
    end = time.time()
    timers.append(end-start)

print("Average verifying time: " + str(sum(timers)/len(timers)))