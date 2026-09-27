import sqlite3

connection = sqlite3.connect("fraud_detection.db")
cursor = connection.cursor()

# Add idempotency_key column
cursor.execute("""
ALTER TABLE alerts
ADD COLUMN idempotency_key TEXT
""")

# Give existing alerts unique keys
cursor.execute("""
UPDATE alerts
SET idempotency_key = 'legacy-' || id
WHERE idempotency_key IS NULL
""")

# Make the values unique
cursor.execute("""
CREATE UNIQUE INDEX IF NOT EXISTS
idx_alerts_idempotency_key
ON alerts(idempotency_key)
""")

connection.commit()
connection.close()

print("Database migration completed successfully!")