swissdutch
==========

A Python implementation of the Dutch pairing system for Swiss tournaments.

Usage
-----

.. code:: python

    from swissdutch.dutch import DutchPairingEngine
    from swissdutch.constants import FideTitle, Colour, FloatStatus
    from swissdutch.player import Player

    engine  = DutchPairingEngine()
    input_players = (
            Player(name='Alice',
                   rating=2500,
                   title=FideTitle.GM,
                   pairing_no=1,
                   score=1,
                   float_status=FloatStatus.none,
                   opponents=(8,),
                   colour_hist=(Colour.white,)),
            Player(name='Bruno',
                   rating=2500,
                   title=FideTitle.IM,
                   pairing_no=2,
                   score=1,
                   float_status=FloatStatus.none,
                   opponents=(9,),
                   colour_hist=(Colour.black,)),
            # ... further cards omitted for brevity
    )
    result_players = engine.pair_round(2, input_players)

Status
------

Alpha. All the rules of the Dutch system have been implemented except for
**D.4** which specifies the correct procedure to obtain the best pairings in
homogenous remainder brackes. See issue #1. I hope to implement this soon.

License
-------

::

   Copyright (c) Ralph Möritz 2014.

   Permission is hereby granted, free of charge, to any person obtaining a copy of
   this software and associated documentation files (the "Software"), to deal in
   the Software without restriction, including without limitation the rights to
   use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
   of the Software, and to permit persons to whom the Software is furnished to do
   so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in all
   copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
   SOFTWARE.

