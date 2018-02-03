#!/usr/bin/python
# -*- coding : utf-8 -*-
# -*- coding : cp949 -*-

import sys
import os
import win32api
from struct import *

def Drive_exist_check(drive_name) :
	try:
		drive_path = win32api.GetVolumeInformation(drive_name+":\\\\")
		#print(drive_path)
		if drive_check(drive_path[4]) == 1 :
			return 1
		else :
			print ("\nThis Drive FileSystem is not FAT32")
	except :
		print ("Can not find!")

def drive_check(driveformat) :
	if driveformat == "FAT32" :
		return 1
	else :
		return 0

def order_string_set(num) :
	global order_string

	if num == 1 :
		order_string = 'st'
	elif num == 2 :
		order_string = 'nd'
	elif num == 3 :
		order_string = 'rd'
	else :
		order_string = 'th'

	return order_string

def vbrAREA() :
	global bps, spc, reserved_sector, fatSize32
	vbr = whole_data.read(0x200)
	bps = unpack('<H',vbr[0x0B:0x0D])[0] # Bytes per Sector
	spc = vbr[0x0D] #Sectors per Cluster
	reserved_sector = unpack('<H',vbr[0x0E:0x10])[0] # Result Value's Unit : Sector
	number_of_FatTable = vbr[0x10]
	media_Type = hex(vbr[0x15])
	hidden_Sector = unpack('<L', vbr[0x1C:0x20])[0]
	total_Sector = unpack('<L', vbr[0x20:0x24])[0]
	fatSize32 = unpack('L', vbr[0x24:0x28])[0] # Result Value's Unit : Sector
	rootDir_Cluset_offset = unpack('<L', vbr[0x2C:0x30])[0]
	FSINFO_sector_loc = unpack('<H', vbr[0x30:0x32])[0]
	backup_bootsector_offset = unpack('<H', vbr[0x32:0x34])[0]
	volume_name = unpack('11s', vbr[0x47:0x52])[0]
	FStype = unpack('8s', vbr[0x52:0x5A])[0]
	signature = hex(unpack('<H', vbr[0x1FE:0x200])[0])

	if media_Type == '0xf8' :
		media = 'Disk'
	elif media_Type == '0xf0' :
		media = 'Floppy Disk'
	else :
		print ("I don't know, what is this")

	print ("\t\t[-] Bytes per Sector : %d" % bps)
	print ("\t\t[-] Sectors per Cluster : %d" % spc)
	print ("\t\t[-] Reserved Sector Count : %d" % reserved_sector)
	print ("\t\t\t\t - **** Next Reserved Sector Count is FAT AREA #1 **** ")
	print ("\t\t\t  - **** We Need to Analysis FAT Area #1 for find Allocated Area ****")
	print ("\t\t[-] Media Type : %s (%s)" % (media_Type, media))
	print ("\t\t[-] Hidden Sector Count : %d" % hidden_Sector)
	print ("\t\t[-] FAT32 Size FAT #? Area Size  : %d sectors (%d Bytes)" % (fatSize32, sector2Bytes(fatSize32)))
	print ("\t\t[-] Root Directory Cluster Offset : %d" % rootDir_Cluset_offset)
	print ("\t\t[-] FSINFO Sector Located : %d%s Sector" % (FSINFO_sector_loc, order_string_set(FSINFO_sector_loc)))
	print ("\t\t[-] backup_bootsector_offset : %d%s Sector" % (backup_bootsector_offset, order_string_set(backup_bootsector_offset)))
	print ("\t\t[-] volume_name : %s" % volume_name)
	print ("\t\t[-] File System Type : %s" % FStype)
	print ("\t\t[-] End signature : %s" % signature)

def FSINFO_Area() :
	global FS_Free_Cluster_Count
	FS_data = whole_data.read(0x200)
	FS_Lead_signature_string = unpack('4s', FS_data[0x00:0x04])[0]
	FS_Lead_signature = unpack('<L', FS_data[0x00:0x04])[0]
	FS_struct_signature_string = unpack('4s', FS_data[0x1E4:0x1E8])[0]
	FS_struct_signature = unpack('<L', FS_data[0x1E4:0x1E8])[0]
	FS_Free_Cluster_Count = unpack('<L', FS_data[0x1E8:0x1EC])[0]
	FS_Next__Free_Cluster_loc = unpack('<L', FS_data[0x1EC:0x1F0])[0]
	FS_Trail_Signature = hex(unpack('<H', FS_data[0x1FE:0x200])[0])
	test = hex(unpack('<H', FS_data[510:512])[0])

	#print (hex(FS_Lead_signature))

	if (hex(FS_Lead_signature) != "0x41615252") and (hex(FS_struct_signature) != "0X61417272") :
		print ('Is not FSINFO Area')
		return 0
	else :
		pass

	print ("\t\t[-] FSINFO Signature_1 : %s(%s)" % (FS_Lead_signature_string, hex(FS_Lead_signature)))
	print ("\t\t[-] FSINFO Signature_2 : %s(%s)" % (FS_struct_signature_string, hex(FS_struct_signature)))
	print ("\t\t[-] FS Free Cluster Count : %d EA" % FS_Free_Cluster_Count)
	print ("\t\t[-] FS Next Free Cluset Location : %d%s Cluster" % (FS_Next__Free_Cluster_loc, order_string_set(FS_Next__Free_Cluster_loc)))
	print ("\t\t[-] FS Trail Signature : %s" % FS_Trail_Signature)

def FATArea() :
	global dataCluster_Count, Non_Data_Cluster, Data_Cluster
	Fat_1_start_loc = sector2Bytes(reserved_sector) # nth Byte of whole disk data Bytes
	sizeFAT = sector2Bytes(fatSize32)
	FA_Custers_Count = int(sizeFAT / 4) # 1 Cluster is expressed by 4Bytes (FAT32 : 4Bytes)
	dataCluster_Count = FA_Custers_Count - 2 # 1st Cluster : Media, 2nd : Partition Status
	whole_data.seek(Fat_1_start_loc)
	Non_Data_Cluster = whole_data.read(0x08)
	Data_Cluster = whole_data.read(sizeFAT-0x08)

	Media_Type_FA1 = hex(unpack('<L', Non_Data_Cluster[0x00:0x04])[0])
	Partition_Stauts = hex(unpack('<L', Non_Data_Cluster[0x04:0x08])[0])

	print ("\t\t[-]FAT #1 Offset : %s" % hex(Fat_1_start_loc))
	print ("\t\t\t[-] Fixed Allcoated Area FAT32")
	print ("\t\t\t\t[-] Media Type : %s" % Media_Type_FA1)
	print ("\t\t\t\t[-] Partition Stauts : %s" % Partition_Stauts)
	

def sector2Bytes (sector_count) :
	return sector_count * bps

def cluster2Sector (cluster_count) :
	return cluster_count * spc

def findUnAllocate() :
	global buf
	buf = 0
	while (buf < FS_Free_Cluster_Count) :
		temp = unpack('4s', Data_Cluster[(buf*4):((buf*4)+4)])[0]
		if temp == b'\x00\x00\x00\x00' :
			#print ("unAllocated : %d%s Cluster (Cluster %d)" % (buf+3, order_string_set(buf), buf+2))
			into_Cluster(buf)
			buf += 1
		else :
			buf += 1
'''			file_cluster = (go_RootDir() / 512 / 8)
			if file_cluster == int(file_cluster) :
				buf = buf + file_cluster
			else :
				buf = buf + int(file_cluster) + 1 
			print ("rounding : %d" %buf)
		else :
			buf = buf + 1'''
def UnAlloc_print() :
	#return ("unAllocated : %d%s Cluster (Cluster %d)" % (buf+3, order_string_set(buf), buf+2))
	return ("\t\t[-] Cluster %d - " % (buf+2))


def into_Cluster(cluster_no) :
	global file_sig_range, unAllo_cluster_offset
	unAllo_cluster_offset = sector2Bytes((reserved_sector + fatSize32 * 2) + cluster2Sector(buf))
	whole_data.seek(unAllo_cluster_offset)
	file_sig_range = whole_data.read(0x20) # hwp old version's signature is 17bytes
	file_sig_b2 = hex(unpack('<H', file_sig_range[0x00:0x02])[0])
	file_sig_b3 = hex(file_sig_range[0x02]) + file_sig_b2[2:]
	file_sig_b4 = hex(unpack('<L', file_sig_range[0x00:0x04])[0])
	file_sig_b8 = hex(unpack('<Q', file_sig_range[0x00:0x08])[0])
	file_sig_b6 = "0x" + file_sig_b8[6:]
	file_sig_b16_1 = hex(unpack('>QQB', total[0x00:0x11])[0])
	file_sig_b16_2 = hex(unpack('>QQB', total[0x00:0x11])[1])
	file_sig_b16_3 = hex(unpack('>QQB', total[0x00:0x11])[2])
	file_sig_b16 = file_sig_b16_1 + file_sig_b16_2[2:] + file_sig_b16_3[2:]


	if file_sig_b2 == "0x5a4d" : # MZ
		result = check_signature_exe(file_sig_b3, file_sig_b8)
		if result == 1 :
			print(UnAlloc_print() + "MZ Executable File")
		else :
			print (UnAlloc_print() + result)
	elif file_sig_b2 == "0x4d42" :
		print (UnAlloc_print() + ".bmp (Windows Bitmap Image)")

	elif signature_print(file_sig_b3) != 0 :
		print (UnAlloc_print() + signature_print(file_sig_b3))

	elif signature_print(file_sig_b4) != 0 :
		if file_sig_b4 == "0x4034b50" : # PK
			if ext_pk_analysis() == 'zip' :
				print (UnAlloc_print() + ext_pk_analysis() + " {" +filename_inzip())
			else :
				print (UnAlloc_print() + ext_pk_analysis())
		elif signature_print(file_sig_b6) != 0 :
			print (UnAlloc_print() + signature_print(file_sig_b6))

	elif signature_print(file_sig_b6) != 0 :
		print (UnAlloc_print() + signature_print(file_sig_b6))

	elif (signature_print(file_sig_b8)) != 0 :
		print (UnAlloc_print() + signature_print(file_sig_b8))

	elif file_sig_b16 == "0x48575020446f63756d656e742046696c65" : # hwp old version signature (97 ~ 3.0)
		print (UnAlloc_print() + "hwp (97 ~ 3.0 old version)")

def check_signature_exe(bytes3, bytes8) :
	if bytes3 == '0x905a4d' :
		return "exe (Microsoft Executable)"
	elif bytes8 == '0x300905a4d' :
		return ".acm (Executable) or .dll (Dynamic Link Library)"
	else :
		return 1

def ext_pk_analysis () :
	pk_classfi = hex(unpack('>L', file_sig_range[0x04:0x08])[0])
	if pk_classfi == "0x14000600" : # zip / docx, pptx, xlsx
		whole_data.seek(unAllo_cluster_offset)
		file_data = whole_data.read(0xA00) # https://kldp.org/node/141380
		if 'word/document' in str(file_data) :
			return "zip [docx] (MS Word 2007+)"
		elif 'xl/worksheets/' in str(file_data) :
			return "zip [xlsx] (MS Excel 2007+)"
		elif 'ppt/slides' in str(file_data) :
			return "zip [pptx] (MS PowerPoint 2007+)"
	else :
		whole_data.seek(unAllo_cluster_offset)
		file_data = whole_data.read(0xA00) 
		if 'xl/worksheets/' in str(file_data) :
			return "zip [xlsx] (MS Excel 2007+)"
		else :
			return "zip"

	"""http://blog.naver.com/PostView.nhn?blogId=koromoon&logNo=220612641115&parentCategoryNo=
		&categoryNo=&viewDate=&isShowPopularPosts=false&from=postView - ZIP File Header """

def filename_inzip () : 
	whole_data.seek(unAllo_cluster_offset)
	zipfileHeader = whole_data.read(0x1E)
	#print (zipfileHeader)
	Header_sig = hex(unpack('>L', zipfileHeader[0x00:0x04])[0])
	filename_len = unpack('<H', zipfileHeader[0x1A:0x1C])[0]
	cnt = 0
	while True :
		find_end_of_dir_record = whole_data.read(0x04)
		if  "0x504b0506" == hex(unpack('>L', find_end_of_dir_record[0x00:0x04])[0]) :
			break
		else :
			cnt += 1
			pass
	whole_data.seek(unAllo_cluster_offset + 0x1E + (cnt*4))
	end_of_dir_record = whole_data.read(0x16)
	filecnt_in_zip = unpack('<H', end_of_dir_record[0x0A:0x0C])[0]

	if Header_sig == "0x504b0304" :
		whole_data.seek(unAllo_cluster_offset+0x1E)
		return ("first file name : " + str(whole_data.read(filename_len))[2:-1]
		 + "}\n\t\t\t[-] Total file count in zip : %d files" % filecnt_in_zip)


def signature_print(sig) :
	global sig_b3, sig_b4, sig_b6, sig_b8
	sig_b3 = {"0x685a42" : "bz or bz2 (Bzip Archive)", "0x88b1f" : "gz (GZ Compressed File)",
	"0x2a4949" : "tif or tiff (Little Endian)", "0x2a4d4d" : "tif or tiff (Big Endian)"}

	sig_b4 = {"0x20495641" : "avi", "0x46464952" : "avi", "0x35706733" : "mp4 (MPEG-4 Video File)",
	"0xe1ffd8ff" : "jpg (JPG Graphical File)", "0xe0ffd8ff" : "JPG (JPG Graphical File)","0x3334449" : "mp3 (MP3 Audio)", "0x1b3" : "mpg or mpeg (MPEG Movie)",
	"0x7461646d" : "mov (QuickTime Movie)", "0x766f6f6d" : "mov (QuickTime Movie)", "0x3e8000f" : "ppt (PowerPoint Presentation)",
	"0x2a004949" : "tif or tiff (Little Endian)", "0x2a004d4d" : "tif or tiff (Big Endian)", "0xfeffd8ff" : "jpeg (JPG Graphical File)",
	"0x15a4c41" : "alz (ESTsoft Alzip Archive)", "0x4034b50" :"Archive files"}
	
	sig_b6 = {"0x613738464947" : "gif (Graphics Interchange Format)", "0x613938464947": "gif (Graphics Interchange Format)",
	"0x70695a6e6957" : "winzip (Winzip Archive)", "0x4554494c4b50" : "zip (PKLITE ZIP Archive)"}

	sig_b8 = {"0x1426a46464952" : "avi (Audio Video interleave File", "0x30322f32312f335b" : "bak (BackUp)",
	"0x6d6d7544204d4552" : "bat (Batch File)", "0x50414dff434353ff" : "bin (Binary File)", "0x6576206c6d783f3c" : "config (xml config file)",
	 "0x461c0d3e0002014c" : "exp (Export File)", "0x505954434f44213c" : "htm (HyperText Markup)",
	 "0x6576206c6d783f3c" : "msc (Microsoft Magement Console Snap-in Control File", "0x10000000060409" : "xml (MS Excel)",
	 "0x332e312d46445025" : "pdf (Adobe Portable Document File)", "0x342e312d46445025" : "pdf (Adobe Portable Document File)",
	 "0x0a1a0a0d474e5089" : "png (Portable Network Graphic)", "0x4143435300000011" : "pf (Windows Prefetch File)",
	 "0x7079746618000000" : "mp4 (MPEG-4 Video File)", "0x707974661c000000" : "mp4 (MPEG-4 Video File)", 
	 "0x8001404034b50" : "jar (Java Archive)", "0xe11ab1a1e011cfd0" : "hwp"}

	if sig in sig_b3.keys() :
		return sig_b3[sig]
	elif sig in sig_b4.keys() :
		return sig_b4[sig]
	elif sig in sig_b6.keys() :
		return sig_b6[sig]
	elif sig in sig_b8.keys() :
		return sig_b8[sig]
	else :
		return 0

if __name__ == '__main__' :
	drive_name = input("\n======> Write the Logical Drive Name : ")
	if Drive_exist_check(drive_name) == 1 :
		global whole_data
		whole_data = open("\\\\.\\" + drive_name + ":", 'rb')
		print ("\n\t[+] FAT32 VBR Area")
		vbrAREA()
		print ("\n\t[+] FSINFO Area")
		FSINFO_Area()
		print ("\n\t[+] FAT Area 1")
		FATArea()
		print ("\n\t[+] UnAllocated Cluster")
		findUnAllocate()
		whole_data.close()

	else :
		print ("\nProgram is Over")
