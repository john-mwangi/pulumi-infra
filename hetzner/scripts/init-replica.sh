#!/bin/bash

# Start MongoDB in the background WITHOUT authentication first
mongod --config /etc/mongod.conf --noauth &
MONGOD_PID=$!

# Wait for MongoDB to start
echo "Waiting for MongoDB to start..."
sleep 10

# Check if this is the first run (no admin user exists)
user_exists=$(mongosh admin --eval "db.getUser('$MONGO_INITDB_ROOT_USERNAME')" --quiet 2>/dev/null | grep -c "null")

if [ "$user_exists" -eq "1" ] || [ -z "$user_exists" ]; then
  echo "First run detected - creating admin user and databases..."
  
  # Run the mongo-init.js script
  mongosh < /docker-entrypoint-initdb.d/mongo-init.js
  
  echo "Databases and users created"
fi

# Now restart MongoDB with authentication
echo "Restarting MongoDB with authentication..."
mongod --shutdown
wait $MONGOD_PID

mongod --config /etc/mongod.conf &
MONGOD_PID=$!

echo "Waiting for MongoDB to restart..."
sleep 10

# Check if replica set is already initialized
rs_status=$(mongosh -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" --authenticationDatabase admin --eval "rs.status().ok" --quiet 2>/dev/null || echo "0")

if [ "$rs_status" != "1" ]; then
  echo "Initiating replica set..."
  mongosh -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" --authenticationDatabase admin --eval "rs.initiate({ _id: 'rs0', members: [{ _id: 0, host: '$MONGO_RS_HOST' }]})"
else
  echo "Replica set already initiated"
fi

# Keep the container running
wait $MONGOD_PID