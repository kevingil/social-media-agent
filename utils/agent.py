from langchain_openai import OpenAI
from langchain.prompts import StringPromptTemplate
from langchain import LLMChain
from PIL import Image
import os
from const import ROOT_DIR



class Agent:
    def __init__(self, api_key):
        self.llm = OpenAI(temperature=0, openai_api_key=api_key)

    def describe_image(self, image_key):
        print(ROOT_DIR)
        img = Image.open(f"{ROOT_DIR}{image_key}")
        description = self.llm(f"Describe this image: {img}")
        return description

    def generate_post_text(self, prompt, target_platform, media_description, purpose):
        template = """
        You are a social media content creator. Your task is to generate a post text for a given platform, media description, and purpose.

        Platform: {target_platform}
        Media Description: {media_description}
        Purpose: {purpose}
        Prompt: {prompt}

        Post Text:
        """
        prompt_template = StringPromptTemplate(input_variables=["target_platform", "media_description", "purpose", "prompt"], template=template)
        post_text_chain = LLMChain(llm=self.llm, prompt=prompt_template)
        post_text = post_text_chain.run(target_platform=target_platform, media_description=media_description, purpose=purpose, prompt=prompt)
        return post_text
