# These are just two example files I used to test this program!
'''https://www.youtube.com/watch?v=eukOuR4vqjg
   https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p
'''
# Enter your default path here:
path = "/home/hp/Videos"

# Now the whole code part
import os
import sys
import re
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
except Exception as e:
	print(e)
	print("An error occured, Sorry")
	sys.exit()

# I rather not touch this function below,if I were you because it was difficult getting it working!
def barr(stream, file_handler, bytes_remaining):
	erase = '\x1b[1A\x1b[2K'
	w = stream.filesize
	n = ((abs(w-bytes_remaining)*100)//w)
#	global s
	print(" Progress : "+str(n)+"% :  |",end ="")
	for i in range(n):
#		print("|",end="|")
		sys.stdout.write("#")
#		s=n
	for i in range(n,100):
		sys.stdout.write(" ")
	sys.stdout.write("|")
	print(erase)
#	print("done")


def complete(stream, file_handle):
	print("\n Download Complete\n")


def direc_regex(s):
	a = s.replace(" ","_")
	bad_char = list(set(re.sub('[A-Za-z0-9_]+',"",a)))
	for i in bad_char:
		a = a.replace(i,"")
	return(a)


def directify(s, flg=0):
	r=[' ', '+', '*', '<', '>', '$', '%', '\\', '^', '@', '#', '!', "(", ")"]
	if flg ==0:
		r.append('/')
	if flg == 2:
		return(direc_regex(s))
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
	except Exception as e:
		print(" Error!! ")
		print(e, end="")
		print(" has occured while Downloading \n")
#		flg=1
#	if flg==0:
#		print(" Video has been downloaded!! ")


def post_process(title, path, f1, f2):
	command = "ffmpeg -i "+f1+" -i "+f2+" -c copy -map 0:v:0 -map 1:a:0 "+title+".mkv"
	flag = 0
	try:
		os.chdir(path)
	except Exception as e:
		print(e)
		sys.exit()
	try:
		os.system(command)
		flag = 1
	except Exception as e:
		print(e)
		print(" The attempt at post processing failed, but don't you worry, the video and audio files are still there!")
	else:
		if flag ==1:
			path2 = os.path.join(path,f1)
			path3 = os.path.join(path,f2)
			try:
				os.remove(path2)
				os.remove(path3)
			except Exception as e:
				print(e)
				print(" Post Processing has been successful, but we failed to delete the temporary files!")
#				print(" The End file has the .mkv extension so use that :-)\n")
			else:
				print("\n Post Processing Complete!!\n")


def adv_playlst():
	global path
	path2 = path
	ch =0
	aflag =0
	print(" Advanced options Menu : ")
	while(ch != 3 ):
		print(" 1. Set Save path ")
		print(" 2. Download audio only ")
		print(" 3. Finish setup and start download")
		print(" 0. Exit\n")
		print(" Enter Choice :  ",end = "")
		ch = int(input())
		if ch == 0:
			sys.exit()
		if ch ==1:
			print(" The Current location for downloading is : ", end="")
			print(path)
			print(" Enter new path in a similar form :  ", end = "")
			p2 = input()
			print(" Checking for invalid characters and presence of Directory: ", end="")
			p2 = directify(p2,1)
#			p2 = p2.split('/')
#			path2 = ""
#			for i in range(len(p2)-1):
#				path2 = p2[i] + "/"
			try:
				os.chdir(p2)
			except FileNotFoundError:
				print(" No such file or directory!! try again \n")
				continue
			else:
				print(" Done! \n")
				path2 = p2
#				ch =3
		elif ch ==2:
			print(" Audio only download set \n")
			aflag = 1
#			ch=3
		elif ch != 3:
			print(" Invalid option Try again \n")
	return path2, aflag			


# Advanced options menu for video
def adv_video(vid):
	codes= []
	global path
	fin = vid.filter(type = 'video',progressive = True).order_by('resolution').last()
	title = directify(fin.title)
	process_flag=0
	ch = 1
	path2 = path
	print(" Advanced options Menu : ")
	while(ch != 4 ):
		print(" 1. Select Resolution and FPS ")
		print(" 2. Set Save path ")
		print(" 3. Download audio only ")
		print(" 4. Finish setup and download")
		print(" 0. Exit\n")
		print(" Enter Choice :  ",end = "")
		ch = int(input())
		if ch == 0:
			sys.exit()
		if ch == 1:
			print("Available options are :  \n")
			vid2 = vid.filter(type = "video").order_by('resolution')			
			for i in range(len(vid2)):
				codes.append([vid2[i].resolution, vid[i].fps, str(vid[i].audio_codec), vid[i].video_codec ])
			for i in range(len(codes)):
				print("\t\t| ", str(i+1) , " | Res = ", codes[i][0], " | FPS = ", codes[i][1], " | Audio codec : ", codes[i][2], " | Video Codec : ",codes[i][3], " |")
			print("\n\tWhich Option do you prefer? : ", end="")
			c = int(input()) - 1
			if c < len(codes) and c >=0:
				print(" Okay! ")
				fin = vid2[c]
				if fin.is_adaptive:
					title = directify(title,2)
					print("Downloading Video part and then the audio part, We will try to join them\n")
					f1 = title+"."+fin.subtype
					print(f1)
					dnld(fin,path2,title)
					fin = vid.filter(type = "audio").order_by('abr').last()					
					title2 = title
					title = title + "Audio"
					f2 = title+"."+fin.subtype
					print(f2)
					process_flag = 1
				ch = 4
			else:
				print(" This is not a valid option ! ")
		if ch == 2:
			print(" The Current location for downloading is : ", end="")
			print(path)
			print(" Enter new path in a similar form :  ", end = "")
			p2 = input()
			print(" Checking for invalid characters and presence: ", end="")
			p2 = directify(p2,1)
#			p2 = p2.split('/')
#			path2 = ""
#			for i in range(len(p2)-1):
#				path2 = p2[i] + "/"
			try:
				os.chdir(p2)
			except FileNotFoundError:
				print(" No such file or directory!! try again\n")
				continue
			else:
				print(" Done!! \n")
				path2 = p2
#				ch =4
		if ch ==3:
			print(" Audio only Download mode set\n")
			fin = vid.filter(type = "audio").order_by('abr').last()
			path2 = path.replace("Videos","Music")
			title = directify(fin.title)
#			ch = 4
		elif ch not in [1,2,3,4]:
			print(" Invalid choice !! \n")		
	if ch==4:
		dnld(fin,path2,title)
	if process_flag ==1:
		print(" Starting post processing!, Dont worry about the messages that come out next :-) ")
		post_process(title2, path2, f1, f2)


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
	global path
	path2 = path
	flag =1
	aflag = 0
	print(" The Playlist is "+yt.title()+" . Continue?  (y/n) : ",end="" )
	ch = input()
	if  ch =='a' or ch == 'A':
		path2 , aflag = adv_playlst()
		ch = 'y'
	if ch == 'y' or ch =='Y':
		os.chdir(path2)
		title = directify(yt.title(),2)
		while(flag ==1):
			try:
				os.mkdir(title)
				flag=2
			except FileExistsError:
				title = title + '1'
				continue	
#				os.mkdir(title)
			except Exception as e:
				print(e)
				print(" There is a problem making a new file\n\n")
				main()
				sys.exit()
		path2 = path2 + '/'+ title
		for i in range(len(l)):
			print(" Downloading video : "+str(i+1))
			yt2= errlist(l[i],0)
			yt2.register_on_complete_callback(complete)
#			yt2.register_on_progress_callback(barr)
			if aflag ==1:
				vid2 = yt2.streams.filter(type = "audio").order_by('abr').last()
			else:
				vid2 = yt2.streams.filter(progressive = True).order_by('resolution').last()			
			title = directify(vid2.title)
			dnld(vid2,path2,title)		


def video(yt):
	global path
	yt.register_on_complete_callback(complete)
#	yt.register_on_progress_callback(barr)
	print("The video is : "+yt.title+ " are you sure?(y/n):  ",end="")
	ch = input()
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
		adv_video(vid)		
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
	elif 'user' in link:
		print(" This is a whole channel!! Not downloading that!")
		main()
		sys.exit()
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
