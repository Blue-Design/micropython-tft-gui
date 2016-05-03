# buttontest.py Test/demo of pushbutton classes for Pybboard TFT GUI

# The MIT License (MIT)
#
# Copyright (c) 2016 Peter Hinch
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from font14 import font14
from tft_local import setup
from ugui import Button, Buttonset, RadioButtons, Checkbox, Label
from ugui import CIRCLE, RECTANGLE, CLIPPED_RECT, WHITE, BLACK, RED, GREEN, BLUE, YELLOW, GREY

def callback(button, arg, label):
    label.show(arg)
    if arg == 'Q':
        button.objsched.stop()

def cbcb(checkbox, label):
    if checkbox.value():
        label.show('True')
    else:
        label.show('False')

# These tables contain args that differ between members of a set of related buttons
table = [
    {'fgcolor' : GREEN, 'text' : 'Yes', 'args' : ['A'], 'fontcolor' : (0, 0, 0)},
    {'fgcolor' : RED, 'text' : 'No', 'args' : ['B']},
    {'fgcolor' : BLUE, 'text' : '???', 'args' : ['C'], 'fill': False},
    {'fgcolor' : GREY, 'text' : 'Quit', 'args' : ['Q'], 'shape' : CLIPPED_RECT},
]

# similar buttons: only tabulate data that varies
table2 = [
    {'text' : 'P', 'args' : ['p']},
    {'text' : 'Q', 'args' : ['q']},
    {'text' : 'R', 'args' : ['r']},
    {'text' : 'S', 'args' : ['s']},
]

# A Buttonset with two entries
# If buttons to be used in a buttonset, Use list rather than tuple for args because buttonset appends.

table3 = [
     {'fgcolor' : GREEN, 'shape' : CLIPPED_RECT, 'text' : 'Start', 'args' : ['Live']},
     {'fgcolor' : RED, 'shape' : CLIPPED_RECT, 'text' : 'Stop', 'args' : ['Die']},
]

table4 = [
    {'text' : '1', 'args' : ['1']},
    {'text' : '2', 'args' : ['2']},
    {'text' : '3', 'args' : ['3']},
    {'text' : '4', 'args' : ['4']},
]

labels = { 'width' : 70,
          'fontcolor' : WHITE,
          'border' : 2,
          'fgcolor' : RED,
          'bgcolor' : (0, 40, 0),
          'font' : font14,
          }

# USER TEST FUNCTION

def cbtest(checkbox):
    while True:
        yield 3
        checkbox.value(not checkbox.value())

def test():
    print('Testing TFT...')
    objsched, tft, touch = setup()
    tft.backlight(100) # light on
    lstlbl = []
    for n in range(3):
        lstlbl.append(Label(tft, (350, 50 * n), **labels))

# Button assortment
    x = 0
    for t in table:
        t['args'].append(lstlbl[2])
        Button(objsched, tft, touch, (x, 0), font = font14, callback = callback, **t)
        x += 70

# Highlighting buttons
    x = 0
    for t in table2:
        t['args'].append(lstlbl[2])
        Button(objsched, tft, touch, (x, 60), fgcolor = GREY,
               fontcolor = BLACK, litcolor = WHITE, font = font14, callback = callback, **t)
        x += 70

# On/Off toggle
    x = 0
    bs = Buttonset(callback)
    for t in table3: # Buttons overlay each other at same location
        t['args'].append(lstlbl[2])
        bs.add_button(objsched, tft, touch, (x, 120), font = font14, fontcolor = BLACK, **t)
    bs.run()

# Radio buttons
    x = 0
    rb = RadioButtons(callback, BLUE) # color of selected button
    for t in table4:
        t['args'].append(lstlbl[2])
        rb.add_button(objsched, tft, touch, (x, 180), font = font14, fontcolor = WHITE,
                      fgcolor = (0, 0, 90), height = 40, **t)
        x += 60
    rb.run()

# Checkbox
    Checkbox(objsched, tft, touch, (300, 0), callback = cbcb, args = [lstlbl[0]])
    cb2 = Checkbox(objsched, tft, touch, (300, 50), fillcolor = RED, callback = cbcb, args = [lstlbl[1]])

    objsched.add_thread(cbtest(cb2)) # Toggle every 2 seconds
    objsched.run()                                          # Run it!

test()
