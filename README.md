# FibPseudoprime-SanitizedInputs

This github repository is a continuation of our work from the repository FibPseudoprime (writte in Haskell) and Primes (written in C++). It was created for the purpose of testing our work from the paper, [Using Fibonacci factors to create Fibonacci pseudoprimes](https://arxiv.org/abs/2105.13513). Included in this repo are several files and folders, which will be explained below:

The `/data` folder contains all of our data used for our tests and verifications. It contains the list of factors of all [Lucas numbers](https://github.com/ensj/FibPseudoprime-SanitizedInputs/blob/master/data/allLucasFactors.txt), and the list of factors of all [odd Fibonacci numbers](https://github.com/ensj/FibPseudoprime-SanitizedInputs/blob/master/data/oddFibFactors.txt). This data is a direct download from the [MersenneUs website](https://mersennus.net/fibonacci/). Formats on how the data was organized may be found there as well. 

`FibText.py` is the program which does all the magic! It extracts all fibonacci numbers and their factors from the data files described above, then generates possible Baillie-PSW pseudoprimes. The descriptive details on how the code works can be found in the comments of the file itself. 

Several things should be noted for `FibText.py` that weren't initially considered before. 
- For an Lth fibonacci number, F_L, if L is divisible by 5 then it must be the case that prime factors of F_L will be congruent to 1 mod L. This is significant because without prime factors that are -1 mod L, we cannot construct possible Baillie-PSW pseudoprimes. This means we may simply skip over all L that is divisible by 5 in the future.
- If L is odd, then we know for a fact that candidates generated by F_L would be included in candidates generated by F_2L. This means we can skip over generating candidates for all odd L, so long as we know we will generate candidates for 2L. 

Lastly, `factors_final.txt` is the list of factors along with the index of the fibonacci number they are associated with that gets used to generate possible Baillie-PSW pseudoprimes. It is an array of arrays containing the following: `[Index of fibonacci number L, [1 mod L factors], [-1 mod L factors]]`

