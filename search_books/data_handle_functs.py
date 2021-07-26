import os
import string
import operator

class DataHandler:
	dict_words_full = dict()
	list_common_return = list()

	def bool_retrieve_books(self, pathBooks):
		"""
		This function reads files from a folder and updates 2 dictionaries and 1 list:
		1. 	dict_words_full (nested) indicates how many times a word appears in each file separately
		2. 	list_common_return a shorted (desc) list with data from dict_words_simple
		Output examples:
		1. {"rick": {"book2.txt": 3, "book1.txt": 3}, "morty": {"book2.txt": 1, "book1.txt": 3}}
		2. [['rick', 6], ['morty', 4], ['rick-morty', 2], ['jessica', 2], ['jerry', 2]]
		"""
		dict_words_simple = dict()
		for file in os.listdir(pathBooks):
			# remove punctuation for a file / words split to list
			list_splitted_words = list_rmv_punct_split(pathBooks,file)
			for word in list_splitted_words:
				# update full dictionary: words per file
				if self.dict_words_full.get(word, 0) == 0: self.dict_words_full[word] = dict()
				self.dict_words_full[word][file] = self.dict_words_full.get(word, {}).get(file, 0) + 1
				# update simple dictionary: words in all files combined
				dict_words_simple[word] = dict_words_simple.get(word, 0) + 1
		# from simple dict to a nested list
		list_words_simple = [ [k,v] for k, v in dict_words_simple.items() ]
		# shorting the nested list descending / old key-vale inner lists ---> space delimeted values of the return list
		[self.list_common_return.append("{0} {1}".format(k, v)) for k, v in sorted(list_words_simple, key=operator.itemgetter(1), reverse=True)]
		return True

	def list_most_common_words(self, num):
		"""
		A function that returns a list with strings that indicates (with space separation)
		how many times the N most common words appear in all books combined
		regarding the list list_common_return
		Outpute example: ['summer 6', 'morty 4', 'rick 4', 'brad 3', 'rick-morty 1']
		"""
		return self.list_common_return[:num]
	
	def list_search_word(self, word):
		"""
		A function that returns a list with strings that indicates (with space separation)
		in which book and how many times the given word appears
		regarding the dictionary dict_words_full
		Outpute exapme: ['book1.txt 3', 'book2.txt 2', 'book3.txt 1']
		"""
		if self.dict_words_full.get(word, 0) == 0: return ["No results :/"]
		list_search_return = []
		# from dict to a list with tuples
		list_words_full = [ k for k in self.dict_words_full.get(word).items() ]
		# shorting the nested list descending / old key-vale inner lists ---> space delimeted values of the return list
		[ list_search_return.append("{0} {1}".format(k, v)) for k, v in sorted(list_words_full, key=operator.itemgetter(1), reverse=True)]
		return list_search_return

def list_rmv_punct_split(pathBooks, file):
	"""
	This function reads a file and returns splitted lower-case words in list.
	The punctuation, non-ascii characters and digits have been removed.
	Words like 'high-level' are considered as one in sentences like 'Python is a high-level language'. 
	Output example: ['rick', 'morty', 'rick', 'summer', 'beth', 'rick-morty', 'beth']
	"""
	list_words_return = open(os.path.join(pathBooks, file))\
							.read()\
            				.decode('unicode_escape')\
            				.encode('ascii', 'ignore')\
            				.rstrip()\
            				.lower()\
            				.translate(None, string.punctuation.replace("-", "") + string.digits)\
            				.split()
	return list_words_return