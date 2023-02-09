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
            
        def __exit__(self, exc_type, exc_value, exc_traceback):
            pass

    return Opener


def test_poller_enter_exit():
    mocker  = mock_open(["Isabelle,6,3,2,1", "Bobby,5,1,3,1", "Charles,5,2,2,1"])

    # with Poller('test.txt', mocker) as poller:
    #     for participant in poller:
    #         while True:
    #             print("%s: (A)nswered (C)orrect (E)xcused (M)issing (Q)uit" % participant)
    #             command = input().lower()
    #             if command == "a":
    #                 poller.attempted()
    #                 break
    #             elif command == "c":
    #                 poller.correct()
    #                 break
    #             elif command == "e":
    #                 poller.excused()
    #                 break
    #             elif command == "q":
    #                 poller.stop()
    #                 break
    #             elif command == "m":
    #                 poller.missing()
    #                 break
    #             print("Unknown response")

    assert mocker.result_to_write == ["Isabelle,6,3,2,1\nBobby,5,1,3,1\nCharles,5,2,2,1"]
    
test_poller_enter_exit()


