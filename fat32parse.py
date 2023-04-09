''' steps:
1.get file system in variable
2.get boot sector and reserved region in two separate variables
3.parse each
4.return the result in an array
'''

from readfs import *
from mbrparse import *

#functions to format the output





def a(bytevalue):#convert2dec
    dec=int(lil2BigE(bytevalue.decode('utf-8')),16)
    return dec 
def b(bytevalue):#convert2ascii
    bytevalue=bytevalue.decode('utf-8')
    asciiValue=bytes.fromhex(bytevalue).decode("ASCII")
    asciiValue=asciiValue.replace(';', '\n- ')
    return asciiValue
def c(bytevalue):#convert2hex
    hex=lil2BigE(bytevalue.decode('utf-8'))
    return hex
def d(bytevalue):#media descriptor
    if c(bytevalue)=='f8':
        medDesc='Hard Disk'
    else:
        medDesc=c(bytevalue)
    return medDesc


sectionToParse=fsContent[0:1024]
sectionToParseElements=[['00', '3', 'Jump instruction'],
 ['03', '8', 'OEM name'],
 ['0B', '2', 'Bytes per sector'],
 ['0D', '1', 'Sectors per cluster'],
 ['0E', '2', 'Reserved sector count'],
 ['10', '1', 'Number of Copies of FAT'],
 ['11', '2', 'Maximum Root Directory Entries'],
 ['13', '2', 'Number of Sectors in Partition Smaller than 32MB'],
 ['15', '1', 'Media descriptor'],
 ['16', '2', 'Sectors Per FAT in Older FAT Systems'],
 ['18', '2', 'Sectors per track'],
 ['1A', '2', 'Number of heads'],
 ['1C', '4', 'Number of Hidden Sectors in Partition'],
 ['20', '4', 'Number of Sectors in Partition'],
 ['24', '4', 'Number of Sectors Per FAT'],
 ['2A', '2', 'Version of FAT32 Drive'],
 ['30', '2', 'Sector Number of the File System Information Sector'],
 ['32', '2', 'Sector Number of the BackupBoot Sector'],
 ['40', '1', 'Logical Drive Number of Partition'],
 ['42', '1', 'Extended boot signature'],
 ['43', '4', 'Serial Number of Partition'],
 ['47', '11', 'Volume label'],
 ['1E8', '4', 'Number of Free Clusters'],
 ['1FE', '2', 'Boot sector signature']]


functions=[c,b,a,a,a,a,a,a,d,a,a,a,a,a,a,a,a,a,a,c,c,b,a,c]
print(functions[0](b'fa'))
print(len(functions))


for element in sectionToParseElements:
    print(f"-{element[2]} : {functions[sectionToParseElements.index(element)](sectionToParse[int(element[0],base=16)*2:int(element[0],base=16)*2+int(element[1])*2])}")



# print(int(sectionToParseElements[2][0],base=16))
# print(sectionToParse[487*2:487*2+2*2])
# print(fsContent[0:500])