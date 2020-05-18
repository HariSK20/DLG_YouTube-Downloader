'''https://www.youtube.com/watch?v=eukOuR4vqjg
   https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p
'''

import os
import sys
try:
	from pytube import YouTube, Playlist
except ModuleNotFoundError:
	print("Looks like you havent downloaded PyTube in your system. May I?(y/n): ")
	ch = input()
	if ch == 'y' or ch =='Y':
		s = os.system('python3 -m pip install pytube3')
		if s == 0:
			print(" PyTube has been installed successfully!! Lets go")
			os.system('python3 dlg.py')
			sys.exit()
		else:
			print(" Sorry, we are facing trouble right now, Please try again Later")
			sys.exit() 
	else:
		print(" Without it we cannot download videos, forced quit activated!")
		sys.exit()
except:
	print("An error occured, Sorry")
	sys.exit()

# Do not touch the following function!! I am Warning you!!
def barr(stream, file_handler, bytes_remaining):
	erase = '\x1b[1A\x1b[2K'
	w = stream.filesize
	n = ((abs(w-bytes_remaining)*100)//w)
#	global s
	print(" Progress : "+str(n)+"% :  ",end ="")
	for i in range(n):
#		print("|",end="|")
		sys.stdout.write("#")
#		s=n
	for i in range(n,101):
		sys.stdout.write(" ")
	sys.stdout.write("|")
	print(erase)
#	print("done")


def complete(stream, file_handle):
	print("\n Download Complete\n")


def directify(s, flg=0):
	r=[' ', '+', '*', '<', '>', '$', '%', '\\', '^', '@', '#', '!']
	if flg ==0:
		r.append('/')
	a = s
	for i in r:
		if i in s:
			a = a.replace(i,'_')
	return(a)


def dnld(vid,path,title):
	flg = 0
	print("\n")
	try:
		vid.download(path,title)
	except:
		print(" Some unfortunate error has occured while Downloading \n")
#		flg=1
#	if flg==0:
#		print(" Video has been downloaded!! ")
	
# Advanced options menu for video
def get_rfps(vid):
	codes= []
	fin = vid.filter(type = 'video',progressive = True).order_by('resolution').last()
	title = directify(fin.title)
	path = "/home/hp/Videos"
	ch = 1
	print(" Advanced options Menu : ")
	while(ch != 4):
		print(" 1. Select Resolution and FPS ")
		print(" 2. Set Save path ")
		print(" 3. Download audio only ")
		print(" 4. Finish setup and download \n")
		print(" Enter Choice :  ",end = "")
		ch = int(input())
		if ch == 1:
			print("Available options are :  \n")
			vid2 = vid.filter(type = "video", progressive = True)			
			for i in range(len(vid2)):
				codes.append([vid2[i].resolution, vid[i].fps])	
			for i in range(len(codes)):
				print("\t\t| ", str(i+1) , " | Res = ", codes[i][0], " | FPS = ", codes[i][1], " |")
			print("\n\tWhich Option do you prefer? : ", end="")
			c = int(input()) - 1
			if c < len(codes) and c >=0:
				print(" Okay! ")
				fin = vid2[c]
				ch =4
			else:
				print(" This is not a valid option ! ")
		elif ch == 2:
			print(" The Current location for downloading is : ", end="")
			print(path)
			print(" Enter new path in a similar form :  ", end = "")
			p2 = input()
			print(" Checking for invalid characters : ")
			p2 = directify(p2,1)
#			p2 = p2.split('/')
#			path2 = ""
#			for i in range(len(p2)-1):
#				path2 = p2[i] + "/"
			try:
				os.chdir(p2)
				path = p2
				ch =4
			except FileNotFoundError:
				print(" No such file or directory!! try again")
				continue			
		elif ch ==3:
			fin = vid.filter(type = "audio").order_by('abr').last()
			path = "/home/hp/Music"
			title = directify(fin.title)
			ch = 4
		elif ch != 4:
			print(" Invalid choice !! ")		
	dnld(fin,path,title)


def errlist(link, flg):
	try:
		if flg==0:
			yt = YouTube(link, on_progress_callback = barr)
		else:
			yt = Playlist(link)
	except pytube.exceptions.RegexMatchError:
		print(" Video is not found, please check again")	
	except pytube.exceptions.ExtractError:
		print("Sorry an Extraction error has occured")
	except pytube.exception.VideoUnavailable:
		print(" Sorry Video is unavailable for download")	
	except pytube.exceptions.LiveStreamError:
		print(" The video link is for a Live Stream, cannot be downloaded now")
	except:
		print("Sorry there's a connection Error, Try again")
		return(-1)
	if flg == 0:	
		print(" Video has been linked ")
	else:
		print(" Playlist has been linked ")
	return(yt)
	

def playlistd(yt):
	l = yt.video_urls
	print(" The Playlist is "+yt.title()+" . Continue? (press a for downloading audio only) (y/n) : ",end="" )
	ch = input()
	if ch == 'y' or ch =='Y' or ch =='a' or ch == 'A':
		path2 = '/home/hp/Videos'
		title = directify(yt.title())
		os.chdir(path2)
		e=1
		while(flag ==1):
			try:
				os.mkdir(title)
				flag=2
			except FileExistsError:
				title = title + '1'
				continue	
#				os.mkdir(title)
			except:
				print(" There is a problem making a new file\n\n")
				main()
				sys.exit()
		path2 = path2 + '/'+ title
		for i in range(len(l)):
			print(" Downloading video : "+str(i+1))
			yt2= errlist(l[i],0)
			yt2.register_on_complete_callback(complete)
#			yt2.register_on_progress_callback(barr)
			if ch == 'a' or ch == 'A':
				vid2 = yt2.streams.filter(type = "audio").order_by('abr').last()
			else:
				vid2 = yt2.streams.filter(progressive = True).order_by('resolution').last()			
			title = directify(vid2.title)
			dnld(vid2,path2,title)		


def video(yt):
	yt.register_on_complete_callback(complete)
#	yt.register_on_progress_callback(barr)
	print("The video is : "+yt.title+ " are you sure?(y/n):  ",end="")
	ch = input()
	path = "/home/hp/Videos"
	if ch == 'y' or ch =='Y':
		vid = yt.streams.filter(progressive = True, type = "video").last()
		title = directify(vid.title)
#		print(title)
		dnld(vid,path,title)
	elif ch == 'n' or ch == 'N':
		main()
#		sys.exit()
	elif ch == 'a' or ch == 'A':
		vid = yt.streams
		get_rfps(vid)		
	else:
		print("I am going to take it as a no ")
		main()
		sys.exit()


def main():
	print("\nEnter the link to download the video (enter 0 to exit): ")
	link = input()
	if link == "0":
		sys.exit()
	print("\t Linking \n")
	listflg=0
	if 'playlist' in link:
		listflg =1
	yt= errlist(link,listflg)
	if yt == -1:
		main()
		sys.exit()
	if listflg == 0:
		video(yt)
	else:
		playlistd(yt)
	

if __name__ == '__main__':
	main()
