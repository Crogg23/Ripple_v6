"""Generate (or rotate) the Snowflake key pair dbt uses to authenticate.

Background: this account has no SAML IdP, its password is not valid for
programmatic login, and its interactive login is OAUTH_AUTHORIZATION_CODE, which
dbt cannot drive. Key-pair auth is the only non-interactive option that also
allows the ACCOUNTADMIN role (Snowflake's default BLOCKED_ROLES_LIST forbids PATs
from using it, and every LIBRARY_MARTS table is ACCOUNTADMIN-owned).

This writes the private key to .keys/ripple_dbt.p8 (gitignored) and prints the
ALTER USER statement to run. It deliberately does NOT execute any SQL and never
prints the private key, so the secret stays out of shell history and transcripts.

Snowflake gives each user two key slots. We use RSA_PUBLIC_KEY_2 so the existing
RSA_PUBLIC_KEY is never disturbed. To rotate without downtime: write the new key
to the slot you are NOT currently using, verify `dbt debug`, then unset the old.

Usage:
    python scripts/rotate_dbt_keypair.py            # refuses to clobber
    python scripts/rotate_dbt_keypair.py --force    # overwrite existing key
    python scripts/rotate_dbt_keypair.py --slot 1   # target RSA_PUBLIC_KEY
"""
import argparse
import os
import sys

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY_PATH = os.path.join(REPO, ".keys", "ripple_dbt.p8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default="CROGG23")
    ap.add_argument("--slot", type=int, choices=(1, 2), default=2,
                    help="which RSA_PUBLIC_KEY slot to target (default 2)")
    ap.add_argument("--force", action="store_true",
                    help="overwrite an existing private key file")
    ap.add_argument("--out", default=KEY_PATH)
    args = ap.parse_args()

    if os.path.exists(args.out) and not args.force:
        print(f"REFUSING: {args.out} already exists. Pass --force to replace it "
              f"(this invalidates the key currently registered in Snowflake).")
        return 1

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    with open(args.out, "wb") as fh:
        fh.write(key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        ))

    pem = key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode()
    body = "".join(l for l in pem.splitlines() if "KEY-----" not in l)

    slot = "RSA_PUBLIC_KEY" if args.slot == 1 else "RSA_PUBLIC_KEY_2"
    print(f"private key written to {args.out} (gitignored -- do not commit)\n")
    print("Run this in Snowflake, then verify with `dbt debug`:\n")
    print(f"ALTER USER {args.user} SET {slot}='{body}';\n")
    print("If profiles.yml points somewhere else, set SNOWFLAKE_PRIVATE_KEY_PATH "
          f"to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
