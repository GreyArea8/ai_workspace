import sqlite3
import stripe
import logging
import time

logging.basicConfig(
    filename='worker.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

DB_FILE = 'engine_history.db'
stripe.api_key = "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"


def process_live_payload(task_id, payout_target):
    try:
        payout = stripe.Payout.create(
            amount=500,  # Amount in cents ($5.00)
            currency="usd",
            description=f"Automated Micro-Task Payout #{task_id}",
            metadata={"task_id": task_id, "destination": payout_target}
        )
        logging.info(f"Stripe Payout initiated successfully: {payout.id} for Task #{task_id}")
    except Exception as e:
        logging.error(f"Failed to execute Stripe payout for Task #{task_id}: {e}")

def complete_task(cursor, conn, task_id, payout_target):
    cursor.execute(
        "UPDATE tasks SET status = 'completed', completed_at = CURRENT_TIMESTAMP WHERE id = ?",
        (task_id,)
    )
    conn.commit()
    logging.info(f"Task completed. Logged target: {payout_target}")
    process_live_payload(task_id, payout_target)

def poll_tasks():
    logging.info("Stripe worker engine active. Polling for pending tasks...")
    while True:
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT id, payout_target FROM tasks WHERE status = 'pending' LIMIT 5;")
            pending_tasks = cursor.fetchall()
            
            for task_id, payout_target in pending_tasks:
                logging.info(f"Processing pending Task #{task_id}")
                complete_task(cursor, conn, task_id, payout_target)
            
            conn.close()
        except Exception as e:
            logging.error(f"Database error during polling: {e}")
        
        time.sleep(3)

if __name__ == "__main__":
    try:
        poll_tasks()
    except KeyboardInterrupt:
        print("\nWorker stopped safely.")
