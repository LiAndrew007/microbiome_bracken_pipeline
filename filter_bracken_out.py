#!/usr/bin/env python
from dataclasses import field
import os, sys, argparse
import math
import numpy as np

# Main method
def main():
	# get arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d','--dir',dest='dirname',help='folder of outputted bracken files')
    #output file, only calculated
    parser.add_argument('-o', '--output', dest='output', help='folder of output files of newly calculated percentages')	
    parser.add_argument('--include', dest='t_include',nargs='*', type=str, required=False, 
        help='List of taxonomy IDs to include in output [space-delimited] - default=All', default=[])
    parser.add_argument('--exclude', dest='t_exclude',nargs='*', type=str, required=False,
        help='List of taxonomy IDs to exclude in output [space-delimited] - default=None',default=[])
    args = parser.parse_args()

    #checking include and exclude
    if len(args.t_include) == 0 and len(args.t_exclude) == 0:
        sys.stderr.write("User must include at least one taxonomy ID to include or exclude\n")
        sys.stderr.write("Please specify either --include or --exclude\n")
        sys.exit(1)
    #CHECK#2: if both are specified, make sure none exists in both lists
    if len(args.t_include) > 0 and len(args.t_exclude) > 0:
        for val in args.t_include:
            if val in args.t_exclude:
                sys.stderr.write("%s cannot be in include AND exclude lists\n" % val)
                sys.exit(1)
    include = False
    exclude = False
    if len(args.t_include) > 0:
        include = True
    if len(args.t_exclude) > 0:
        exclude = True       
    #rading in input path and checking if it exists
    path = args.dirname
    if os.path.isdir(path) == False:
        print("Input folder doesn't exist. Try new folder next run")
        sys.exit(1)
    #rading in outputpath and checking if it exists
    path_out = args.output
    if os.path.isdir(path_out) == False:
        print("Output folder previously non-existing, new one created")
        os.mkdir(path_out)
    #print(path)
    dir_list = os.listdir(path)

    #looping all files within input folder
    for f in dir_list:
    #open all files for reading and writing
        f_output = path_out + "/" + f
        file_new_proportion = open(f_output,"w")
        full_path_f = path + "/" + f
        input_file = open(full_path_f)

        
        #create arrays
        count = 0
        header_line = []
        info_header = []
        table = []

        for sample_line in input_file:
            #split line by tabs to separate into [name, tax_id, tax_lvl, ...]
            sample_split = sample_line.split("\t")

            
            if count == 0:
                header_line = sample_split
            else:
                if len(args.t_include) > 0:
                    if sample_split[1] in args.t_include:
                        info_header.append(sample_split[0 : 6])
                        normal_line = float(sample_split[-2])
                        table.append(normal_line)
                elif len(args.t_exclude) > 0:
                    if sample_split[1] not in args.t_exclude:
                        info_header.append(sample_split[0 : 6])
                        normal_line = float(sample_split[-2])
                        table.append(normal_line)
            count = count + 1
        #make into numpy array for easier manipulation
        table = np.array(table)

        #summed row
        table_sum = np.sum(table)

        #divide row by sum, calculating new percentages
        table = table / table_sum
    
        #writing out header of out file
        file_new_proportion.write(header_line[0] + "\t")
        file_new_proportion.write(header_line[1] + "\t")
        file_new_proportion.write(header_line[2] + "\t")
        file_new_proportion.write(header_line[3] + "\t")
        file_new_proportion.write(header_line[4] + "\t")
        file_new_proportion.write(header_line[5] + "\t")
        
        
        file_new_proportion.write(header_line[-1]) 

        #write out data for each bacteria  
        for i in range(len(table)):
            file_new_proportion.write(info_header[i][0] + "\t" + info_header[i][1] + "\t" + info_header[i][2] + "\t" + info_header[i][3] + "\t" + info_header[i][4] + "\t" + info_header[i][5] + "\t")
            file_new_proportion.write(str(table[i]) + "\t")
            file_new_proportion.write("\n")


        #close files
        
        file_new_proportion.close()
        input_file.close()
    

if __name__ == "__main__":
    main()
