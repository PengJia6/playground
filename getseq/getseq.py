#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""==============================================================================
# Project: playground
# Script : getseq.py
# Author : Peng Jia
# Date   : 2020.08.03
# Email  : pengjia@stu.xjtu.edu.cn
# Description: get a sequence for a bam file or a fasta file based on a bed or
               a region (chr1:12345-45678)
=============================================================================="""
import pysam
import argparse
import sys
import logging
import os

curpath = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(os.path.dirname(curpath))

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)

formatter = logging.Formatter('[%(levelname)s] %(message)s')
consoleHandler.setFormatter(formatter)

logger.addHandler(consoleHandler)

logger.info("command: " + " ".join(sys.argv))

global_dict = {
    "tool_name": "getseq",
    "tool_version": " 0.0.1",
    "description": " get a sequence for a bam file or a fasta file based on a bed or a region (chr1:12345-45678)"

}


def args_process():
    """
    argument procress
    """
    # defaultPara = get_value("default")

    commands = []
    commandsParser = {}
    parser = argparse.ArgumentParser(description=global_dict["tool_name"] + ':' + global_dict["description"]
                                     # + ".show help of subcommand with '"
                                     # + get_value("tools_name") + " <subcommand> -h'"
                                     )
    # parser.usage = parser.print_usage()+" > output.fa"
    parser.add_argument('-V', '--version', action='version',
                        version=global_dict["tool_name"] + global_dict["tool_version"])
    subparsers = parser.add_subparsers(title="command", metavar="", dest='command')

    ###################################################################################################################
    # add arguments for fasta module
    parser_fasta = subparsers.add_parser('fasta', help='Get sequence for fasta file')
    parser_fasta.description = 'Get sequence for fasta file.'
    commands.append("fasta")
    # group input and output
    parser_fasta.add_argument('-f', '--fasta', required=True, type=str, nargs=1,
                              help="Input fasta with index [required]")
    parser_fasta.add_argument('regions', type=str, nargs='*',
                              help="Regions sush as chr1:123456-235689\n"
                                   "path of bed file \n"
                                   "[required]")
    commandsParser["fasta"] = parser_fasta

    # parser_arg=parser.parse_args()

    ###################################################################################################################
    # subparsers = parser.add_subparsers(title="command", metavar="", dest='command')
    #
    # print(parser_arg.fa)
    # print(parser_arg.regions)
    parser_bam = subparsers.add_parser('bam', help='Get sequence for bam file')
    parser_bam.description = 'Get sequence for bam file.'
    commands.append("bam")
    # group input and output
    parser_bam.add_argument('-b', '--bam', required=True, type=str, nargs=1,
                            help="Input fasta with index [required]")
    parser_bam.add_argument('-r', '--only_in', type=bool, nargs=1, choices=[True, False],
                            default=True,
                            help="True: only output sequence in a region; "
                                 "False: output read cover a region")

    parser_bam.add_argument('regions', type=str, nargs='*',
                            help="Regions sush as chr1:123456-235689\n"
                                 "path of bed file \n"
                                 "[required]")
    commandsParser["bam"] = parser_bam

    if len(os.sys.argv) < 2:
        parser.print_help()
        return False

    if os.sys.argv[1] in ["-h", "--help", "-?"]:
        parser.print_help()
        return False
    if os.sys.argv[1] in ["-V", "-v", "--version"]:
        # parser.print_help()
        print(global_dict["tool_name"] + " " + global_dict["tool_version"])
        return False
    if os.sys.argv[1] not in commands:
        logger.error("Command Error! " + os.sys.argv[1] + " is not the available command")
        logger.error("Please input correct command such as " + "/".join(commands) + "!")
        parser.print_help()
        # parser.parse_args()
        return False
    if len(os.sys.argv) == 2 and (os.sys.argv[1] in commands):
        commandsParser[os.sys.argv[1]].print_help()
        return False

    # return parser
    this_command = os.sys.argv[1]

    args = {}
    parser_arg = parser.parse_args()
    if this_command == "fasta":
        args["command"] = this_command
        args["fasta"] = parser_arg.fasta[0]
        if not os.path.exists(args["fasta"]):
            logger.error("No such fasta file:" + args["fasta"])
            return False
    else:
        args["only_in"] = parser_arg.only_in
        args["command"] = this_command
        args["bam"] = parser_arg.bam[0]
        if not os.path.exists(args["bam"]):
            logger.error("No such bam file:" + args["bam"])
            return False

    regions = []
    bed_file = []
    for region in parser_arg.regions:
        if ":" in region:
            regions.append(region)
        else:
            if os.path.exists(region):
                bed_file.append(region)
            else:
                logger.warning("No such bed file:" + region)
    args["regions"] = regions
    args["bed"] = bed_file
    if len(regions) + len(bed_file) < 1:
        logger.error("No available regions input")
        return False
    return args


def get_seq_from_bam(region, bam, only_in=True):
    logger.info("Processing region:" + region)
    chrom = region.split(":")[0]
    start, end = map(int, region.split(":")[1].split("-"))
    cont = 0
    for read in pysam.AlignmentFile(bam).fetch(chrom, start, end):
        if read.is_duplicate or read.is_unmapped: continue
        header = region + "_" + str(read.query_name)
        align_start = read.reference_start
        print(start, read.reference_start, end, read.reference_end)
        if not (isinstance(read.query_sequence, str) and (len(read.query_sequence) > 2)):
            continue
        if start >= read.query_alignment_start and end <= read.query_alignment_end:
            continue

        if not only_in:
            seq = read.query_sequence
        else:
            read_pos = 0
            sub_read_str = []
            this_read_str = read.query_sequence
            print(len(this_read_str))
            # print(read.cigartuples)
            for cigartuple in read.cigartuples:
                print(cigartuple)
                if cigartuple[0] in [0, 7, 8]:  # 0 : M : match or mishmatch ; 7: :=:match; 8:X:mismatch
                    # print(this_read_str, read_pos, read_pos + cigartuple[1])
                    match_read = list(this_read_str[read_pos:read_pos + cigartuple[1]])
                    sub_read_str.extend(match_read)
                    read_pos += cigartuple[1]

                elif cigartuple[0] in [1, 4, 5]:  # 1:I:inserion ;4:S:soft clip 5:H:hardclip
                    if cigartuple[0] == 1:
                        print(read_pos)
                        # print(alignment.cigartuples)
                        print(this_read_str[read_pos])
                        print(this_read_str[read_pos + cigartuple[1]])
                        print(sub_read_str[-1])
                        sub_read_str[-1] += this_read_str[read_pos:read_pos + cigartuple[1]]
                        read_pos += cigartuple[1]
                elif cigartuple[0] in [2, ]:  # 2:D; 3:N: skip region of reference
                    sub_read_str.extend([""] * cigartuple[1])
                else:
                    return -1
                seq = "".join(sub_read_str[start - align_start:end - align_start])
        print(header)
        print(seq)
        cont += 1

    if cont < 1:
        logger.warning("No sequence in " + region)


def get_seq_from_fasta(region, fasta):
    logger.info("Processing region:", region)

    chrom = region.split(":")[0]
    start, end = map(int, region.split(":")[1].split("-"))
    header = ">" + region
    seq = pysam.FastaFile(fasta).fetch(chrom, start, end + 1)
    if len(seq) < 1:
        logger.warning("No sequence in " + region)
        seq = "N"
    print(header)
    print(seq)


def main():
    args = args_process()
    # print(args)
    if not args:
        return
    if args["command"] == "bam":
        for region in args["regions"]:
            get_seq_from_bam(region, args["bam"], only_in=args["only_in"])
        for bed in args["bed"]:
            for line in open(bed):
                lineinfo = line[:-1].split("\t")
                chrom = lineinfo[0]
                start, end = map(int, lineinfo[1:3])
                region = chrom + ":" + str(start) + "-" + str(end)
                get_seq_from_bam(region, args["bam"], only_in=args["only_in"])
    elif args["command"] == "fasta":
        for region in args["regions"]:
            get_seq_from_fasta(region, args["fasta"])
        for bed in args["bed"]:
            for line in open(bed):
                lineinfo = line[:-1].split("\t")
                chrom = lineinfo[0]
                start, end = map(int, lineinfo[1:3])
                region = chrom + ":" + str(start) + "-" + str(end)
                get_seq_from_fasta(region, args["fasta"])


if __name__ == "__main__":
    main()
