"""Shared Snowflake connection for repo scripts, using the dbt key pair.

Reads the same private key dbt uses (.keys/ripple_dbt.p8, gitignored) so scripts and
dbt authenticate identically. Nothing here holds a secret: the key is loaded from
disk at call time and never printed.
"""
import os

from cryptography.hazmat.primitives import serialization

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_KEY = os.path.join(REPO, ".keys", "ripple_dbt.p8")

ACCOUNT = os.environ.get("SNOWFLAKE_ACCOUNT", "ONEAFDA-UMB20733")
USER = os.environ.get("SNOWFLAKE_USER", "CROGG23")
ROLE = os.environ.get("SNOWFLAKE_ROLE", "ACCOUNTADMIN")
WAREHOUSE = os.environ.get("SNOWFLAKE_ETL_WAREHOUSE",
                           os.environ.get("SNOWFLAKE_WAREHOUSE", "DBT_WH"))


def private_key_der(path=None):
    path = path or os.environ.get("SNOWFLAKE_PRIVATE_KEY_PATH") or DEFAULT_KEY
    with open(path, "rb") as fh:
        key = serialization.load_pem_private_key(fh.read(), password=None)
    return key.private_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )


def connect(database=None, schema=None):
    import snowflake.connector

    return snowflake.connector.connect(
        account=ACCOUNT,
        user=USER,
        role=ROLE,
        warehouse=WAREHOUSE,
        private_key=private_key_der(),
        database=database,
        schema=schema,
    )


def columns_of(table, database="LIBRARY_RAW", schema="LANDING", conn=None):
    """Return the column names of a table in declaration order, exact case."""
    close = conn is None
    conn = conn or connect()
    try:
        cur = conn.cursor()
        cur.execute(
            f"select column_name from {database}.information_schema.columns "
            f"where table_schema = %s and table_name = %s "
            f"order by ordinal_position",
            (schema, table),
        )
        return [r[0] for r in cur.fetchall()]
    finally:
        if close:
            conn.close()
