#include<stdio.h>
int main(){
    int n,x,a[100],i,mid,first,last;
    scanf("%d",&n);
    first=0;
    last=n-1;
    mid=(first+last)/2;
    
   for(i=0;i<n;i++){
   scanf("%d",&a[i]);}
   scanf("%d",&x);
   
   while(first<=last)
   {
       if(a[mid]<x)
       first=mid+1;
       if(a[mid]==x)
       {
           printf("%d is found at %d",x,mid+1);
           break;
        }
       else
       last=mid-1;
       mid=(first+last)/2;
   }
   if(first>last)
   printf("not found");
    return 0;
}
