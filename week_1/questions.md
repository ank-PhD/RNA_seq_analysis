- how to extract strand directions from the pileup format?
    => Use sam record instead of pileup or look at the genes directly 
    => plane sweep algorithm to keep track of the alignement mapping 

- I chopped 70 bp on each side before calculating the coverage in order to account for the 
  decreased probability of sequencing the ends of reads
    => see cufflinks

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
  
- why do we need sorting in the bam/sam files? 

- what are the specialization of different aligners? What is the difference between Bowtie and BWA?
    => specificity, speed, precision
    => Bowtie - speed
    => BWA-mem + precision on error - high rate of heterozigocity - short reads
    => Teaser system