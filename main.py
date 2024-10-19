import azure.cognitiveservices.speech as speechsdk
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Azure Speech Service configuration
speech_key = os.getenv('AZURE_SPEECH_KEY')
service_region = os.getenv('AZURE_SPEECH_REGION')

def text_to_speech(text, output_file):
    # Initialize speech config
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    
    # Set the voice name, you can change this to other available voices
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

    # Initialize speech synthesizer
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    # Synthesize speech
    result = speech_synthesizer.speak_text_async(text).get()

    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        # Save synthesized audio to file
        audio_data = result.audio_data
        with open(output_file, "wb") as audio_file:
            audio_file.write(audio_data)
        print(f"Speech synthesized and saved to {output_file}")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {cancellation_details.error_details}")

def main():
    # Example usage
    text = "Hello, this is a test of the Blog to Podcast converter."
    output_file = "output.wav"
    text_to_speech(text, output_file)

if __name__ == "__main__":
    main()