#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Yinqiang <yinqiang.zhu@gmail.com>
# Doc: QR v5 image maker
#

def createQr(text, savePath, iconPath=None):
	import qrcode

	qr = qrcode.QRCode(
		version = 5,
		error_correction = qrcode.constants.ERROR_CORRECT_H,
		box_size = 10,
		border = 1
	)

	qr.add_data(text)
	qr.make(fit=True)

	img = qr.make_image()

	if iconPath != None:
		from PIL import Image

		icon = Image.open(iconPath)

		img = img.convert("RGBA")
		img_w, img_h = img.size
		factor = 4
		size_w = int(img_w/factor)
		size_h = int(img_h/factor)

		icon_w, icon_h = icon.size
		if icon_w > size_w:
			icon_w = size_w
		if icon_h > size_h:
			icon_h = size_h
		icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

		w = int((img_w - icon_w) / 2)
		h = int((img_h - icon_h) / 2)
		img.paste(icon, (w, h), icon)

	img.save(savePath)


def createQrWithFile(filePath, savePath, iconPath=None):
	f = open(filePath, "r")
	data = f.read(64)
	f.close()
	createQr(data, savePath, iconPath)


def printHelp():
	print """
usage:
    -t, --text     The information text. 64 chars max.
    -f, --file     The information in file. 64 chars max.
    -o, --output   QR image save path.
    -i, --icon     The icon image path.
    -h, --help     Show this.

etc:
    ./sqr.py -t "text" -o output.png -i icon.png
	"""


def parseOpt(config, argv):
	opts, args = getopt.getopt(argv, "ht:f:o:i:", [
		'help',
		'text=',
		'file=',
		'output=',
		'icon='
	])
	for option, value in opts:
		if option in ["-h", "--help"]:
			printHelp()

		elif option in ["-t", "--text"]:
			config["text"] = value.strip()

		elif option in ["-f", "--file"]:
			config["file"] = value.strip()

		elif option in ["-o", "--output"]:
			config["output"] = value.strip()

		elif option in ["-i", "--icon"]:
			config["icon"] = value.strip()


if __name__ == "__main__":
	import sys, getopt

	if len(sys.argv) < 2:
		printHelp()
		sys.exit(1)

	config = {
		"text": "",
		"file": None,
		"output": "output.png",
		"icon": None
	}
	parseOpt(config, sys.argv[1:])

	try:
		if config["file"] != None:
			createQrWithFile(config["file"], config["output"], config["icon"])
		else:
			createQr(config["text"], config["output"], config["icon"])
	except:
		printHelp()
		sys.exit(1)