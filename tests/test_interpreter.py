import pytest

from interpreter import parse_tokens, join_tokens, is_valid_greek_number, interpretations


def interpret(text):
    return interpretations(parse_tokens(text))


@pytest.mark.parametrize("text, number, valid", [
    ("30 2 5 58", "302558", False),
    ("2 10 69 30 6 6 4", "2106930664", True),
    ("2 10 69 30 6 60 4", "21069306604", False),
    ("0 0 30 69 74 0 9 22 52", "00306974092252", True),
])
def test_base_level(text, number, valid):
    assert join_tokens(parse_tokens(text)) == number
    assert is_valid_greek_number(number) == valid


def test_example_1():
    assert set(interpret("2 10 6 9 30 6 6 4")) == {"2106930664", "210693664"}


def test_example_2():
    assert set(interpret("2 10 69 30 6 6 4")) == {
        "2106930664", "210693664", "2106093664", "21060930664",
    }


def test_example_3():
    results = interpret("0 0 30 69 700 24 1 3 50 2")
    for expected in ["0030697002413502", "003069700241352", "00306972413502", "00306097241352"]:
        assert expected in results
    assert is_valid_greek_number("00306972413502")


def test_first_result_is_the_recognized_number():
    assert interpret("2 10 69 30 6 6 4")[0] == "2106930664"


def test_no_duplicates():
    results = interpret("0 0 30 69 700 24 1 3 50 2")
    assert len(results) == len(set(results))


def test_single_ambiguities():
    assert set(interpret("20 5")) == {"205", "25"}
    assert set(interpret("75")) == {"75", "705"}
    assert set(interpret("700 24")) == {"70024", "724", "7204", "700204"}


def test_no_ambiguity():
    assert interpret("10 6") == ["106"]  # "sixteen" is one word
    assert interpret("6 9") == ["69"]
    assert interpret("30") == ["30"]


def test_extra_spaces_are_ignored():
    assert parse_tokens("  30  2   5 ") == ["30", "2", "5"]


@pytest.mark.parametrize("text", ["", "   ", "12a", "1234", "3.5", "-5"])
def test_invalid_input(text):
    with pytest.raises(ValueError):
        parse_tokens(text)
