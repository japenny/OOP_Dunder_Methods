from poller import *
import randopoll
import pytest

"""
Testing Participant class
"""

"""Testing string return in participant class"""
@pytest.mark.parametrize(
    ['name', 'poll', 'corr', 'att', 'exc', 'expected'],
    [("Isabelle", 5, 3, 1, 1, "Isabelle,5,3,1,1"),
     ("Bobby",4,1,2,1, "Bobby,4,1,2,1")]
)
def test_participant_string(name, poll, corr, att, exc, expected):
    participant = Participant( name, poll, corr, att, exc )
    assert str(participant) == expected

"""Testing increments in participant class"""
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

"""Creates mock class for testing data"""
def mock_open(input_list):
    class Opener:
        input = input_list
        result_to_write = []

        def __init__(self, file_name, mode=""):
            pass

        def __iter__(self):
            return iter(Opener.input)
            
        def __enter__(self):
            return self
        
        def write(self, text):
            Opener.result_to_write.append(text)

        def close(self):
            pass
            
        def __exit__(self, exc_type, exc_value, exc_traceback):
            pass

    return Opener

"""Testing enter & exit functionality"""
@pytest.mark.parametrize(
    ['data', 'expected'],
    [(["Isabelle,6,3,2,1", "Bobby,5,1,3,1"], ["Isabelle,6,3,2,1\nBobby,5,1,3,1"]),
     (["Lisa,1,1,0,0", "Tom,0,0,0,0"], ["Lisa,1,1,0,0\nTom,0,0,0,0"])]
)
def test_poller_enter_exit(data, expected):
    mocker = mock_open(data)
    poll = Poller('test.txt', mocker)

    poll.__enter__()
    poll.__exit__()

    assert mocker.result_to_write == expected

"""Testing iter & next functionality"""
@pytest.mark.parametrize(
    ['data', 'expected'],
    [(["Isabelle,6,3,2,1", "Bobby,5,1,3,1"], ["Isabelle,6,3,2,1\nBobby,5,1,3,1"]),
     (["Lisa,1,1,0,0", "Tom,0,0,0,0"], ["Lisa,1,1,0,0\nTom,0,0,0,0"])]
)
def test_poller_iter_next(data, expected):
    mocker = mock_open(data)
    poll = Poller('test.txt', mocker)

    poll.__enter__()
    iter_test = poll.__iter__()

    for i,_ in enumerate(iter_test):
        if i > 3:
            break
    poll.__exit__()

    assert mocker.result_to_write == expected

"""Testing pollers increments w/participant class"""
@pytest.mark.parametrize(
    ['data', 'expected'],
    [(["Isabelle,2,0,0,0"], ["Isabelle,4,1,1,0"]),
     (["Lisa,1,1,0,0"], ["Lisa,3,2,1,0"])]
)
def test_poller_participant_increment(data, expected):
    mocker = mock_open(data)
    poll = Poller('test.txt', mocker)
    
    poll.__enter__()
    poll.__iter__()
    poll.__next__()
    poll.attempted()
    poll.correct()
    poll.__exit__()

    assert mocker.result_to_write == expected

"""Testing pollers randomness"""
@pytest.mark.parametrize(
    ['data', 'expected'],
    [(["Boop,0,0,0,0","Beep,0,0,0,0","Bop,0,0,0,0", "Flop,0,0,0,0"], None),
     (["Fall,0,0,0,0", "Tall,0,0,0,0", "Call,0,0,0,0", "Ball,0,0,0,0"], None)]
)
def test_poller_random(data, expected):
    mocker = mock_open(data)
    comp1 = ''
    comp2 = ''

    poll = Poller('test.txt', mocker)
    poll.__enter__()
    poll.__iter__()
    poll.__next__()
    comp1 = [i[1] for i in poll.rand_data]

    poll = Poller('test.txt', mocker)
    poll.__enter__()
    poll.__iter__()
    poll.__next__()
    comp2 = [i[1] for i in poll.rand_data]

    assert comp1 != comp2