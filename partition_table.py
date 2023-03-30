
def is_bootable(value, num):
    if value == 80:
        print("the partition {n} is bootable".format(n=num))
    else:
        print("the partition {n} is not bootable".format(n=num))

def CHS_start(little):
    bytes_data = bytes.fromhex(little)
    integer_value = int.from_bytes(bytes_data, byteorder='little')
    print("the partition start from sector : {start}".format(start=integer_value))

def Partition_type(value):
    if value == '83':
        print("partition type : ext4")
        partition = ext4
    if value == '07':
        print("partition type : NTFS")
        partition = ntfs
    else:
        print("file system not supported !")
        return partition


def CHS_end(value):
    bytes_data = bytes.fromhex(value)
    integer_value = int.from_bytes(bytes_data, byteorder='little')
    print("The ending cylinder, head, and sector of the partition : {end}".format(end=integer_value))

def LBA_start(value):
    bytes_data = bytes.fromhex(value)
    integer_value = int.from_bytes(bytes_data, byteorder='little')
    print("The starting sector of the partition in LBA : {start}".format(start=integer_value))


def LBA_size(value):
    bytes_data = bytes.fromhex(value)
    integer_value = int.from_bytes(bytes_data, byteorder='little')
    print("Size in sector is {size} sector ".format(size=integer_value))
    megabytes = (integer_value * 512) / (1024 * 1024)
    print("Size in Mb : {size}".format(size=megabytes))
