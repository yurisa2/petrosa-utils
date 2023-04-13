def convert_backtest_duration(duration):
    duration_split = duration.split(" ")

    total = int(int(duration_split[0]) * 24) + int(duration_split[2].split(":")[0]) + (
            int(duration_split[2].split(":")[1]) / 60) + (int(duration_split[2].split(":")[2]) / 3600)

    return total