-- Create the users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    password TEXT NOT NULL
);


-- Create the product_brand table
CREATE TABLE product_brand (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL,
    description TEXT,
    industry TEXT,
    website_url TEXT,
    location TEXT,
    target_audience TEXT,
    mission_statement TEXT,
    unique_selling_proposition TEXT,
    competitors TEXT,
    product_categories TEXT,
    distribution_channels TEXT,
    key_values TEXT
);


-- Create the campaign table
CREATE TABLE campaign (
    id INTEGER PRIMARY KEY,
    product_brand_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    user_prompt TEXT,
    user_id INTEGER,
    objectives TEXT,
    target_platforms TEXT NOT NULL,
    target_audience TEXT,
    key_messages TEXT,
    hashtags TEXT,
    FOREIGN KEY (product_brand_id) REFERENCES product_brand(id)
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Create the post table
CREATE TABLE post (
    id INTEGER PRIMARY KEY,
    post_date DATE NOT NULL,
    target_platform TEXT NOT NULL,
    text_content TEXT NOT NULL,
    campaign_id INTEGER,
    FOREIGN KEY(campaign_id) REFERENCES campaign(id)
);

-- Create the media_content table
CREATE TABLE media_content (
    id INTEGER PRIMARY KEY,
    key TEXT NOT NULL,
    post_id INTEGER,
    campaign_id INTEGER,
    description TEXT,
    identified_brand TEXT,
    FOREIGN KEY(post_id) REFERENCES post(id),
    FOREIGN KEY(campaign_id) REFERENCES campaign(id)
);

-- Create indexes
CREATE INDEX idx_product_brand_name ON product_brand (name);
CREATE INDEX idx_campaign_product_brand ON campaign (product_brand_id);
CREATE INDEX idx_campaign_post_campaign ON post (campaign_id);
