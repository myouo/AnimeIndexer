-- Core anime table
CREATE TABLE IF NOT EXISTS anime (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  title_original TEXT,
  author TEXT,
  description TEXT,
  score REAL,
  cover_url TEXT,
  air_date TEXT,
  updated_at TEXT
);

-- Tags (many-to-many)
CREATE TABLE IF NOT EXISTS tag (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS anime_tag (
  anime_id INTEGER NOT NULL,
  tag_id INTEGER NOT NULL,
  PRIMARY KEY (anime_id, tag_id),
  FOREIGN KEY (anime_id) REFERENCES anime(id) ON DELETE CASCADE,
  FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_anime_score ON anime(score);
CREATE INDEX IF NOT EXISTS idx_tag_name ON tag(name);
CREATE INDEX IF NOT EXISTS idx_anime_tag_tag ON anime_tag(tag_id);
