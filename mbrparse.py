#importing libraries
import binascii
import mbrprints as mp

#reading file
filename=r"C:\Users\ily455\Desktop\fat32sample"
filename.replace('\\','/')

# variable to keep track of existing filesystems
existingFS=[]

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
    # print(partInfos)
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

#function to print the results
def printResult():
    index=1
    print('''
[+]Parsing...
[+]Reading... \n''')
    print("[+]Partitions:\n")
    for part in splitPartitions()[0:4] :
        print('#Partion number ', index, ':')
        if part!=b'00000000000000000000000000000000' :
            currentPart=mp.prettifyInfos(parsePartition(part))
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
    # return existingFS

# function to parse the filesystem
def parseFS():
    supported=["FAT32, CHS","FAT32, LBA","Hidden FAT32, CHS","Hidden FAT32, LBA","Linux"]
    for type in existingFS:
        if type == "NiHaHaHa":
            None
        else:
            if type in supported:
                print(f"\n[+]Parsing the filesystem from partition {existingFS.index(type)+1}.")
                # parse filesystem accordingly
            else:
                print(f"\n[-]Filesystem from partition {existingFS.index(type)+1} not supported.")
    


# printResult()
# parseFS()

# print(printResult())
# print(readFroma2b('8200','8202'))