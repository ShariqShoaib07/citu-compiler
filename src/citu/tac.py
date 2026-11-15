"""Three-address-code instruction data model."""

from dataclasses import dataclass


@dataclass
class TAC:
    """A single TAC instruction as specified in doc/design.md section 3.4."""

    op: str
    arg1: str
    arg2: str
    result: str
