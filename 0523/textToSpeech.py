#!/usr/bin/env python

# Copyright 2018 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Text-To-Speech API sample application .
Example usage:
    python quickstart.py
"""

from google.cloud import texttospeech
import os
def answer(txt):
    # [START tts_quickstart]
    """Synthesizes speech from the input string of text or ssml.
        Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/
    """
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.types.SynthesisInput(text=txt)

    voice = texttospeech.types.VoiceSelectionParams(
    language_code='ko-KR',  #Korean: ko-KR , 'en-US'
    ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)

    # Select the type of audio file you want returned
    audio_config = texttospeech.types.AudioConfig(
    audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    # The response's audio_content is binary.
    with open('output.mp3', 'wb') as out:
        # Write the response to the output file.
        out.write(response.audio_content)    
    os.system('mpg123 output.mp3')
    # [END tts_quickstart]

if __name__ == '__main__':
    txt='컴 공 최은강 취뽀하자'
    answer(txt)#playing tts with txt
