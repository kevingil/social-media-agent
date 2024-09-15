from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from PIL import Image
import base64
from const import ROOT_DIR


class Agent:
    def __init__(self, openai_api_key, anthropic_api_key):
        self.anthropic_api_key = anthropic_api_key
        self.openai_api_key = openai_api_key
        self.vision = ChatOpenAI(model_name="gpt-4o-mini", api_key=openai_api_key)
        self.llm = ChatAnthropic(
            model="claude-3-haiku-20240307", api_key=anthropic_api_key
        )

    def describe_image(self, image_key):
        # Load and encode the image
        with open(f"{ROOT_DIR}{image_key}", "rb") as image_file:
            image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", 
                     "text": "This image will be used in social media, describe the image for the social media manager."},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                    },
                ],
            }
        ]

        response = self.vision.invoke(messages)

        return response.content

    def generate_post_text(self, prompt, target_platform, media_description, purpose):

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a social media content creator AI agent. Your task is to generate a text post for {target_platform}.
                    The purpose of this social media campagin, is to {purpose}.
                    Use the described image to create a short and engagin social media post.
                    The user would also like you to: {prompt}.""",
                ),
                (
                    "human",
                    """
                    Image Description: {media_description}
                    Reply with only the short text post:
                    """,
                ),
            ]
        )
        post_text_chain = prompt | self.llm
        post_text = post_text_chain.invoke(
            {
                "target_platform": target_platform,
                "media_description": media_description,
                "purpose": purpose,
                "prompt": prompt,
            }
        )
        return post_text
