import threading
import time


def process_files_thread(file_paths, keywords, results, lock):
    thread_results = {}
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as file:
                text = file.read()
                for keyword in keywords:
                    if keyword in text:
                        if keyword not in thread_results:
                            thread_results[keyword] = []
                        thread_results[keyword].append(file_path)
        except FileNotFoundError:
            print(f"File {file_path} not found")
    with lock:
        results.append(thread_results)


def parallel_file_processing_thread(file_paths, keywords, num_threads):
    results = []
    threads = []
    lock = threading.RLock()

    # Split file paths among threads
    chunk_size = len(file_paths) // num_threads
    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_threads - 1 else len(file_paths)
        thread = threading.Thread(target=process_files_thread,
                                  args=(file_paths[start:end], keywords, results, lock))
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Merge results from all threads
    final_results = {}
    for thread_result in results:
        for keyword, file_list in thread_result.items():
            if keyword not in final_results:
                final_results[keyword] = []
            final_results[keyword].extend(file_list)

    return final_results


# Example usage
def main():
    file_paths = ['../goit-cs-hw-01/task-2.py', '../goit-cs-hw-02/task-2/main.py',
                  '../goit-cs-hw-03/task-1/seed.py', '../goit-cs-hw-03/task-2/cats.py']  # List of file paths
    keywords = ['import', 'from']  # List of keywords to search for
    num_threads = 4  # Number of threads to use

    start_time = time.time()
    results = parallel_file_processing_thread(file_paths, keywords, num_threads)
    end_time = time.time()

    print("Results:", results)
    print("Execution time:", end_time - start_time, "seconds")


if __name__ == "__main__":
    main()
