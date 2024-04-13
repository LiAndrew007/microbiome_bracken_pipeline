#!/usr/bin/env python
import os, sys, argparse
import math

# Main method
def main():
	# get arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--files',dest='filename',help='combined bracken files with count and fraction values')
    #2 output files, order Count first and Frac second
    parser.add_argument('-o', '--output', dest='output', nargs = '+', help='Two output files. First one for counts, Second one for frac ')	
    args = parser.parse_args()

    #open all files for reading and writing
    file_Count = open(args.output[0], "w")
    file_Frac = open(args.output[1],"w")
    input_file = open(args.filename)

    
    #loop each line of file
    for sample_line in input_file:
        
        #split line by tabs to separate into [name, tax_id, tax_lvl, patient1Count, patient1Frac, patient2Count, ...]
        sample_split = sample_line.split("\t")
        
        #loop each sample_split to write into correct outputfiles
        for i in range(len(sample_split)):
            if i < 3:
                file_Count.write(sample_split[i] + '\t')
                file_Frac.write(sample_split[i] + '\t')
            elif i % 2 == 1:
                file_Count.write(sample_split[i] +"\t")
            else:
                if i == len(sample_split) - 1:
                    file_Frac.write(sample_split[i])
                else:
                    file_Frac.write(sample_split[i] + "\t")
        #new line after current line is read through
        file_Count.write("\n")
        #file_Frac.write("\n")

    #close files
    file_Count.close()
    file_Frac.close()
    input_file.close()
    

if __name__ == "__main__":
    main()
