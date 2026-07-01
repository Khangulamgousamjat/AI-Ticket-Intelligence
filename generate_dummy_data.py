import pandas as pd
import random

categories = ['Billing', 'Technical Issue', 'Account', 'General Query']
priorities = ['Low', 'Medium', 'High']

templates = [
    ("I have a problem with my invoice from last month. It seems I was charged twice.", "Billing", "High"),
    ("My account is locked and I cannot log in.", "Account", "High"),
    ("How do I change my profile picture?", "General Query", "Low"),
    ("The server is returning a 500 error when I try to upload a file.", "Technical Issue", "High"),
    ("When is the next feature update coming out?", "General Query", "Low"),
    ("I need a refund for my subscription.", "Billing", "Medium"),
    ("I forgot my password and the reset link is not arriving to my email.", "Account", "High"),
    ("The application crashes when I click on the dashboard.", "Technical Issue", "High"),
    ("Can I pay using PayPal?", "Billing", "Low"),
    ("Where can I find the documentation for the API?", "General Query", "Low"),
    ("My data is not syncing across devices.", "Technical Issue", "Medium"),
    ("I want to upgrade my plan to premium.", "Account", "Medium"),
    ("I keep receiving spam emails from your service.", "General Query", "Medium"),
    ("The mobile app is very slow after the last update.", "Technical Issue", "Medium"),
    ("My credit card was declined but I have sufficient funds.", "Billing", "High"),
    ("How can I delete my account permanently?", "Account", "Medium")
]

# Generate synthetic dataset
data = []
for _ in range(1000):
    text, category, priority = random.choice(templates)
    noise_prefixes = ["Please help.", "Fix this ASAP!", "Hello,", "Hi team,", "URGENT:", "Question:"]
    noise_suffixes = ["Thanks.", "Regards.", "Appreciate it.", "Get back to me.", ""]
    
    text = random.choice(noise_prefixes) + " " + text + " " + random.choice(noise_suffixes)
    data.append([text.strip(), category, priority])

df = pd.DataFrame(data, columns=['ticket_text', 'category', 'priority'])
df.to_csv('support_tickets_synthetic.csv', index=False)
print("Generated support_tickets_synthetic.csv with 1000 synthetic ticket samples.")
