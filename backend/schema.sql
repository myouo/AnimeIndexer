CREATE TABLE IF NOT EXISTS anime (
  id INTEGER PRIMARY KEY,
  type INTEGER,
  name TEXT,
  name_cn TEXT,
  title TEXT NOT NULL,
  title_original TEXT,
  summary TEXT,
  score REAL,
  rank INTEGER,
  rating_total INTEGER,
  rating_count_total INTEGER,
  cover_url TEXT,
  date TEXT,
  platform TEXT,
  nsfw INTEGER,
  series INTEGER,
  locked INTEGER,
  eps INTEGER,
  total_episodes INTEGER,
  volumes INTEGER,
  images_json TEXT,
  infobox_json TEXT,
  meta_tags_json TEXT,
  rating_json TEXT,
  collection_json TEXT,
  raw_json TEXT,
  updated_at TEXT
);

CREATE TABLE IF NOT EXISTS tag (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS anime_tag (
  anime_id INTEGER NOT NULL,
  tag_id INTEGER NOT NULL,
  tag_count INTEGER,
  PRIMARY KEY (anime_id, tag_id),
  FOREIGN KEY (anime_id) REFERENCES anime(id) ON DELETE CASCADE,
  FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS sync_state (
  key TEXT PRIMARY KEY,
  value TEXT
);

CREATE INDEX IF NOT EXISTS idx_anime_score ON anime(score);
CREATE INDEX IF NOT EXISTS idx_anime_rank ON anime(rank);
CREATE INDEX IF NOT EXISTS idx_tag_name ON tag(name);
CREATE INDEX IF NOT EXISTS idx_anime_tag_tag ON anime_tag(tag_id);
