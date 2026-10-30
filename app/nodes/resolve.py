import dns.resolver
import dns.exception

from app.state import State

# Use explicit public DNS servers instead of whatever your OS is configured with
resolver = dns.resolver.Resolver(configure=False)
resolver.nameservers = ["1.1.1.1", "8.8.8.8", "9.9.9.9"]  # Cloudflare, Google, Quad9
resolver.lifetime = 5  # total seconds before giving up


def resolve_ip(state: State) -> dict:
    """Plain Python: real DNS lookup for IPv4 (A) and IPv6 (AAAA)."""
    domain = state["domain"]
    ips: list[str] = []

    for record_type in ("A", "AAAA"):
        try:
            answers = resolver.resolve(domain, record_type)
            ips.extend(r.address for r in answers)
        except dns.resolver.NXDOMAIN:
            return {"error": f"'{domain}' does not exist (NXDOMAIN). Possibly a typo or unregistered."}
        except dns.resolver.NoAnswer:
            continue  # no record of this type; try the next one
        except (dns.resolver.NoNameservers, dns.exception.Timeout):
            return {"error": "DNS servers didn't respond. Try again in a moment."}

    if not ips:
        return {"error": f"'{domain}' exists but has no A/AAAA records."}

    return {"ips": ips}