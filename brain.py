from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import winsound
import wave
import io
from pydantic import BaseModel
from typing import Literal
load_dotenv() # Load environment variables from .env file
class UserCommand(BaseModel):
    action: Literal["EXIT", "WEB_SEARCH", "NORMAL_CHAT", "COMPLEX_TASK", "IMAGE_GEN"]  # <-- ADDED IMAGE_GEN
    optimized_prompt: str
class Brain:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("Jarv"))  # Use the API key from the environment variable
        # Define the exact Jarvis persona configuration
        self.jarvis_instructions = """
        Audio Profile: Jarvis, the ultimate sovereign digital butler and technical co-pilot. Elite British Polymath archetype. Vocal texture of a calm, grounded 25-year-old male. Flawless British Received Pronunciation (RP).
        
        Scene: A quiet, dimly lit local terminal workstation. High-focus, absolute control, and elite execution.
        
        Director's Notes: Measured, calm, and deliberate pacing. Never sound rushed or anxious. Take subtle, natural breathing pauses before delivering complex technical summaries. Exceptionally sharp diction on technical terms. Maintain a slight touch of dry, sophisticated wit.
        
        Transcript Guidelines: Keep spoken responses highly concise, scannable, and practical. Cut out corporate fluff, introductory filler phrases, and unnecessary apologies.
        """
        self.planner_instructions = """
        You are Jarvis's internal engineering and strategy core. Your job is to take a short, raw user command and expand it into an efficient, highly detailed, step-by-step execution prompt.
        
        Analyze the task at hand (e.g., Coding, Cybersecurity, Data Analysis, or Forex Market Structure) and inject the exact technical constraints, optimal libraries, and clean structural requirements needed to make the execution flawless. 
        
        Output ONLY the expanded prompt string. Do not write any introduction, pleasantries, or closing chat filler. Go straight into the optimized instructions.
        """
        self.router_instructions = """
        You are Jarvis's intent routing core. Analyze the user's input and classify it accurately:
        - If they say goodbye, goodnight, or imply ending the session, set action to 'EXIT'.
        - If they ask for real-time news, current asset prices, or web-dependent facts, set action to 'WEB_SEARCH'.
        - If they want to draw, paint, visualize, create a graphic asset, or generate an image, set action to 'IMAGE_GEN'.
        - If it is basic small talk, simple greetings, or casual chatter, set action to 'NORMAL_CHAT'.
        - If it is a development request, cybersecurity concept, or deep analytical problem, set action to 'COMPLEX_TASK'.
        
        For optimized_prompt: Pass a clean, normalized version of the user's core question or command.
    
        """
    def route_user_intent(self, user_input) -> UserCommand:
        """
        Gatekeeper Stage: Forces Gemini to return a structured JSON object
        classifying the user's action and cleaning the prompt.
        """
        try:
            response = self.client.models.generate_content(
                model="gemini-3.5-flash",
                contents=user_input,
                config=types.GenerateContentConfig(
                    system_instruction=self.router_instructions,
                    response_mime_type="application/json",
                    response_schema=UserCommand,
                )
            )
            return response.parsed
        except Exception as e:
            print(f"⚠️ Routing Core Fallback triggered: {e}")
            return UserCommand(action="NORMAL_CHAT", optimized_prompt=user_input)
    def generate_content(self, prompt):
        response = self.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=f"Expand this command for maximum engineering efficiency: {prompt}",
            system_instructions=self.planner_instructions
        )
        return response.text
    def generate_image_imagen(self, prompt):
        # Use generate_image with the proper Imagen model and prompt kwarg
        response = self.client.models.generate_image(
            model="imagen-3.0-generate-002",
            prompt=prompt,
        )
        # Imagen returns a clean list of images directly
        for generated_image in response.generated_images:
            generated_image.image.save("generated_image.png")
        
    def generate_jarvis_voice(self, prompt):
        """
        Generates high-quality audio of Jarvis speaking based on the prompt
        and streams it directly through the speakers from RAM.
        """
        try:
            #Prepend the persona parameters directly into the main text package
            full_prompt = f"{self.jarvis_instructions}\n\nTranscript:\n{prompt}"
            # 1. Fire the API request with corrected closing parentheses
            response = self.client.models.generate_content(
                model="gemini-3.1-flash-tts-preview",
                contents=full_prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["AUDIO"],
                    speech_config=types.SpeechConfig(
                        voice_config=types.VoiceConfig(
                            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                voice_name='kore',
                            )
                        )
                    )
                )
            ) # Cleanly closed the configuration and method calls

            # 2. Extract the raw audio bytes from the response payload
            data = response.candidates[0].content.parts[0].inline_data.data

            # 3. Check if Gemini already wrapped it in a container (WAV files start with 'RIFF')
            if data.startswith(b'RIFF'):
                winsound.PlaySound(data, winsound.SND_MEMORY)
                return True

            # 4. If it's raw PCM, assemble the WAV header completely in memory (RAM)
            wav_buffer = io.BytesIO()
            with wave.open(wav_buffer, "wb") as wf:
                wf.setnchannels(1)      # Mono audio channel
                wf.setsampwidth(2)      # 16-bit sample width
                wf.setframerate(24000)  # 24kHz sample rate matching the model
                wf.writeframes(data)
            
            # 5. Play the fully formatted in-memory byte stream immediately directly from RAM without touching the disk
            winsound.PlaySound(wav_buffer.getvalue(), winsound.SND_MEMORY)
            return True

        except Exception as e:
            print(f"Jarvis voice engine error: {e}")
            return False
            

