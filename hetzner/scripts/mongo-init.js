db = db.getSiblingDB('admin');

db.createUser({
  user: process.env.MONGO_INITDB_ROOT_USERNAME,
  pwd: process.env.MONGO_INITDB_ROOT_PASSWORD,
  roles: [
    { role: 'root', db: 'admin' }
  ]
});

db = db.getSiblingDB('llm_browser');
db.createCollection("prompts");
db.createCollection("results");
db.createCollection("resumes");
db.createCollection("weekly_context");
db.createCollection("monthly_context");
