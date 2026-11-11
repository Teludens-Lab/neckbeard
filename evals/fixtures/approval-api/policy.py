"""A second repository's policy dependency for multi-repository drift evaluations."""
ALLOWED_ROLES = {'participant'}

def can_submit(role):
    return role in ALLOWED_ROLES
