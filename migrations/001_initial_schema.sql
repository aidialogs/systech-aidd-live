-- Initial database schema for systech-aidd-live
-- Create messages table for storing conversation history

-- depends: 

-- Create messages table
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    chat_id BIGINT NOT NULL,
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create index for efficient queries by user_id and chat_id
CREATE INDEX IF NOT EXISTS idx_user_chat ON messages(user_id, chat_id);

-- Create index for ordering by creation time
CREATE INDEX IF NOT EXISTS idx_created_at ON messages(created_at);




