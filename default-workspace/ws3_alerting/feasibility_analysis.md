# ws3_alerting/feasibility_analysis.md — the "IP address alerting" idea, settled honestly (P12, WS3)

Phase P12 · RESEARCH-ONLY. MASTER_PROMPT P12 task 2. VERDICT-FIRST, then the technical reasoning. No
own-system claim (Rule 16). Capability numbers (ranges/throughput) live in architecture.md and are sourced
from the P12 reader (717e5ad8); THIS file is networking fact + the verdict.

## 0. The original wish
"A CCTV camera detects a fire nearby and the software alerts everyone near the area without internet using
their IP addresses."

## 1. VERDICT (clear, up front)
Using IP addresses to reach "everyone near a location" is NOT FEASIBLE and should be ABANDONED as a
targeting mechanism. IP addresses do not encode physical location, cannot be enumerated for "nearby" devices,
and in realistic mobile/consumer networks cannot be used to push an unsolicited message to a stranger's phone
— especially not "offline". The feasible path is PROXIMITY BROADCAST (local radio/mesh/siren) + AUTHORIZED
CELLULAR BROADCAST (operated by agencies), designed as tiers (architecture.md). This verdict stands on the
networking facts below.

## 2. Why IP addresses do not encode physical location
- IP addresses are TOPOLOGICAL (where you attach to the network), not GEOGRAPHIC. Allocation follows ISPs/
  ASNs, not streets. Geo-IP databases resolve, at best, to a city/ISP centroid and are routinely wrong by
  tens–hundreds of km for mobile users; they are commercial estimates, not ground truth.
- A phone on mobile data often appears at the carrier's gateway city, not the user's cell. Two neighbours can
  have IPs from different ASNs; a user and someone 500 km away can share the same CGNAT public IP.

## 3. Why you cannot enumerate or push to "nearby" devices by IP
- NAT / DHCP: home and enterprise devices sit behind NAT with private, dynamically-reassigned RFC1918
  addresses; there is no routable per-device address to target from outside.
- CARRIER-GRADE NAT (CGNAT): mobile carriers share one public IPv4 among thousands of subscribers; inbound
  connections to a specific handset are impossible without carrier infrastructure.
- Mobile networks: no inbound listening socket on consumer handsets; firewalls/radios drop unsolicited
  inbound packets; apps receive background pushes only via OS push services (FCM/APNs) — which REQUIRE
  internet and per-app registration, i.e. the opposite of "offline, by IP".
- VPNs: present an exit-node IP unrelated to the user's location.
- IPv6: even with globally-routable addresses, firewalls, privacy-extension address rotation, and the lack of
  any "devices near here" directory make geographic enumeration impossible.
- There is NO registry mapping "IP → person at location who consented to alerts". Building one by scanning is
  both infeasible (NAT/CGNAT) and abusive (unsolicited scanning/messaging).

## 4. What "offline" even means for IP communication
- IP packets still need a shared link. "Offline" realistically means "no internet/WAN", but devices can still
  share a LOCAL link (same Wi-Fi AP, an ad-hoc/mesh network, a local server's hotspot). On a SHARED LOCAL
  LINK you can use UDP broadcast / multicast / mDNS — but only to devices ALREADY JOINED to that link and
  ALREADY RUNNING software that listens. You cannot reach a passer-by's phone that never joined your network.
- So "offline + by IP" collapses to "devices on my LAN running my app" — a tiny, opt-in population, not
  "everyone near the area".

## 5. Who could and could not be reached by address
- COULD (narrow): devices on the SAME local network running our listener app/having our local web page open
  (UDP broadcast / multicast / WebSocket/SSE from a local server / captive-portal notice). Opt-in only.
- COULD NOT: any phone on mobile data; any device behind a different NAT; any passer-by not joined to our
  network; any phone without our app in the foreground/registered. I.e. the large majority of "people near
  the area".

## 6. Therefore — the feasible reframing (full options in architecture.md)
- PROXIMITY, not addressing: alert by PHYSICAL proximity to a transmitter — Tier 1 SIREN/STROBE/PA (reaches
  everyone in earshot/eyeshot, no device needed); Tier 2 LOCAL radio/mesh/BLE advertising + local Wi-Fi push
  to opt-in devices; Tier 3 CELLULAR BROADCAST (Cell Broadcast / WEA / India's CAP-based system) which needs
  NO per-user address and reaches unmodified phones in a geographic cell — BUT is operated by AUTHORIZED
  AGENCIES (regulatory reality confirmed in architecture.md/threat_model.md; a private party generally cannot
  originate it and must integrate via an authority).
- Geo-fencing WITHOUT IP = transmitter placement + radio coverage + (for cellular broadcast) the cell/
  polygon the authority targets; and opt-in consented registries for app/SMS users.

## 7. Honesty
This verdict is a networking-fact conclusion, independent of any paper. The capability claims that follow
(ranges, reachability, latency) are sourced in architecture.md from the P12 reading quota and datasheets;
where a number is unverified it is marked UNVERIFIED. Nothing is simulated or built.
