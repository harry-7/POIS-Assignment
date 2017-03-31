""" Contains Diffie Heilman code and tests on it"""
import random

from bsgs import hack
from util_functions import ipow


class DiffieHeilman:
    """ Class to deal with DiffieHeilman """

    def __init__(self, p, g):
        """
        Default Constructor
        :param p: prime used for cyclic group
        :param g: genertor of the group
        """
        self.p = p
        self.g = g
        self.__a = None

    def generate_key(self):
        """ Generates public key for the recipient"""
        if self.__a is None:
            a = random.randint(0, self.p - 1)
            self.__a = a
            # print "private-key", a
        key = ipow(self.g, self.__a, self.p)
        return key

    def caluclate_session_key(self, pk):
        return ipow(pk, self.__a, self.p)

    def enc_message(self, sk, m):
        return m ^ sk

    def dec_message(self, sk, c):
        return sk ^ c


def correctness_tester(p, g):
    """
    Performs Diffie Heilman key exchange and tries to hack it
    :param p: prime for DHKE
    :param g: Generator of the Zp*
    """
    print "Verifying the correctness"
    p = long(p)
    g = long(g)
    alice = DiffieHeilman(p, g)
    bob = DiffieHeilman(p, g)
    print "Generating keys for A"
    pka = alice.generate_key()
    print "public key", pka, "\nDone"
    print "Generating keys for B"
    pkb = bob.generate_key()
    print "public key", pkb, "\nDone"
    sk1 = alice.caluclate_session_key(pkb)
    sk2 = bob.caluclate_session_key(pka)
    print "Is session key same: sk1 =", sk1, "sk2 =", sk2, " so ", sk1 == sk2  # 7b
    print "Done testing..."


def man_in_the_middle(p, g):
    """ Trying to perform man in the middle attack"""
    print "Performing Man in the middle attack"
    p = long(p)
    g = long(g)
    print "Caluclating the keys..."
    alice = DiffieHeilman(p, g)
    bob = DiffieHeilman(p, g)
    eve = DiffieHeilman(p, g)
    pka = alice.generate_key()
    pkb = bob.generate_key()
    pke = eve.generate_key()
    print "Done....\n Generating Session keys"
    ska = alice.caluclate_session_key(pke)
    skb = bob.caluclate_session_key(pke)
    ske1 = eve.caluclate_session_key(pka)
    ske2 = eve.caluclate_session_key(pkb)
    print "Session keys are..."
    print "Alice :", ska
    print "Bob :", skb
    print "Eve :", ske1, ske2

    print "Can Eve read messages sent by Alice? :", ske1 == ska
    print "Can Eve read messages sent by Bob? :", ske2 == skb
    print "Can Bob read messages sent by Alice? :", skb == ska


if __name__ == "__main__":
    correctness_tester(37, 5)
    man_in_the_middle(37, 5)
