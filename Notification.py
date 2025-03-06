from playsound import playsound




#! Very simple implementation to play the notification sound
def notification_sound(sound_file="tone.wav"):
    try:
        playsound(sound_file)
    except Exception as e:
        print(f"[ERROR] Could not play sound: {e}")


#! Test the notification sound separately   
if __name__ == "__main__":
    notification_sound("tone.wav")