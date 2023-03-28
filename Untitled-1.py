#steps:
#1-open image file
import binascii
filename=r"C:\Users\ily455\Desktop\SICS\2\S4\forensics\tp\1-2\deviceImageCorrupted.raw"
filename.replace('\\','/')
# print(filename)
position='8200'
with open(filename,'rb') as f:
    f.seek(int(position,base=16))
    bloc=binascii.hexlify(f.read())
    print(bloc)

#2-parse
#3-print results