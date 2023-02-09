from poller import *
import randopoll
import pytest

"""
Testing Participant class
"""
@pytest.mark.parametrize(
    ['name', 'poll', 'corr', 'att', 'exc', 'expected'],
    [("Isabelle", 5, 3, 1, 1, "Isabelle,5,3,1,1"),
     ("Bobby",4,1,2,1, "Bobby,4,1,2,1")]
)
def test_participant_string(name, poll, corr, att, exc, expected):
    participant = Participant( name, poll, corr, att, exc )
    assert str(participant) == expected

@pytest.mark.parametrize(
    ['name', 'poll', 'corr', 'att', 'exc', 'expected'],
    [
        ("Isabelle", 5, 3, 1, 1, "Isabelle,6,3,2,1"),
        ("Bobby",4,1,2,1, "Bobby,5,1,3,1")
    ]
)
def test_participant_increment(name, poll, corr, att, exc, expected):
    participant = Participant( name, poll, corr, att, exc )
    participant.attempted()
    assert str(participant) == expected


"""
Testing Poller class
"""

# How do i test the poller class, 
# as the way i see it, 
# i need to pass it a file inorder to run

@pytest.mark.parametrize(
    ['file_name', 'expected'],
    [
        ('participant.csv', None)
    ]
)
def test_poller_enter_exit(file_name, expected):


