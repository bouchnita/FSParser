from datetime import datetime


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


def Free_indode(value):
    bytes_data = bytes.fromhex(value)
    free_inode = int.from_bytes(bytes_data, byteorder='little')
    return free_block

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
	write_time = datetime.fromtimestamp(mount_time).strftime("%A, %B %d, %Y %I:%M:%S")
	return write_time


def Number_of_mount(value):
	bytes_data = bytes.fromhex(value)
	number_of_mount = int.from_bytes(bytes_data, byteorder='little')
	return number_of_mount


def Magic_signature(value):
	bytes_data = bytes.fromhex(value)
	magic_signature = int.from_bytes(bytes_data, byteorder='little')
	return magic_signature


def FS_state(value):
	if value == '0001':
		state = 'cleanly unmounted'
	elif value == '0002':
		state = 'Error detected'
	elif value == '0004':
		state = 'Orphans being recovred'
	return state


def Creator_OS(value):
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








