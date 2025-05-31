# This file makes the agents directory a Python package
# and initializes agent instances

from app.agents.email_agent import EmailAgent
from app.agents.json_agent import JsonAgent
from app.agents.classifier import ClassifierAgent

# Create agent instances
email_agent = EmailAgent()
json_agent = JsonAgent()
classifier_agent = ClassifierAgent()