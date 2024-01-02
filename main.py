import threading

def format_card_details(number, month, year, cvv):
    formatted_date = f"{month:02}{str(year)[-2:]}"  # Considering only the last two digits of the year
    formatted = f"{number}:{formatted_date}:{cvv}"
    return formatted

def process_card_details(line):
    parts = line.strip().split(',')
    if len(parts) == 5:
        name, number, month, year, cvv = parts
        formatted = format_card_details(number, int(month), int(year), cvv)
        return formatted
    return None

def process_file():
    with open('input.txt', 'r') as input_file, open('output.txt', 'w') as output_file:
        for line in input_file:
            formatted = process_card_details(line)
            if formatted:
                output_file.write(f"{formatted}\n")

# Creating a thread for processing the file
thread = threading.Thread(target=process_file)

# Start the thread
thread.start()

# Wait for the thread to complete
thread.join()
