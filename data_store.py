import time

# global list to hold past weather data
history=[]

def save_data(data):
    # save the new data
    history.append(data)

    # remove old data older than 24 hours
    cutoff = time.time() - (24 * 3600)
    history[:] = [entry for entry in history if entry["timestamp"] >= cutoff]

def get_past_data(hours):
    cutoff = time.time() - (hours * 3600)
    return [entry for entry in history if entry["timestamp"] >= cutoff]