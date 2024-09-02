def dsToText(datestamp: str):
    spl = datestamp.split("+")[0].split("T")
    date = spl[0]
    time = spl[1]
    date = date.split("-")
    months = {
        "01": "january",
        "02": "february",
        "03": "march",
        "04": "april",
        "05": "may",
        "06": "june",
        "07": 'july',
        '08': 'august',
        '09': 'september',
        '10': 'october',
        '11': 'november',
        '12': 'december'
    }
    s = months[date[1]] + " " + date[2] + " at "
    time = time.split(':')
    if time[0] == "00" and time[1] == "00":
        return s + "midnight"
    if time[0] == "12" and time[1] == "00":
        return s + "noon"
    pm = int(time[0]) >= 12
    time[0] = str(int(time[0])-12) if pm else time[0]
    t = f"{time[0]} {time[1]} {'P.M' if pm else 'A.M'}"
    return s + t
