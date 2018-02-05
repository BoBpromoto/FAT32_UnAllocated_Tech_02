		===============================================================
		|| 	BoB 6th Digital_Forensic 3rd Stage Assignment	     ||
		||							     ||
		||	    Category : Tech 	      No. 03		     ||	
		||							     ||
		||		@Author : L3ad0xff (Lee Moonwon)	     ||
		||							     ||
		||	       Groping by Exif's Tag values and		     ||
		||	        What is artificially modulated?		     ||
		===============================================================

  ��� ������ python3.6 ȯ�濡�� �̷������.
  �Ʒ� python code�� ���� ��Ű�� ���ؼ��� �߰� ����� �ʿ��ϴ�.

======================================= ȯ�漳�� ================================================

  1. Window
	- Windowȯ�濡�� python3�� ��ġ, ���� ��� ����
	- cmdȭ�鿡�� pip install openpyxl�� ���� (openpyxl ��� ��ġ)
	- cmdȭ�鿡�� pip install piexif ���� (piexif ��� ��ġ)
	  (��, python2�� ���� ��ġ �Ǿ� ���� ��� pip3�� �̿��Ͽ� ����)
	- python2�� �Բ� ��ġ�� �Ǿ� ���� ��� cmd���� python �Է� �� python3�� ����ǵ��� ����

  2. Linux
	- Linux �͹̳� â���� ������ ���� python3.6 ��ġ
		1) wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz
		2) tar xvfz Python-3.6.4.tgz 
		3) cd Python-3.6.4/
		4) /configure
		5) make
	- ������ ���� ��ɾ�� python3�� ��ɾ�� ������ �� �ֵ��� ����
		1) cd /usr/bin/
		2) ln -s /root/Python-3.6.4/python ./python3

======================================== ������ ===============================================

  1. exif2excel : �׸������� exif�� ifd�� tag, value�� excel�� ����
	- Window : cmd â���� wincmd_parsing2excel.py�� ����
	- Linux : Terminal â���� linux_parsing2excel.py�� ����
		=> linux�� ��� python3 linux_parsing2excel.py
			-> �����ϰ��� �ϴ� python code�տ� python3�� ����.
	
	��, �ش� python code�� �̿��Ͽ� jpg ������ exif�� excel�� �����Ϸ��� �� ���,
	    �׸������� �ִ� ��ο��� �����ؾ� �Ѵ�!!!
	-> ���������� ��� ������ ������ ��ο� �׸����Ϸ� ����

  2. tag_value_search.py
     - ���� �ڵ带 �����Ͽ� �Է� ���� argv�� �� 3�� �ʿ��ϴ�.

	- Window : cmd â���� tag_value_search.py [ifd] [tag name] ����
	- Linux : Terminal â����tag_value_search.py [ifd] [tag name] ����
		=> linux�� ��� python3 tag_value_search.py [ifd] [tag name] 
			-> �����ϰ��� �ϴ� python code�տ� python3�� ����.

  * ifd�� exif2excel�� �ܰ踦 �������� ��, �����Ǵ� excel file����
    �����ϴ� sheet���� �̸�. [ ex) 0th, Exif...]
  * Tag name�� ���� �� excel file���� �� sheet�� A�� �����Ͽ� ��ҹ��� �����Ͽ� �Է�!











