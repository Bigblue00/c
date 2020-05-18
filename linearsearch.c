#include<stdio.h>
int main()
{
int n,x,a[100],count=0,i;
scanf("%d",&n);

for(i=0;i<n;i++)
scanf("%d",&a[i]);

scanf("%d",&x);
for(i=0;i<n;i++)
if(a[i]==x)
count++;

if(count>0)
printf("found");
else
printf("not found")
return 0;
}
