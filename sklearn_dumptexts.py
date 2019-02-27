
from sklearn.datasets import fetch_20newsgroups

if __name__ == '__main__':

    useN = None
    nd = fetch_20newsgroups(shuffle=True, random_state=0)
    texts, fnames =  nd['data'][:useN], nd['filenames'][:useN]

    for fn,t in zip(fnames,texts):
        with open('tmp/'+fn.split('/')[-1]+'.txt', 'w') as f:
            f.write(t)


