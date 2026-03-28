"""Tests for ANSI colour helpers."""

from lomsh.colours import _fg, _bg, prompt_style, agent_style, RESET


def test_fg_produces_truecolor_escape():
    result = _fg("#fb8500")
    assert result == "\033[38;2;251;133;0m"


def test_bg_produces_truecolor_escape():
    result = _bg("#023047")
    assert result == "\033[48;2;2;48;71m"


def test_fg_strips_hash():
    assert _fg("#ffffff") == _fg("ffffff")


def test_style_functions_wrap_and_reset():
    styled = prompt_style("hello")
    assert "hello" in styled
    assert RESET in styled


def test_agent_style_includes_background():
    styled = agent_style("text")
    # should contain both a fg (38;2) and bg (48;2) escape
    assert "38;2;" in styled
    assert "48;2;" in styled


def test_black_hex():
    assert _fg("#000000") == "\033[38;2;0;0;0m"


def test_white_hex():
    assert _fg("#ffffff") == "\033[38;2;255;255;255m"
