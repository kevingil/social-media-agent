from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from const import GROQ_API_KEY


class WrittingAgent:
    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant", api_key=GROQ_API_KEY
        )
        
    def generate_draft(self, campaign, media_description):
        
        
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a social media AI agent. Your task is to generate a short text post for {target_platforms} as part of a campaign titled "{title}". 
                    The target audience for this campaign is {target_audience}, and the key objectives are {objectives}.
                    We are marketing {brand_name}. Use the described image to create an engaging and concise post that highlights the key messages: {key_messages}, and include relevant hashtags: {hashtags}. Additional context: {user_prompt}.
                    Please reply with only the short text post, avoiding the use of banned words: elevate, transform.
                    Reply with only the short text post. Do not used banned words. <banned-words>elevate, transform</banned-words>.
                    """,
                ),
                (
                    "human",
                    """
                    Image Description: {media_description}
                    """,
                )
            ]
        )
        post_text_chain = prompt | self.llm
        draft = post_text_chain.invoke(
            {
                "target_platform": campaign['target_platforms'],
                "media_description": media_description,
                "title": campaign['title'],
                "user_prompt": campaign['user_prompt'],
                "target_audience": campaign['target_audience'],
                "objectives": campaign['objectives'],
                "key_messages": campaign['key_messages'],
                "hashtags": campaign['hashtags'],
                "brand_name": campaign['brand_name'], 
                "target_platforms": campaign['target_platforms']
            }
        )
        
        
        return draft
    
    def review_draft(self, campaign, draft):
        review_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a social media expert. Please review the following draft for clarity, engagement, and adherence to campaign objectives. 
                    Provide constructive feedback and suggest improvements.
                    """,
                ),
                (
                    "human",
                    """Draft: {draft}
                    Campaign Title: {title}
                    Target Audience: {target_audience}
                    Key Messages: {key_messages}
                    """,
                )
            ]
        )
        critique_chain = review_prompt | self.llm
        critique = critique_chain.invoke(
            {
                "draft": draft,
                "title": campaign['title'],
                "target_audience": campaign['target_audience'],
                "key_messages": campaign['key_messages'],
            }
        )
        return critique
    
    def final_draft(self, campaign, critique, draft):
        finalize_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a social media AI agent. Review and finalize the following draft by making it more engaging and ensuring it fits the campaign's tone and style.
                    Use the reviewer's critique as a guide to improve the draft. This is a final draft,  response with the final post.
                    """,
                ),
                (
                    "human",
                    """Draft: {draft}
                    Campaign Title: {title}
                    Reviewer's critique: {critique}
                    """,
                )
            ]
        )
        finalize_chain = finalize_prompt | self.llm
        post = finalize_chain.invoke(
            {
                "draft": draft,
                "title": campaign['title'],
                "critique": critique,
            }
        )
        return post
    
    def finalize_post(self, draft):
        finalize_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You're a text processor that will extract the final draft and clean it up for social media.
                    You need to remove the markdown formatting and any other extraneous text from the draft.
                    """,
                ),
                (
                    "human",
                    """Draft: {draft}
                    """,
                )
            ]
        )
        finalize_chain = finalize_prompt | self.llm
        post = finalize_chain.invoke(
            {
                "draft": draft
            }
        )
        return post

    def generate_post(self, campaign, media_description):
        draft = self.generate_draft(campaign, media_description)
        print("\n\nDraft: ", draft)
        critique = self.review_draft(campaign, draft)
        print("\n\nCritique: ", critique)
        final_draft = self.final_draft(campaign, critique, draft)
        print("\n\nFinal Draft: ", final_draft)
        output = self.finalize_post(final_draft)
        print("\n\nFinal Output: ", output)
        return output

