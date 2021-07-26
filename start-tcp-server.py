# -*- coding: utf-8 -*-
import SocketServer
import os
import time
from search_books.data_handle_functs import DataHandler

class MyTCPHandler(SocketServer.StreamRequestHandler): 

    def handle(self):
        #send welcome message on-connection
        self.wfile.write(self.welcome_message)

        _handlers = {'common': self.common_cmd,
                     'search': self.search_cmd}
        data = self.rfile.readline().strip()
        l = data.split()
        
        # number of arguments check
        if len(l) == 2:
            command, args = l[0], l[1:]
            f = _handlers.get(command, None)
            if f:
                ans = f(*args)
            else:
                ans = 'Invalid command'
        else:
            ans = 'Invalid Usage'

        self.request.sendall('===========\n' + ans + '\r\n')

    def common_cmd(self, *args):
        """
        Returns a string with the N most common words (descending) and how many times appear in all books combined
        """
        print("Command: common")
        ans = self.dh.list_most_common_words(int(args[0])) if args[0].isdigit() == True else ["Wrong input :/"]
        return '\n'.join(ans)

    def search_cmd(self, *args):
        """
        Returns a string that indicates how many times the given word appears in each book separately
        """
        print("Command: search")
        ans = self.dh.list_search_word(args[0])
        return '\n'.join(ans)

    dh = DataHandler()

    welcome_message = ( "\nYou're connected!\n"
                        "-------------------\n"
                        "You can use two commands:\n"
                        "1.common: returns the N most common words (descending) and how many times appear in all books combined\n"
                        "2.search: returns in which book and how many times the given word appears\n"
                        "-------------------\n"
                        "examples:\n"
                        "  common 5\n"
                        "  search morty\n"
                        "-------------------\n"
                        "Notice: use only one argument\n\n")

    # books data initialization / current file and books folder must be in the same directory
    print("\nRetriving books. Please wait...")
    tic = time.time()
    try: 
        dh.bool_retrieve_books(os.path.join(os.path.dirname(os.path.realpath(__file__)),'books/'))
    except: 
        exit("\nERROR !!!\nPlease check for corrupted files and make sure that you have followed\nthe given instructions about the 'books' folder")
    toc = time.time()
    print("Books data initialization time: {0} seconds".format(round((toc - tic), 2)))

if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    
    print ("** TCP server is alive **")
    
    server.serve_forever()