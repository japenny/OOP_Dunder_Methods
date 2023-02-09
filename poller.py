import csv
from ast import Expr
from random import shuffle

"""Records a participant's data"""
class Participant:
    """Constructor method to create object"""
    def __init__(self, name, poll, corr, att, exc):
        self._name = name
        self._poll = int(poll)
        self._correct = int(corr)
        self._attempted  = int(att)
        self._excused  = int(exc)

    """Increments polled each time the other methods are called"""
    def _polled(self):
        self._poll += 1

    """Increments correct (corr) by 1"""
    def correct(self):
        self._polled()
        self._correct += 1
    
    """Increments attempted (att) by 1"""
    def attempted(self):
        self._polled()
        self._attempted += 1
    
    """Increments excused (exc) by 1"""
    def excused(self):
        self._polled()
        self._excused += 1
    
    """Increments missing (miss) by 1"""
    def missing(self):
        self._polled()
    
    """Formats participant as string"""
    def __str__(self):
        return (f"{self._name},{self._poll},{self._correct},{self._attempted},{self._excused}")


"""Main class to open and operate on participants data"""
class Poller:
    """Initializes basic variables"""
    def __init__(self, file_name):
        self.file_name = file_name
        self.curr_idx = 0
        self.total = 0
        self.len = 0
        self.loop = True
    
    """Enters and records file data"""
    def __enter__ (self):
        self.rand_data = []
        self.order = dict()

        """Reads file and records data to self.data and self.order"""
        with open(self.file_name, 'r') as read:
            csv_read = csv.reader(read)
            for line in csv_read:
                if len(line) != 5:
                    raise ValueError('Incorrect Format, Expected: name, #polled, #correct, #attempted, #excused')
                
                part = Participant(line[0], line[1], line[2], line[3], line[4])

                self.rand_data.append( [part._poll, part._name] )
                self.order.update( {part._name : part} )
                self.len += 1
        
        """Checks if theres no participants data"""
        if self.len < 1:
            raise ValueError('No Participants Data')

        return self


    """Returns iterator"""
    def __iter__(self):
        return self
    
    """#Returns participants name"""
    def __next__(self):
        """Exits operation"""
        if not self.loop:
            raise StopIteration

        """Randomize and sort data"""
        if self.curr_idx >= self.len or self.curr_idx == 0:
            shuffle(self.rand_data)
            self.rand_data.sort( key = lambda data: data[0] )
            self.curr_idx = 0
          
        """Saves name and participant inorder to change their data"""
        self.curr_name = self.rand_data[self.curr_idx][1]
        self.curr = self.order[self.curr_name]
        self.curr_idx += 1
        return self.curr_name


    """Increments total # of complete iterations"""
    def _total(self):
        self.total += 1
    
    """
    Records Changes to Participant Class
    Calls participant object
    ------------------------------------
    """
    """Increments correct"""
    def correct(self):
        self._total()
        self.curr.correct()
    
    """Increments attempted"""
    def attempted(self):
        self._total()
        self.curr.attempted()
    
    """Increments excused"""
    def excused(self):
        self._total()
        self.curr.excused()
    
    """Increments polled"""
    def missing(self):
        self._total()
        self.curr.missing()
    
    """#Stops iteration by making self.loop False"""
    def stop(self):
        self.loop = False


    """Overwrite csv and close file"""
    def __exit__ (self, type='', value='', traceback=''):
        """Overwrite file"""
        file_w = open(self.file_name, 'w')
        for i in self.order.values():
          file_w.write( str(i) + ' \n' )
        file_w.close()

        """Print total Participants polled"""
        print(f"Total Participants Polled: {self.total}")