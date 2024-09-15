-- Create the users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    country TEXT NOT NULL,
    password TEXT NOT NULL
);

-- Create the campaign table
CREATE TABLE campaign (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    purpose TEXT,
    user_prompt TEXT,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Create the post table
CREATE TABLE post (
    id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    target_platform TEXT NOT NULL,
    text_content TEXT NOT NULL,
    campaign_id INTEGER,
    media_id INTEGER,
    FOREIGN KEY(media_id) REFERENCES media_content(id),
    FOREIGN KEY(campaign_id) REFERENCES campaign(id)
);

-- Create the media_content table
CREATE TABLE media_content (
    id INTEGER PRIMARY KEY,
    key TEXT NOT NULL,
    description TEXT,
    post_id INTEGER,
    campaign_id INTEGER,
    FOREIGN KEY(post_id) REFERENCES post(id),
    FOREIGN KEY(campaign_id) REFERENCES campaign(id)
);

-- Create the indexes
CREATE INDEX post_media_content_index ON media_content (post_id, campaign_id);
CREATE INDEX campaign_post_index ON post (campaign_id);
