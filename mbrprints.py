

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


def LBA_start(value):
    bytes_data = bytes.fromhex(value)
    integer_value = int.from_bytes(bytes_data, byteorder='little')
    return integer_value


def size(value):
    bytes_data = bytes.fromhex(value)
    integer_value = int.from_bytes(bytes_data, byteorder='little')
    megabytes = (integer_value * 512) / (1024 * 1024)
    result=[integer_value, megabytes]
    return result


def prettifyInfos(infos):
    infos=[is_bootable(infos[0]), Partition_type(infos[1]), chs_values(infos[2]), chs_values(infos[3]), LBA_start(infos[4]), size(infos[5])]
    return infos

def chs_values(value):
    head = (int('0x'+value[0:2],16))
    sector = (int('0x'+value[2:4],16))
    cylinder = (int('0x'+value[4:],16))
    return [head, sector, cylinder]



# print(chs_values('FE3F08'))

# print(LBA_start('3f000000'))