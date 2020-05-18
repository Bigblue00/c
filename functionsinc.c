#include <stdio.h>
/*
Add `int max_of_four(int a, int b, int c, int d)` here.
*/
int max_of_four(int a,int b, int c,int d)
{
    if(a+b+c>d)
    {
        if(a>b && b>c)
        return a;
        else{ 
        if(b>c)
        return b;
        else
        return c;
        }
    }
    if(d>a+b+c)
    return d;
    return 0;
}
int main() {
    int a, b, c, d;
    scanf("%d %d %d %d", &a, &b, &c, &d);
      
    printf("%d", max_of_four(a, b, c, d));
return 0;
}
