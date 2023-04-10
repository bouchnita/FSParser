#importing libraries
import binascii
import argparse
import os
from banner import *
from datetime import datetime


SECTOR_SIZE = 512
# variable to keep track of existing filesystems
existingFS=[]

#elements of the FAT FS
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
#elements of the ext superblock
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
  ['44', '4', 'Check interval in seconds'],
  ['48', '4', 'Creator OS'],
  ['4C', '4', 'Revision level'],
  ['50', '2', 'Default UID for reserved blocks'],
  ['52', '2', 'Default GID for reserved blocks']]




#function to check if a partition is bootable
def is_bootable(value):
    invalid=[hex(n).replace('0x','') for n in range(1,128)]
    if value == '80':
        status = 'bootable'
    elif value == '00':
        status = 'inactive'
    elif value in invalid:
        status = 'invalid'
    else :
        status = 'unknown'
    return status

#partition types
def Partition_type(value):
    types = {
    0x00: "Empty",
    0x01: "FAT12, CHS",
    0x04: "FAT16, 16-32 MB, CHS",
    0x05: "Microsoft Extended, CHS",
    0x06: "FAT16, 32 MB-2GB, CHS",
    0x07: "NTFS",
    0x0b: "FAT32, CHS",
    0x0c: "FAT32, LBA",
    0x0e: "FAT16, 32 MB-2GB, LBA",
    0x0f: "Microsoft Extended, LBA",
    0x11: "Hidden Fat12, CHS",
    0x14: "Hidden FAT16, 16-32 MB, CHS",
    0x16: "Hidden FAT16, 32 MB-2GB, CHS",
    0x1b: "Hidden FAT32, CHS",
    0x1c: "Hidden FAT32, LBA",
    0x1e: "Hidden FAT16, 32 MB-2GB, LBA",
    0x42: "Microsoft MBR, Dynamic Disk",
    0x82: "Solaris x86 -or- Linux Swap",
    0x83: "Linux",
    0x84: "Hibernation",
    0x85: "Linux Extended",
    0x86: "NTFS Volume Set",
    0x87: "NTFS Volume SET",
    0xa0: "Hibernation",
    0xa1: "Hibernation",
    0xa5: "FreeBSD",
    0xa6: "OpenBSD",
    0xa8: "Mac OSX",
    0xa9: "NetBSD",
    0xab: "Mac OSX Boot",
    0xb7: "BSDI",
    0xb8: "BSDI swap",
    0xde: "Dell Diagnostic Partition",
    0xee: "EFI GPT Disk",
    0xef: "EFI System Partition",
    0xfb: "Vmware File System",
    0xfc: "Vmware swap",
    }
    type=types.get(value)
    if type==None:
        type='Unknown'
    else:
        None
    return type

#function format start address
def LBA_start(value):
    bytes_data = bytes.fromhex(value)
    integer_value = int.from_bytes(bytes_data, byteorder='little')
    return integer_value

#function format size 
def size(value):
    bytes_data = bytes.fromhex(value)
    integer_value = int.from_bytes(bytes_data, byteorder='little')
    megabytes = (integer_value * 512) / (1024 * 1024)
    result=[integer_value, megabytes]
    return result

#function format CHS coordinates
def chs_values(value):
    head = (int('0x'+value[0:2],16))
    sector = (int('0x'+value[2:4],16))
    cylinder = (int('0x'+value[4:],16))
    return [head, sector, cylinder]

#function assembles all the parsed data in a single array 
def prettifyInfos(infos):
    infos=[is_bootable(infos[0]), Partition_type(infos[1]), chs_values(infos[2]), chs_values(infos[3]), LBA_start(infos[4]), size(infos[5])]
    return infos

##function to read from an offset a to an offset b
def readFroma2b( a, b):
    with open(filename,'rb') as f:
        lenght=int(b,base=16)-int(a,base=16)
        f.seek(int(a,base=16))
        readBytes=binascii.hexlify(f.read(lenght))
    return readBytes

##functin to parse each partition field and assign it to a variable
def parsePartition(partition):
    status=partition[0:2]
    partType=partition[8:10]
    LBA=partition[16:24]
    numSectors=partition[24:32]
    CHSaddrFirst=partition[2:8]
    CHSaddrLast=partition[10:16]
    partInfos=[status.decode("utf-8"), int('0x'+partType.decode("utf-8"),base=16) , CHSaddrFirst.decode("utf-8"), CHSaddrLast.decode("utf-8") , LBA.decode("utf-8") , numSectors.decode("utf-8") ]
    return partInfos

#function to print mbr information
def printParsed(infos):
    print(f''' 
    -This partition is {infos[0]} 

    -Partition type : {infos[1]}

    -Number of sectors : {infos[5][0]} sector
    
    -Size of the partition : {infos[5][1]} MB
    
    -LBA of first absolute sector in the partition : {infos[4]}
    
    -CHS Start coordinates : 
        Head : {infos[2][0]}
        Sector : {infos[2][1]}
        Cylinder : {infos[2][2]}

    -CHS End coordinates : 
        Head : {infos[3][0]}
        Sector : {infos[3][1]}
        Cylinder : {infos[3][2]}
    ''')
    return None

#function to read each mbr partition
def splitPartitions():
    part1=readFroma2b('01BE','01CE')
    part2=readFroma2b('01CE','01DE')
    part3=readFroma2b('01DE','01EE')
    part4=readFroma2b('01EE','01FE')
    btsig=readFroma2b('01FE','0200')
    partitions=[part1,part2,part3,part4,btsig]
    return partitions


############################################################

#this function converts little endian to big endian, creds to dkuers on stackoverflow
def lil2BigE(value):
    bytes_data = bytes.fromhex(value)
    s = int.from_bytes(bytes_data, byteorder='little')
    s=hex(s).replace('0x','')
    return s



#################################################################

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
#function to format the parsed fields put in a single array 
functions=[c,b,a,a,a,a,a,a,d,a,a,a,a,a,a,a,a,a,a,c,c,b,a,c]


#printing the result
def printFAT32(sectionToParse):
    for element in sectionToParseElements:
        print(f"-{element[2]} : {functions[sectionToParseElements.index(element)](sectionToParse[int(element[0],base=16)*2:int(element[0],base=16)*2+int(element[1])*2])}")

####################################################################
#check if first block of ext is empty or not
def checkExt(fsContent):
    if fsContent[0:16]==b'0000000000000000':
        superBlock=fsContent[2048:2048+60]
        blocsize=2**(10+int(lil2BigE(superBlock[48:48+8].decode('utf-8')),16))
        superBlock=fsContent[2048:2048+blocsize*2]
    else:
        superBlock=fsContent[0:0+60]
        blocsize=2**(10+int(lil2BigE(superBlock[48:48+8].decode('utf-8')),16))
        superBlock=fsContent[0:0+blocsize*2]
    return superBlock



#functions to format the parsed fields
def Inode_count(value): #size 32
	bytes_data = bytes.fromhex(value)
	inode_count = int.from_bytes(bytes_data, byteorder='little')
	return inode_count


def Block_count(value): #size 32
    bytes_data = bytes.fromhex(value)
    block_count = int.from_bytes(bytes_data, byteorder='little')
    return block_count


def Su_block(value): #size 32
	bytes_data = bytes.fromhex(value)
	su_value = int.from_bytes(bytes_data, byteorder='little')
	return su_value


def Free_block(value):
    bytes_data = bytes.fromhex(value)
    free_block = int.from_bytes(bytes_data, byteorder='little')
    return free_block


def Free_inode(value):
    bytes_data = bytes.fromhex(value)
    free_inode = int.from_bytes(bytes_data, byteorder='little')
    return free_inode 

def First_data_block(value): #Where group0 start
	bytes_data = bytes.fromhex(value)
	first_data_block = int.from_bytes(bytes_data, byteorder='little')
	return first_data_block

def Block_size(value):
    bytes_data = bytes.fromhex(value)
    power = int.from_bytes(bytes_data, byteorder='little')
    block_size = 2**(10+power)
    return block_size


def Cluster_size(value):
	bytes_data = bytes.fromhex(value)
	power = int.from_bytes(bytes_data, byteorder='little')
	cluster_size = 10**power
	return cluster_size


def Block_per_group(value):
	bytes_data = bytes.fromhex(value)
	block_per_group = int.from_bytes(bytes_data, byteorder='little')
	return block_per_group


def Cluster_per_group(value):
	bytes_data = bytes.fromhex(value)
	cluster_per_group = int.from_bytes(bytes_data, byteorder='little')
	return cluster_per_group


def Inode_per_group(value):
	bytes_data = bytes.fromhex(value)
	inode_per_group = int.from_bytes(bytes_data, byteorder='little')
	return inode_per_group


def Mount_time(value):
	bytes_data = bytes.fromhex(value)
	mount_time = int.from_bytes(bytes_data, byteorder='little')
	mount_time = datetime.fromtimestamp(mount_time).strftime("%A, %B %d, %Y %I:%M:%S")
	return mount_time


def Write_time(value):
	bytes_data = bytes.fromhex(value)
	write_time = int.from_bytes(bytes_data, byteorder='little')
	write_time = datetime.fromtimestamp(write_time).strftime("%A, %B %d, %Y %I:%M:%S")
	return write_time


def Number_of_mount(value):
	bytes_data = bytes.fromhex(value)
	number_of_mount = int.from_bytes(bytes_data, byteorder='little')
	return number_of_mount

def Max_mount_count(value):	#added
	bytes_data = bytes.fromhex(value)
	max_mount_count = int.from_bytes(bytes_data, byteorder='little')
	return max_mount_count


def Magic_signature(value):

	return value

def FS_state(value):
	bytes_data = bytes.fromhex(value)
	value = int.from_bytes(bytes_data, byteorder='little')
	state=''
	if value == 1:
		state = 'Cleanly unmounted'
	elif value == 2:
		state = 'Error detected'
	elif value == 4:
		state = 'Orphans being recovered'
	else:
		state= 'Unknown state'
	return state


def S_errors(value):	#added
	behaviour=''
	bytes_data = bytes.fromhex(value)
	value = int.from_bytes(bytes_data, byteorder='little')	
	if value == 1:
		behaviour = 'Continue'
	elif value == 2:
		behaviour = 'Remount read-only '
	elif value == 3:
		behaviour = 'Panic'
	return behaviour


def Minor_rev_level(value):	#added
	bytes_data = bytes.fromhex(value)
	minor_rev_level = int.from_bytes(bytes_data, byteorder='little')
	return minor_rev_level


def Last_time_check(value): #added
	bytes_data = bytes.fromhex(value)
	last_time_check = int.from_bytes(bytes_data, byteorder='little')
	last_time_check = datetime.fromtimestamp(last_time_check).strftime("%A, %B %d, %Y %I:%M:%S")
	return last_time_check


def Check_interval(value):	#added
	bytes_data = bytes.fromhex(value)
	check_interval = int.from_bytes(bytes_data, byteorder='little')
	return check_interval

	
	
def Creator_OS(value):
	creator=''
	bytes_data = bytes.fromhex(value)
	value = int.from_bytes(bytes_data, byteorder='little')	
	if value == 0:
		creator = 'Linux'
	elif value == 1:
		creator = 'Hurd'
	elif value == 2:
		creator = 'Masix'
	elif value == 3:
		creator = 'FreeBSD'
	elif value == 4:
		creator = 'Lites'
	return creator



def Revision_level(value):
	bytes_data = bytes.fromhex(value)
	value = int.from_bytes(bytes_data, byteorder='little')
	if value == 1:
		level = 'Original format'
	elif value == 1:
		level = 'v2 format w/ dynamic inode sizes'
	else:
		level = 'Unknown'
	return level


def Default_uid(value):
	bytes_data = bytes.fromhex(value)
	default_uid = int.from_bytes(bytes_data, byteorder='little')
	return default_uid

def Default_gid(value):
	bytes_data = bytes.fromhex(value)
	default_gid = int.from_bytes(bytes_data, byteorder='little')
	return default_gid


#function to parse the superblock
def SB_split(sBlock): #superblock == list dyal bytes li extr.decode('utf-8')actiti
		s_inodes_count = sBlock[int('00',base=16)*2:int('04',base=16)*2].decode('utf-8')		#0
		s_blocks_count_lo = sBlock[int('04',base=16)*2:int('08',base=16)*2].decode('utf-8')	#1
		s_r_blocks_count_lo = sBlock[int('08',base=16)*2:int('0C',base=16)*2].decode('utf-8')	#2
		s_free_blocks_count_lo = sBlock[int('0C',base=16)*2:int('10',base=16)*2].decode('utf-8')	#3
		s_free_inodes_count = sBlock[int('10',base=16)*2:int('14',base=16)*2].decode('utf-8')	#4
		s_first_data_block = sBlock[int('14',base=16)*2:int('18',base=16)*2].decode('utf-8')	#5
		s_log_block_size = sBlock[int('18',base=16)*2:int('1C',base=16)*2].decode('utf-8')	#6
		s_log_cluster_size = sBlock[int('1C',base=16)*2:int('20',base=16)*2].decode('utf-8')	#7
		s_blocks_per_group = sBlock[int('20',base=16)*2:int('24',base=16)*2].decode('utf-8')	#8
		s_clusters_per_group = sBlock[int('24',base=16)*2:int('28',base=16)*2].decode('utf-8')	#9
		s_inodes_per_group = sBlock[int('28',base=16)*2:int('2C',base=16)*2].decode('utf-8')	#10
		s_mtime = sBlock[int('2C',base=16)*2:int('30',base=16)*2].decode('utf-8')		#11	
		s_wtime = sBlock[int('30',base=16)*2:int('34',base=16)*2].decode('utf-8')		#12
		s_mnt_count = sBlock[int('34',base=16)*2:int('36',base=16)*2].decode('utf-8')		#13
		s_max_mnt_count = sBlock[int('36',base=16)*2:int('38',base=16)*2].decode('utf-8') #added	14
		s_magic = sBlock[int('38',base=16)*2:int('3A',base=16)*2].decode('utf-8')		#15
		s_state = sBlock[int('3A',base=16)*2:int('3C',base=16)*2].decode('utf-8')		#16
		s_errors = sBlock[int('3C',base=16)*2:int('3E',base=16)*2].decode('utf-8')	#added	#17
		s_minor_rev_level = sBlock[int('3E',base=16)*2:int('40',base=16)*2].decode('utf-8') 	#added 18
		s_lastcheck = sBlock[int('40',base=16)*2:int('44',base=16)*2].decode('utf-8')	#added	19
		s_checkinterval = sBlock[int('44',base=16)*2:int('48',base=16)*2].decode('utf-8')	#added 20
		s_creator_os = sBlock[int('48',base=16)*2:int('4C',base=16)*2].decode('utf-8')		#21
		s_rev_level = sBlock[int('4C',base=16)*2:int('50',base=16)*2].decode('utf-8')		#22
		s_def_resuid = sBlock[int('50',base=16)*2:int('52',base=16)*2].decode('utf-8')		#23
		s_def_resgid = sBlock[int('52',base=16)*2:int('54',base=16)*2].decode('utf-8')		#24

		fields = [s_inodes_count,s_blocks_count_lo,s_r_blocks_count_lo,s_free_blocks_count_lo,s_free_inodes_count,s_first_data_block,s_log_block_size,s_log_cluster_size,s_blocks_per_group,s_clusters_per_group,s_inodes_per_group,s_mtime,s_wtime,s_mnt_count,s_max_mnt_count,s_magic,s_state,s_errors,s_minor_rev_level,s_lastcheck,s_checkinterval,s_creator_os,s_rev_level,s_def_resuid,s_def_resgid]
		return fields


#function puts all the fields in a single array
def Parser(content):
	fields=SB_split(content)
	result=[Inode_count(fields[0]),
	Block_count(fields[1]),
	Su_block(fields[2]),
	Free_block(fields[3]),
	Free_inode(fields[4]),
	First_data_block(fields[5]),
	Block_size(fields[6]),
	Cluster_size(fields[7]),
	Block_per_group(fields[8]),
	Cluster_per_group(fields[9]),
	Inode_per_group(fields[10]),
	Mount_time(fields[11]),
	Write_time(fields[12]),
	Number_of_mount(fields[13]),
	Max_mount_count(fields[14]),
	Magic_signature(fields[15]),
	FS_state(fields[16]),
	S_errors(fields[17]),
	Minor_rev_level(fields[18]),
	Last_time_check(fields[19]),
	Check_interval(fields[20]),
	Creator_OS(fields[21]),
	Revision_level(fields[22]),
	Default_uid(fields[23]),
	Default_gid(fields[24])]
	return result




#printing the result
def printEXT(fsContent):
    superBlock=checkExt(fsContent)
    for element in superBlockElements:
	    print(f"-{element[2]} : {Parser(superBlock)[superBlockElements.index(element)]}")

#####################################################
#function to print the results
def printResult(what):
    if what == 'mbr':
        index=1
        print("[+]Partitions:\n")
        for part in splitPartitions()[0:4] :
            print('#Partion number ', index, ':')
            if part!=b'00000000000000000000000000000000' :
                currentPart=prettifyInfos(parsePartition(part))
                printParsed(currentPart)
                existingFS.append(currentPart[1])
                index+=1
            else:
                print('     -This partition is empty')
                existingFS.append('NiHaHaHa')
                index+=1
            print('-------------------------------------')
        if splitPartitions()[4] == b'55aa':
            print('#Boot signature is valid. (==55AA)')
        else:
            print('!!!!Boot signature is invalid. (!=55AA)')
        print('-------------------------------------')
    elif what == 'fs':
        supported=["FAT32, CHS","FAT32, LBA","Hidden FAT32, CHS","Hidden FAT32, LBA","Linux"]
        index=1
        for part in splitPartitions()[0:4] :
            if part!=b'00000000000000000000000000000000' :
                currentPart=prettifyInfos(parsePartition(part))
                existingFS.append(currentPart[1])
                index+=1
            else:
                existingFS.append('NiHaHaHa')
                index+=1
        if splitPartitions()[4] == b'55aa':
            None
        else:
            None
        supported=["FAT32, CHS","FAT32, LBA","Hidden FAT32, CHS","Hidden FAT32, LBA","Linux"]
          
        for type in existingFS:
            if type == "NiHaHaHa":
                None
            else:
                if type in supported:
                    print(f"\n[+]Parsing the filesystem from partition {existingFS.index(type)+1}.")
                    if type==supported[4]:
                        LBA=prettifyInfos(parsePartition(splitPartitions()[existingFS.index(type)]))[4]
                        numSectors=prettifyInfos(parsePartition(splitPartitions()[existingFS.index(type)]))[5][0]
                        fsContent=readFroma2b(calStartAddr(LBA), calEndAddr(LBA, numSectors))
                        printEXT(fsContent)

                    elif type in supported[0:4]:
                        LBA=prettifyInfos(parsePartition(splitPartitions()[existingFS.index(type)]))[4]
                        numSectors=prettifyInfos(parsePartition(splitPartitions()[existingFS.index(type)]))[5][0]
                        fsContent=readFroma2b(calStartAddr(LBA), calEndAddr(LBA, numSectors))
                        printFAT32(fsContent[0:1024])
                    break
                else:
                    print(f"\n[-]Filesystem from partition {existingFS.index(type)+1} not supported.")
                break

#function to calculate the fs starting address
def calStartAddr(addr):
    A=str(hex(addr*SECTOR_SIZE)).replace('0x', '')
    return A

#function to calculate the fs ending address
def calEndAddr(startAddr, numOfSec):
    B=str(hex(10*SECTOR_SIZE+startAddr*SECTOR_SIZE)).replace('0x', '')
    return B


#Banner
print_banner()
# Create an argument parser
parser = argparse.ArgumentParser(description='Parse MBR partitions and filesystems.')

# Add the arguments
parser.add_argument('-m', '--mbr', action='store_true', help='parse MBR only')
parser.add_argument('-f', '--filesystem', action='store_true', help='parse filesystem')
parser.add_argument('-i', '--image', type=str, required=True, help='path to disk image')
parser.add_argument('-a', '--all', action='store_true', help='Parse both MBR partition and filesystem.')

# Parse the arguments
args = parser.parse_args()

# Check the arguments
if args.all and (args.mbr or args.filesystem):
    print('Error: -a option cannot be used with -m or -f options.')
    parser.print_help()
    exit(1)

if not (args.mbr or args.filesystem or args.all):
    print('Error: must use at least one of -m, -f, or -a options.')
    parser.print_help()
    exit(1)

if (args.mbr or args.filesystem) and not args.image:
    print('Error: -m or -f option requires specifying an image file.')
    parser.print_help()
    exit(1)

# Read the disk image file
if args.image:
    filename = args.image
    filename.replace('\\','/')


if args.all or args.mbr:
    # Parse the MBR partition table
    printResult('mbr')
    
if args.all or args.filesystem:
    # Detect the filesystem type
    printResult('fs')
