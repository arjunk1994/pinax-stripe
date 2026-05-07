# Hand-written: convert all pinax-stripe JSON columns from TEXT (jsonfield package,
# Django 1.11 era) to JSONB (Django 5.x native models.JSONField).
#
# This migration belongs in this fork — pinax-stripe's own migration history is
# the right place for changes to its own tables. The fork's earlier 0001..0014
# migrations were rewritten to declare these columns as native models.JSONField,
# but Django doesn't re-run already-applied 0001_initial migrations, so existing
# production databases (originating from pinax-stripe 1.x with jsonfield.fields.JSONField)
# end up with TEXT columns that the new code expects to be JSONB.
#
# Symptoms when this migration is missing:
#   - reads work (psycopg2 returns text, JSONField.from_db_value calls json.loads)
#   - writes work (Django serialises dict to JSON string, Postgres stores as text)
#   - BUT JSON ORM operators (__contains, __has_key, etc.) generate `@>` SQL that
#     requires JSONB and fails on TEXT with `operator does not exist: text @> jsonb`.
#   - Confirmed in apps/payment/views.py: `Event.objects.filter(webhook_message__contains=...)`
#
# Affected columns (9 total across 7 tables):
#     pinax_stripe_account.metadata
#     pinax_stripe_account.verification_fields_needed
#     pinax_stripe_bankaccount.metadata
#     pinax_stripe_charge.outcome
#     pinax_stripe_coupon.metadata
#     pinax_stripe_event.webhook_message
#     pinax_stripe_event.validated_message
#     pinax_stripe_plan.metadata
#     pinax_stripe_transfer.metadata
#
# Idempotency:
#   `ALTER COLUMN ... TYPE jsonb USING column::jsonb` is safe to re-run against an
#   already-jsonb column (Postgres detects the no-op and skips the table rewrite),
#   so applying this on a fresh install (where the columns came in as jsonb via
#   the rewritten 0001_initial) is harmless.
#
# Pre-flight check:
#   Run the SQL in `.junie/docs/upgrades/PREFLIGHT_jsonb_conversion_check.sql`
#   on each tenant schema before applying. Any returned row contains invalid JSON
#   in a TEXT column and must be cleaned up first (the cast will otherwise fail
#   for that tenant).
#
# Locking:
#   pinax_stripe_event is the largest table (one row per Stripe webhook event,
#   years of accumulation). Expect 30s-2min per tenant for the event-table
#   rewrites. atomic=False below releases ACCESS EXCLUSIVE locks between
#   statements so the migration doesn't hold ALL locks for the duration.

from django.db import migrations


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ('pinax_stripe', '0015_auto_20260120_1608'),
    ]

    operations = [
        migrations.RunSQL(
            sql=[
                # pinax_stripe_event (largest table — Stripe webhook history)
                "ALTER TABLE pinax_stripe_event "
                "ALTER COLUMN webhook_message TYPE jsonb USING webhook_message::jsonb;",
                "ALTER TABLE pinax_stripe_event "
                "ALTER COLUMN validated_message TYPE jsonb USING validated_message::jsonb;",

                # pinax_stripe_plan
                "ALTER TABLE pinax_stripe_plan "
                "ALTER COLUMN metadata TYPE jsonb USING metadata::jsonb;",

                # pinax_stripe_coupon
                "ALTER TABLE pinax_stripe_coupon "
                "ALTER COLUMN metadata TYPE jsonb USING metadata::jsonb;",

                # pinax_stripe_charge
                "ALTER TABLE pinax_stripe_charge "
                "ALTER COLUMN outcome TYPE jsonb USING outcome::jsonb;",

                # pinax_stripe_account
                "ALTER TABLE pinax_stripe_account "
                "ALTER COLUMN metadata TYPE jsonb USING metadata::jsonb;",
                "ALTER TABLE pinax_stripe_account "
                "ALTER COLUMN verification_fields_needed TYPE jsonb USING verification_fields_needed::jsonb;",

                # pinax_stripe_bankaccount
                "ALTER TABLE pinax_stripe_bankaccount "
                "ALTER COLUMN metadata TYPE jsonb USING metadata::jsonb;",

                # pinax_stripe_transfer
                "ALTER TABLE pinax_stripe_transfer "
                "ALTER COLUMN metadata TYPE jsonb USING metadata::jsonb;",
            ],
            reverse_sql=[
                # JSONB -> TEXT. Postgres has a built-in jsonb_out cast.
                "ALTER TABLE pinax_stripe_transfer "
                "ALTER COLUMN metadata TYPE text USING metadata::text;",
                "ALTER TABLE pinax_stripe_bankaccount "
                "ALTER COLUMN metadata TYPE text USING metadata::text;",
                "ALTER TABLE pinax_stripe_account "
                "ALTER COLUMN verification_fields_needed TYPE text USING verification_fields_needed::text;",
                "ALTER TABLE pinax_stripe_account "
                "ALTER COLUMN metadata TYPE text USING metadata::text;",
                "ALTER TABLE pinax_stripe_charge "
                "ALTER COLUMN outcome TYPE text USING outcome::text;",
                "ALTER TABLE pinax_stripe_coupon "
                "ALTER COLUMN metadata TYPE text USING metadata::text;",
                "ALTER TABLE pinax_stripe_plan "
                "ALTER COLUMN metadata TYPE text USING metadata::text;",
                "ALTER TABLE pinax_stripe_event "
                "ALTER COLUMN validated_message TYPE text USING validated_message::text;",
                "ALTER TABLE pinax_stripe_event "
                "ALTER COLUMN webhook_message TYPE text USING webhook_message::text;",
            ],
        ),
    ]
