#include <stdio.h>
#include "PythonC.h"

int add_numbers(int a, int * in, int * out)
{
    int i = 0;
    int sum = 0;

    
    for(i = 0; i < a; i++){
      sum += in[i];
      out[i] = sum;
    }
    
    return sum;
}
