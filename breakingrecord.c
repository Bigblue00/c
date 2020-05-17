#include<stdio.h>
int main(){
int n,a[1000],i,max,min,cmax=0,cmin=0,h[1000],l[1000];
scanf("%d",&n);
for(i=0;i<n;i++)
scanf("%d",&a[i]);
for(i=0;i<n;i++)
{
    h[i]=a[i];
    l[i]=a[i];
}
min=l[0];
max=h[0];
for(i=0;i<n;i++){
if(min<=l[i]){
l[i]=min;
//printf("%d\t",min);
}
if(min>l[i]){
min=l[i];
  //  printf("%d\t",l[i]);
}
}
//printf("\n");
for(i=0;i<n;i++){
if(h[i]>=max){
max=h[i];
   // printf("%d\t",h[i]);
}
if(h[i]<max){
h[i]=max;
  //  printf("%d\t",max);
}
}
//printf("\n");
for(i=0;i<=n-1;i++){
if(h[i]<h[i+1])
cmax++;}
printf("%d ",cmax);
for(i=0;i<=n-1;i++){
if(l[i+1]<l[i])
cmin++;}
printf("%d",cmin);
return 0;
}
