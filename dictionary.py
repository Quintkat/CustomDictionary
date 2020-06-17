from pickle import dump, load
from os import listdir, remove
from datetime import datetime
from googletrans import Translator


def getAddress(name: str) -> str:
	return DIRECTORY + name + EXTENSION


def getFilename(name: str) -> str:
	return name + EXTENSION


def saveDict(dictionary, name, console=False):
	if name == '':
		name = dictionary[NAMEKEY]
	address = getAddress(name)
	with open(address, 'wb') as file:
		dump(dictionary, file, 0)

	if console:
		print("dictionary saved to file at" + address)


def loadDict(name, console=False):
	address = getAddress(name)
	with open(address, 'rb') as file:
		if console:
			print("dictionary loaded from file at " + address)

		return load(file)


def deleteDict(name, console=False):
	if getFilename(name) not in getDictNames():
		print(getFilename(name) + " not deleted, because it doesn't exist")
		return

	address = getAddress(name)
	remove(address)

	if console:
		print("dictionary deleted")


def nevermind(word):
	if word == 'NEVERMIND' or word == 'NEVER MIND' or word == 'NVM':
		print('aborted')
		return True
	return False


def listToString(data, separator=' '):
	output = ''
	for el in data:
		output += el + separator

	return output


def createDict(name, console=False):
	while getFilename(name) in getDictNames():
		print("dictionary with filename already exists, try again")
		name = input(">filename: ").strip(' ')

		if nevermind(name):
			return

	columnFormat = []
	cfAmount = 1
	print("'end' to end input")
	while True:
		cfInput = input(">column " + str(cfAmount) + ": ")
		if cfInput == 'end':
			break
		cfAmount += 1
		columnFormat.append(cfInput)

	newDict = {NAMEKEY: name, COLUMNFORMATKEY: columnFormat}

	if console:
		print("dictionary created: " + str(newDict))
	return newDict


def createEntry(dictionary, word, console=False):
	while word in dictionary:
		print("word already in dictionary: " + getEntry(dictionary, word))
		word = input(">conword: ")

		if nevermind(word):
			return

	dictionary[word] = []
	for column in dictionary[COLUMNFORMATKEY]:
		dictionary[word].append(input(">" + column + ": "))

	if console:
		print("word created: " + getEntry(dictionary, word))


def editEntry(dictionary, word, console=False):
	notExist = createEntryIfNotExist(dictionary, word, console)
	if notExist:
		return

	print(getColumnFormat(dictionary, True) + " ('end' to stop editing)")
	while True:
		print(getEntry(dictionary, word, True))
		command = input(">column to edit, to change to: ")
		if command == 'end':
			break
		else:
			command = command.split(' ')
			column = int(command[0]) - 1
			if len(command) > 1:
				edit = command[1:]
				dictionary[word][column] = listToString(edit)
			else:
				print("not a valid command")


def removeEntry(dictionary, word, console=False):
	entry = dictionary.pop(word, "nothing (because it didn't exist in " + dictionary[NAMEKEY] + ")")
	if console:
		print("removed " + str(entry) + " from " + dictionary[NAMEKEY])


def createEntryIfNotExist(dictionary, word, console):
	if word not in dictionary:
		decision = input(">" + word + " does not exist in dictionary " + dictionary[NAMEKEY] + ", do you want to create an entry? (y/n)")
		if decision == 'y':
			createEntry(dictionary, word, console)
		else:
			print('aborted')

		return True
	return False


def getDictNames() -> list:
	return listdir(DIRECTORY)


def getName(dictionary):
	return dictionary[NAMEKEY]


def getColumnFormat(dictionary, numbers=False):
	return "Conword \t" + getEntry(dictionary, COLUMNFORMATKEY, numbers, False)


def getEntry(dictionary, word, numbers=False, includeWord=True):
	notExist = createEntryIfNotExist(dictionary, word, console)
	if notExist:
		return "original command not followed"

	output = word + " \t" if includeWord else ''
	entry = dictionary[word]

	if numbers:
		for i, element in enumerate(entry):
			output += "(" + str(i + 1) + ")" + element + " \t"
	else:
		for element in entry:
			output += element + " \t"

	return output


def showDictionary(dictionary):
	print(dictionary[NAMEKEY])

	columnOutput = 'Conword \t'
	columnWidth = 0
	for column in dictionary[COLUMNFORMATKEY]:
		string = column + " \t"
		columnOutput += string
		columnWidth = max(columnWidth, len(string))
	print(columnOutput)

	words = list(dictionary.keys())
	words.remove(NAMEKEY)
	words.remove(COLUMNFORMATKEY)
	for i in range(len(words)):
		word = words[i]
		output = str(i) + " " + word

		entry = dictionary[word]
		for element in entry:
			output += "\t" + element
		print(output)


def sortDictionary(dictionary: dict, console=False) -> dict:
	if console:
		print("dictionary " + dictionary[NAMEKEY] + " sorted by conword")
	return dict(sorted(dictionary.items()))


def setLanguages(word, console=False):
	languages = word.split(', ')
	if console:
		print("Translation languages set to", languages)
	return languages


def multiTranslate(word, translationLanguages):
	words = word.split(', ')
	for w in words:
		output = 'English: ' + w + ', \t'
		for destL in translationLanguages:
			output += destL + ': '
			output += translator.translate(text=w, src='English', dest=destL).text + ', \t'
		print(output)


def console():
	dictionary = ''
	translationLanguages = []

	while True:
		# Get the command input
		line = input(">>").split()
		command = line[0]
		word = ''
		if len(line) > 1:
			for i, el in enumerate(line[1:]):
				word += str(el)
				if i < len(line[1:]) - 1:
					word += ' '

		# No-word commands
		if command == 'quit' or command == 'q':
			break

		if command == 'getnames' or command == 'gn':
			print(getDictNames())
			continue

		if command == 'getname' or command == 'g':
			print(getName(dictionary))
			continue

		if command == 'getcf' or command == 'cf':
			print(getColumnFormat(dictionary, True))

		if command == 'unassign':
			dictionary = ''
			continue

		if command == 'sort':
			dictionary = sortDictionary(dictionary)
			continue

		if command == 'showdict' or command == 'sd':
			showDictionary(dictionary)
			continue

		# Semi-word commands, aka commands that can take words but aren't necessary
		if command == 'save' or command == 's':
			saveDict(dictionary, word, True)
			continue

		# Word commands
		if word != '':
			if command == 'load' or command == 'l':
				dictionary = loadDict(word, True)
				continue

			if command == 'delete':
				deleteDict(word)
				continue

			if command == 'create' or command == 'c':
				dictionary = createDict(word, True)
				continue

			if command == 'entry' or command == 'ce':
				createEntry(dictionary, word, True)
				continue

			if command == 'remove':
				removeEntry(dictionary, word, True)
				continue

			if command == 'show' or command == 'se':
				print(getEntry(dictionary, word))
				continue

			if command == 'edit' or command == 'e':
				editEntry(dictionary, word, True)
				continue

			if command == 'setlanguages' or command == 'sl':
				translationLanguages = setLanguages(word, True)
				continue

			if command == 'translate' or command == 't':
				multiTranslate(word, translationLanguages)
				continue

		print("unknown commands")


timeFull = datetime.now()

DIRECTORY = 'dictionaries/'
EXTENSION = '.pkl'
NAMEKEY = 'NAME'
COLUMNFORMATKEY = 'COLUMN FORMAT'
translator = Translator()

console()

print("FULL RUNNING TIME: " + str(datetime.now() - timeFull))
