#!/usr/bin/python

import argparse
import random

_mrpt_num_trials = 5 # number of bases to test

def is_probable_prime(n):
    """
    Miller-Rabin primality test.
 
    A return value of False means n is certainly not prime. A return value of
    True means n is very likely a prime.
 
    >>> is_probable_prime(1)
    Traceback (most recent call last):
        ...
    AssertionError
    >>> is_probable_prime(2)
    True
    >>> is_probable_prime(3)
    True
    >>> is_probable_prime(4)
    False
    >>> is_probable_prime(5)
    True
    >>> is_probable_prime(123456789)
    False
 
    >>> primes_under_1000 = [i for i in range(2, 1000) if is_probable_prime(i)]
    >>> len(primes_under_1000)
    168
    >>> primes_under_1000[-10:]
    [937, 941, 947, 953, 967, 971, 977, 983, 991, 997]
 
    >>> is_probable_prime(6438080068035544392301298549614926991513861075340134\
3291807343952413826484237063006136971539473913409092293733259038472039\
7133335969549256322620979036686633213903952966175107096769180017646161\
851573147596390153)
    True
 
    >>> is_probable_prime(7438080068035544392301298549614926991513861075340134\
3291807343952413826484237063006136971539473913409092293733259038472039\
7133335969549256322620979036686633213903952966175107096769180017646161\
851573147596390153)
    False
    """
    assert n >= 2
    # special case 2
    if n == 2:
        return True
    # ensure n is odd
    if n % 2 == 0:
        return False
    # write n-1 as 2**s * d
    # repeatedly try to divide n-1 by 2
    s = 0
    d = n-1
    while True:
        quotient, remainder = divmod(d, 2)
        if remainder == 1:
            break
        s += 1
        d = quotient
    assert(2**s * d == n-1)
 
    # test the base a to see whether it is a witness for the compositeness of n
    def try_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in xrange(s):
            if pow(a, 2**i * d, n) == n-1:
                return False
        return True # n is definitely composite
 
    for i in xrange(_mrpt_num_trials):
        a = random.randrange(2, n)
        if try_composite(a):
            return False
 
    return True # no base tested showed n as composite

import string
digs = string.digits + string.letters

def int2base(x, base):
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[x % base])
        x /= base

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits)

def pp(args, p):
    if not args.count:
        print int2base(p, args.base)

def left(args, n, l):
    k = args.base ** l
    l += 1
    count = 0
    for i in xrange(1, args.base):
        t = n + i * k
        if is_probable_prime(t):
            pp(args, t)
            count += left(args, t, l) + 1
    return count

def right(args, n, l):
    n *= args.base
    count = 0
    for i in xrange(1, args.base):
        t = n + i
        if is_probable_prime(t):
            pp(args, t)
            count += right(args, t, None) + 1
    return count

def palindromic(args, n, l):
    k = args.base ** (2*l)
    n *= args.base
    l += 1
    count = 0
    for i in xrange(1, args.base):
        t = n + i * k + i
        if is_probable_prime(t):
            pp(args, t)
            count += palindromic(args, t, l) + 1
    return count

def run(args):
    count = 0
    for i in xrange(2, args.base):
        if not is_probable_prime(i):
            continue
        pp(args, i)
        count += args.type(args, i, 1) + 1
    if args.count:
        print count

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', type=int, default=10,help='base to generate in')
    parser.add_argument('--left', action='store_const', dest='type',
                        const=left, default=left, help='find left truncatable primes')
    parser.add_argument('--right', action='store_const', dest='type',
                        const=right, help='find right truncatable primes')
    parser.add_argument('--palindromic', action='store_const', dest='type',
                        const=palindromic, help='find palindromic truncatable primes')
    parser.add_argument('--count', action='store_true', help='count instead of listing')
    args = parser.parse_args()
    #print args

    run(args)
