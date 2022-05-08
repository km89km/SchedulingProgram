import pickle

with open('current_staff', 'rb') as f:
    current_staff = pickle.load(f)

for col in current_staff.colleagues:
    if col.prev_wknd is False:
        print(col.name())
