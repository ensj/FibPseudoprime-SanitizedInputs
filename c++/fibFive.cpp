#include <iostream>
#include <gmp.h>  //Required for MPZ Integers, which is what allows us to use big numbers for calculations.



//Fast Fibonacci Calculator: A proven and optimized method for computing large Fibonacci numbers. Credits to ----. 

int fastfib(mpz_t result, int n)
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



//Main Function: Conducts the rest of the process

int main() 
{
  std::vector<__mpz_struct> test;
  mpz_t two;
  mpz_set_ui(two, 2); //This sets two as 2, allowing us to use it as a MPZ Integer.

  std::cout << "["; //Formatting
  bool firstEntry = true; //Variable only exists for formatting purposes.

  for (size_t i = 1; i <= 50000; ++i)
  {
    mpz_t candidate, fibCandidate;
    mpz_set_ui(candidate, i + i + 1); //Set Candidate to the index: (2*i + 1.)
  
    if (mpz_probab_prime_p(candidate, 2)) //If the index is prime:
    {
      mpz_init(fibCandidate);
      fastfib(fibCandidate, i + i + 1); //Set fibCandidate to the (2*i + 1)th Fibonacci number.

      if(mpz_probab_prime_p(fibCandidate, 2)) //If the Fibonacci number is prime, do nothing.
      {;}
      
      else //If the Fibonacci number is not prime:
      {
        mpz_t exp, res;

        mpz_init(exp);
        mpz_init(res);

        mpz_sub_ui(exp, fibCandidate, 1);
        mpz_powm(res, two, exp, fibCandidate);

        if(!mpz_cmp_ui(res, 1)) //In the unlikely event that a base-2 pseudoprime is found:
        {
          std::cout << "Base-2 Pseudoprime found!" << std::endl;  //This result is reported
          return EXIT_SUCCESS;
        }

        else  //Else, we print in the format given in the README file.
        {

          if(firstEntry)  //This if statement exists solely to print it in the desired format.
          {
            gmp_printf("[%d, %Zd, %Zd]", i + i + 1, fibCandidate, res);
            firstEntry = false;
          }

          else
            gmp_printf(", [%d, %Zd, %Zd]", i + i + 1, fibCandidate, res);
        }
      
      }

    }

  }

  std::cout << "]" << std::endl; //Formatting

  return EXIT_SUCCESS;
}
