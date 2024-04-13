# microbiome_bracken_pipeline
Start with folder called standardBracken2
Filtering out human data (run this code): python filter_bracken_out.py -d standardBracken2 -o filtered_dataset2 --exclude 9606
Will create new output folder called filtered_dataset2 exactly same as original standardBracken2, except species 9606 (humans) has been removed from raw data
Combine Data (run this): python combine_bracken_outputs.py --files "filtered_dataset2" -o "combined_dataset2.tsv"
Takes input filtered_dataset2 (step 2 output) and combines all separate files into one big one called combined_dataset2.tsv
Result should look something like this

Separating combined data into counts and fraction (use this code): python separate_count_frac.py --files "combined_dataset2.tsv" -o "count_dataset2.tsv" "frac_dataset2.tsv"
Takes step 3 output and splits into two separate datasheets
If frac_dataset2 look likes image below, you should be good for both

Can look ahead to alpha_combined.py, but first issue comes here
There is a line of code in alpha that is specific to my first dataset and needs to be changed for 2nd
Line 190: it removes a sample datafile that only exists within dataset, but does not have the information that matches it with alpha diversity (its unnecessary), need to check new data to see if any outliers like this
