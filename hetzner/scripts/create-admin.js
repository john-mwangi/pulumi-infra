db = db.getSiblingDB("admin");

db.createUser(
    {
        user: "root",
        pwd: "mongo_hetzner",
        roles: [
            // { role: "userAdminAnyDatabase", db: "admin" },
            // { role: "readWriteAnyDatabase", db: "admin" },
            { role: "root", db: "admin" }
        ]
    }
)
