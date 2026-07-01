# AI Ticket Intelligence — Expanded Synthetic Data Generator

"""generate_more_data.py

Creates an expanded synthetic support ticket dataset for AI-Ticket-Intelligence.
Produces `support_tickets_synthetic_expanded.csv` with a configurable number of samples.

Usage:
    python generate_more_data.py --count 5000 --out support_tickets_synthetic_expanded.csv

This script builds on the original `generate_dummy_data.py` but introduces:
- More templates and language variations
- Noise prefixes/suffixes and common typos
- Optional timestamp and ticket_id columns
- Slightly imbalanced class distributions to better mimic real data
"""

import csv
import random
import argparse
from datetime import datetime, timedelta
import uuid

CATEGORIES = [
    'Billing', 'Technical Issue', 'Account', 'General Query', 'Feature Request', 'Security', 'Integration'
]
PRIORITIES = ['Low', 'Medium', 'High']

BASE_TEMPLATES = [
    ("I was charged twice for my subscription this month.", 'Billing', 'High'),
    ("My account is locked and I cannot log in.", 'Account', 'High'),
    ("How can I change my profile picture?", 'General Query', 'Low'),
    ("The server returns a 500 error when uploading files.", 'Technical Issue', 'High'),
    ("I'd like to request a new feature for reporting.", 'Feature Request', 'Low'),
    ("I need help removing a saved payment method.", 'Billing', 'Medium'),
    ("The reset password link does not arrive in my email.", 'Account', 'High'),
    ("App crashes when opening the dashboard after update.", 'Technical Issue', 'High'),
    ("Can I pay using PayPal or another provider?", 'Billing', 'Low'),
    ("Where can I find the API documentation for integrations?", 'Integration', 'Low'),
    ("My data is not syncing across devices.", 'Technical Issue', 'Medium'),
    ("I want to upgrade to the premium plan.", 'Account', 'Medium'),
    ("I'm receiving spam notifications from your service.", 'Security', 'Medium'),
    ("The mobile app is very slow after the last update.", 'Technical Issue', 'Medium'),
    ("My credit card was declined but funds are available.", 'Billing', 'High'),
    ("How can I permanently delete my account?", 'Account', 'Medium'),
    ("There is a vulnerability warning in my dashboard.", 'Security', 'High'),
    ("Our integration is failing with a timeout error.", 'Integration', 'High')
]

NOISE_PREFIXES = [
    "Please help", "URGENT", "Hi team", "Hello", "FYI", "Quick question", "URGENT:", "Hi",
    "Hello Support", "Good morning", "Good evening"
]

NOISE_SUFFIXES = [
    "Thanks.", "Regards.", "Appreciate it.", "Please respond ASAP.", "", "Thank you!", "Best, Customer"
]

TYPO_MAPPINGS = [
    ("password", ["pasword", "passwrd", "passwords"]),
    ("account", ["acount", "accoutn", "acct"]),
    ("payment", ["paymnt", "paymet", "payment"]),
    ("upgrade", ["upgrde", "upgrad", "upgrde"]),
]

def maybe_introduce_typo(text, prob=0.12):
    if random.random() > prob:
        return text
    for word, typos in TYPO_MAPPINGS:
        if word in text.lower():
            typo = random.choice(typos)
            # Replace first occurrence (case-insensitive)
            idx = text.lower().find(word)
            if idx != -1:
                return text[:idx] + typo + text[idx+len(word):]
    return text


def random_time(start_days_ago=180):
    now = datetime.utcnow()
    delta = timedelta(days=random.randint(0, start_days_ago),
                      seconds=random.randint(0, 86400))
    return (now - delta).isoformat()


def build_ticket(template_count=1):
    text, category, priority = random.choice(BASE_TEMPLATES)

    # Add noise, prefixes/suffixes
    prefix = random.choice(NOISE_PREFIXES)
    suffix = random.choice(NOISE_SUFFIXES)

    # Occasionally add multi-sentence context
    extra_context = ''
    if random.random() < 0.2:
        extra_context = ' ' + random.choice([
            "I tried multiple times and it still fails.",
            "This started happening after the latest update.",
            "I need this resolved before EOD.",
            "This affects our production environment.",
            "Please escalate to engineering if needed."
        ])

    # Combine
    full_text = f"{prefix}: {text}{extra_context} {suffix}".strip()

    # Randomly introduce typos
    full_text = maybe_introduce_typo(full_text)

    # Small chance to change category/priority to introduce noise
    if random.random() < 0.03:
        category = random.choice(CATEGORIES)
    if random.random() < 0.05:
        priority = random.choices(PRIORITIES, weights=[0.6, 0.3, 0.1])[0]

    return full_text, category, priority


def generate_dataset(out_file='support_tickets_synthetic_expanded.csv', count=5000):
    print(f"Generating {count} synthetic tickets to {out_file}...")
    with open(out_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ticket_id', 'created_at', 'ticket_text', 'category', 'priority'])
        for i in range(count):
            ticket_id = str(uuid.uuid4())
            created_at = random_time()
            ticket_text, category, priority = build_ticket()
            writer.writerow([ticket_id, created_at, ticket_text, category, priority])
    print("Done.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate expanded synthetic support tickets CSV')
    parser.add_argument('--count', type=int, default=5000, help='Number of tickets to generate')
    parser.add_argument('--out', type=str, default='support_tickets_synthetic_expanded.csv', help='Output CSV filename')
    args = parser.parse_args()

    generate_dataset(out_file=args.out, count=args.count)
