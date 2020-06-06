from pickle import dump, load
from os import listdir, remove
from datetime import datetime


def getFD(name: str) -> str:
	return DIRECTORY + name + EXTENSION


def getF(name: str) -> str:
	return name + EXTENSION


def saveDict(dict, name=None):
	if name is None:
		name = dict['NAME']
	filename = getFD(name)
	with open(filename, 'wb') as file:
		dump(dict, file, 0)


def loadDict(name):
	filename = getFD(name)
	with open(filename, 'rb') as file:
		return load(file)


def deleteDict(name):
	filename = getFD(name)
	remove(filename)


def getDictNames() -> list:
	return listdir(DIRECTORY)


def createDict():
	name = input("filename: ")
	while getF(name) in getDictNames():
		print("dictionary with filename already exists, try again")
		name = input("filename: ")

	columnFormat = []
	cfAmount = 1
	while True:
		cfInput = input("column " + str(cfAmount) + "('end' to end input): ")
		if cfInput == 'end':
			break
		cfAmount += 1
		columnFormat.append(cfInput)

	newDict = {'NAME': name, 'COLUMN FORMAT': columnFormat}
	return newDict


def createEntry(dict):
	word = input("input word: ")
	if word not in dict:
		dict[word] = []
		for column in dict['COLUMN FORMAT']:
			dict[word].append(input(column + ": "))
	else:
		print("word already in dictionary")


def showDictionary(dict):
	for number, word in enumerate(dict):
		output = str(number) + " " + word

		entry = dict[word]
		for element in entry:
			output += "\t" + element

		print(output)


timeFull = datetime.now()

DIRECTORY = 'dictionaries/'
EXTENSION = '.pkl'

dictionary = createDict()
createEntry(dictionary)
createEntry(dictionary)
createEntry(dictionary)
showDictionary(dictionary)
saveDict(dictionary, dictionary['NAME'])

dictionary = createDict()
# dict = {'a':1,'b':2,'c':3}
# print(str('a' in dict))
# print(str(1 in dict))

columnFormat = ['English Trans.', 'Part of speech', 'Phono. Transc.', 'Extra Descr.']

print("FULL RUNNING TIME: " + str(datetime.now() - timeFull))
