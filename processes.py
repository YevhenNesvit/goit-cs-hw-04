import os
import multiprocessing
import time

def process_files_process(file_paths, keywords, results):
    process_results = {}
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            text = file.read()
            for keyword in keywords:
                if keyword in text:
                    if keyword not in process_results:
                        process_results[keyword] = []
                    process_results[keyword].append(file_path)
    results.put(process_results)

def parallel_file_processing_process(file_paths, keywords, num_processes):
    results = multiprocessing.Queue()
    processes = []

    # Split file paths among processes
    chunk_size = len(file_paths) // num_processes
    for i in range(num_processes):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i < num_processes - 1 else len(file_paths)
        process = multiprocessing.Process(target=process_files_process, args=(file_paths[start:end], keywords, results))
        processes.append(process)
        process.start()

    # Wait for all processes to finish
    for process in processes:
        process.join()

    # Merge results from all processes
    final_results = {}
    while not results.empty():
        process_result = results.get()
        for keyword, file_list in process_result.items():
            if keyword not in final_results:
                final_results[keyword] = []
            final_results[keyword].extend(file_list)

    return final_results

# Example usage
def main():
    file_paths = ['../goit-cs-hw-01/task-2.py', '../goit-cs-hw-02/task-2/main.py', '../goit-cs-hw-03/task-1/seed.py', '../goit-cs-hw-03/task-2/cats.py']  # List of file paths
    keywords = ['import', 'from']  # List of keywords to search for
    num_processes = 4  # Number of processes to use

    start_time = time.time()
    results = parallel_file_processing_process(file_paths, keywords, num_processes)
    end_time = time.time()

    print("Results:", results)
    print("Execution time:", end_time - start_time, "seconds")

if __name__ == "__main__":
    main()
