from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from PIL import Image
import os
from const import ROOT_DIR


class Agent:
    def __init__(self, openai_api_key, anthropic_api_key):
        self.anthropic_api_key = anthropic_api_key
        self.openai_api_key = openai_api_key
        self.vision = ChatOpenAI(model_name="gpt-4o", api_key=openai_api_key)
        self.llm = ChatAnthropic(
            model="claude-3-5-sonnet-20240620", api_key=anthropic_api_key
        )

    def describe_image(self, image_key):
        print(ROOT_DIR)
        img = Image.open(f"{ROOT_DIR}{image_key}")
        description = self.vision(f"Describe this image: {img}")
        return description

    def generate_post_text(self, prompt, target_platform, media_description, purpose):
        template = """
        

        """
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a social media content creator. Your task is to generate a post text for a given platform, media description, and purpose.",
                ),
                (
                    "human",
                    """
                    Platform: {target_platform}
                    Media Description: {media_description}
                    Purpose: {purpose}
                    Prompt: {prompt}

                    Post Text:
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
