db = db.getSiblingDB('llm_browser');
db.createCollection("prompts");
db.createCollection("results");