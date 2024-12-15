-- Table 1: Channels
CREATE TABLE channels (
    channel_id VARCHAR(50) PRIMARY KEY,
    channel_name VARCHAR(255) NOT NULL,
    retrieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: Videos
CREATE TABLE videos (
    video_id VARCHAR(50) PRIMARY KEY,
    channel_id VARCHAR(50),
    title VARCHAR(255) NOT NULL,
    published_at DATETIME NOT NULL,
    views INT DEFAULT 0,
    likes INT DEFAULT 0,
    dislikes INT DEFAULT 0,
    comments_count INT DEFAULT 0,
    rating FLOAT DEFAULT 0.0,
    video_link VARCHAR(255) UNIQUE,
    FOREIGN KEY (channel_id) REFERENCES channels(channel_id)
);

-- Table 3: Comments
CREATE TABLE comments (
    comment_id INT AUTO_INCREMENT PRIMARY KEY,
    video_id VARCHAR(50),
    text TEXT NOT NULL,
    sentiment_score FLOAT DEFAULT 0.0,
    sentiment_label ENUM('Positive', 'Neutral', 'Negative') DEFAULT 'Neutral',
    FOREIGN KEY (video_id) REFERENCES videos(video_id)
);

-- Table 4: Video Sentiments
CREATE TABLE video_sentiments (
    video_id VARCHAR(50) PRIMARY KEY,
    average_sentiment FLOAT DEFAULT 0.0,
    sentiment_label ENUM('Positive', 'Neutral', 'Negative') DEFAULT 'Neutral',
    FOREIGN KEY (video_id) REFERENCES videos(video_id)
);
