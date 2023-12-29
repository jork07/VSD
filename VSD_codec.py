import codecs
import binascii
import numpy as np
import time
import random
import subprocess
import os

# Get hex string
def read_hex_string(path):
    f = codecs.open(path, 'rb')
    with f:
        fileText = f.read()
        hexstr = binascii.hexlify(fileText)
        string = hexstr.decode('utf-8')
    return string

# parse boxes info
def get_content(string):
    mark_dict = {'ftyp': '66747970', 'free': '66726565', 'moov': '6d6f6f76', 'mdat': '6d646174'}
    ftyp_pos = string.index(mark_dict['ftyp'])
    offset = int(string[ftyp_pos - 8:ftyp_pos], 16)
    ftyp_content = string[ftyp_pos + 8:ftyp_pos + 8 + (offset - 8) * 2]
    moov_pos = string.index(mark_dict['moov'])
    offset = int(string[moov_pos - 8:moov_pos], 16)
    moov_content = string[moov_pos+8:moov_pos+8+(offset-8)*2]
    mdat_pos = string.index(mark_dict['mdat'])
    offset = int(string[mdat_pos - 8:mdat_pos], 16)
    mdat_content = string[mdat_pos + 8:mdat_pos + 8 + (offset - 8) * 2]
    return ftyp_content,moov_content,mdat_content

# Hex transcode to decimal
def hex_to_dec(string):
    decimal_list = []
    for i in range(0, len(string), 4):
        hex_string = string[i:i+4]
        decimal_num = int(hex_string, 16)
        rule_indices = []
        for index in range(3):
            rule_indices.append(int(decimal_num % 41))
            decimal_num -= rule_indices[-1]
            decimal_num /= 41
        rule_indices = rule_indices[::-1]
        decimal_list += rule_indices
    return decimal_list

# Set length to compare with others
def hex_segmentation(str, length = 40):
    padding = length - len(str)%length
    padding_str = str + '0' * padding
    split_strings = [padding_str[i:i+length] for i in range(0,len(padding_str),length)]
    index_length = len(hex(len(split_strings))[2:])
    print(index_length)
    for i in range(len(split_strings)):
        split_strings[i] = hex(i)[2:].zfill(index_length)+split_strings[i]
    return split_strings

# write sequences to text file
def write_dna_file(path, dna_sequences):
    # with open(path, "w") as file:
    #     for index, dna_sequence in enumerate(dna_sequences):
    #         str = "".join(dna_sequence)
    #         file.write(str + "\n")
    with open(path, "w") as file:
        for index, dna_sequence in enumerate(dna_sequences):
            _out = ">seq{}\n{}\n".format(index, "".join(dna_sequence))
            file.write(_out)

    return True


def encode(dec_list,AT,GC,Oe,Ee,default,o_base,e_base):
    offset = int(np.median(dec_list))
    # print(offset)
    is_odd = True
    flag = True
    sequence = ""
    for num in dec_list:
        if num == 40:
            if is_odd:
                sequence += Oe
                is_odd = False
            else:
                sequence += Ee
                is_odd = True
        else:
            if offset == 0:
                if num == 0:
                    if flag:
                        sequence += o_base
                        flag = False
                    else:
                        sequence += e_base
                        flag = True
                elif num < 20:
                    sequence += AT[num]
                else:
                    sequence += GC[num - 20]
            elif offset < 20:
                if num < offset and num>=0:
                    sequence += AT[num]
                elif num >= 20 + offset:
                    sequence += AT[num - 20]
                else:
                    sequence += GC[num - offset]
            elif offset > 20:
                if num >= offset:
                    sequence += GC[num - 20]
                elif num < offset - 20:
                    sequence += GC[num]
                else:
                    sequence += AT[offset - num - 1]
            else:
                if num < 20:
                    sequence += AT[num]
                else:
                    sequence += GC[num-20]
    sequence += default[offset]
    return sequence


AT = ['ACA','TCA','AGA','TGA','CTA','GTA','AAC','TAC','ATC','TTC','AAG','TAG','ATG','TTG','CAT','GAT','ACT','TCT','AGT','TGT']
GC = ['CCA','GCA','CGA','GGA','CAC','GAC','AGC','TGC','CTC','GTC','CAG','GAG','ACG','TCG','CTG','GTG','CCT','GCT','CGT','GGT']
odd_extra_triplet = 'TAT'
even_extra_triplet = 'CGC'
# need a default table to store index
default_table = ['ACA','CCA','TCA','GCA','AGA','CGA','TGA','GGA','CTA','CAC','GTA','GAC','AAC','AGC','TAC','TGC','ATC','CTC','TTC','GTC',
                                'AAG','CAG','TAG','GAG','ATG','ACG','TTG','TCG','CAT','CTG','GAT','GTG','ACT','CCT','TCT','GCT','AGT','CGT','TGT','GGT','ATA']
odd_table = ['ACA','TCA','AGA','TGA','CTA','GTA','AAC','TAC','ATC','TTC','AAG','TAG','ATG','TTG','CAT','GAT','ACT','TCT','AGT','TGT','ATA','TTA','AAT',
                        'CCA','GCA','CGA','GGA','CAC','GAC','AGC','TGC','CTC','GTC','CAG','GAG','ACG','TCG','CTG','GTG','CCT','GCT','CGT','GGT','GCG','GGC','CCG']
even_table = ['CCA','GCA','CGA','GGA','CAC','GAC','AGC','TGC','CTC','GTC','CAG','GAG','ACG','TCG','CTG','GTG','CCT','GCT','CGT','GGT','GCG','GGC','CCG',
                        'ACA','TCA','AGA','TGA','CTA','GTA','AAC','TAC','ATC','TTC','AAG','TAG','ATG','TTG','CAT','GAT','ACT','TCT','AGT','TGT','ATA','TTA','AAT']
positive_base = 'ATA'
negative_base = 'GCG'

def gc(sequence):
    """返回GC含量"""
    gc_content = float(sequence.count("C") + sequence.count("G")) / float(len(sequence))*100
    return round(gc_content, 2)


def decimal2OtherSystem(decimal_number: int, other_system: int, precision: int = None) -> list:
    remainder_list = []
    while True:
        remainder = decimal_number % other_system
        quotient = decimal_number // other_system
        remainder_list.append(str(remainder))
        if quotient == 0:
            break
        decimal_number = quotient

    num_list = remainder_list[::-1]
    # Specify precision
    if precision != None:
        if precision < len(num_list):
            raise ValueError("The precision is smaller than the length of number. Please check the [precision] value!")
        else:
            num_list = ["0"] * (precision - len(num_list)) + num_list
    return num_list

def getHomoLen(seq: str) -> int:
    seq_new = seq + "$"
    pos1 = 0
    pos2 = 1
    max_len = 0
    while pos1 < len(seq):
        while seq_new[pos2] == seq_new[pos1]:
            pos2 += 1
        max_len = max(max_len, pos2 - pos1)
        pos1, pos2 = pos2, pos2 + 1

    return max_len

def getPrimerList(save_path, primer_len: int = 20, primer_num: int = 100, homo: int = 3, gc=0.5):
    mapping_rule = {"0": "A", "1": "C", "2": "G", "3": "T"}

    primer_set = set()
    max_num = int('3' * primer_len, 4)

    f = open(save_path, "w")
    n = 0
    while True:
        primer_decimal_num = random.randint(0, max_num)
        primer_quaternary_num_list = decimal2OtherSystem(primer_decimal_num, 4, primer_len)
        primer_seq = "".join([mapping_rule[i] for i in primer_quaternary_num_list])

        # filter
        if (primer_seq.endswith("A") or primer_seq.endswith("T")):
            continue
        if abs((primer_seq.count("G") + primer_seq.count("C")) / primer_len - gc) > 0.1:
            continue
        if getHomoLen(primer_seq) > homo:
            continue

        primer_set.add(primer_seq)
        _out = ">seq_{}\n{}\n".format(n, primer_seq)
        f.write(_out)
        n += 1

        if len(primer_set) >= primer_num:
            break
    f.close()

    return list(primer_set)

def runBlast(ref_path, primer_path):
    blast_path = r"G:\BLAST 2.15\blast-2.15.0+\bin"
    print(ref_path)
    print(primer_path)
    result_path = os.path.dirname(ref_path) + os.sep + "result.blast"
    shell = "makeblastdb -dbtype nucl -in {}\n".format(ref_path)
    shell += "blastn -query {} -db {} -out {} -outfmt 6\n".format(primer_path, ref_path, result_path)
    # print(shell)
    os.system('cd')
    subprocess.run([os.path.join(blast_path,"makeblastdb"),"-dbtype","nucl", "-in", ref_path])
    # os.system(shell)

    return result_path

def filterPrimer(blast_path, primer_list):

    homology_index = []
    with open(blast_path) as f:
        for i in f:
            _index = i.strip().split("\t")[0]
            _index = int(_index.split("_")[1])
            homology_index.append(_index)

    # chose primer
    primer_select_list = []
    for _index, primer in enumerate(primer_list):
        if _index in homology_index:
            continue
        primer_select_list.append(primer)

        if len(primer_select_list) == 2:
            break

    print("primer_F: {}\nprimer_R: {}\n".format(primer_select_list[0], primer_select_list[1]))
    return primer_select_list

def addPrimer(primer_f, primer_r, sequences):
    compement_dic = {"A":"T", "T":"A", "C":"G", "G":"C"}
    add_primer_r = "".join([compement_dic[i] for i in primer_r][::-1])
    with_primer_seq_list = ["{}{}{}".format(primer_f, i, add_primer_r) for i in sequences]
    return with_primer_seq_list

# test
if __name__ == '__main__':
    hex_string = read_hex_string("../output_video/output012.mp4")
    string_list = hex_segmentation(hex_string, 40)
    seq_list = []
    for segment in string_list:
        dec = hex_to_dec(segment)
        seq = encode(dec,AT,GC,odd_extra_triplet,even_extra_triplet,default_table,positive_base,negative_base)
        seq_list.append(seq)
    save_path = "./blast\\vsd_index.txt"
    primer_path = os.path.dirname(save_path) + os.sep + "primers.fa"
    primer_list = getPrimerList(primer_path)
    blast_path = runBlast(save_path, primer_path)
    primer_f, primer_r = filterPrimer(blast_path, primer_list)
    with_primer_seq_list = addPrimer(primer_f, primer_r, seq_list)
    primer_save_path = "result_i.dna"
    write_dna_file(primer_save_path, with_primer_seq_list)