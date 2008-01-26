#!/usr/bin/python
# -*- coding: utf-8 -*-
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
__name__="mediainfo"

import subprocess, re

class mediainfo:
	
	def __init__ (self, mplayer = "mplayer", debug = None):
		
		self.mplayer = mplayer
		self.debug = debug
		pass
	
	def fileinfo (self, file):
		
		video = subprocess.Popen(["mplayer", "-identify", "-frames", "0", "-vo", "null", "-ao", "-null", "-really-quiet", str(file)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout, stderror = video.communicate() 
		
		if self.debug:
			print stdout
		
		video_values = 'DEMUXER|FORMAT|BITRATE|WIDTH|HEIGHT|FPS|LENGTH'
		tracks_regex = re.compile ('ID_(AID|SID|VID)_(\d)_(\w+)=(?P<value>\w+)')
		tracks_temp = tracks_regex.findall (stdout)
		tracks = {}
		for i in tracks_temp:
			if i[0] not in tracks:
				tracks[i[0]] = []
			tracks[i[0]].append ({i[2]: i[3]})
			
		print tracks
				
		
		media_regex = re.compile ('ID_(VIDEO)_(' + video_values +')=(?P<value>\w+)')
		media_temp = media_regex.findall (stdout)
		media = {}
		for i in media_temp:
			if i[0] not in media:
				media[i[0]] = {}
			media[i[0]][i[1]] = i[2]
			
		print media
		
		media_regex = re.compile ('ID_LENGTH=(\w+)')
		length = media_regex.findall (stdout)
		
		print length
		
		return (tracks, media, length)
			


