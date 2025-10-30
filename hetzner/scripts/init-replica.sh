#!/bin/bash

# Start MongoDB in the background
mongod --config /etc/mongod.conf &
MONGOD_PID=$!

# Wait for MongoDB to start
echo "Waiting for MongoDB to start..."
sleep 10

# Check if replica set is already initialized
rs_status=$(mongosh -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" --authenticationDatabase admin --eval "rs.status().ok" --quiet 2>/dev/null || echo "0")

if [ "$rs_status" != "1" ]; then
  echo "Initiating replica set..."
  mongosh -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" --authenticationDatabase admin --eval 'rs.initiate({ _id: "rs0", members: [{ _id: 0, host: "91.99.227.30:27017" }]})'
else
  echo "Replica set already initiated"
fi

# Keep the container running and forward signals
wait $MONGOD_PID