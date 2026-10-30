import re
import tldextract

from app.state import State

DOMAIN_REGEX = re.compile(
    r"^(?!-)[a-z0-9-]{1,63}(?<!-)(\.(?!-)[a-z0-9-]{1,63}(?<!-))+$"
)


def validate_domain(state: State) -> dict:
    """Plain Python: check format, TLD, and main domain name."""
    domain = state["domain"]

    # Safety net: never trust LLM output blindly
    domain = re.sub(r"^https?://", "", domain).split("/")[0].split(":")[0]

    # Unicode domains: münchen.de -> xn--mnchen-3ya.de
    try:
        domain = domain.encode("idna").decode("ascii")
    except UnicodeError:
        return {"error": f"'{domain}' is not a valid domain name."}

    if not DOMAIN_REGEX.match(domain):
        return {"error": f"'{domain}' is not a valid domain format."}

    ext = tldextract.extract(domain)

    if not ext.suffix:
        return {"error": f"'{domain}' doesn't end in a valid TLD (like .com, .in, .org)."}
    if not ext.domain:
        return {"error": f"'{domain}' has no main domain name."}

    return {
        "domain": domain,
        "main_domain": ext.domain,
        "tld": ext.suffix,
    }