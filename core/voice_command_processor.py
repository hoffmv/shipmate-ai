# shipmate_ai/core/voice_command_processor.py

import os
import sqlite3
import speech_recognition as sr
from core.shipmate_command_router import ShipmateCommandRouter
from core.sitrep_push import generate_and_send_sitrep
from core.notification_center import add_notification

DATABASE_PATH = os.path.join(os.getcwd(), 'shipmate_ledger.db')

class VoiceCommandProcessor:
    """
    Battlefield processor for voice and text commands in Shipmate AI.
    """

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.router = ShipmateCommandRouter()

        self.command_map = {
            "shipmate send sit-rep": self.send_sitrep,
            "shipmate lock crypto sector": self.lock_crypto_sector,
            "shipmate unlock crypto sector": self.unlock_crypto_sector,
            "shipmate lock stock sector": self.lock_stock_sector,
            "shipmate unlock stock sector": self.unlock_stock_sector,
            "shipmate lock all sectors": self.lock_all_sectors,
            "shipmate unlock all sectors": self.unlock_all_sectors,
            "shipmate show last alerts": self.show_last_alerts
        }

    def listen_for_command(self) -> str:
        """
        Listens via microphone for a spoken command.
        """
        with self.microphone as source:
            print("🛡️ Shipmate listening... Speak now, Captain.")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            command_text = self.recognizer.recognize_google(audio)
            print(f"[Voice Input Captured]: {command_text}")
            return command_text
        except sr.UnknownValueError:
            return "Sorry Captain, I couldn't understand that."
        except sr.RequestError as e:
            return f"Shipmate is offline. Error: {e}"

    def process_voice_command(self) -> str:
        """
        Captures and processes a spoken command.
        """
        command = self.listen_for_command()
        return self.process_text_command(command)

    def process_text_command(self, command_text: str) -> str:
        """
        Processes a direct text or transcribed command.
        """
        normalized_command = command_text.lower().strip()

        if normalized_command in self.command_map:
            print(f"[VoiceCommandProcessor] Recognized Command: '{normalized_command}'")
            return self.command_map[normalized_command]()
        else:
            print(f"[VoiceCommandProcessor] Unrecognized Command: '{normalized_command}'")
            return self.router.route_command(normalized_command)

    def send_sitrep(self) -> str:
        try:
            generate_and_send_sitrep()
            add_notification("Captain ordered Sit-Rep dispatch.")
            return "✅ Sit-Rep dispatched successfully!"
        except Exception as e:
            return f"❌ Sit-Rep dispatch failed: {e}"

    def lock_crypto_sector(self) -> str:
        return self._update_sector_lockout("Crypto", True)

    def unlock_crypto_sector(self) -> str:
        return self._update_sector_lockout("Crypto", False)

    def lock_stock_sector(self) -> str:
        return self._update_sector_lockout("Stocks", True)

    def unlock_stock_sector(self) -> str:
        return self._update_sector_lockout("Stocks", False)

    def lock_all_sectors(self) -> str:
        return self._update_all_sectors(True)

    def unlock_all_sectors(self) -> str:
        return self._update_all_sectors(False)

    def show_last_alerts(self) -> str:
        add_notification("Captain requested last field alerts.")
        return "✅ Last field alerts displayed in dashboard."

    def _update_sector_lockout(self, sector: str, lock: bool) -> str:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE sector_lockouts SET is_locked = ? WHERE sector = ?;",
                (1 if lock else 0, sector)
            )
            conn.commit()
            status = "LOCKED" if lock else "UNLOCKED"
            add_notification(f"{sector} sector {status} by Captain command.")
            return f"✅ {sector} sector {status}."
        except Exception as e:
            return f"❌ Failed to update {sector}: {e}"
        finally:
            conn.close()

    def _update_all_sectors(self, lock: bool) -> str:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE sector_lockouts SET is_locked = ?;",
                (1 if lock else 0,)
            )
            conn.commit()
            status = "LOCKED" if lock else "UNLOCKED"
            add_notification(f"All sectors {status} by Captain command.")
            return f"✅ All sectors {status}."
        except Exception as e:
            return f"❌ Failed to update all sectors: {e}"
        finally:
            conn.close()
