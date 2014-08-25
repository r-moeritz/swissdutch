swissdutch
==========

A Python implementation of the Dutch pairing system for Swiss tournaments.

Usage
-----

.. code:: python

    from swissdutch.dutch import DutchPairingEngine
    from swissdutch.constants import FideTitle, Colour, FloatStatus
    from swissdutch.pairing import PairingCard

    engine  = DutchPairingEngine()
    input_cards = (
            PairingCard(name='Alice',
                        rating=2500,
                        title=FideTitle.GM,
                        pairing_no=1,
                        score=1,
                        float_status=FloatStatus.none,
                        opponents=(8,),
                        colour_hist=(Colour.white,)),
            PairingCard(name='Bruno',
                        rating=2500,
                        title=FideTitle.IM,
                        pairing_no=2,
                        score=1,
                        float_status=FloatStatus.none,
                        opponents=(9,),
                        colour_hist=(Colour.black,)),
            # ... further cards omitted for brevity
    )
    result_cards = engine.pair_round(2, input_cards)

Status
------

Pre-alpha. At this stage the library is not yet usable since the following
functionality has not yet been implemented. Watch this space!

1. Exchanges (partially implemented)
2. Backtracking
3. Lowering requirements (partially implemented)
4. Exceptions for top scorers in the last round

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

