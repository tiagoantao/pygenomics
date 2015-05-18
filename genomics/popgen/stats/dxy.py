# -*- coding: utf-8 -*-
'''
.. module:: Dxy
   :synopsis: Calculating Dxy

.. moduleauthor:: Tiago Antao <tra@popgen.net>
'''
from __future__ import division


def calc_seq_freqs(seqs):
    """ Calculates the frequency of sequences.

    >>> calc_seq_freqs(['a'])
    {'a': 1.0}
    >>> calc_seq_freqs(['a', 'b']) == {'a': 0.5, 'b': 0.5}
    True
    >>> calc_seq_freqs(['a', 'b', 'b']) == {'a': 0.3333333333333333, 'b': 0.6666666666666666}
    True
    """
    cnt_seq = 0
    seq_freqs = {}
    for seq in seqs:
        cnt_seq += 1
        seq_freqs[seq] = seq_freqs.get(seq, 0) + 1
    for seq, cnt in seq_freqs.items():
        seq_freqs[seq] = cnt / cnt_seq
    return seq_freqs


def calc_num_diffs(seq1, seq2):
    """Calculates the number of differences between 2 sequences.

    >>> calc_num_diffs("a", "a")
    0
    >>> calc_num_diffs("c", "a")
    1
    >>> calc_num_diffs("ac", "aa")
    1
    >>> calc_num_diffs("cc", "aa")
    2
    """
    return sum([0 if x == y else 1 for x, y in zip(seq1, seq2)])


def get_n_poses(seqs):
    n_poses = set()
    for seq in seqs:
        seq_pos = [i for i in range(len(seq)) if seq[i] in ["n", "N"]]
        n_poses = n_poses.union(seq_pos)
    n_poses = list(n_poses)
    n_poses.sort()
    return n_poses


def calc_pi_XY(seq_freq1, seq_freq2):
    pi_XY = 0.0
    seqs1 = list(seq_freq1.keys())
    seqs2 = list(seq_freq2.keys())
    nposes = get_n_poses(seqs1 + seqs2)

    def convert_seq_freq(nposes, old_sfreq):
        new_seqs = set()
        sfreq = {}
        for old_seq, freq in old_sfreq.items():
            new_seq = "".join([old_seq[i]
                               for i in range(len(old_seq))
                               if i not in nposes])
            if new_seq in new_seqs:
                sfreq[new_seq] += freq
            else:
                new_seqs.add(new_seq)
                sfreq[new_seq] = freq
        return sfreq
    seq_freq1 = convert_seq_freq(nposes, seq_freq1)
    seq_freq2 = convert_seq_freq(nposes, seq_freq2)
    seqs1 = list(seq_freq1.keys())
    seqs2 = list(seq_freq2.keys())
    for i in range(len(seqs1)):
        seq1 = seqs1[i]
        len_seq = len(seq1)
        fi = seq_freq1[seq1]
        for j in range(len(seqs2)):
            seq2 = seqs2[j]
            if seq1 == seq2:
                continue
            fj = seq_freq2[seq2]
            num_diffs = calc_num_diffs(seq1, seq2)
            pi_XY += fi * fj * (num_diffs / len_seq)
    return pi_XY, len(seq1)


def calc_nuc_div(seq_freq):
    """Nucleotide diversity - Pi"""
    return calc_pi_XY(seq_freq, seq_freq)[0]


def calc_d_XY(seq_freq1, seq_freq2, num_freqs1, num_freqs2):
    """Diversity between two pops"""
    pi_XY, lseq = calc_pi_XY(seq_freq1, seq_freq2)
    pi1 = (num_freqs1 / (num_freqs1 - 1)) * calc_nuc_div(seq_freq1)
    pi2 = (num_freqs2 / (num_freqs2 - 1)) * calc_nuc_div(seq_freq2)
    d_XY = pi_XY - (pi1 + pi2) / 2
    return d_XY, (pi_XY, pi1, pi2, lseq)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
