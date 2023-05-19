#include<stdio.h>
void main()
{
    int i = 0;
    int j = 0;
    if (i++ == j++)
    {
        printf("%d %d",i++,j);
    }
    else{
        printf("%d %d", i+1,j);
    }
}