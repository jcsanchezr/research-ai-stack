#!/bin/sh
set -eu

SECRET_FILE="/run/secrets/blablador_token"
TEMPLATE="/etc/nginx/nginx.conf"
RUNTIME="/tmp/nginx-runtime.conf"

if [ ! -r "$SECRET_FILE" ]; then
    echo "ERROR: Blablador secret is missing or unreadable" >&2
    exit 1
fi

TOKEN="$(cat "$SECRET_FILE")"

if [ -z "$TOKEN" ]; then
    echo "ERROR: Blablador secret is empty" >&2
    exit 1
fi

# Escape characters significant to sed replacement.
ESCAPED_TOKEN="$(printf '%s' "$TOKEN" | sed \
    -e 's/[\/&]/\\&/g')"

sed "s/__BLABLADOR_TOKEN__/${ESCAPED_TOKEN}/" \
    "$TEMPLATE" > "$RUNTIME"

unset TOKEN ESCAPED_TOKEN

exec nginx -c "$RUNTIME" -g 'daemon off;'
