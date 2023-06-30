import pickle

a = [1, 2, 3]
with open('1.pkl', 'rb') as f:
    b =  pickle.load(f)
print(b)