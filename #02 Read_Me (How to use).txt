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

  모든 개발은 python3.6 환경에서 이루어졌다.
  아래 python code를 실행 시키기 위해서는 추가 모듈이 필요하다.

======================================= 환경설정 ================================================

  1. Window
	- Window환경에서 python3를 설치, 실행 경로 지정
	- cmd화면에서 pip install openpyxl을 실행 (openpyxl 모듈 설치)
	- cmd화면에서 pip install piexif 실행 (piexif 모듈 설치)
	  (단, python2와 같이 설치 되어 있을 경우 pip3를 이용하여 실행)
	- python2와 함께 설치가 되어 있을 경우 cmd에서 python 입력 시 python3가 실행되도록 설정

  2. Linux
	- Linux 터미널 창에서 다음과 같이 python3.6 설치
		1) wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz
		2) tar xvfz Python-3.6.4.tgz 
		3) cd Python-3.6.4/
		4) /configure
		5) make
	- 다음과 같은 명령어로 python3를 명령어로 실행할 수 있도록 설정
		1) cd /usr/bin/
		2) ln -s /root/Python-3.6.4/python ./python3

======================================== 실행방법 ===============================================

  1. exif2excel : 그림파일의 exif를 ifd와 tag, value를 excel로 정리
	- Window : cmd 창에서 wincmd_parsing2excel.py를 실행
	- Linux : Terminal 창에서 linux_parsing2excel.py를 실행
		=> linux의 경우 python3 linux_parsing2excel.py
			-> 실행하고자 하는 python code앞에 python3로 실행.
	
	단, 해당 python code를 이용하여 jpg 형식의 exif를 excel로 생성하려고 할 경우,
	    그림파일이 있는 경로에서 실행해야 한다!!!
	-> 압축파일의 경우 압축을 실행할 경로에 그림파일로 해제

  2. tag_value_search.py
     - 실행 코드를 포함하여 입력 인자 argv가 총 3개 필요하다.

	- Window : cmd 창에서 tag_value_search.py [ifd] [tag name] 실행
	- Linux : Terminal 창에서tag_value_search.py [ifd] [tag name] 실행
		=> linux의 경우 python3 tag_value_search.py [ifd] [tag name] 
			-> 실행하고자 하는 python code앞에 python3로 실행.

  * ifd는 exif2excel의 단계를 수행했을 때, 생성되는 excel file에서
    존재하는 sheet들의 이름. [ ex) 0th, Exif...]
  * Tag name은 생성 된 excel file에서 각 sheet의 A열 참조하여 대소문자 구별하여 입력!











