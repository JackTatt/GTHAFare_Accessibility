import acc
from multiprocessing import Pool

# python3 accessibility/compute_transit_accessibility.py

# simple runs
# acc.levelofservice("District of Columbia", "2020-06-21")
# acc.levelofservice("San Francisco-Oakland", "2021-01-17")
# acc.transit_accessibility("Philadelphia", "2021-02-14", "MP")
# acc.transit_accessibility("Philadelphia", "2021-02-14", "PM")
# acc.transit_accessibility("Philadelphia", "2021-02-14", "WE")

# def compute_accessibility(date):
#     print(region, date)
#     acc.transit_accessibility(region, date, "MP")
#     acc.transit_accessibility(region, date, "PM")
#     acc.transit_accessibility(region, date, "WE")
#
# def compute_tlos(date):
#     print(region, date)
#     acc.levelofservice(region,date)
#
# def compute_both(date):
#     print(region, date)
#     compute_accessibility(date)
#     compute_tlos(date)
#
# if __name__ == '__main__':
#     with Pool(13) as p:
#         # pick either access, tlos, or both
#         p.map(compute_tlos, dates)
