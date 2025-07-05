import datetime
import re

class InboxResponderAgent:
    TONE_MAP = {
        'client': 'professional',
        'vendor': 'professional',
        'colleague': 'neutral',
        'recruiter': 'professional',
        'friend': 'casual'
    }

    WARM_ROLES = {'colleague', 'friend'}
    PROFESSIONAL_ROLES = {'client', 'vendor', 'recruiter'}

    URGENCY_KEYWORDS = [
        r'\burgent\b', r'\bASAP\b', r'\bimmediately\b', r'\bdeadline\b',
        r'\bas soon as possible\b', r'\bimportant\b', r'\bpriority\b',
        r'\btime[- ]?sensitive\b', r'\bby (?:[0-9]{1,2}(:[0-9]{2})? ?[ap]m)?\b',
        r'\bend of (?:day|week)\b', r'\bthis (?:morning|afternoon|evening)\b'
    ]

    def analyze_message(self, message: dict) -> dict:
        sender_name = message.get('sender_name', 'Sender')
        sender_role = message.get('sender_role', '').lower()
        subject = message.get('subject', '')
        body = message.get('body', '')
        received_datetime = message.get('received_datetime', '')

        # 1. Analyze urgency
        urgency = self._detect_urgency(body, subject)
        # 2. Analyze tone
        tone_used = self._choose_tone(sender_role, urgency, body)
        # 3. Generate subject line
        subject_line = self._generate_subject(subject, urgency)
        # 4. Generate response body
        response_body = self._generate_response_body(
            sender_name, sender_role, subject, body, urgency, tone_used
        )
        # 5. Rationale
        rationale = self._generate_rationale(sender_role, urgency, tone_used, body)

        return {
            "subject_line": subject_line,
            "response_body": response_body,
            "tone_used": tone_used,
            "rationale": rationale
        }

    def _detect_urgency(self, body, subject):
        text = f"{subject} {body}".lower()
        for pattern in self.URGENCY_KEYWORDS:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        # Check for explicit dates/times in the near future
        date_matches = re.findall(r'\b(?:on )?(?:[0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4}|[A-Za-z]+ \d{1,2}(?:st|nd|rd|th)?)\b', text)
        if date_matches:
            # If a date is mentioned, assume urgency
            return True
        return False

    def _choose_tone(self, sender_role, urgency, body):
        # Default tone by sender_role
        tone = self.TONE_MAP.get(sender_role, 'neutral')
        # Adjust tone for urgency
        if urgency:
            if sender_role in self.PROFESSIONAL_ROLES:
                return 'assertive'
            elif sender_role in self.WARM_ROLES:
                return 'warm'
            else:
                return 'assertive'
        # Adjust for friendly/casual content
        if sender_role == 'friend':
            if any(word in body.lower() for word in ['thanks', 'appreciate', 'catch up', 'see you']):
                return 'warm'
            return 'casual'
        return tone

    def _generate_subject(self, original_subject, urgency):
        if urgency:
            if not original_subject.lower().startswith('re:'):
                return f"RE: {original_subject} [URGENT]"
            elif '[URGENT]' not in original_subject.upper():
                return f"{original_subject} [URGENT]"
            else:
                return original_subject
        else:
            if not original_subject.lower().startswith('re:'):
                return f"RE: {original_subject}"
            return original_subject

    def _generate_response_body(self, sender_name, sender_role, subject, body, urgency, tone_used):
        greeting = self._get_greeting(sender_name, sender_role, tone_used)
        closing = self._get_closing(sender_role, tone_used)
        # Short summary/acknowledgement
        if urgency:
            ack = "Thank you for bringing this to my attention. I'll prioritize this and get back to you as soon as possible."
        else:
            ack = "Thank you for your message."
        # Customization by sender_role and tone
        if sender_role == 'friend':
            if urgency:
                ack = "Got your message—I'll get on this right away!"
            else:
                ack = "Thanks for reaching out! I'll get back to you soon."
        elif sender_role == 'colleague':
            if urgency:
                ack = "I've received your request and will address it as a priority."
            else:
                ack = "Thanks for letting me know."
        elif sender_role == 'recruiter':
            if urgency:
                ack = "Thank you for your update. I'll respond promptly."
            else:
                ack = "Thank you for reaching out. I'll review and get back to you soon."
        elif sender_role == 'vendor':
            if urgency:
                ack = "Thank you for the update. I'll review and respond as soon as possible."
            else:
                ack = "Thank you for the information. I'll follow up shortly."
        elif sender_role == 'client':
            if urgency:
                ack = "Thank you for your message. I'll address this as a priority and keep you updated."
            else:
                ack = "Thank you for reaching out. I'll review and respond soon."
        # Add a prompt for further info if needed
        if self._needs_more_info(body):
            followup = "Could you please provide a bit more detail so I can assist you better?"
            ack = f"{ack} {followup}"
        return f"{greeting}\n\n{ack}\n\n{closing}"

    def _get_greeting(self, sender_name, sender_role, tone_used):
        if tone_used == 'professional':
            return f"Hello {sender_name},"
        elif tone_used == 'assertive':
            return f"Hi {sender_name},"
        elif tone_used == 'warm':
            return f"Hi {sender_name},"
        elif tone_used == 'casual':
            return f"Hey {sender_name},"
        else:  # neutral
            return f"Hello {sender_name},"

    def _get_closing(self, sender_role, tone_used):
        if tone_used == 'professional':
            return "Best regards,\n[Your Name]"
        elif tone_used == 'assertive':
            return "Regards,\n[Your Name]"
        elif tone_used == 'warm':
            return "Thanks so much,\n[Your Name]"
        elif tone_used == 'casual':
            return "Cheers,\n[Your Name]"
        else:  # neutral
            return "Best,\n[Your Name]"

    def _needs_more_info(self, body):
        # If the message is vague or asks a question without details
        vague_phrases = [
            "let me know", "what do you think", "can you help", "need your input",
            "thoughts?", "any ideas", "please advise", "not sure", "unclear"
        ]
        for phrase in vague_phrases:
            if phrase in body.lower():
                return True
        # If the message is very short and doesn't contain specifics
        if len(body.strip()) < 30:
            return True
        return False

    def _generate_rationale(self, sender_role, urgency, tone_used, body):
        rationale = []
        # Tone rationale
        if urgency:
            rationale.append("The message contains urgency indicators, so a prompt and direct tone was chosen.")
        else:
            rationale.append("No urgency detected, so a standard tone was used.")
        # Sender role rationale
        if sender_role in self.PROFESSIONAL_ROLES:
            rationale.append("Since the sender is a professional contact, the response maintains a professional and respectful tone.")
        elif sender_role == 'colleague':
            rationale.append("As the sender is a colleague, the tone is neutral or warm to foster collaboration.")
        elif sender_role == 'friend':
            rationale.append("Since the sender is a friend, a casual or warm tone is appropriate.")
        # Message content rationale
        if self._needs_more_info(body):
            rationale.append("The message appears to lack detail, so the response prompts for more information.")
        return " ".join(rationale)