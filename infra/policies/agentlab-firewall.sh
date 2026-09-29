#!/bin/sh
set -eu

OLD_NET="172.30.250.0/24"
DSH_NET="172.30.251.0/24"
GW_NET="172.30.252.0/24"

OLD_CHAIN="AGENTLAB-EGRESS"
GW_CHAIN="AGENTLAB-GATEWAY-EGRESS"

# Remove obsolete rules from the previous topology
while iptables -C DOCKER-USER -s "$OLD_NET" -j "$OLD_CHAIN" 2>/dev/null; do
  iptables -D DOCKER-USER -s "$OLD_NET" -j "$OLD_CHAIN"
done

while iptables -C INPUT -s "$OLD_NET" -j DROP 2>/dev/null; do
  iptables -D INPUT -s "$OLD_NET" -j DROP
done

if iptables -nL "$OLD_CHAIN" >/dev/null 2>&1; then
  iptables -F "$OLD_CHAIN"
  iptables -X "$OLD_CHAIN" 2>/dev/null || true
fi

# Gateway egress chain
iptables -N "$GW_CHAIN" 2>/dev/null || true
iptables -F "$GW_CHAIN"

iptables -C DOCKER-USER -s "$GW_NET" -j "$GW_CHAIN" 2>/dev/null || \
iptables -I DOCKER-USER 1 -s "$GW_NET" -j "$GW_CHAIN"

# Block private / local destinations from provider gateway
iptables -A "$GW_CHAIN" -d 10.0.0.0/8       -j DROP
iptables -A "$GW_CHAIN" -d 172.16.0.0/12    -j DROP
iptables -A "$GW_CHAIN" -d 192.168.0.0/16   -j DROP
iptables -A "$GW_CHAIN" -d 100.64.0.0/10    -j DROP
iptables -A "$GW_CHAIN" -d 169.254.0.0/16   -j DROP
iptables -A "$GW_CHAIN" -d 127.0.0.0/8      -j DROP

# Allow public HTTPS only
iptables -A "$GW_CHAIN" -p tcp --dport 443 -j ACCEPT

# Deny everything else
iptables -A "$GW_CHAIN" -j DROP

# Protect DasChulito itself from both agent networks
iptables -C INPUT -s "$DSH_NET" -j DROP 2>/dev/null || \
iptables -I INPUT 1 -s "$DSH_NET" -j DROP

iptables -C INPUT -s "$GW_NET" -j DROP 2>/dev/null || \
iptables -I INPUT 1 -s "$GW_NET" -j DROP
