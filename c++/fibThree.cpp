#include <iostream>
#include <gmp.h>

int main() {
  mpz_t two;
  mpz_set_ui(two, 2);

  std::cout << "[";
  bool firstEntry = true;

  for (size_t i = 0; i <= 1000000; ++i)
  {
    mpz_t first, sec, product, res, exp;
    mpz_set_ui(first, ((10 * i) + 7));
    mpz_set_ui(sec, ((10 * i) + 9));
  
    if (mpz_probab_prime_p(first, 2) && mpz_probab_prime_p(sec, 2))
    {
      mpz_init(product);
      mpz_init(res);
      mpz_init(exp);

      mpz_mul(product, first, sec);
      mpz_sub_ui(exp, product, 1);
      //gmp_printf("%Zd, %Zd: ", exp, product);
      mpz_powm(res, two, exp, product);

      if(!mpz_cmp_ui(res, 1))
      {
        std::cout << "Base-2 Pseudoprime found!" << std::endl;
        return EXIT_SUCCESS;
      }

      else
      {
        if(firstEntry)
        {
          gmp_printf("[%d, %Zd]", ((10 * i) + 7), res);
          firstEntry = false;
        }
        else
          gmp_printf(", [%d, %Zd]", ((10 * i) + 7), res);
      }

    }
  }

  std::cout << "]" << std::endl;

  return EXIT_SUCCESS;
}
