#include<stdio.h>
int main()
{
    int n,i,a[10],x,pos;
    scanf("%d",&n);
    for(i=0;i<n;i++)
        scanf("%d",&a[i]);
    
    scanf("%d",&x);
    scanf("%d",&pos);
    for(i=n-1;i>=pos-1;i--)
        a[i+1]=a[i];
    a[pos-1]=x;
    for(i=0;i<=n;i++)
        printf("%d\t",a[i]);
    return 0;
}
