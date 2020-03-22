import csv

def save_to_file(comm_info):
    file = open("comm.csv",mode="a+", newline='', encoding="euc-kr")
    writer = csv.writer(file)
    # writer.writerow(['title','score','genre','comment'])
    for comm in comm_info:
        writer.writerow(list(comm.values()))
    return
