"""ws3_alert.dtn — delay-tolerant Spray-and-Wait store-carry-forward queue (M8, offline path, C1).

When the cloud/SACHET link is down, alerts and readings are queued and rebroadcast over the LoRa mesh with
a bounded number of copies (spray count L), then delivered when a link returns. Pure stdlib.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DTNMessage:
    msg_id: str
    payload: bytes
    copies: int                    # remaining spray copies (binary spray-and-wait halves on relay)
    delivered: bool = False


@dataclass
class DTNQueue:
    L: int = 8                                   # initial copy budget
    store: dict[str, DTNMessage] = field(default_factory=dict)

    def enqueue(self, msg_id: str, payload: bytes) -> None:
        if msg_id not in self.store:
            self.store[msg_id] = DTNMessage(msg_id=msg_id, payload=payload, copies=self.L)

    def relay(self, msg_id: str):
        """Binary spray: hand off half the copies to a peer; keep the rest. Returns copies handed off."""
        m = self.store.get(msg_id)
        if not m or m.copies <= 1:
            return 0
        give = m.copies // 2
        m.copies -= give
        return give

    def deliver(self, msg_id: str) -> bool:
        """Mark delivered when a link to the destination is available."""
        m = self.store.get(msg_id)
        if not m:
            return False
        m.delivered = True
        return True

    def pending(self) -> list[str]:
        return [k for k, m in self.store.items() if not m.delivered]
