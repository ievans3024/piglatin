from itertools import takewhile
import re

def translatePhrase(phrase):
	words = re.split(r"(\w[\w']*\w)", phrase)

	words = map( lambda word: translateWord(word) if word.isalpha() else word, words  )
	return ''.join(words)

def translateWord(psWord):
	sWord = psWord
	sFirst = sWord[0]
	bCapitalize = sFirst.isupper()

	sSuffix = ''

	if sFirst in "AEIOUaeiou":
		sSuffix = 'way'
		sLast = sWord[-1]

		if(sLast == sLast.isupper and len(sWord) > 1):
			sSuffix = 'way'.upper()

	else:
		if sWord != sWord.upper():
			sFirst = sFirst.lower()

		iChars = len(sWord)

		while(iChars):
			sSuffix += sFirst
			sLast = sFirst
			iChars -= 1

			bCapsFlag = sFirst.isupper()

			sWord = sWord[1:]
			if len(sWord) > 0:
				sFirst = sWord[0]

			if sFirst in "AEIOUaeiouYy":
				if (not((sLast == "q" or sLast == "Q") and (sFirst == "u" or sFirst == "U"))):
					break

		if (bCapsFlag):
			sSuffix += 'ay'.upper()
		else:
			sSuffix += 'ay'

	sWord += sSuffix

	if (bCapitalize):
		sFirst = sWord[0]
		sWord = sFirst.upper() + sWord[1:len(sWord)]

	return sWord
