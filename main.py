# main.py
import os
import azure.cognitiveservices.speech as speechsdk
from openai import AzureOpenAI
from dotenv import load_dotenv
from pydub import AudioSegment
import time

# Load environment variables
load_dotenv()

class ContentProcessor:
    """
    Handles the processing of text content into conversational format using Azure OpenAI.
    """
    def __init__(self):
        # Check for required environment variables
        required_vars = [
            "AZURE_OPENAI_KEY",
            "AZURE_OPENAI_ENDPOINT",
            "AZURE_OPENAI_DEPLOYMENT",
            "AZURE_OPENAI_API_VERSION"
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
            
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    
    def process_content_conversational(self, text):
        """
        Process content into a conversational format.
        """
        system_prompt = system_prompt = """You are an expert podcast script writer specializing in creating engaging, upbeat conversations.
        Transform the given text into a dynamic discussion between two enthusiastic hosts:

        Host Personalities:
        - Alex: Energetic, curious, and great at asking insightful questions. Uses conversational language and often relates topics to real-world examples.
        - Sarah: Knowledgeable, friendly, and excellent at explaining complex ideas simply. Brings enthusiasm and often adds interesting insights.

        Conversation Style Requirements:
        1. Keep it upbeat and engaging throughout
        2. Include natural reactions ("That's fascinating!", "Wow, I hadn't thought of that!")
        3. Use conversational language rather than formal speech
        4. Add brief personal touches or relevant anecdotes
        5. Include occasional light humor where appropriate
        6. Use short, punchy sentences for better audio flow
        7. Total word count: exactly 300 words

        Structure:
        1. Start with a warm, engaging welcome and topic introduction
        2. Main discussion with back-and-forth interaction
        3. Include relevant examples or real-world applications
        4. End with key takeaways and an upbeat conclusion

        Interaction Guidelines:
        - Add verbal nods ("Exactly!", "Right!", "I see what you mean")
        - Include natural transitions between points
        - Use questions to drive the conversation forward
        - Balance speaking time between hosts
        - Keep segments concise for better listening experience

        Format Example:
        Alex: Hey everyone! I'm super excited about today's topic. Sarah, shall we dive in?
        Sarah: Absolutely, Alex! This is something I think our listeners will find fascinating.
        Alex: [Introduces main point with enthusiasm]
        Sarah: [Adds insight with real-world example]
        [Continue natural back-and-forth...]

        Remember: The conversation should feel like two friends having an exciting discussion over coffee, while being informative and valuable to listeners.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Original text to convert into conversation:\n{text}"}
                ],
                temperature=0.7,
                max_tokens=1000,
                n=1
            )
            
            return self.parse_conversation_script(response.choices[0].message.content)
            
        except Exception as e:
            print(f"Error in content processing: {str(e)}")
            return None

    def parse_conversation_script(self, script):
        """
        Parse the conversation script into structured format.
        """
        lines = script.strip().split('\n')
        conversation = []
        
        for line in lines:
            if not line.strip():
                continue
            if ':' not in line:
                continue
                
            speaker, dialogue = line.split(':', 1)
            conversation.append({
                'speaker': speaker.strip(),
                'dialogue': dialogue.strip()
            })
            
        return conversation

class TextToSpeechConverter:
    def __init__(self):
        # Check for required environment variables
        required_vars = ["AZURE_SPEECH_KEY", "AZURE_SPEECH_REGION"]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
            
        self.speech_key = os.getenv('AZURE_SPEECH_KEY')
        self.service_region = os.getenv('AZURE_SPEECH_REGION')
        self.voices = {
            'Alex': 'en-US-GuyNeural',
            'Sarah': 'en-US-JennyNeural'
        }
        
        # Set FFmpeg path explicitly
        AudioSegment.converter = os.path.join(os.path.dirname(__file__), "ffmpeg.exe")
        
        # Initialize content processor
        self.content_processor = ContentProcessor()
        
        # Create temp directory if it doesn't exist
        os.makedirs('temp', exist_ok=True)

    def create_conversation_audio(self, text, output_file="conversation.wav"):
        try:
            conversation = self.content_processor.process_content_conversational(text)
            if not conversation:
                return False, None, "Failed to process content into conversation"

            speech_config = speechsdk.SpeechConfig(
                subscription=self.speech_key, 
                region=self.service_region
            )
            
            temp_files = []
            
            for i, segment in enumerate(conversation):
                speaker = segment['speaker']
                dialogue = segment['dialogue']
                
                temp_file = os.path.join('temp', f"segment_{i}_{speaker}.wav")
                temp_files.append(temp_file)
                
                speech_config.speech_synthesis_voice_name = self.voices[speaker]
                
                audio_config = speechsdk.audio.AudioOutputConfig(
                    filename=temp_file
                )
                
                synthesizer = speechsdk.SpeechSynthesizer(
                    speech_config=speech_config,
                    audio_config=audio_config
                )
                
                result = synthesizer.speak_text_async(dialogue).get()
                
                if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
                    return False, None, f"Failed to synthesize speech for {speaker}"
                
                time.sleep(0.1)

            combined_audio = None
            
            for temp_file in temp_files:
                if not os.path.exists(temp_file):
                    continue
                    
                segment_audio = AudioSegment.from_wav(temp_file)
                
                if combined_audio is None:
                    combined_audio = segment_audio
                else:
                    combined_audio = combined_audio + AudioSegment.silent(duration=500) + segment_audio

            if combined_audio:
                combined_audio.export(output_file, format="wav")
                
                for temp_file in temp_files:
                    try:
                        os.remove(temp_file)
                    except:
                        pass
                        
                try:
                    os.rmdir('temp')
                except:
                    pass
                
                return True, output_file, "Conversation generated successfully"
            else:
                return False, None, "Failed to combine audio segments"
                
        except Exception as e:
            return False, None, f"An error occurred: {str(e)}"

# For testing
if __name__ == "__main__":
    converter = TextToSpeechConverter()
    test_text = """This is a test of the conversational podcast system. 
    It will convert this content into a dialogue between two hosts."""
    
    success, result, message = converter.create_conversation_audio(
        test_text,
        output_file="test_conversation.wav"
    )
    print(f"Success: {success}")
    print(f"Result: {result}")
    print(f"Message: {message}")