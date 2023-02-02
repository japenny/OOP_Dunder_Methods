from poller import *
import randopoll

def test_participant():
    participant = Participant("Isabelle",5,3,1,1)
    print("this: ", participant)
    assert str(participant) == "Isabelle,5,3,1,1"

print(test_participant())

def test_poller():
    pass

