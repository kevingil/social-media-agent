from database.campaign import CampaignQueries, MediaQueries, PostQueries

class Campaign:
    def __init__(self, campaign_data):
        self.db = CampaignQueries()
        self.campaign_data = campaign_data

    def create_campaign(self):
        self.db.create_campaign(self.campaign_data)

    def get_campaign(self, id):
        return self.db.get_campaign(id)
    
    def update_campaign(self, id):
        self.db.update_campaign(id, self.campaign_data)

    def update_campaign_purpose(self, id):
        self.db.update_campaign_purpose(id, self.campaign_data)

    def delete_campaign(self, id):
        self.db.delete_campaign(id)

    def get_all_by_user(self, user_id):
        return self.db.get_all_by_user(user_id)

class Post:
    def __init__(self, post_data):
        self.db = PostQueries()
        self.post_data = post_data

    def create_post(self):
        self.db.create_post(self.post_data)

    def get_post(self, id):
        return self.db.get_post(id)

    def update_post(self, id):
        self.db.update_post(id, self.post_data)

    def delete_post(self, id):
        self.db.delete_post(id)

    def get_all_by_campaign(self, campaign_id):
        return self.db.get_all_by_campaign(campaign_id)

class Media:
    def __init__(self, media_data):
        self.db = MediaQueries()
        self.media_data = media_data

    def create_media(self):
        self.db.create_media(self.media_data)

    def get_media(self, id):
        return self.db.get_media(id)

    def update_media(self, id):
        self.db.update_media(id, self.media_data)

    def delete_media(self, id):
        self.db.delete_media(id)

    def get_all_by_post(self, post_id):
        return self.db.get_all_by_post(post_id)

    def get_all_by_campaign(self, campaign_id):
        return self.db.get_all_by_campaign(campaign_id)
