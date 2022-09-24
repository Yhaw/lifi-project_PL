from csv import writer
import numpy as np
import cv2 as cv
import pickle,struct,imutils
import time
import serial


def ByteToHex( byteStr ):
    """
    Convert a byte string to it's hex string representation e.g. for output.
    """
    
    # Uses list comprehension which is a fractionally faster implementation than
    # the alternative, more readable, implementation below
    #   
    hex = []
    for aChar in byteStr:
        hex.append( "%02X " % ord( aChar ) )

    return ''.join( hex ).strip()        

    #return ''.join( [ "%02X " % ord( x ) for x in byteStr ] ).strip()

#-------------------------------------------------------------------------------

def HexToByte( hexStr ):
    """
    Convert a string hex byte values into a byte string. The Hex Byte values may
    or may not be space separated.
    """
    # The list comprehension implementation is fractionally slower in this case    
    #
    #    hexStr = ''.join( hexStr.split(" ") )
    #    return ''.join( ["%c" % chr( int ( hexStr[i:i+2],16 ) ) \
    #                                   for i in range(0, len( hexStr ), 2) ] )
 
    bytes = []

    hexStr = ''.join( hexStr.split(" ") )

    for i in range(0, len(hexStr), 2):
        bytes.append( chr( int (hexStr[i:i+2], 16 ) ) )

    return ''.join( bytes )

def makeHexStr(hexSeq):
    hexStr = ''
    for x in hexSeq:
        x = x.split('x')[1]
        if len(x) == 1:
            x = '0'+x
        hexStr += x.upper()
    return hexStr

def TurnByteStr(intSeq):
    byteStr = ''
    hexSeq = [hex(x) for x in intSeq]
    hexStr = makeHexStr(hexSeq)
    return HexToByte(hexStr)


cap = cv.VideoCapture('test2.mp4')
#ser = serial.Serial('/dev/serial0', 115200, timeout=0.050)

while cap.isOpened():

    ret, frame = cap.read()
    frame = imutils.resize(frame,width=320)
    a = pickle.dumps(frame)
    message = struct.pack("Q",len(a))+a
    mess_str = str(message)

    info = ByteToHex(mess_str)

    f = open('data.txt','a')
    f.write(info)
    f.close()

    f = open('data.txt','r')
    deal = f.read()
    real = deal
    mybyte = bytes.fromhex(str(real))
    binary_string = "{:08b}".format(int(mybyte.hex(),16))
    print(binary_string)
    f.close()

    #ser.write(bytes(message))
    #print(type(message))

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    if cv.waitKey(1) == ord('q'):
        break
cap.release()
cv.destroyAllWindows()