from playsound import playsound
import threading

#! Very simple implementation to play the notification sound
def notification_sound(sound_file="messagesound.wav"):
    try:
        threading.Thread(target=playsound, args=(sound_file,)).start()
    except Exception as e:
        print(f"[ERROR] Could not play sound: {e}")

#! Test the notification sound separately   
if __name__ == "__main__":
    notification_sound("messagesound.wav")