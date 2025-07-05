# shipmate_ai/generate_sitrep.py

from core.daily_briefing_generator import DailyBriefingGenerator
import pyttsx3
import re

def clean_text_for_speech(text):
    """
    Cleans the Sit-Rep text so it sounds natural when spoken.
    - Replaces underscores with spaces
    - Removes brackets and braces
    - Flattens dictionary outputs
    """
    # Replace underscores with spaces
    text = text.replace("_", " ")
    
    # Remove brackets and braces
    text = re.sub(r"[\{\}\[\]]", "", text)
    
    # Optional: fix specific phrases
    text = text.replace("bills due today", "Bills due today")
    text = text.replace("monthly income", "Monthly income")
    text = text.replace("monthly bills", "Monthly bills")
    text = text.replace("goals progress", "Goals progress")
    
    return text

def main():
    print("🛳️ Shipmate Morning Sit-Rep - Captain's Eyes Only\n")
    
    briefing = DailyBriefingGenerator()
    report = briefing.generate_briefing()
    
    # Print to screen
    print(report)

    # Clean text before speaking
    cleaned_report = clean_text_for_speech(report)

    # Speak it
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)  # Adjust voice speed if needed
    engine.setProperty('volume', 1.0)  # Max volume
    engine.say(cleaned_report)
    engine.runAndWait()

if __name__ == "__main__":
    main()
