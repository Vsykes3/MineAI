import pyttsx3

engine = pyttsx3.init()
current_volume = 1.0
current_voice = None

def update_voice_settings(volume, voice):
    global current_volume, current_voice
    current_volume = volume
    engine.setProperty('volume', volume)

    voices = engine.getProperty('voices')
    
    selected_voice = None
    if voice == "female":
        for v in voices:
            if "female" in v.name.lower() or "zira" in v.name.lower():  # Windows female
                selected_voice = v
                break
    elif voice == "male":
        for v in voices:
            if "male" in v.name.lower() or "david" in v.name.lower():  # Windows male
                selected_voice = v
                break
    
    if not selected_voice:
        selected_voice = voices[0]  # Default fallback
    
    engine.setProperty('voice', selected_voice.id)
    current_voice = selected_voice.id

def speak(text):
    engine.say(text)
    engine.runAndWait()
