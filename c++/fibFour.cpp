#include <iostream>
#include <fstream>
#include <gmp.h>
#include <string.h>



//Fast Fibonacci Calculator: A proven and optimized method for computing large Fibonacci numbers. Credits to ----. 

int fastfib(mpz_t result, int n) //PIRATED COPY, MAY NEED WORK
{

    int cons[2][2]={{1,1},{1,0}};      //"constant" matrix
    mpz_t mat[2][2];                   //actual matrix holding fibonacci numbers
    mpz_t ans;                         //holds f(n+1)   
    mpz_t return_val;                  //used for calculations
    mpz_t temp;                        //used for calculations as well

    mpz_init(ans);
    mpz_init(return_val);
    mpz_init(temp);
    mpz_init(mat[0][0]);
    mpz_init(mat[0][1]);
    mpz_init(mat[1][0]);
    mpz_init(mat[1][1]);

    mpz_set_ui(mat[0][0],1);
    mpz_set_ui(mat[1][0],1);
    mpz_set_ui(mat[0][1],1);
    mpz_set_ui(mat[1][1],0);

    if(n==0){
        mpz_set_ui(result,0);
        return 0;
    }
    if(n==1){
        mpz_set_ui(result,1);
        return 0;
    }
    if(n==2){
        mpz_set_ui(result,1);
        return 0;
    }

    n--;


    while(n>1)
    {

        mpz_set_ui(ans,0);

        mpz_mul_ui(temp,mat[0][0],cons[0][0]);
        mpz_add(ans,ans,temp);
        mpz_mul_ui(temp,mat[0][1],cons[1][0]);
        mpz_add(ans,ans,temp);

        //update matrix


        mpz_set(mat[1][1],mat[1][0]);   //mat[1][1]=mat[1][0];
        mpz_set(mat[1][0],mat[0][0]);   //mat[0][1]=mat[1][0]=mat[0][0];
        mpz_set(mat[0][1],mat[0][0]);
        mpz_set(mat[0][0],ans);         //mat[0][0]=ans;

        n--;
    }


    //clear vars
    mpz_clear(ans);
    mpz_clear(return_val);
    mpz_clear(temp);

    mpz_set(result,mat[0][0]);
    return 0;

}



//Main function: 

int main() 
{
  mpz_t two;
  mpz_set_ui(two, 2);

  bool firstEntry = true; //Variable used for formatting

  for(size_t j = 0; j <= 5; ++j)
  {
  size_t low_limit = j*1000;
  size_t top_limit = low_limit + 1000;

  //This block opens up a file in which our results will be written
  std::string flname = "2n_set-" + std::to_string(j) + ".txt";

  FILE *myfile;
  myfile = fopen(flname.c_str(), "wt");

  gmp_fprintf(myfile, "["); //Formatting

  for (size_t i = low_limit; i <= top_limit; ++i)
  {
      size_t z = i + i + 1; 
      mpz_t candidate, fibCandidate;
      mpz_set_ui(candidate, z); //Assigns an odd number index to candidate

      if (mpz_probab_prime_p(candidate, 2) && ((z % 5 == 2)||(z % 5 == 3))) //If our index is prime and +/- 2 mod 5:
      {
        mpz_t exp, res;

        mpz_init(fibCandidate);
        fastfib(fibCandidate, z + z); //Set fibCandidate to be the 2*z-th Fibonacci pseudoprime

        mpz_init(exp);
        mpz_init(res);

        mpz_sub_ui(exp, fibCandidate, 1);
        mpz_powm(res, two, exp, fibCandidate);

        if(!mpz_cmp_ui(res, 1)) //In the unlikely event that a base-2 pseudoprime is found:
        {
          gmp_fprintf(myfile, "Base-2 Pseudoprime found!\n"); //The result is reported
          return EXIT_SUCCESS;
        }

        else  //Else, we print in the format given in the README file.
        {
          if(firstEntry)  //This if statement exists solely to print it in the desired format.
          {
            gmp_fprintf(myfile, "[%d, %Zd, %Zd]", z, fibCandidate, res);
            firstEntry = false;
          }
          else
            gmp_fprintf(myfile, ", [%d, %Zd, %Zd]", z, fibCandidate, res);
        }
      }
  }
  gmp_fprintf(myfile, "]\n"); //Formatting
  fclose(myfile);
  firstEntry = true;
  }

  return EXIT_SUCCESS;
}
