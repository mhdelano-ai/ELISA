"""elisa_auto — orchestration skeleton for the automated electrochemical ELISA (docs/02 s3.2, docs/05 s4.1).

Runs entirely with simulated devices; real-hardware drivers are stubs that state which vendor call belongs where.
The Gamry worker (gamry_worker.py) is written for Gamry's own 32-bit Python 3.7 and talks to this package over a
local TCP socket; everything else needs Python >= 3.10.
"""
__version__ = "0.1.0"
