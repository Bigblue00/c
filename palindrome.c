#include<stdio.h>
int main(){
    int x,n,rev=0,t,rem;
    scanf("%d",&n);
    t=n;
    
while(t!=0)
{
    rem=t%10;
    rev=rev*10+rem;
    t=t/10;
}
    x=(n+rev)/2;
    if(x==n && n>10)
    printf("%d is pal",n);
    else
    printf("%d not a pal",n);
    return 0;
}
