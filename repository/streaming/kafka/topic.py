import time
from confluent_kafka.admin import AdminClient, NewTopic, KafkaException

def wait_for_topic_deletion(admin_client, topic_name, timeout=60):
    """Waits for the topic to be fully deleted."""
    end_time = time.time() + timeout
    while time.time() < end_time:
        topics = admin_client.list_topics(timeout=10).topics
        if topic_name not in topics:
            print(f"Topic '{topic_name}' has been deleted.")
            return True
        print(f"Waiting for topic '{topic_name}' to be deleted...")
        time.sleep(5)  # Wait for 5 seconds before checking again
    print(f"Timed out waiting for topic '{topic_name}' to be deleted.")
    return False

def create_kafka_topic(admin_client, topic_name, num_partitions=1, replication_factor=1):
    """Creates a Kafka topic."""
    new_topic = NewTopic(topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
    try:
        create_result = admin_client.create_topics([new_topic])
        for topic, future in create_result.items():
            try:
                future.result()  # Block until topic creation is complete
                print(f"Topic '{topic}' created successfully.")
            except Exception as e:
                print(f"Failed to create topic '{topic}': {e}")
    except KafkaException as e:
        print(f"Kafka exception occurred: {e}")

def delete_kafka_topic(admin_client, topic_name):
    """Deletes a Kafka topic."""
    delete_result = admin_client.delete_topics([topic_name])
    for topic, future in delete_result.items():
        try:
            future.result()  # Block until topic deletion is complete
            print(f"Topic '{topic}' is marked for deletion.")
        except Exception as e:
            print(f"Failed to delete topic '{topic}': {e}")
            
def create_topic(topic_name):
    admin_client = AdminClient({
        'bootstrap.servers': 'localhost:9092'
    })

    # Step 1: Delete the topic (if it exists and is not already deleted)
    print(f"Attempting to delete topic '{topic_name}' if it exists...")
    delete_kafka_topic(admin_client, topic_name)

    # Step 2: Wait for the topic deletion to complete
    if wait_for_topic_deletion(admin_client, topic_name, timeout=60):
        # Step 3: Recreate the topic after deletion
        print(f"Recreating topic '{topic_name}'...")
        create_kafka_topic(admin_client, topic_name)
    else:
        print(f"Failed to delete topic '{topic_name}' within the timeout period.")