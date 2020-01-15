# flake8: noqa: B101

"""
App interface tests cases
"""

import pytest
import app


def deep_diff(left, right, keys=[], order=False):
    """
    Allows for recursive approx comparassions.
    This is needed for acurate assesment of relevant differences in deep objects.
    """
    if isinstance(left, dict):
        for key in left.keys():
            diff = deep_diff(left[key], right[key], keys + [key])
            if diff:
                return diff
    elif isinstance(left, list):
        if not order:
            left = sorted(left)
            right = sorted(right)
        for key, (left_value, right_value) in enumerate(zip(left, right)):
            diff = deep_diff(left_value, right_value, keys + [key])
            if diff:
                return diff
    else:
        try:
            if pytest.approx(left) != float(right):
                return f"sub-key `{keys}` differs: {left} != {right}"
        except TypeError:
            if left != right:
                return f"sub-key `{keys}` differs: {left} != {right}"


def test__group_anagrams(app, anagrams_pairs):
    words, result = anagrams_pairs
    groups = app.group_anagrams(words)
    assert not deep_diff(result, groups)
