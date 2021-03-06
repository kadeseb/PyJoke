#!/usr/bin/python2.7
# -*- coding: utf8 -*-
# ========================================
# Projet:	PyJoke
# Rôle:		Gère le son
# Crée le:	09/10/2016
# ========================================
import os
import time
import pygame.mixer as Mixer
from config import *
from volume import *

class Manager():
	Mixer.init()

	# Constructeur
	def __init__( self ):
		self.soundList = os.listdir( CONFIG['SOUNDS_DIR'] )
		self.playlist = []
		self.playlistTimer = time.time()
		self.nextDelay = 0
		self.volume = Volume()

	# Contrôle la validité d'un son
	#
	# -?-
	# [int] soundID:    ID du son
	# -!-
	# [bool]            Le son est valide
	def validSound( self, soundID ):
		try:
			soundID = int( soundID )
		except ValueError:
			return False

		return soundID >= 0 and soundID < len( self.soundList )

	# Retourne la liste des son
	#
	# -!-
	# [list]            Liste des sons
	def getSoundList( self ):
		return self.soundList

	# Joue la liste de lecture
	def performPlaylist( self ):
		if( Mixer.music.get_busy() ):
			self.volume.maximize()
			return
		elif( not len( self.playlist  ) ):
			return
		else:
			self.volume.maximize()

		if( (time.time() - self.playlistTimer) >= self.nextDelay ):
			soundConfig = self.playlist.pop( 0 )

			Mixer.music.load( CONFIG['SOUNDS_DIR'] + self.soundList[ soundConfig['ID'] ] )
			Mixer.music.play()
			self.playlistTimer = time.time()

			if( len( self.playlist ) ):
				self.nextDelay = soundConfig['nextDelay']
			else:
				self.nextDelay = 0

	#//////////////////////////////////////
	# Manipulation de la liste de lecture /
	#//////////////////////////////////////
	# Ajoute un son dans la liste de lecture
	#
	# -?-
	# [int] soundID:    ID du son
	# [int] delay:		Delais avant la lecture suivante
	# -!-
	# [bool]:           Le son a été ajouté
	def playlistAdd( self, soundID, delay=0 ):
		if( not self.validSound( soundID ) or not isinstance( delay, int ) ):
			return False

		soundConfig = {
			'ID': soundID,
			'nextDelay': delay
		}

		self.playlist.append( soundConfig )
		return True

	# Vide la liste de lecture
	def playlistPurge( self ):
		self.playlist = []
		Mixer.music.stop()
