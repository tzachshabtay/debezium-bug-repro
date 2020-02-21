# Minimal repro for possible bug in Debezium (skipping events)

This is a reproduction of a possible bug we're seeing in Debezium where it skips messages after restarting.

To reproduce:

1. docker-compose build
2. docker-compose up
3. Wait for our `BuggyConverter` to raise an exception and crash the connector/Debezium (the exception message should be: `crashing on purpose on id 5000`)
4. In a different tab kill the container: `docker container stop debezium-bug_connector_1`
5. Restart the container with `docker-compose up connector`
6. At this point the container should crash again. If the message is again `crashing on purpose on id 5000` it means that the bug was not reproduced yet (we didn't skip messages, we're on the same message which is what we want), and we need to restart the connector again (i.e repeat steps 4-5). If the exception message is `bug reproduced! we're on id x` the bug reproduced, we somehow got to a message id higher than 5000.