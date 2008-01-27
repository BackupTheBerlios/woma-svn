#!/usr/bin/env python
#
# ProgressBar.py
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



import sys

import pygtk, gtk, gtk.glade
import string 
import threading, time

class ProgressBar (gtk.HScale):
	""" Class for handling progress bar - subclass of HScale"""
	
	__lock = False			# is progress bar locked for mplayer process?
							# True on user interraction
	scroll_lock = 0			# unlock thread stack
	__seekable = True		# for future use :-)
	__trueValue = gtk.HScale(gtk.Adjustment (lower = 0, upper = 100000))  # Invisible HScale object, always gets 
	
	class Unlock( threading.Thread ):
		""" This class creates unlock threads - push 1 on stack waits 0.5s pop 1 from stack
		and if is last thread unlock progress bar """
		def __init__ (self, scale, lock, *arg):
			threading.Thread.__init__(self)
			self.scale = scale
		
		def run ( self ):
			self.scale.scroll_lock = self.scale.scroll_lock + 1 # push 1 to progressbar stack
			time.sleep (0.5)
			self.scale.scroll_lock = self.scale.scroll_lock - 1 # pop 1 from stack
			if self.scale.scroll_lock == 0:		# check if is last thread
				self.scale.seek_unlock()		# unlock progress bar

	def __init__ (self):
		""" Initialize 	ProgressBar"""
		gtk.HScale.__init__(self)		# standard HScale init function
		
		self.set_draw_value (False)		#turn off drawing value
		
		self.__trueValue.connect("value-changed", self.__set_visible_value)	# do when gets new value from mplayer
		
		self.connect('change-value', self.__seek_lock)						# lock progress bar on move
		self.connect('button-press-event', self.__seek_lock)				# lock on mouse button events
		self.connect('button-release-event', self.__seek_unlock)			# 
		self.connect('key-press-event', self.__seek_lock)					# lock on keyboard events
		self.connect('key-release-event', self.__seek_unlock)				#
		self.connect('scroll-event', self.__seek_lock, True)				# lock on scroll events
		
		self.set_update_policy (gtk.UPDATE_DELAYED)
		
	def __seek_lock(self, scale, event,  scroll = False):					
		""" Lock progress bar """
		self.__lock = True													# lock progress bar
		if scroll == True:													# if scroll event, unlock after short time
			self.__seek_unlock (True)
		
	def __seek_unlock(self, scroll, *event):
		""" Unlock progress bar"""
		if scroll != True:													# check if not called by scroll event (dont let scroll emit signal imidietly)
			self.emit ('value-changed')										# emit value change 
		self.unlock = self.Unlock(self, self.__lock, self.scroll_lock)		# Create unlock thread
		self.unlock .setDaemon (True)										
		self.unlock.start()

	def seek_unlock (self):
		""" Public unlock function propably not neded :-) """
		self.__lock = False
	
	def __set_visible_value (self, scale):
		""" Update progress bar with time from mplayer if not locked """
		if self.__lock == False:
			self.set_value (self.__trueValue.get_value())
	
	def set_max_value (self, max_value):
		""" Set max value  """
		self.set_adjustment (gtk.Adjustment (lower = 0, upper = max_value, value = 0, page_incr = (max_value / 100), step_incr = (max_value / 20) ) )
		
	def set_position (self, value):
		""" Metod used to send actual time from mplayer """
		self.__trueValue.set_value(value)
		pass
	
	def get_position (self):
		""" Get most actual position  """
		return self.__trueValue.get_value()
		
	def get_lock (self):
		""" Get lock status """
		return self.__lock
		
