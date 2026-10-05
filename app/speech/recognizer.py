import speech_recognition as sr


class SpeechRecognizer:

    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        """
        Listen from microphone and return text.
        """

        try:

            with sr.Microphone() as source:

                print("🎤 Listening...")

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=1
                )

                audio = self.recognizer.listen(
                    source,
                    timeout=10,
                    phrase_time_limit=10
                )

            print("Recognizing...")

            text = self.recognizer.recognize_google(
                audio,
                language="en-US"
            )

            return {
                "success": True,
                "text": text,
                "error": None
            }

        except sr.WaitTimeoutError:

            return {
                "success": False,
                "text": "",
                "error": "Listening timed out."
            }

        except sr.UnknownValueError:

            return {
                "success": False,
                "text": "",
                "error": "Speech could not be understood."
            }

        except sr.RequestError as e:

            return {
                "success": False,
                "text": "",
                "error": str(e)
            }

        except Exception as e:

            return {
                "success": False,
                "text": "",
                "error": str(e)
            }