#steps:
#1-open image file
#2-parse
#3-print results
##########################
#importing libraries
import binascii

#reading file
filename=r"C:\Users\ily455\Desktop\SICS\2\S4\forensics\tp\1-2\deviceImageCorrupted.raw"
filename.replace('\\','/')


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
    CHSaddrFirst=partition[2:8]
    partType=partition[8:10]
    CHSaddrLast=partition[10:16]
    LBA=partition[16:24]
    numSectors=partition[24:32]
    partInfos=[status, CHSaddrFirst, CHSaddrLast, partType, LBA, numSectors]
    return partInfos

#hanta al7aj rani ktbt hadchi from scratch gadlna had l fonction bach tb9a tchd dok les valeurs li 
# kat3titha parsePartition w trdhom meaningful bhal dik 80 y3ni bootable, 
# chmn systeme de fichier kada kada, w khli dik l valeur kat afficha bach 
# l user ta ila kna ghltna f chi haja wla inputa chi file system 3wj yabno les valeurs bli machi homa hadok
#bghit bach f dak str li rani dayr fih printParsed(parsePartition(part)) nwli dayr printParsed(beautifyInfos(parsePartition(part)))

#hna bdat l fonction
#function to assign a human readble information to each value returned by parsePartition()
#def beautifyInfos(infos):

#hna salat l fonction

#function to print mbr information
def printParsed(infos):
    print(f''' 
    This partition is a {infos[0]} filesystem
    Start address : {infos[1]}
    End address : {infos[2]}
    Partition type : {infos[3]}
    LBA : {infos[4]}
    Number of sectors is {infos[5]}
    ''')
    return None

#function to read each mbr partition
def splitPartitions():
    part1=readFroma2b('01BE','01CE')
    part2=readFroma2b('01CE','01DE')
    part3=readFroma2b('01DE','01EE')
    part4=readFroma2b('01EE','01FE')
    btsig=readFroma2b('01FE','0200')
    partitions=[part1,part2,part3,part4]
    return partitions

#function to print the results
def printResult():
    index=1
    for part in splitPartitions():
        print('***Partion number ', index, ':')
        if part!=b'00000000000000000000000000000000':
            printParsed(parsePartition(part))
            index+=1
        else:
            print('This partition is empty')
            index+=1
        print('-------------------------------------')

# print(readFroma2b('8200','8202'))