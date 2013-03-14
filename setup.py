from distutils.core import setup

setup(
	name = 'truco',
	version = '0.0.1',
	description = "Implementacion en Python del juego de cartas truco",
	long_description = open('README.md').read(),
	url = 'https://github.com/falziots/truco',
	author = 'Gonzalo Ciruelos',
	author_email = 'comp.gonzalo@gmail.com',
	packages = ['truco','cartaymano'],
	license = 'GPLv3',
)
