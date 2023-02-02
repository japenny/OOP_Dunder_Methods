import csv
from ast import Expr
from random import shuffle

class Participant:
    def __init__(self, name, poll = 0, corr = 0, att = 0, exc = 0, miss = 0):
        self.name = name
        self.poll = poll
        self.corr = corr
        self.att  = att
        self.exc  = exc
        
    def _polled(self):
        self.poll += 1

    def correct(self):
        self._polled()
        self.corr += 1
    
    def attempted(self):
        self._polled()
        self.att += 1
    
    def excused(self):
        self._polled()
        self.exc += 1
    
    def missing(self):
        self._polled()

    def __str__(self):
        return (f"{self.name},{self.poll},{self.corr},{self.att},{self.exc}")


class Poller:
    def __init__(self, file_name):
        self.file_name = file_name
        self.total = 0
        self.len = 0
        self.i = 0

    def __enter__ (self):
        print("File Entered")
        try:
            self.file = open(self.file_name, 'r+')
            read_obj = csv.reader(self.file)
        except:
            raise Exception("Unable to access file!")
            
        header = next(read_obj)
        if len(header) != 5:
            raise ValueError('Empty Data or Incorrect Format Length, Expected: name, #polled, #correct, #attempted, #excused')

        format = ['Name ', 'Polled', 'Correct', 'Attempted', 'Excused']
        for i in range(5):
            if format[i] != header[i]:
                raise ValueError('Incorrect Format, Expected: name, #polled, #correct, #attempted, #excused')
        
        self.data = []
        self.order = dict()

        for line in read_obj:
            part = Participant(line[0],
                               int(line[1]), int(line[2]),
                               int(line[3]), int(line[4])
                              )
            self.data.append( [part.poll, part.name] )
            self.order.update( {part.name : part} )
            self.len += 1
        
        #Checks if 
        if self.len < 1:
            raise ValueError('No Participants Data')

        #Randomizes and sorts data
        shuffle(self.data)
        self.data.sort( key = lambda data: data[0] )
        return self

    def __iter__(self):
        print("iter")
        return self
    
    def __next__(self):
        print("next")
        if self.i >= self.len:
          raise StopIteration

        self.name = self.data[self.i][1]
        self.curr = self.order[self.name]
        self.i += 1
        return self.name

    #Records Changes to Participant Class
    def _total(self):
        self.total += 1

    def correct(self):
        self._total()
        self.curr.correct()
    
    def attempted(self):
        self._total()
        self.curr.attempted()
    
    def excused(self):
        self._total()
        self.curr.excused()
    
    def missing(self):
        self._total()
        self.curr.missing()
    
    #Ends program and conducts final changes to csv
    def stop(self):
        self.i = float('inf')

    def __exit__ (self, type='', value='', traceback=''):
        #Overwrite file
        self.file.write("name, #polled, #correct, #attempted, #excused")
        for i in self.order.values():
          self.file.write( str(i) )

        print(f"Total Participants Polled: {self.total}")
        print("File Exited")
        self.file.close()