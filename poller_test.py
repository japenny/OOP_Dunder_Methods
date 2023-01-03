import pytest
from poller import Participant


def test_participant():
    participant = Participant("Isabelle",5,3,1,1)
    assert str(participant) == "Isabelle,5,3,1,1"
