#!/usr/bin/env python
import os, sys, argparse
import math
 
def shannons_alpha(p):   
    # shannons = -sum(pi ln(pi))
    h = []
    for i in p:
        h.append(i * math.log(i))
	#print("Shannon's diversity: %s" %(-1 *sum(h)))
    #o.write("%s" %(-1 *sum(h)) + "\n")
    return (-1 *sum(h))

def berger_parkers_alpha(p):
	# bp is nmax/N which is equal to the max pi == max(p)
	#o.write("Berger-parker's diversity: %s" %max(p))
	return max(p)

def simpsons_alpha(D):
	# simpsons index of diversity = 1 - D
	# D = (sum ni(ni-1))/ N*(N-1)
	#o.write("Simpson's index of diversity: %s" %(1-D))
	return 1-D

def inverse_simpsons_alpha(D):
	# simsons inverse = 1/D
	#o.write("Simpson's Reciprocal Index: %s" %(1/D))
	return 1/D

def fishers_alpha():	
	global np
	import numpy as np
	from scipy.optimize import fsolve
	
	fish = fsolve(eqn_output,1)
	
	# NOTE:
	# if ratio of N/S > 20 then x > 0.99 (Poole,1974)
	# x is almost always > 0.9 and never > 1.0 i.e. ~ 0.9 < x < 1.0
	#o.write("Fisher's index: %s" %fish[0])
	return fish

def eqn_output(a):
	return a * np.log(1+N_f/a) - S_f

# Main method
def main():
	# get arguments
    parser = argparse.ArgumentParser(description='Pick an alpha diversity.')
    parser.add_argument('-d','--dir',dest='dirname',help='direcotry of bracken files with species abundance estimates')
    parser.add_argument('-f','--files',dest='filename',help='direcotry of bracken files with species abundance estimates')
    #parser.add_argument('--names', dest='names', 
        #default='',required=False,
        #help='Names for each input file - to be used in column headers of output [separate names with commas]')
    parser.add_argument('-o', '--output', dest='output', required=True, help='Name of output file with combined Bracken results.')
	
	
    parser.add_argument('-a','--alpha',dest='value',default='Sh',type=str,  help='type of alpha diversity to calculate Sh, BP, Si, ISi, F, All default = Sh')
	
    args = parser.parse_args()
    #print(args)
    #Get sample names
    outputFile = open(args.output, "w")
    path = args.dirname
    #print("path: " + path)

    sample_name = []
    alpha_Sh = []
    alpha_BP = []
    alpha_Si = []
    alpha_ISi = []
    alpha_F = []
    dir_list = os.listdir(path)
    for root,folder,dir_list in os.walk(path):
         
        dir_list.sort()
        for fileName in dir_list:
            curr_name = os.path.basename(fileName)
            print(curr_name)
            
            
            sample_name.append(curr_name.split("_")[0])
            #sys.stdout.write("Processing File %s:: Sample %s\n" % (fileName, curr_name))
            full_path_f = path + "/" + fileName
            
            status_path_list = path.split("/")[:-1]
            status_path = "/".join(status_path_list)
            
            full_path_status_f = status_path + "/" + args.filename
            f = open(full_path_f)
            status_f = open(full_path_status_f)
            
            
            f.readline()
            n = []
            # read in the file
            for line in f: 
                ind_abund = line.split('\t')[5] # finds the abundance estimate
                n.append(float(ind_abund)) 
            
            f.close()

            status_f.readline()
            status_name = []
            status = []

            
            for status_line in status_f:
                curr_line = status_line.split('\t')
                #print(curr_line)
                sample_n = curr_line[2][1:-2]
                status_name.append(sample_n)
                

                sample_status = curr_line[1]
                status_simple = sample_status[:-1]
                status_simple = status_simple[16:]
                
                status.append(status_simple)
                #print(status)

            
            
            # calculations
            N = sum(n) # total number of individuals
            S = len(n) # total number of species
            # calculate all the pi's
            p = [] # store pi's 
            D = 0
            for i in n: # go through each species
                if i != 0: # there should not be any zeros
                    p.append(i/N) # pi is the ni/N
                    D += i*(i-1)
            
            D = D/(N*(N-1))
            # find the indicated alpha
            if args.value == 'Sh' or args.value == "All": # calculate shannon's diversity
                alpha_Sh.append(shannons_alpha(p))
            if args.value == 'BP' or args.value == "All": # calculate berger-parker's dominance index
                alpha_BP.append(berger_parkers_alpha(p))
            if args.value == 'Si' or args.value == "All": # calculate Simpson's alpha 
                alpha_Si.append(simpsons_alpha(D))
            if args.value == 'ISi' or args.value == "All": # calculate Inverse Simpson's alpha 
                alpha_ISi.append(inverse_simpsons_alpha(D))
            if args.value == 'F' or args.value == "All": # calculate fisher's alpha
                #print("Fisher's alpha...loading")
                global N_f
                N_f = sum(n)
                global S_f
                S_f = len(n)
                alpha_F.append(fishers_alpha()[0])
            if args.value != 'Sh' and args.value != 'BP' and args.value != 'Si' and args.value != 'Isi' and args.value != 'F' and args.value != 'All':
                print("Not a supported alpha")
        header = ""
        if args.value == 'Sh' or args.value == "All": # calculate shannon's diversity
                header = header + "\tSh"
        if args.value == 'BP' or args.value == "All": # calculate berger-parker's dominance index
            header = header + "\tBP"
        if args.value == 'Si' or args.value == "All": # calculate Simpson's alpha 
            header = header + "\tSi"
        if args.value == 'ISi' or args.value == "All": # calculate Inverse Simpson's alpha 
            header = header + "\tISi"
        if args.value == 'F' or args.value == "All": # calculate fisher's alpha
            header = header + "\tF"
        header = header + "\tStatus"
        header = header + "\n"
        outputFile.write(header)
        i = 0
        #print(sample_name)
        print("before here")
        for row in sample_name:
            line = row
            #print("Line:" + line)
            if args.value == 'Sh' or args.value == "All": # calculate shannon's diversity
                line = line + "\t" + str(alpha_Sh[i])
            if args.value == 'BP' or args.value == "All": # calculate berger-parker's dominance index
                line = line + "\t" + str(alpha_BP[i])
            if args.value == 'Si' or args.value == "All": # calculate Simpson's alpha 
                line = line + "\t" + str(alpha_Si[i])
            if args.value == 'ISi' or args.value == "All": # calculate Inverse Simpson's alpha 
                line = line + "\t" + str(alpha_ISi[i])
            if args.value == 'F' or args.value == "All": # calculate fisher's alpha
                line = line + "\t" + str(alpha_F[i])
            i = i+1

            val = 0
            #print("here")
            sample_id = row
            #print(sample_id)
            if sample_id == "SRR11952321":
                print("Reached")
                #sys.exit(0)
            for j in status_name:
                if j == sample_id:
                    break
                val = val + 1
            
            
            line = line + "\t" + status[val]

            line = line + "\n"
            outputFile.write(line)



if __name__ == "__main__":
    main()
