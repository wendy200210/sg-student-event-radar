#!/usr/bin/env python3
import sys
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

TRACKING_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid", "ref", "source"}


def normalize_url(value):
    parts = urlsplit(value.strip())
    if parts.scheme.lower() not in {"http", "https"} or not parts.hostname:
        raise ValueError("URL must use http or https and include a hostname")
    host = parts.hostname.lower()
    port = parts.port
    if port and not ((parts.scheme.lower() == "http" and port == 80) or (parts.scheme.lower() == "https" and port == 443)):
        host = f"{host}:{port}"
    path = parts.path or "/"
    if path != "/":
        path = path.rstrip("/")
    query = []
    for key, item in parse_qsl(parts.query, keep_blank_values=True):
        lower = key.lower()
        if lower.startswith("utm_") or lower in TRACKING_KEYS:
            continue
        query.append((key, item))
    query.sort()
    return urlunsplit((parts.scheme.lower(), host, path, urlencode(query, doseq=True), ""))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: normalize_url.py URL")
    try:
        print(normalize_url(sys.argv[1]))
    except ValueError as exc:
        raise SystemExit(str(exc))
