"""Empower side.

PassiveEmpower is the primary scheme of docs/02 s3.2: Empower runs the sample set (one line per sample; its BSM
programme carries the A1/B1 steps) and Python only listens to Inject Start. Nothing needs to be called.

ToolkitEmpower is a STUB for docs/02 Fallback A. The Empower Toolkit is licensed (docs/00), but whether it can
start a sample set and report run state on this installation is UNVERIFIED (docs/02 Q5; ask Waters, docs/06 S0.2).
The Toolkit is a Windows COM interface; its object model (Empower Toolkit Programmer's Reference Guide, Waters
71500031805 [S]) was not read in this session, so no call is written here.
"""
from __future__ import annotations

from .base import Empower


class PassiveEmpower(Empower):
    def describe(self):
        return "passive: Empower is the fluidic master; Python listens to Inject Start (docs/02 s3.2)"


class ToolkitEmpower(Empower):  # pragma: no cover - lab only
    def __init__(self, project: str, system: str):
        self.project, self.system = project, system

    def describe(self):
        return f"Empower Toolkit (STUB) project={self.project} system={self.system}"

    def start_sample_set(self, name):
        # TODO: COM automation via pywin32 per the Empower Toolkit Programmer's Reference Guide. UNVERIFIED that
        # the Toolkit can start acquisition (docs/02 s3.1). Bitness of the COM server vs Python also UNVERIFIED.
        raise NotImplementedError("Empower Toolkit control not implemented (UNVERIFIED capability)")
