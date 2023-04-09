from datetime import datetime
from mbrparse import *


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
	bytes_data = bytes.fromhex(value)
	magic_signature = int.from_bytes(bytes_data, byteorder='little')
	return magic_signature

#had jouj dyal les variables(state w behavious) drthom la79ach les fonctions li jayin makay9doch y returniw valeur dyal variable tcreeat f wst if w else, wlkn ba9i lmochkil li gtlk fl audio
def FS_state(value):
	state=''
	if value == '0001':
		state = 'cleanly unmounted'
	elif value == '0002':
		state = 'Error detected'
	elif value == '0004':
		state = 'Orphans being recovred'
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


