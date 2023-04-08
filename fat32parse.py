''' steps:
1.get file system in variable
2.get boot sector and reserved region in two separate variables
3.parse each
4.return the result in an array
'''

import readfs
from readfs import *
from mbrparse import *

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
#  ['25', '1', 'Current head'],
#  ['27', '4', 'Partition serial number'],
 ['2A', '2', 'Version of FAT32 Drive'],
 ['30', '2', 'Sector Number of the File System Information Sector'],
 ['32', '2', 'Sector Number of the BackupBoot Sector'],
#  ['36', '8', 'File system type'],
 ['40', '1', 'Logical Drive Number of Partition'],
 ['42', '1', 'Extended boot signature'],
 ['43', '4', 'Serial Number of Partition'],
 ['47', '11', 'Volume label'],
 ['1E8', '4', 'Number of Free Clusters'],
 ['1FE', '2', 'Boot sector signature']]




sum=0
for element in sectionToParseElements:
    print(f"-{element[2]} : {sectionToParse[int(element[0],base=16)*2:int(element[0],base=16)*2+int(element[1])*2]}")
    sum+=int(element[1])
print(sum)
# print(int(sectionToParseElements[2][0],base=16))
# print(sectionToParse[487*2:487*2+2*2])
# print(fsContent[0:500])