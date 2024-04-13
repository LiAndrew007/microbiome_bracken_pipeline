#!/usr/bin/env python
################################################################
#bray_curtis.py takes multiple reports of classifications or
#abundances and calculates a matrix of bray-curtis dissimilarity
#metrics
#Copyright (C) 2019 Jennifer Lu, jlu26@jhmi.edu
#
#This file is part of KrakenTools
#KrakenTools is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 3 of the license, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, see <http://www.gnu.org/licenses/>.

#################################################################
#Jennifer Lu, jlu26@jhmi.edu
#Christopher Pockrandt, pockrandt@jhu.edu
#Updated: 08/12/2019
#
#This program takes multiple reports of classifications or
#abundances and calculates a matrix of bray-curtis dissimilarity
#metrics
#
#Parameters:
#   -h, --help................show help message.
#   -i X, --input-files X.....all (at least 2) input files (separated by spaces)
#Input File options (all input files must be of the same format)
#   --single [default]........all samples are within a single tab-delimited file
#                             where the first column is the category and the rest are counts
#   --simple .................input files must be tab-delimited with the first
#                             two columns representing categories and then counts
#   --bracken.................input files are Bracken outputs: col  2=taxonomy, 6=counts
#   --kraken..................input files are Kraken reports: col 5=taxonomy, 3=counts
#   --krona...................input files are Krona format: col 1=counts, 2=taxonomy
#Input options:
#   --level [S, G, etc].......user specifies which level to measure at
#                             (for kraken, krona, or bracken input files)
####################################################################
import os, sys, argparse
import operator
from time import gmtime
from time import strftime
import numpy as np
####################################################################
#Main method
def main():
    
    #Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--dir',dest='dirname',help='direcotry of bracken files')
    parser.add_argument('-f','--files',dest='filename',help='status file matching SRR ID with sample status')
    parser.add_argument('--type', required=False, default='single', dest='filetype',
        choices=['single','simple','bracken','kreport','kreport2','krona'],
        help='Type of input file[s]: single, simple [tab-delimited, specify --cols], \
            bracken, kreport, kreport2, krona. See docs for details')
    parser.add_argument('--cols','--columns', dest='cols',required=False, default='1,2',
        help='Specify category/counts separated by single comma: cat,counts (1 = first col)')
    parser.add_argument('--level', '-l', dest='lvl', required=False, default='all',choices=['all', 'S', 'G', 'F', 'O'],
        help='For Kraken or Krona files, taxonomy level for which to compare samples. Default: all')
    parser.add_argument('-o', '--output', dest='output', required=True, help='Name of output file with combined Bracken results.')
    args=parser.parse_args()

    outputFile = open(args.output, 'w')
    
    path = args.dirname

    dir_list = os.listdir(path)
    #print(dir_list)
    #sys.exit(0)
    for root,folder,dir_list in os.walk(path):
         
        dir_list.sort()
        ordered_list = []
        ordered_list_a = []
        ordered_list_c = []

        status_path_list = path.split("/")[:-1]
        status_path = "/".join(status_path_list)
            
        full_path_status_f = status_path + "/" + args.filename
        status_f = open(full_path_status_f)
            
        status_f.readline()
        status_name = []
        status = []

        mismatch = False

        for status_line in status_f:
                
                curr_line = status_line.split('\t') 
                #print(curr_line)
                sample_n = curr_line[2][1:-2]
                for i in range(len(dir_list)):
                    #print(dir_list[i][0:11])
                    if dir_list[i][0:11] == sample_n:
                        mismatch = False
                        break
                    elif dir_list[i][0:11] != sample_n and i == len(dir_list) - 1:
                        mismatch = True
                if mismatch == False:
                    status_name.append(sample_n)
                    #print(curr_line)
                    

                    sample_status = curr_line[1]
                    status_simple = sample_status[:-1]
                    status_simple = status_simple[16:]
                    
                    status.append(status_simple)
                #print(status)
        #print(len(dir_list))
        #print((status))
        #print(len(status_name))
        #sys.exit(0)
        # print(status[0])
        # sys.exit(0)
        # #print(status_name)
        #print(status)
        
        ordered_status = []
        ordered_status_a = []
        ordered_status_c = []
        
        for i in range(len(dir_list)):
            #print(i)
            curr_sample = dir_list[i][0:11]
            # if(curr_sample != status_name[i]):
            #     print("here" + curr_sample)
            #     print(status_name[i])
            #     print("break at " + str(i))
            #     print(status_name[i])
            #     sys.exit(0)
            #print(curr_sample)
            #print(status[i + 1])
            #print(curr_sample)
            #if(curr_sample == status_name[i]):
                #print(i)
            if(status[i] == "asthmatic"):
                ordered_list_a.append(dir_list[i])
                ordered_status_a.append("A")
            else:
                ordered_list_c.append(dir_list[i])
                ordered_status_c.append("C")
        ordered_list = ordered_list_a + ordered_list_c
        ordered_status = ordered_status_a + ordered_status_c
        print(len(ordered_status))
        print(ordered_list_a)
        #print(range(len(dir_list)))
        #sys.exit(0)

        #     dir_list[i] = path + "\\" + i
        #################################################
        #Test input files
        in2counts = {}
        # if args.filetype == 'single' and len(args.in_files) > 1:
        #     sys.stderr.write("Please specify only one file for '--type simple'\n")
        #     exit(1)
        # for f in inputFile:
        #     if not os.path.isfile(f):
        #         sys.stderr.write("File %s not found\n" % f)
        #         exit(1)

        #################################################
        #Determine columns for extracting
        categ_col = -1
        count_col = -1
        if args.filetype in ['single','simple']:
            if ',' not in args.cols:
                sys.stderr.write("Please specify column as 'a,b' where a = column of category, \
                b = column of first count\n")
                exit(1)
            else:
                [categ_col, count_col] = args.cols.split(',')
                if not categ_col.isdigit():
                    sys.stderr.write("%s is not an integer\n" % categ_col)
                    exit(1)
                elif not count_col.isdigit():
                    sys.stderr.write("%s is not an integer\n" % count_col)
                    exit(1)
                categ_col = int(categ_col) - 1
                count_col = int(count_col) - 1
        elif args.filetype == "bracken":
            categ_col = 0 # TODO taxid (col 1) does not seem to be properly set
            count_col = 5
            taxlvl_col = 2
        elif args.filetype == "kreport" or args.filetype == "kreport2": # TODO: what about kuniq reports?
            categ_col = 4
            count_col = 2
            taxlvl_col = 3
        elif args.filetype == "krona":
            categ_col = 1
            count_col = 0
        #################################################
        #STEP 1: READ IN SAMPLES
        i2totals = {}
        i2counts = {}
        i2names = {}
        num_samples = 0
        num_categories = 0
        if args.filetype == "single":
            #ALL SAMPLE COUNTS WITHIN A SINGLE FILE
            sys.stdout.write(">>STEP 1: READING INPUT FILE\n")
            sys.stdout.write("\t....reading line 1 as header\n")
            header = True
            i_file = open(ordered_list[0],'r')
            for line in i_file:
                l_vals = line.strip().split("\t")
                #Read header
                if header:
                    s_count = 0
                    for i in range(count_col, len(l_vals)):
                        i2names[s_count] = l_vals[i]
                        i2counts[s_count] = {}
                        i2totals[s_count] = 0
                        s_count += 1
                    num_samples = s_count
                    header = False
                    #sys.stdout.write("\t....reading %i samples\n" % s_count)
                else:
                    #Otherwise, save_counts
                    s_count = 0
                    curr_categ = l_vals[categ_col]
                    for i in range(count_col, len(l_vals)):
                        if int(l_vals[i]) > 0:
                            i2totals[s_count] += int(l_vals[i])
                            i2counts[s_count][curr_categ] = int(l_vals[i])
                        s_count += 1
                    num_categories += 1
            i_file.close()
            #sys.stdout.write("\t....finished reading counts for %i samples in %i categories\n" % (num_samples,num_categories))
        else: # for braken, kraken, kraken2 and krona
            num_samples = 0
            i2names = {}
            i2totals = {}
            i2counts = {}
            genus = {}

            for f in ordered_list:
                i_file = open(path + "/" + f,'r')
                i2names[num_samples] = f
                i2totals[num_samples] = 0
                i2counts[num_samples] = {}
                genus[num_samples] = {}

                for line in i_file:
                    l_vals = line.strip().split("\t")

                    # empty line, header line or line is a comment
                    if len(l_vals) == 0 or (not l_vals[count_col].isdigit()) or l_vals[0] == '#':
                        continue

                    if int(l_vals[count_col]) > 0:
                        if args.filetype == "krona":
                            # we don't know which column will be the genus type (might change for every line)
                            # hence, we iterate over it
                            for i in range(count_col, len(l_vals)):
                                if l_vals[i].startswith(args.lvl.lower() + "__") or args.lvl == "all":
                                    categ_col = i
                                    tax_name = l_vals[categ_col]
                                    i2totals[num_samples] += int(l_vals[count_col])
                                    if not tax_name in i2counts[num_samples]:
                                        i2counts[num_samples][tax_name] = 0
                                    i2counts[num_samples][tax_name] += int(l_vals[count_col])
                                    # sys.stdout.write("%s\t%s\t%i\n" % (f, tax_name, int(l_vals[count_col])))
                        else:
                            if l_vals[taxlvl_col][0] == args.lvl or args.lvl == "all": # TODO: what if it is G1?
                                # TODO: cant do this because of broken bracken files: tax_id = int(l_vals[categ_col])
                                tax_id = l_vals[categ_col]
                                genus[num_samples][tax_id] = l_vals[0]
                                i2totals[num_samples] += int(l_vals[count_col])
                                if tax_id not in i2counts[num_samples]:
                                    i2counts[num_samples][tax_id] = 0
                                i2counts[num_samples][tax_id] += int(l_vals[count_col])
                                # sys.stdout.write("%s\t%s\t%i\n" % (f, line, i2counts[num_samples][tax_id]))
                i_file.close()
                num_samples += 1
        #################################################
        #STEP 2: CALCULATE BRAY-CURTIS DISSIMILARITIES
        #sys.stdout.write(">>STEP 2: COMPARING SAMPLES TO CALCULATE DISSIMILARITIES\n")

        bc = np.zeros((num_samples,num_samples))
        for i in range(0,num_samples):
            i_tot = i2totals[i]
            for j in range(i+1, num_samples):
                j_tot = i2totals[j]
                C_ij = 0.0
                for cat in i2counts[i]:
                    if cat in i2counts[j]:
                        C_ij += min(i2counts[i][cat], i2counts[j][cat])
                #Calculate bray-curtis dissimilarity
                bc_ij = 1.0 - ((2.0*C_ij)/float(i_tot+j_tot))
                #sys.stdout.write("%s\t%s\t%i\t%i\t%i\n" % (i2names[i], i2names[j], C_ij, i_tot, j_tot))
                bc[i][j] = bc_ij
                bc[j][i] = bc_ij

        #################################################
        #sys.stdout.write(">>STEP 3: PRINTING MATRIX OF BRAY_CURTIS DISSIMILARITIES\n")
        for i in i2names:
            sys.stdout.write("#%i\t%s (%i reads)\n" % (i,i2names[i],i2totals[i]))
            outputFile.write("#%i\t%s (%i reads)\n" % (i,i2names[i],i2totals[i]))
        #Print headers
        sys.stdout.write("x")
        outputFile.write("x")
        for i in range(num_samples):
            sys.stdout.write("\t%i" % i)
            outputFile.write("\t%i" % i)
        sys.stdout.write("\n")
        outputFile.write("\n")
        #Print matrix
        for i in range(num_samples):
            sys.stdout.write("%i" % i)
            outputFile.write("%i" % i)
            for j in range(num_samples):
                if i <= j:
                    sys.stdout.write("\tx.xxx")
                    outputFile.write("\tx.xxx")
                else:
                    sys.stdout.write("\t%0.3f" % bc[i][j])
                    outputFile.write("\t%0.3f" % bc[i][j])
            sys.stdout.write("\n")
            outputFile.write("\n")
        outputFile.close()
####################################################################
# def main():
#     f = []
#     fOutput = "betaOut.out"
    
#     for filename in os.listdir("C:\\Users\\lixia\\Summer Research\\standardBracken"):
#         f.append(os.path.join("C:\\Users\\lixia\\Summer Research\\standardBracken", filename))
#     #for filename in os.listdir("C:\\Users\\lixia\\Summer Research\\controlGroupInput"):
#         #f.append(os.path.join("C:\\Users\\lixia\\Summer Research\\controlGroupInput", filename))
#     print(len(f))
#     oldMain(f, fOutput)
#     #o_file.close()
if __name__ == "__main__":
    main()