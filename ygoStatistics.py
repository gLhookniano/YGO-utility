#!/usr/bin/python
#coding:utf-8

"""
详细见:
https://ygobbs.com/t/lexusl%E4%B8%8E%E6%B8%B8%E6%88%8F%E7%8E%8B%EF%BC%881%EF%BC%89%EF%BC%9A%E5%8D%A1%E7%BB%84%E6%9E%84%E5%BB%BA%E7%9A%84%E6%A6%82%E7%8E%87%E5%AD%A6/102771

总数（Population Size）(N)：卡组数量

成功数（Number of successes in population）(K)：卡组里同名卡a的数量

样本大小（Sample Size）(n)：抽卡数量

样本成功数（Number of successes in sample）(k)：手卡里希望抽到多少张a
"""



import re


def parse_ydk(file_ydk):
    """ 
    Read .ydk file, to get deck list

    Return:
        dict : key is card number in ygopro, value is the present in this .ydk file. (the number in the deck)
    """
    d_card_num={}
    card_num=0
    with open(file_ydk, 'r') as fp:
        l=fp.readlines()
        l.sort()
        for i in l:
            j=re.search(r'[0-9]*', i).group()
            if not j:
                continue
            if j != card_num:
                d_card_num[j]=1
                card_num=j
            elif j==card_num:
                d_card_num[j]+=1
    return d_card_num

def combine(a, b):
    """
    calculate the combine of (a, b).
    """
    ai = 1
    for i in list(range(a+1))[1:]:
        ai *= i
    
    bi = 1
    for i in list(range(b+1))[1:]:
        bi *= i
    
    ambi = 1
    for i in list(range(a-b+1))[1:]:
        ambi *= i

    return ai/(bi*ambi)

def statistics(N=40, n=5, K=3, k=1):
    """
    Calculate the statistics of first draw card from whole deck, and can draw in the card (place 3, first draw 1).

    Args:
        N (int) : The total number of deck.
        n (int) : The first draw number.
        K (int) : Total card number in deck that want to first draw in.
        k (int) : Want first draw in number.

    Returns:
        float : The statistics of first draw in that card.
    """

    cmb_Kk = combine(K, k)
    cmb_Nkmnk = combine(N-K, n-k)
    cmb_Nn = combine(N, n)
    return cmb_Kk*cmb_Nkmnk/cmb_Nn

def deck_statistics(d_deck):
    """
    Calculate whole deck statistics, that is, each card statistics of first draw in.

    Args:
        d_deck (dict) : key is card name (OR card number), value is the number in the deck.

    Returns:
        dict : key is card name (OR card number), value is the statistics of this card thar first draw in the deck.
    """
    N = 40
    n = 5
    K = 3
    k = 1

    d = {}
    for i in d_deck:
        k = d_deck[i]
        d[i] = statistics(N,n,K,k)
    return d

if __name__ == "__main__":
    N = 40
    n = 5
    K = 3
    k = 1
    print(statistics(N,n,K,k))

    #d = parse_ydk('./a.ydk')
    #d2 = deck_statistics(d)
    #print(d2)
