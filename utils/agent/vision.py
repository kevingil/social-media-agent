from langchain_openai import ChatOpenAI 
import base64
from const import ROOT_DIR, OPENAI_API_KEY


class VisionAgent:
    def __init__(self):
        self.vision = ChatOpenAI(model_name="gpt-4o-mini", api_key=OPENAI_API_KEY)

    def describe_image(self, image_key):
        
        with open(f"{ROOT_DIR}{image_key}", "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
        
        IMAGE_DATA_URL = f"data:image/jpeg;base64,{image_base64}"
        

        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "This image will be used in social media, describe the image for the social media manager."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": IMAGE_DATA_URL,
                        }
                    }
                ]
            }
        ]

        response = self.vision.invoke(messages)

        return response.content

    