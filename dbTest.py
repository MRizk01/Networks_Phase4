from db import DB  # Assuming your database class is named DB
import threading
import time
import matplotlib.pyplot as plt

# Lock for thread-safe printing
print_lock = threading.Lock()

def join_chatroom_performance_test(db, num_users, roomname):
    x = []
    y = []

    for i in range(1, num_users + 1):
        threads = []

        for _ in range(i):
            t = threading.Thread(target=db.join_room, args=(roomname, f"User{_}"))
            threads.append(t)

        start_time = time.time()

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        end_time = time.time()
        elapsed_time = (end_time - start_time )

        with print_lock:
            print(f"Elapsed time for {i} users joining the chatroom: {elapsed_time:.4f} milliseconds")

        x.append(i)
        y.append(elapsed_time)

    # Plot the performance graph
    plt.plot(x, y, marker='o', linestyle='-', color='b')
    plt.title('Join Chatroom Performance')
    plt.xlabel('Number of Users Joining')
    plt.ylabel('Elapsed Time')
    plt.show()

if __name__ == "__main__":
    # Adjust these parameters as needed
    num_users_to_test = 100
    chatroom_name = "r1"

    # Initialize your database object
    db = DB()

    # Run the performance test
    join_chatroom_performance_test(db, num_users_to_test, chatroom_name)
