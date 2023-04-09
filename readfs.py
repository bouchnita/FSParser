#ntfs parsing functions


import binascii
from mbrparse import *
import mbrparse as m
import mbrprints as mp

SECTOR_SIZE = 512

#this function converts little endian to big endian, creds to dkuers on stackoverflow
def lil2BigE(value):
    bytes_data = bytes.fromhex(value)
    s = int.from_bytes(bytes_data, byteorder='little')
    s=hex(s).replace('0x','')
    return s

#function to calculate the fs starting address
def calStartAddr(addr):
    A=str(hex(addr*SECTOR_SIZE)).replace('0x', '')
    return A

#function to calculate the fs ending address
def calEndAddr(startAddr, numOfSec):
    B=str(hex(numOfSec*SECTOR_SIZE+startAddr*SECTOR_SIZE)).replace('0x', '')
    return B

LBA=mp.prettifyInfos(m.parsePartition(m.splitPartitions()[0]))[4]
numSectors=mp.prettifyInfos(parsePartition(splitPartitions()[0]))[5][0]

fsContent=m.readFroma2b(calStartAddr(LBA), calEndAddr(LBA, numSectors))




# print(fsContent)
# print(lil2BigEndian('123456'))
# print(calEndAddr(LBA, tb))
# print(type(calStartAddr(LBA)))
# print(int('F',base=16))
# print(str(int.from_bytes(binascii.unhexlify(ta))))
# print(type(ta))
# print(hex(int(decode(ta))+int(decode(tb))))
# string='5a223f'
# arr = bytes(string, 'utf-8')
# print(type(arr))


