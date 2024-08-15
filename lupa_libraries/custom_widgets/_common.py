"""
Module containing common functions for custom widgets. 
"""

###############
### Imports ###
###############

# Kivy imports #

from kivy.uix.widget import Widget

#################
### Functions ###
#################


def hide_widget(widget: Widget, do_hide=True):
    """
    Hide or unhide a widget.

    Parameters
    ----------
    widget : Widget
        Widget to change.
    do_hide : bool, optional (default is True)
        Indicates whether to hide or unhide.
    """

    if hasattr(widget, "saved_attributes"):
        if not do_hide:
            widget.height, widget.size_hint_y, widget.opacity, widget.disabled = widget.saved_attributes
            del widget.saved_attributes
    elif do_hide:
        widget.saved_attributes = widget.height, widget.size_hint_y, widget.opacity, widget.disabled
        widget.height, widget.size_hint_y, widget.opacity, widget.disabled = 0, None, 0, True
