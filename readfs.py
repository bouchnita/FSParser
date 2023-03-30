#ntfs parsing functions


import binascii
import mbrparse as m

SECTOR_SIZE = 512

#this function converts little endian to big endian, creds to dkuers on stackoverflow
def lil2BigEndian(hex):
    ba = bytearray.fromhex(hex.decode("utf-8"))
    ba.reverse()
    s = ''.join(format(x, '02x') for x in ba)
    s = bytes(s, 'utf-8')
    return s

#function to calculate the fs starting address
def calStartAddr(addr):
    A=str(hex(int.from_bytes(binascii.unhexlify(lil2BigEndian(addr)))*SECTOR_SIZE+1024)).replace('0x', '')
    return A

#function to calculate the fs ending address
def calEndAddr(startAddr, numOfSec):
    B=str(hex(int.from_bytes(binascii.unhexlify(lil2BigEndian(numOfSec)))*SECTOR_SIZE+int.from_bytes(binascii.unhexlify(lil2BigEndian(startAddr)))*SECTOR_SIZE+1024)).replace('0x', '')
    return B

LBA=b'3f000000'
numSectors=b'8a340200'

fsContent=m.readFroma2b(calStartAddr(LBA), calEndAddr(LBA, numSectors))





# print(NTFS)
# print(calEndAddr(LBA, tb))
# print(type(calStartAddr(LBA)))
# print(int('F',base=16))
# print(str(int.from_bytes(binascii.unhexlify(ta))))
# print(type(ta))
# print(hex(int(decode(ta))+int(decode(tb))))
# string='5a223f'
# arr = bytes(string, 'utf-8')
# print(type(arr))


