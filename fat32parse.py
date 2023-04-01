''' steps:
1.get file system in variable
2.get boot sector and reserved region in two separate variables
3.parse each
4.return the result in an array
'''

import readfs
from readfs import *
from mbrparse import *

bootSector=fsContent[0:1024]
bootSectorElements=[['00', '3', 'Jump instruction'],
 ['03', '8', 'OEM name'],
 ['0B', '2', 'Bytes per sector'],
 ['0D', '1', 'Sectors per cluster'],
 ['0E', '2', 'Reserved sector count'],
 ['10', '1', 'Number of FATs'],
 ['11', '2', 'Number of root directory entries'],
 ['13', '2', 'Total sectors (if less than 32 MB)'],
 ['15', '1', 'Media descriptor'],
 ['16', '2', 'Sectors per FAT'],
 ['18', '2', 'Sectors per track'],
 ['1A', '2', 'Number of heads'],
 ['1C', '4', 'Hidden sector count'],
 ['20', '4', 'Total sector count (if greater than or equal to 32 MB)'],
 ['24', '1', 'Logical drive number'],
 ['25', '1', 'Current head'],
 ['26', '1', 'Extended boot signature'],
 ['27', '4', 'Partition serial number'],
 ['2B', '11', 'Volume label'],
 ['36', '8', 'File system type'],
 ['3E', '420', 'Bootstrap code'],
 ['1FE', '2', 'Boot sector signature']]




sum=0
for element in bootSectorElements:
    print(f"-{element[2]} : {bootSector[int(element[0],base=16)*2:int(element[0],base=16)*2+int(element[1])*2]}")
    sum+=int(element[1])
print(sum)
# print(int(bootSectorElements[2][0],base=16))
# print(bootSector[487*2:487*2+2*2])
# print(fsContent[0:500])