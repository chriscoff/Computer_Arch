#include<stdio.h>

void main()
{
    int n=100000;
    int array1[100000];
    int array_size=0;
    int j, i, k, temp;

    printf("Finding Primes:\n");

    for(i=2;i<=n;i++)
    {
        int c=0;
        for(j=1;j<=i;j++)
        {
            if(i%j==0)
            {
                c++;
            }
        }

       if(c==2)
        {
            printf("%d ",i);
            array1[array_size] = i;
            array_size++;
        }
    }
    printf("Multiplying Primes:\n");
    for(k=0; k<array_size;k++)
    {
        temp = array1[array_size-k]*array1[k] ;
        printf("%d ", temp);
    }
    printf("Done:\n");
}
