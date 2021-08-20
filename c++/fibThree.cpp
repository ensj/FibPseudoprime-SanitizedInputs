#include <iostream>
#include <gmp.h>

int main() {
  mpz_t two;
  mpz_set_ui(two, 2);

  std::cout << "["; //Formatting
  bool firstEntry = true; //Variable only exists for formatting

  for (size_t i = 0; i <= 1000000; ++i)
  {
    mpz_t first, sec, product, res, exp;

    //This block generates all pairs that are 7 and 9 mod 10. 
    mpz_set_ui(first, ((10 * i) + 7)); 
    mpz_set_ui(sec, ((10 * i) + 9));
  
    if (mpz_probab_prime_p(first, 2) && mpz_probab_prime_p(sec, 2)) //If both numbers are prime:
    {
      mpz_init(product);
      mpz_init(res);
      mpz_init(exp);

      mpz_mul(product, first, sec);
      mpz_sub_ui(exp, product, 1);
      mpz_powm(res, two, exp, product);

      if(!mpz_cmp_ui(res, 1))
      {
        std::cout << "Base-2 Pseudoprime found!" << std::endl;
        return EXIT_SUCCESS;
      }

      else
      {
        if(firstEntry)  //If statement is only for formatting
        {
          gmp_printf("[%d, %Zd]", ((10 * i) + 7), res);
          firstEntry = false;
        }
        else
          gmp_printf(", [%d, %Zd]", ((10 * i) + 7), res);
      }

    }
  }

  std::cout << "]" << std::endl; //Formatting

  return EXIT_SUCCESS;
}
