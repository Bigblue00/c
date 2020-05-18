#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main() {
	
    int n;
    scanf("%d", &n);
    int sum=0,t,rem;
    t=n;
    while(t!=0)
    {
        rem=t%10;
        sum=sum+rem;
        t=t/10;
    }
    printf("%d",sum);
    return 0;
}
