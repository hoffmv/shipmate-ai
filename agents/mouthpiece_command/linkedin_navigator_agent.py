class LinkedInNavigatorAgent:
    def analyze_profile(self, profile: dict) -> dict:
        full_name = profile.get('full_name', 'This professional')
        headline = profile.get('headline', '')
        location = profile.get('location', '')
        current_position = profile.get('current_position', '')
        previous_positions = profile.get('previous_positions', [])
        mutual_connections = profile.get('mutual_connections', 0)
        summary_text = profile.get('summary', '')
        last_interaction = profile.get('last_interaction', None)

        # Build summary
        summary_parts = []
        if full_name:
            summary_parts.append(f"{full_name}")
        if headline:
            summary_parts.append(f"is {headline}")
        if location:
            summary_parts.append(f"based in {location}")
        if current_position:
            summary_parts.append(f"and currently works as {current_position}")
        if previous_positions:
            prev_titles = ', '.join(previous_positions[:2])
            if len(previous_positions) > 2:
                prev_titles += ', and others'
            summary_parts.append(f"with previous experience as {prev_titles}")
        summary_sentence = ' '.join(summary_parts) + '.'
        if summary_text:
            summary_sentence += f" {summary_text.strip()}"

        # Decide suggested_action
        if last_interaction:
            # If we've interacted before, suggest message
            suggested_action = 'message'
            rationale = (
                f"You have previously interacted with {full_name}. "
                "Continuing the conversation helps maintain the relationship."
            )
            suggested_message = (
                f"Hi {full_name.split()[0]},\n\n"
                "I hope you're well! I wanted to follow up on our last conversation and see how things are going on your end."
            )
        elif mutual_connections >= 5:
            # Many mutual connections, suggest connect
            suggested_action = 'connect'
            rationale = (
                f"{full_name} shares {mutual_connections} mutual connections with you, "
                "which indicates a strong network overlap. Connecting could be mutually beneficial."
            )
            suggested_message = (
                f"Hi {full_name.split()[0]},\n\n"
                "I noticed we have several mutual connections and similar professional interests. "
                "I'd be glad to connect and explore potential synergies."
            )
        elif mutual_connections > 0:
            # Some mutual connections, suggest connect
            suggested_action = 'connect'
            rationale = (
                f"{full_name} shares {mutual_connections} mutual connection"
                f"{'s' if mutual_connections > 1 else ''} with you, "
                "which can help establish rapport. Connecting could open up new opportunities."
            )
            suggested_message = (
                f"Hi {full_name.split()[0]},\n\n"
                "I came across your profile and noticed we have mutual connections. "
                "I'd be happy to connect and learn more about your work."
            )
        elif summary_text or headline or current_position:
            # No mutuals, but profile is relevant
            suggested_action = 'connect'
            rationale = (
                f"Although you do not share mutual connections with {full_name}, "
                "their background and experience align with your interests. "
                "Reaching out could be valuable."
            )
            suggested_message = (
                f"Hi {full_name.split()[0]},\n\n"
                "I found your profile and was impressed by your experience. "
                "I'd appreciate the opportunity to connect and exchange insights."
            )
        else:
            # Not enough info, suggest ignore
            suggested_action = 'ignore'
            rationale = (
                f"{full_name}'s profile lacks sufficient information or relevance to warrant engagement at this time."
            )
            suggested_message = ""

        return {
            "summary": summary_sentence.strip(),
            "suggested_action": suggested_action,
            "suggested_message": suggested_message.strip(),
            "rationale": rationale.strip()
        }