#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram import ReplyKeyboardMarkup, KeyboardButton, ChatAction
from telegram.ext import Updater, CommandHandler
import logging
import os
import RPi.GPIO as GPIO
import picamera
import datetime

#Modifier la borne GPIO correspodant à l'endroit où est branché le capteur pyroélectrique.
sensor = 6
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor, GPIO.IN, GPIO.PUD_DOWN)
previous_state = False
current_state = False
service = "hors"
start, stop, ping, photo, video, quit = ("/start","/stop","/ping","/photo","/video","/quit")
reply = ReplyKeyboardMarkup([[KeyboardButton(start),KeyboardButton(stop)],[KeyboardButton(ping),KeyboardButton(photo),KeyboardButton(video)]],one_time_keyboard=False)
upphoto = ChatAction.UPLOAD_PHOTO
upvideo = ChatAction.UPLOAD_VIDEO
chatid = 'none'
job = None
camera = picamera.PiCamera()
#Ajuster les aramère de caméra ici
camera.resolution = (1280, 720)
camera.framerate = 25
camera.rotation = 180
camera.exposure_mode = 'night'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def utilisateur(user):
#Modifier les noms d'utilisateur pour votre bot
	if (user == "utilisateur 1" or user == "utilisateur 2"):
		return True
	else:
		return False


def start(bot, update):
	global service, chatid, job
	if (utilisateur(update.message.from_user.username) and service == "hors"):
		service = "en"
		chatid = update
		bot.sendMessage(chatid.message.chat_id, text="Mise en service de l'alarme.", reply_markup=reply)
		job.put(alarme, 1, repeat=True)


def stop(bot, update):
	global service, job
	if (utilisateur(update.message.from_user.username) and service == "en"):
		service = "hors"
		bot.sendMessage(update.message.chat_id, text="Mise hors service de l'alarme.", reply_markup=reply)
		job.stop()


def ping(bot, update):
	if (utilisateur(update.message.from_user.username)):
		bot.sendMessage(update.message.chat_id, text="L'alarme est %s service !" % service, reply_markup=reply)


def quitter(bot, update):
	if (utilisateur(update.message.from_user.username)):
		bot.sendMessage(update.message.chat_id, text="Good Bye !")
		os._exit(0)


def alarme(bot):
	global previous_state, current_state, service
	if (not camera.recording):
		previous_state = current_state
		current_state = GPIO.input(sensor)
		if (current_state != previous_state):
			new_state = "Présence détectée" if current_state else "Pas de présence"
			bot.sendMessage(chatid.message.chat_id, text=new_state)
			if (new_state == "Présence détectée"):
				sendimage(bot, chatid)


def sendimage(bot, update):
	if (utilisateur(update.message.from_user.username)):
		bot.sendChatAction(update.message.chat_id, action=upphoto)
		ladate = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H-%M-%S')
		filename = "%s.jpg" % ladate
		camera.annotate_text = ladate
		camera.capture(filename)
		bot.sendPhoto(update.message.chat_id, photo=open(filename, 'rb'), caption = ladate)


def sendvideo(bot, update):
	if (utilisateur(update.message.from_user.username)):
		bot.sendMessage(update.message.chat_id, text="Enregistrement de la vidéo...")
		ladate = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d_%H-%M-%S')
		filename = "%s.mp4" % ladate
		camera.start_recording('Video.h264', format='h264')
		camera.wait_recording(10)
		camera.stop_recording()
		os.system("MP4Box -add Video.h264 " + filename)
		bot.sendChatAction(update.message.chat_id, action=upvideo)
		bot.sendVideo(update.message.chat_id, video=open(filename, 'rb'), caption = ladate)


def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
	global job
#Remplacer par votre Token
	updater = Updater("Token")
	job = updater.job_queue
	dp = updater.dispatcher
	dp.addHandler(CommandHandler("start", start))
	dp.addHandler(CommandHandler("stop", stop))
	dp.addHandler(CommandHandler("ping", ping))
	dp.addHandler(CommandHandler("photo", sendimage))
	dp.addHandler(CommandHandler("video", sendvideo))
	dp.addHandler(CommandHandler("quit", quitter))
	dp.addErrorHandler(error)
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()
