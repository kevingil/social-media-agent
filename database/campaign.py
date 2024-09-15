from sqlite3 import connect


class CampaignQueries:
    def __init__(self):
        self._connection = connect("./database.db")
        self._cursor = self._connection.cursor()

    def get_all(self):
        data = self._cursor.execute("SELECT * FROM campaign")
        columns = [column[0] for column in data.description]
        return [dict(zip(columns, row)) for row in data.fetchall()]

    def get_campaign(self, id):
        campaign = self._cursor.execute(f"SELECT * FROM campaign WHERE id = {id}")
        columns = [column[0] for column in campaign.description]
        return dict(zip(columns, campaign.fetchone()))

    def create_campaign(self, campaign):
        self._cursor.execute(
            f"""INSERT INTO campaign (title, start_date, end_date, purpose, user_id)
                VALUES('{campaign['title']}', '{campaign['start_date']}', '{campaign['end_date']}', '{campaign['purpose']}', {campaign['user_id']})
            """
        )
        self._connection.commit()

    def update_campaign_purpose(self, id, campaign):
        self._cursor.execute(
            f"""UPDATE campaign SET title = '{campaign['title']}', start_date = '{campaign['start_date']}', end_date = '{campaign['end_date']}', purpose = '{campaign['purpose']}', user_id = {campaign['user_id']}
                WHERE id = {id}
            """
        )
        self._connection.commit()

    def update_campaign(self, id, campaign):
        self._cursor.execute(
            f"""UPDATE campaign SET title = '{campaign['title']}', start_date = '{campaign['start_date']}', end_date = '{campaign['end_date']}', purpose = '{campaign['purpose']}', user_prompt = '{campaign['user_prompt']}', user_id = {campaign['user_id']}
                WHERE id = {id}
            """
        )
        self._connection.commit()

    def delete_campaign(self, id):
        self._cursor.execute(f"DELETE FROM campaign WHERE id = {id}")
        self._connection.commit()

    def get_all_by_user(self, user_id):
        data = self._cursor.execute(f"SELECT * FROM campaign WHERE user_id = {user_id}")
        columns = [column[0] for column in data.description]
        return [dict(zip(columns, row)) for row in data.fetchall()]

    def get_last_insert_id(self):
        return self._cursor.lastrowid

    def __del__(self):
        self._connection.close()


class PostQueries:
    def __init__(self):
        self._connection = connect("./database.db")
        self._cursor = self._connection.cursor()

    def get_all(self):
        data = self._cursor.execute("SELECT * FROM post")
        columns = [column[0] for column in data.description]
        return [dict(zip(columns, row)) for row in data.fetchall()]

    def get_post(self, id):
        post = self._cursor.execute(f"SELECT * FROM post WHERE id = {id}")
        columns = [column[0] for column in post.description]
        return [dict(zip(columns, row)) for row in post.fetchall()]

    def create_post(self, post):
        self._cursor.execute(
            """INSERT INTO post (date, target_platform, text_content, media_id, campaign_id)
               VALUES (?, ?, ?, ?, ?)""",
            (post['date'], post['target_platform'], post['text_content'], post['media_id'], post['campaign_id'])
        )
        self._connection.commit()

    def update_post(self, id, post):
        self._cursor.execute(
            f"""UPDATE post SET date = '{post['date']}', target_platform = '{post['target_platform']}', text_content = '{post['text_content']}', media_id = '{post['media_id']}', campaign_id = {post['campaign_id']}
                WHERE id = {id}
            """
        )
        self._connection.commit()

    def delete_post(self, id):
        self._cursor.execute(f"DELETE FROM post WHERE id = {id}")
        self._connection.commit()

    def get_all_by_campaign(self, campaign_id):
        data = self._cursor.execute(
            f"""SELECT post.*, media_content.key AS media_key
                FROM post 
                JOIN media_content ON post.media_id = media_content.id
                WHERE post.campaign_id = {campaign_id}"""
        )
        columns = [column[0] for column in data.description]
        return [dict(zip(columns, row)) for row in data.fetchall()]

    def __del__(self):
        self._connection.close()


class MediaQueries:
    def __init__(self):
        self._connection = connect("./database.db")
        self._cursor = self._connection.cursor()

    def get_all(self):
        data = self._cursor.execute("SELECT * FROM media_content")
        columns = [column[0] for column in data.description]
        return [dict(zip(columns, row)) for row in data.fetchall()]

    def get_media(self, id):
        media = self._cursor.execute(f"SELECT * FROM media_content WHERE id = {id}")
        columns = [column[0] for column in media.description]
        return [dict(zip(columns, row)) for row in media.fetchall()]

    def create_media(self, media):
        self._cursor.execute(
            f"""INSERT INTO media_content (key, description, campaign_id)
                VALUES('{media['key']}', '{media['description']}', {media['campaign_id']})
            """
        )
        self._connection.commit()

    def update_media(self, id, media):
        self._cursor.execute(
            f"""UPDATE media_content SET key = '{media['key']}', description = '{media['description']}', post_id = {media['post_id']}, campaign_id = {media['campaign_id']}
                WHERE id = {id}
            """
        )
        self._connection.commit()

    def delete_media(self, id):
        self._cursor.execute(f"DELETE FROM media_content WHERE id = {id}")
        self._connection.commit()

    def get_all_by_post(self, post_id):
        data = self._cursor.execute(
            f"SELECT * FROM media_content WHERE post_id = {post_id}"
        )
        columns = [column[0] for column in data.description]
        return [dict(zip(columns, row)) for row in data.fetchall()]

    def get_all_by_campaign(self, campaign_id):
        data = self._cursor.execute(
            f"SELECT * FROM media_content WHERE campaign_id = {campaign_id}"
        )
        columns = [column[0] for column in data.description]
        return [dict(zip(columns, row)) for row in data.fetchall()]

    def __del__(self):
        self._connection.close()
