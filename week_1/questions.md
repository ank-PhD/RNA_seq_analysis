- how to extract strand directions from the pileup format?

- I chopped 70 bp on each side before calculating the coverage in order to account for the 
  decreased probability of sequencing the ends of reads

- instead of the rpkm I used a "normalized coverage depth" followed by the quintile normalization
  to make sure timepoints were comparable between them
  
- data formats explanation:
    - sai
    - sam
    - bam
    - bai
    - sorted
    - fa
    - fq
    - fai

- why the gff did not work out? how do I get the actual gene names to be called rather than 
  having to match them manually?
  
- why do we need sorting?