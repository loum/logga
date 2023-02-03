"""Tests for the global fixture arrangement.

"""
from typing import Text


def test_working_dir(working_dir: Text):
    """Test the "working_dir" fixture."""
    msg = 'conftest "working_dir" fixture should provide string type'
    assert isinstance(working_dir, str), msg
