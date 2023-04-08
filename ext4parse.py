
from readfs import *
from mbrparse import *




if fsContent[0:16]==b'0000000000000000':
    superBlock=fsContent[2048:2048+60]
    blocsize=2**(10+lil2BigEndian(superBlock[48:48+8].decode('utf-8')))
    superBlock=fsContent[2048:2048+blocsize*2]
else:
    superBlock=fsContent[0:0+60]
    blocsize=2**(10+lil2BigEndian(superBlock[48:48+8].decode('utf-8')))
    superBlock=fsContent[0:0+blocsize*2]



superBlockElements = [  ['00', '4', 'Inode count'],
  ['04', '4', 'Block count'],
  ['08', '4', 'Reserved block count for super user'],
  ['0C', '4', 'Free block count'],
  ['10', '4', 'Free inode count'],
  ['14', '4', 'First data block'],
  ['18', '4', 'Block size'],
  ['1C', '4', 'Cluster size'],
  ['20', '4', 'Blocks per group'],
  ['24', '4', 'Clusters per group'],
  ['28', '4', 'Inodes per group'],
  ['2C', '4', 'Mount time'],
  ['30', '4', 'Write time'],
  ['34', '2', 'Mount count'],
  ['36', '2', 'Maximal mount count'],
  ['38', '2', 'Magic signature'],
  ['3A', '2', 'File system state'],
  ['3C', '2', 'Error handling'],
  ['3E', '2', 'Minor revision level'],
  ['40', '4', 'Last check time'],
  ['44', '4', 'Check interval'],
  ['48', '4', 'Creator OS'],
  ['4C', '4', 'Revision level'],
  ['50', '4', 'Default UID for reserved blocks'],
  ['54', '2', 'Default GID for reserved blocks']]


for element in superBlockElements:
    print(f"-{element[2]} : {superBlock[int(element[0],base=16)*2:int(element[0],base=16)*2+int(element[1])*2]}")
