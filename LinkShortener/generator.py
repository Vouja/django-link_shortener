import datetime
from randomwordgenerator import randomwordgenerator


def format_link(linkb):
	if linkb[:7] != 'http://' and linkb[:8] != 'https://':
		linkb = 'http://{}'.format(linkb)
	return linkb


def generate_short_link(link, name):
	if name == '':
		name = randomwordgenerator.generate_random_words(1)
	now = datetime.datetime.now()
	return '{}{}{}{}'.format(name, now.strftime("%d"), now.strftime("%S"), now.strftime("%f")[:2])
