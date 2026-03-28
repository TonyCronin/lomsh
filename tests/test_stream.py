"""Tests for _process_stream — the pure stream-parsing function."""

import pytest
from lomsh.agent import _process_stream


class FakeDelta:
    def __init__(self, content):
        self.content = content


class FakeChoice:
    def __init__(self, content):
        self.delta = FakeDelta(content)


class FakeUsage:
    def __init__(self, prompt_tokens, completion_tokens):
        self.prompt_tokens      = prompt_tokens
        self.completion_tokens  = completion_tokens


class FakeChunk:
    def __init__(self, content=None, usage=None):
        self.choices = [FakeChoice(content)] if content is not None else []
        self.usage   = usage


def make_stream(*contents, usage_in=10, usage_out=5):
    """Build a fake stream: content chunks then a usage-only chunk."""
    chunks = [FakeChunk(content=c) for c in contents]
    chunks.append(FakeChunk(usage=FakeUsage(usage_in, usage_out)))
    return iter(chunks)


def test_basic_text_assembly():
    stream = make_stream("hello", " ", "world")
    text, _, _ = _process_stream(stream)
    assert text == "hello world"


def test_token_counts_returned():
    stream = make_stream("hi", usage_in=123, usage_out=45)
    _, usage_in, usage_out = _process_stream(stream)
    assert usage_in  == 123
    assert usage_out == 45


def test_empty_stream():
    stream = make_stream(usage_in=0, usage_out=0)
    text, usage_in, usage_out = _process_stream(stream)
    assert text     == ""
    assert usage_in  == 0
    assert usage_out == 0


def test_none_content_chunks_skipped():
    # chunks with no content (e.g. role-only chunks) should not add to text
    chunks = [
        FakeChunk(content=None),
        FakeChunk(content="real"),
        FakeChunk(usage=FakeUsage(1, 1)),
    ]
    text, _, _ = _process_stream(iter(chunks))
    assert text == "real"


def test_multipart_response():
    parts = ["The ", "answer ", "is ", "42."]
    stream = make_stream(*parts)
    text, _, _ = _process_stream(stream)
    assert text == "The answer is 42."
