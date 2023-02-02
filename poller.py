import csv
from ast import Expr
from random import shuffle

#Records a participant's data
class Participant:
    # Constructor method to create object
    def __init__(self, name, poll = 0, corr = 0, att = 0, exc = 0, miss = 0):
        self.name = name
        self.poll = poll
        self.corr = corr
        self.att  = att
        self.exc  = exc

    # Increments polled each time the other methods are called
    def _polled(self):
        self.poll += 1

    # Increments correct (corr) by 1
    def correct(self):
        self._polled()
        self.corr += 1
    
    # Increments attempted (att) by 1
    def attempted(self):
        self._polled()
        self.att += 1
    
    # Increments excused (exc) by 1
    def excused(self):
        self._polled()
        self.exc += 1
    
    # Increments missing (miss) by 1
    def missing(self):
        self._polled()
    
    # Represents participant as string
    def __str__(self):
        return (f"{self.name},{self.poll},{self.corr},{self.att},{self.exc}")

#Main class to open and operate on participants data
class Poller:
    #Initializes basic variables
    def __init__(self, file_name):
        self.file_name = file_name
        self.total = 0
        self.len = 0
        self.i = 0
    
    #Enters and records file data
    def __enter__ (self):
        print("File Entered")
        #Opens the file
        try:
            self.file = open(self.file_name, 'r+')
            read_obj = csv.reader(self.file)
        except:
            raise Exception("Unable to access file!")
            
        header = next(read_obj)
        #Checks if header has correct length
        if len(header) != 5:
            raise ValueError('Empty Data or Incorrect Format Length, Expected: name, #polled, #correct, #attempted, #excused')

        format = ['Name ', 'Polled', 'Correct', 'Attempted', 'Excused']
        #checks if header has the correct format
        for i in range(5):
            if format[i] != header[i]:
                raise ValueError('Incorrect Format, Expected: name, #polled, #correct, #attempted, #excused')
        
        self.data = []
        self.order = dict()
        #Reads csv file and records data to self.data and self.order
        for line in read_obj:
            part = Participant(line[0],
                               int(line[1]), int(line[2]),
                               int(line[3]), int(line[4])
                              )
            self.data.append( [part.poll, part.name] )
            self.order.update( {part.name : part} )
            self.len += 1
        
        #Checks if theres no participants data
        if self.len < 1:
            raise ValueError('No Participants Data')

        #Randomize and sort data
        shuffle(self.data)
        self.data.sort( key = lambda data: data[0] )
        return self

    #Returns iterator
    def __iter__(self):
        print("iter")
        return self
    
    #Returns participants name
    def __next__(self):
        print("next")
        #Exits operation
        if self.i >= self.len:
          raise StopIteration
          
        #Saves name and object inorder to m
        self.name = self.data[self.i][1]
        self.curr = self.order[self.name]
        self.i += 1
        return self.name

    #Increments total # of complete iterations
    def _total(self):
        self.total += 1
    
    #Records Changes to Participant Class
    #Calls participant object
    #------------------------------------
    #Increments correct
    def correct(self):
        self._total()
        self.curr.correct()
    
    #Increments attempted
    def attempted(self):
        self._total()
        self.curr.attempted()
    
    #Increments excused
    def excused(self):
        self._total()
        self.curr.excused()
    
    #Increments polled
    def missing(self):
        self._total()
        self.curr.missing()
    
    #Stops iteration by making self.i infinite
    def stop(self):
        self.i = float('inf')

    #Overwrite csv and closes file
    def __exit__ (self, type='', value='', traceback=''):
        #Overwrite files
        self.file.write("name, #polled, #correct, #attempted, #excused")
        for i in self.order.values():
          self.file.write( str(i) )

        # Print total Participants polled and closes file
        print(f"Total Participants Polled: {self.total}")
        print("File Exited")
        self.file.close()