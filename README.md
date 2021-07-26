# Α Python implemented TCP server. 
# Storing data from text files, indexing and serving.
---
## Requirements

File books.tar.gz contains several books in text format downloaded from https://www.gutenberg.org.
Implement in *python* using *only* facilities from the standard library a simple TCP Server that does the following:

1. has a method that returns the n most common words
2. has a method that returns in which books a word W appears into. The results (books) should be ordered by the number of appearances of the word W)

Example of usage:
```
# this command should start the server
python start-tcp-server.py --host localhost --port 9999
```
In another terminal connect to the server
```
nc locahost 9999
```
and send the first command:
```
common 10
```
The server should reply with the 10 most common words, example:
```
and 1000
with 999
I 998
...
```

The second command should be invoked like:
```
search word
```
And the server should reply with the filenames that ```word``` appears into (ordered by the number of appearances)
example:
```
1.txt 30
2.txt 10
3.text 1
```
---
## Notes 

- Read the txt files
- Split the files into words and remove numbers and punctuation
- Store the words in an appropriate data structure
- query the data structure you created to answer the queries.
- First start with a naive approach that works and optimize later
- What is the time complexity of your solution? Does it scale with more books?
- If you have some concerns about your implementation or you have a better
  solution write the better solution in a comment if you do not implement it.
- Your solution does not have to be perfect but you need to know the limitations
  and comment them
- Do not use any kind of DBMS (sqlite included)
- If you have any questions feel free to contact us.

You may use python 2.7.x or python >= 3.5.2, c++, php or golang and only facilities from the standard libraries to solve the task. 
In case of C++ please send compile instructions for linux using a makefile.

If you have any questions feel free to contact us.

---
## Implementation

The given books are stored in a folder called `books` that contains all extracted files from `books.tar.gz` file. The books are not updated after the server is initialized, so the structures that store the data from books are created in memory once. In our case this is very helpful, because we avoid the I/O delay of retrieving files every time a command is called or updating the data structures every time a new book is being stored or deleted from folder.

The boolean function that creates the above structures is called `bool_retrieve_books`. It starts calling the `list_rmv_punct_split` function that splits the given text documents in lower-case words without punctuation and digits. In order for the commands to return results as fast as possible, the function `bool_retrieve_books` creates two different data structures. 

The first one is a simple descended shorted list with strings, that indicates how many times each word appears in all books combined; its name is `list_common_return`. This structure is used as a specific indexer for the common command. 

Structure example:
```
[['rick', 6], ['morty', 4], ['jessica', 2], ['jerry', 2]]
```

The second one is a nested dictionary that indicates how many times each word appears in each book separately; its name is `dict_words_full`. As long as the search is up to a given word, the outer keys of the dictionary are the words from all books combined. The values of these keys - the inner dictionaries - have the books as key and the number of times each word appears as value. This structure alikes a two-dimensional table and is used as a specific indexer for the search command.

Structure example:
```
{"rick": {"book2.txt": 3, "book1.txt": 3}, "morty": {"book2.txt": 1, "book1.txt": 3}}
```

The function `bool_retrieve_books` is called every time the server is initialized and it takes about 30 seconds to produce results. It is reasonable for someone to ask why to create two data structures, as long as all the appropriate data is already stored in `dict_words_full` dictionary. After some tests, we can be sure that this is not a good idea. If we use only one indexer, the initialization process drops down to 20 seconds but the `common` command takes about one second to return results, something that is not “acceptable”.



The `common` command is implemented in `list_most_common_words` function which returns the N top items of the already sorted list `list_common_return`. The command has complexity O(1) and returns results instantly. 


Example: 
```
['summer 6', 'morty 4', 'rick 4', 'brad 3']
```

The `search` command is implemented in `list_search_word` function. This function makes use of the nested dictionary `dict_words_full`, retrieves the inner dictionary that refers to the given word-key and returns a sorted list. The command has complexity O(1) and returns results instantly.

Example: 
```
['book1.txt 3', 'book2.txt 2', 'book3.txt 1]
```



All three functions, `bool_retrieve_books`, `list_most_common_words` and `list_search_word` are implemented in a class called `DataHandler`. This class contains all principal functions of our implementation and is accessible from the main class `MyTCPHandler`.

---

## Limitations

As long as the data structures initialization takes about 30 seconds, it is evident that it has to be optimized , so I tried to implement the whole process with a multi threading approach. 

I considered to split the book files in batches of 100 and call the `bool_retrieve_books` function to handle these batches in parallel using the class `Thread` from `threading` module.

```
pathBooks = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))),'books/')
files = [f for f in os.listdir(pathBooks)]
batches = [files[i:i+100] for i in range(0, len(files), 100)
results = [{} for filelist in batches]
threads = []

for files in batches:
    thread = Thread(target=bool_retrieve_books, args=[files, results, i])
    threads.append(thread)
    thread.start()
    i=i+1
for thread in threads:
	thread.join()
```

The result of each thread was stored as a dictionary in a global list called `results` and the final results called `final_results` was a merged dictionary from all these individual dictionaries.

```
for i in range(0, len(results)):
	final_results = {x: c.get(x, 0) + results[i].get(x, 0) for x in set(c).union(results[i])}
``` 
The logic was to keep the same keys (words) and add their values.

List of individual results:
```
{"rick": 1, "morty": 2, "beth": 3}
{"rick": 2, "morty": 3, "summer": 1}
```
Final result:
```
{"rick": 3, "morty": 5, "summer": 1, "beth": 3}
```

Although the results of this approach matched with the results of the first approach, the whole process took about 180 seconds. With multi threading overhead rises, the creation of threads costs and as a result to slow down the performance. 

I’m not quite sure if another multithreading approach could optimize the initialization time or we should consider to make use of multiprocessing technology in order to use all cores of the processor in parallel. It’s appropriate a “deeper” investigation in how Python handles processes, threads and cores and of course how GIL effects on Python's performance scaling.

---
## Instructions

- Extract the `interview-project` folder from `interview-project.zip` 
- Download the `books.tar.gz` from this repo: https://bitbucket.org/_gosom/interview-project/src/master/books.tar.gz
- Inside the `interview-project` folder extract the `books` folder from `books.tar.gz` file
Now the `interview-project` folder should contain:
```
/interview-project/books/
/interview-project/search_books/data_handle_functs.py
/interview-project/search_books/__init__.py
/interview-project/start-tcp-server.py
/interview-project/README.md
``` 
- Create a Python version 2.7.x virtual environment (the project implemented with version 2.7.15 64-bit)
- Activate your virtual environment 
```
source ~/your_venv/bin/activate
```
- Execute the  `start-tcp-server.py` file
```
~/your_venv/bin/python ~/interview-project/start-tcp-server.py
```
- Wait until the following message appears
```
** TCP server is alive **
```
- Open another terminal, make sure Netcat is installed on your system and connect to the TCP server
```
nc localhost 9999
```
- If you see the following message you are connected to the server
```
You're connected!
```

- Follow the instructions that appear on your terminal 
```
You can use two commands:
1.common: returns the N most common words (descending) and how many times appear in all books combined
2.search: returns in which book and how many times the given word appears
-------------------
examples:
  common 5
  search morty
-------------------
Notice: use only one argument
```
Output examples:
```
common 3
===========
und 881734
die 779026
der 752088
```
```
search athens
===========
23756-8.txt 46
10223-0.txt 8
10223-8.txt 8
10055-8.txt 1
10055.txt 1
16880-0.txt 1
21053-8.txt 1
17142-0.txt 1
17142-8.txt 1
20589-8.txt 1
24899-8.txt 1
14330-8.txt 1
20589-0.txt 1
24899-0.txt 1
21053-0.txt 1
```
##### ... have fun!