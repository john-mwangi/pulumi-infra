db = db.getSiblingDB('llm_browser');
db.createCollection("prompts");
db.createCollection("results");
db.createCollection("resumes");
db.createCollection("weekly_context");
db.createCollection("monthly_context");
