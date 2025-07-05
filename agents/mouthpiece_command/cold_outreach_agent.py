# cold_outreach_agent.py

from typing import Dict, Optional


class ColdOutreachAgent:
    def __init__(self):
        pass

    def generate_message(self, input: Dict) -> Dict:
        recipient_name = input.get("recipient_name", "")
        recipient_role = input.get("recipient_role", "")
        recipient_company = input.get("recipient_company", "")
        message_goal = input.get("message_goal", "").lower()
        context: Optional[Dict] = input.get("context", {})

        product_name = context.get("product_name")
        referral_source = context.get("referral_source")
        custom_notes = context.get("custom_notes")

        # Determine tone based on goal and role
        if message_goal in ["introduce product", "introduce solution"]:
            tone_used = "professional"
        elif message_goal in ["book a meeting", "request meeting"]:
            tone_used = "persuasive"
        elif message_goal in ["explore collaboration", "partnership"]:
            tone_used = "warm"
        else:
            tone_used = "professional"

        # Subject line templates
        if message_goal == "introduce product" and product_name:
            subject_line = f"Introducing {product_name} to {recipient_company}"
        elif message_goal == "book a meeting":
            subject_line = f"Quick chat with {recipient_company}?"
        elif message_goal == "explore collaboration":
            subject_line = f"Exploring Collaboration: {recipient_company} & Us"
        elif message_goal == "request meeting":
            subject_line = f"Meeting Request: {recipient_company} & Our Team"
        else:
            subject_line = f"Connecting with {recipient_company}"

        # Greeting
        greeting = f"Hi {recipient_name}," if recipient_name else "Hello,"

        # Referral mention
        referral_line = ""
        if referral_source:
            referral_line = f"I was referred to you by {referral_source}, who thought you might be interested."

        # Custom notes
        custom_line = ""
        if custom_notes:
            custom_line = f"{custom_notes}\n\n"

        # Message body templates
        if message_goal == "introduce product":
            product_intro = (
                f"I'm reaching out to introduce {product_name}, a solution designed to help teams like yours at {recipient_company}."
                if product_name else
                f"I'm reaching out to introduce a new solution that could benefit {recipient_company}."
            )
            body = (
                f"{greeting}\n\n"
                f"{referral_line}\n" if referral_line else f"{greeting}\n\n"
            )
            body += (
                f"{custom_line}"
                f"{product_intro}\n"
                "I'd be happy to share more details or answer any questions you might have.\n\n"
                "Would you be open to a brief conversation?"
            )
        elif message_goal in ["book a meeting", "request meeting"]:
            body = (
                f"{greeting}\n\n"
                f"{referral_line}\n" if referral_line else f"{greeting}\n\n"
            )
            body += (
                f"{custom_line}"
                f"I wanted to see if you'd be open to a short call to discuss how we might support {recipient_company}'s goals."
            )
            if product_name:
                body += f" Our product, {product_name}, has helped similar organizations streamline their processes."
            body += (
                "\n\nWould you have 20 minutes this week or next for a quick conversation?"
            )
        elif message_goal == "explore collaboration":
            body = (
                f"{greeting}\n\n"
                f"{referral_line}\n" if referral_line else f"{greeting}\n\n"
            )
            body += (
                f"{custom_line}"
                f"I'm reaching out to explore potential collaboration opportunities between our teams."
            )
            if product_name:
                body += f" With {product_name}, we've seen strong results in related industries."
            body += (
                "\n\nIf this sounds interesting, I'd love to connect and discuss ideas."
            )
        else:
            body = (
                f"{greeting}\n\n"
                f"{referral_line}\n" if referral_line else f"{greeting}\n\n"
            )
            body += (
                f"{custom_line}"
                f"I wanted to connect and see if there might be an opportunity to work together or share insights."
                "\n\nLet me know if you'd be open to a conversation."
            )

        # Follow-up strategy
        if message_goal in ["book a meeting", "request meeting"]:
            follow_up_strategy = "Follow up in 3 days if no response"
        elif message_goal == "introduce product":
            follow_up_strategy = "Send a gentle reminder in 5 days if no reply"
        elif message_goal == "explore collaboration":
            follow_up_strategy = "Follow up in 1 week if no response"
        else:
            follow_up_strategy = "Follow up in 4 days if no reply"

        # Clean up whitespace
        message_body = "\n".join([line.strip() for line in body.splitlines() if line.strip()])

        return {
            "subject_line": subject_line,
            "message_body": message_body,
            "tone_used": tone_used,
            "follow_up_strategy": follow_up_strategy
        }