import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure Speech configuration
speech_key = os.getenv('AZURE_SPEECH_KEY')
service_region = os.getenv('AZURE_SPEECH_REGION')

# Configure the Azure Speech service
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Set the voice to be used for speech synthesis
speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"


def text_to_speech(text, output_file="output.wav"):
    try:
        # Configure the Azure Speech service
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

        # Configure audio output
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
        
        # Create speech synthesizer
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        
        # Synthesize speech
        result = speech_synthesizer.speak_text_async(text).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"Speech synthesized to {output_file}")
            return output_file
        else:
            print(f"Speech synthesis failed: {result.reason}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

# Test the function
if __name__ == "__main__":
    result = text_to_speech("This is a test of the text-to-speech system.")
    print(f"Result: {result}")