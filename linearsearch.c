#include<stdio.h>
int main()
{
    int i,a[100],x,n,count=0;
    scanf("%d",&n);
    for(i=0;i<n;i++){
    scanf("%d",&a[i]);
    }
    scanf("%d",&x);
    for(i=0;i<n;i++)
    {
        if(a[i]==x)
        {
            count++;
            if(count>0)
            {   
            printf("%d is present %d times at %d\n",x,count,i+1);
            }
        }
    }
    
    return 0;
}
