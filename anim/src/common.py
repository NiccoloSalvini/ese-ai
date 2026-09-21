"""Shared palette and helpers for the AI-course clips.

Every clip is 10-14 seconds: long enough to see the idea move, short enough to
play twice without losing the room. Plotted functions must be module level —
manim caches them, and pickling a bound method drags the whole Scene along.
"""
from manim import *

NAVY, RED, GREY, GOLD, GREEN = "#2471a3", "#c0392b", "#7f8c8d", "#cdba80", "#1e8449"


def caption(text, size=28):
    return Tex(text, font_size=size).to_edge(DOWN, buff=0.22)


def panel(title, colour=GREY, width=5.6, height=3.0):
    """A labelled box, for the side-by-side comparisons these clips keep needing."""
    box = Rectangle(width=width, height=height, stroke_color=colour, stroke_width=3)
    lab = Tex(title, font_size=26, color=colour).next_to(box, UP, buff=0.12)
    return VGroup(box, lab)
