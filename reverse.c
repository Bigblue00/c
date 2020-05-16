#include<stdio.h>
int main(){
    int t,n,rev=0,rem;
    scanf("%d",&n);
    t=n;
    while(t!=0)
    {
        rem=t%10;
        rev=rev*10+rem;
        t=t/10;
    }
    printf("%d",rev);
    return 0;
}
