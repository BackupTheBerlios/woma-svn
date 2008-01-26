#!/usr/bin/python
#
# main.py
# Copyright (C) WoodenJesus 2007 <woodenjesus666@gmail.com>
# 
# main.py is free software.
# 
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 2 of the License, or (at your option)
# any later version.
# 
# main.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with main.py.  If not, write to:
# 	The Free Software Foundation, Inc.,
# 	51 Franklin Street, Fifth Floor
# 	Boston, MA  02110-1301, USA.


__version__ = '0.0.1'
__name__="__woma__"


import sys

import pygtk, gtk, gtk.glade
import subprocess, string , sys 
import mediainfo
import threading, time
import os, select
import re

woma = None
if '--version' in sys.argv:
    print __name__ ," version:", __version__
    sys.exit(0)


print "Welcom in ",__name__, " initial relase"

class WomaWindow:

	def __init__(self):
		
		#SET SOCKET
		
		self.getfileinfo = mediainfo.mediainfo ()
		self.glade = gtk.glade.XML("main.glade")
		self.window = self.glade.get_widget('main')
		self.window_fullscreen = self.glade.get_widget('window_fullscreen')
		self.dupa = self.glade.get_widget('dupa')
		self.pudlo = self.glade.get_widget('pudlo')
		#self.window_fullscreen.add (self.pudlo)
		#self.videobox = self.glade.get_widget('aspectframe1')
		self.videobox = gtk.AspectFrame(label=None, xalign=0.5, yalign=0.5,  obey_child=False)
		self.videobox.set_border_width(0)
		#self.note = self.glade.get_widget('vbox2')
		#self.background = gtk.EventBox()
		self.background = self.glade.get_widget('background')
		self.background.add (self.videobox)
		self.background.modify_bg ("normal", gtk.gdk.color_parse ("#000"))
		#self.note.add (self.background)
		self.videobox.ratio = 1.78
		self.videobox.set_shadow_type (gtk.SHADOW_NONE)
		self.videobox.set_border_width (0)
		

		
		self.hbox2 = self.glade.get_widget('hbox3')
		self.position = self.glade.get_widget('hscale1')

		self.socket = gtk.Socket()

		self.videobox.add(self.socket)
		#self.videobox.attach(self.socket,1, 2, 1, 2)
		self.socket.show()

		lol = self.videobox.check_resize()
		self.socket_id = self.socket.get_id()
	
		self.volume = gtk.VolumeButton()
		self.hbox2.add(self.volume)
		adj = gtk.Adjustment (lower = 0, upper = 100, step_incr = 2)
		self.volume.set_adjustment (adj)

		#CREATE VIDEO OBJECT
		self.video = Video(self.socket_id, self.volume, self.position)
		#self.connect_events(self.video)

		#connect_events(self, video)

		self.window = self.glade.get_widget('main')
		self.playbar = self.glade.get_widget('playtoolbar')
		#self.videobox.add(self.socket)


		self.icon_play = gtk.Image()
		self.icon_play.set_from_file("play.png") # Toolbar items should be 22x22 pixel images
		self.pauseplay = gtk.ToolButton(icon_widget=self.icon_play, label="Play/Pause")
		self.pauseplay.connect("clicked", self.video.pauseplay) # Connect the signal handler for the button
		self.playbar.insert(self.pauseplay, -1) # Add button to toolbar

		self.icon_stop = gtk.Image()
		self.icon_stop.set_from_file("stop.png") # Toolbar items should be 22x22 pixel images
		self.stop = gtk.ToolButton(icon_widget=self.icon_stop, label="Stop")
		self.stop.connect("clicked", self.video.stop) # Connect the signal handler for the button
		self.playbar.insert(self.stop, -1) # Add button to toolbar
		
		self.icon_fs = gtk.Image()
		self.icon_fs.set_from_file("fullscreen.png") # Toolbar items should be 22x22 pixel images
		self.fs = gtk.ToolButton(icon_widget=self.icon_fs, label="Fullscreen")
		self.fs.connect("clicked", self.fullscreen)
		self.dupa.connect("clicked", self.unfullscreen)
		self.playbar.insert(self.fs, -1) # Add button to toolbar

		self.openvideo = self.glade.get_widget('file')
		self.openvideo.connect("activate", self.OpenVideo)
		
		self.exit = self.glade.get_widget('exit')
		self.exit.connect("activate", self.Exit)
		
		self.window.connect ("destroy", self.Exit)
		
		#self.videobox.connect("size-allocate", self.ScaleVideo)
		
		self.volume.connect("value-changed", self.video.setVolume) # Connect the signal handler for the button
		#self.volume.connect("change-value", self.video.loli) # Connect the signal handler for the button		
		
		self.position.set_update_policy (gtk.UPDATE_DELAYED)
		self.position.connect("change-value", self.video.lolen) # Connect the signal handler for the button
		self.position.connect("value-changed", self.video.setPosition) # Connect the signal handler for the button

		
		self.window.show_all()

		print "connect events"

	def begin(self):
		pass
		
	def fullscreen (self, *args):
		self.window_fullscreen.show_all()
		self.background.reparent (self.pudlo)
		self.window_fullscreen.fullscreen ()		
		self.window.hide()
		#self.dupa.hide ()
		#self.fs.connect("clicked", self.unfullscreen)
		#self.window.unfullscreen ()
		
	def unfullscreen (self, *args):
		self.window.show_all()
		self.background.reparent (self.background)
		self.window.unfullscreen ()
		self.window_fullscreen.hide()
		#self.fs.connect("clicked", self.fullscreen)
		#self.window.unfullscreen ()

	def OpenVideo(self, button):
		dialog = gtk.FileChooserDialog("Open..",
										None,
										gtk.FILE_CHOOSER_ACTION_OPEN,
										(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
										gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)
	
		filter = gtk.FileFilter()
		filter.set_name("Video")
		filter.add_pattern("*.avi")
		filter.add_pattern("*.mkv")
		filter.add_pattern("*.ogm")
		dialog.add_filter(filter)

		filter = gtk.FileFilter()
		filter.set_name("All files")
		filter.add_pattern("*")
		dialog.add_filter(filter)
		
		response = dialog.run()
		if response == gtk.RESPONSE_OK:
			self.video.path = dialog.get_filename()
			print dialog.get_filename(), 'selected'
			self.tracks, self.media, self.dlugosc = self.getfileinfo.fileinfo(self.video.path)
			#print self.media
			lolek = float (self.media['VIDEO']['WIDTH']) / float (self.media['VIDEO']['HEIGHT'])
			self.videobox.set ( xalign=0.5, yalign=0.5, ratio=lolek, obey_child=False)
			self.position.set_range (0, int (self.dlugosc[0]))
			
			print lolek
			if self.media['VIDEO']['WIDTH'] == '1280':
				self.video.PlayVideo()
			else:
				self.video.PlayVideo('gl')
		elif response == gtk.RESPONSE_CANCEL:
			print 'Closed, no files selected'
		dialog.destroy() 

	def open_video(self, socket_id):
		return Video(self.socket_id)
		
	def Exit (self, *args):
		if self.video.playstatus != "STOP":
			self.video.vstdin.write('quit\n')
			self.video.lol.communicate()
		exit()
		
class OutputParse ( threading.Thread ):
	def __init__ (self, video):
		threading.Thread.__init__(self)
		self.video = video
		
	def run ( self ):
		while True:
			
			if self.video.playstatus == "PLAY":	
				self.video.exitstatus = self.video.wait ( )
				self.video.exitstatus
				if "NONE" not in self.video.exitstatus:
					self.video.playstatus = "STOP"
				
			if self.video.playstatus == "PLAY":	
				#if self.video.position_lock == False:
				self.video.vstdin.write('get_time_pos\n')
				self.video.vstdin.write('get_property volume\n')
				lol =  os.read (self.video.vstdout.fileno(), 10000)
				#print lol
				#media_regex = re.compile ('ANS_volume=(\w+)')
				#media_temp = media_regex.findall (lol)
				#if len (media_temp) > 0:
					#print media_temp.pop()
					#self.video.volume.set_value(int(media_temp.pop()))
				media_regex = re.compile ('ANS_TIME_POSITION=(\w+)')
				media_temp = media_regex.findall (lol)
				if len (media_temp) > 0 and self.video.position_lock == False:
					#print media_temp
					self.video.position.set_value(int(media_temp.pop()))
			time.sleep( 0.1 )
			

class Video:

	def __init__(self, socket_id, volume, position):
		
		
		print self
		self.video = None
		self.position_lock = False
		self.played = 0
		self.playerState = None
		self.socket_id = socket_id
		self.path = None
		self.exitstatus = 'LOL'
		self.position = position
		self.volume = volume
		self.playstatus = "STOP"
		#if (sys.argv[1] != None):
		#	self.path = sys.argv[1]
		#	self.play_video()
		
	def pid(self):
		"""Return the process id of the process.
		   Note that if the process has died (and successfully been waited
		   for), that process id may have been re-used by the operating
		   system.
		"""
		return self.video.pid	
			
	def wait(self, flags=os.WNOHANG):
		"""Return the process' termination status.

		   If bitmask parameter 'flags' contains os.WNOHANG, wait() will
		   return None if the process hasn't terminated.  Otherwise it
		   will wait until the process dies.

		   It is permitted to call wait() several times, even after it
		   has succeeded; the Process instance will remember the exit
		   status from the first successful call, and return that on
		   subsequent calls.
		"""
		#if self.__exitstatus is not None:
		#	return self.__exitstatus
		pid,exitstatus = os.waitpid(self.pid(), flags)
		if pid == 0:
			return 'EXIT_STATUS=NONE'
			#return None
		if os.WIFEXITED(exitstatus) or os.WIFSIGNALED(exitstatus):
			self.__exitstatus = exitstatus
			# If the process has stopped, we have to make sure to stop
			# our threads.  The reader threads will stop automatically
			# (assuming the process hasn't forked), but the feeder thread
			# must be signalled to stop.
				#if self.__process.stdin:
				#self.closeinput()
			# We must wait for the reader threads to finish, so that we
			# can guarantee that all the output from the subprocess is
			# available to the .read*() methods.
			# And by the way, it is the responsibility of the reader threads
			# to close the pipes from the subprocess, not our.
				#if self.__process.stdout:
				#self.__stdout_thread.join()
				#if self.__process.stderr:
				#self.__stderr_thread.join()
		#return exitstatus
		return 'EXIT_STATUS=' + str(exitstatus)
	
	def PlayVideo (self, vo = 'xv'):
		
		if (self.played == 1):
			if "STOP" not in  self.playstatus:
				self.vstdin.write('quit\n')
		self.exitStatus = None
		self.video = subprocess.Popen(["mplayer", "-slave","-vo", 'xv', '-softvol',  '-softvol-max' , '500', "-quiet", "-double" , "-wid", str(self.socket_id),  str(self.path)], stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
		#video = Process(["mplayer", "-slave","-vo", "xv", "-wid", str(self.socket_id), "-quiet",  str(self.path)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		(self.vstdin, self.vstderr, self.vstdout) = (self.video.stdin, self.video.stderr, self.video.stdout)
		self.playstatus = "PLAY"		
		#self.Parser = OutputParse ()
		#self.Parser.setDaemon (True)
		#OutputParse.__init__(lol, )
		#threading.Thread.__init__()
		
		self.vstdin.write('set_property volume 30')
		self.volume.set_value (50)
		
		self.Parser = OutputParse(self)
		self.Parser.setDaemon (True)
		self.Parser.start()

		(self.input, self.error, self.output) = (self.vstdin, self.vstderr, self.vstdout)
		self.lol = self.video
		self.played = 1
		self.lol = self.video
		#print self.vsdtout.read()


	def PlayCheck(self):
		return self.played
	
	def stop(self, button):
		if "STOP" not in  self.playstatus:
			self.vstdin.write('quit\n')
			
		self.played = 0

	def loli(self, scale, *lol):
		if "PAUSE" not in  self.playstatus:
			self.vstdin.write('pause\n')

	def lolen (self, scale, *lol):
		#gtk.gdk.threads_enter()
		#print 'lol'
		self.position_lock = True
		#print 'lolen'
		#print self.position_lock
		
		
		#gtk.gdk.threads_leave()
	
	def setPosition (self, scale, *lol):
		#gtk.gdk.threads_enter()
		if self.position_lock == True:
			scale.set_value (int(round(scale.get_value())))
			self.vstdin.write('get_time_pos\n')
			self.vstdin.write('seek ' + str(round(scale.get_value())) + ' 2\n')
			self.position_lock = False
			#print self.position_lock		
	def setVolume (self, scale, *lol):
		self.vstdin.write('set_property volume ' + str(round(scale.get_value())) + '\n')			
		self.vstdin.write('pause\n')
		
	def pauseplay(self, button):
		if "NONE" in self.exitstatus:
			self.vstdin.write('pause\n')
			print "PAUSE"
			if self.playstatus == "PAUSE":
				self.playstatus = "PLAY"
			else:
				self.playstatus = "PAUSE"
		
		#self.played_check = self.PlayCheck()
		#print self.lol.read()
		#
		
		#self.vstdin.write('get_video_resolution\n')	


def main():
	gtk.gdk.threads_init()
	gtk.gdk.threads_enter()	
	woma = WomaWindow()
	gtk.main()
	gtk.gdk.threads_leave()
#	woma.open_video(woma.socket_id)


main()
#if __name__ == "__woma__": 
 #   try:
  #      main()
   # except SystemExit:
    #    raise
    #except: 
     # 	pass
		#traceback.print_exc()
   		#xlmisc.log_exception()
