"""ws3_alert.cap — CAP 1.2 alert builder + signer, HUMAN-GATED (M8, Rule 19).

COMPONENT_DESIGN.md §2.5/§3.3. Severity/Urgency/Certainty are a DETERMINISTIC function of the advisory
Level — never inferred by a model from free text. Building a CAP alert REQUIRES a human approval token
(ws3_alert.operator); without it we raise SafetyViolation. No autonomous public alert can exist.
"""
from __future__ import annotations

import hashlib
import hmac

from lxml import etree

from ..common.exceptions import SafetyViolation
from ..common.types import Decision, Level

CAP_NS = "urn:oasis:names:tc:emergency:cap:1.2"

# Deterministic Level -> CAP (severity, urgency, certainty)
_MAP = {
    Level.GREEN: None,  # no public CAP for GREEN
    Level.YELLOW: ("Minor", "Future", "Possible"),
    Level.ORANGE: ("Severe", "Expected", "Likely"),
    Level.RED: ("Extreme", "Immediate", "Observed"),
}


def cap_fields_for_level(level: Level):
    return _MAP[level]


def build_cap(decision: Decision, approval_token: str | None, *, sender: str,
              area_polygon: str | None = None, key: bytes | None = None) -> str:
    """Return a signed CAP 1.2 XML string for an operator-APPROVED decision. Raises without approval."""
    if not approval_token or not approval_token.startswith("APPROVED:"):
        raise SafetyViolation(
            "CAP build refused: no valid human approval token (Rule 19 — public alerts are human-gated)"
        )
    fields = cap_fields_for_level(decision.level)
    if fields is None:
        raise SafetyViolation(f"no public CAP is issued for level {decision.level.name}")
    severity, urgency, certainty = fields

    nsmap = {None: CAP_NS}
    alert = etree.Element("alert", nsmap=nsmap)
    cid = f"urn:trinetra:{decision.zone_id}:{decision.t.strftime('%Y%m%dT%H%M%SZ')}"
    etree.SubElement(alert, "identifier").text = cid
    etree.SubElement(alert, "sender").text = sender
    etree.SubElement(alert, "sent").text = decision.t.isoformat()
    etree.SubElement(alert, "status").text = "Actual"
    etree.SubElement(alert, "msgType").text = "Alert"
    etree.SubElement(alert, "scope").text = "Public"

    info = etree.SubElement(alert, "info")
    etree.SubElement(info, "category").text = "Geo" if decision.hazard.value != "FIRE" else "Fire"
    etree.SubElement(info, "event").text = decision.hazard.value
    etree.SubElement(info, "urgency").text = urgency
    etree.SubElement(info, "severity").text = severity
    etree.SubElement(info, "certainty").text = certainty
    # Honesty: advisory + reliability + class flag surfaced in the parameters.
    for name, val in [("advisory", "true"),
                      ("reliability", decision.conformal.reliability.value),
                      ("uncertain", str(decision.uncertain).lower()),
                      ("used_classC", str(decision.used_classC).lower()),
                      ("approved_by", approval_token.split(":", 1)[1])]:
        p = etree.SubElement(info, "parameter")
        etree.SubElement(p, "valueName").text = name
        etree.SubElement(p, "value").text = val
    area = etree.SubElement(info, "area")
    etree.SubElement(area, "areaDesc").text = decision.zone_id
    if area_polygon:
        etree.SubElement(area, "polygon").text = area_polygon

    xml = etree.tostring(alert, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    if key is not None:
        tag = hmac.new(key, xml, hashlib.sha256).hexdigest()
        comment = etree.Comment(f" signature hmac-sha256:{tag} ")
        alert.append(comment)
        xml = etree.tostring(alert, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    return xml.decode("utf-8")
