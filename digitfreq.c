#include<stdio.h>
int main()
{
    char s[100];
    int i,j,count=0;
    scanf("%s",s);
    for(j=0;j<10;j++)
    {
    for(i=0;s[i]!='\0';i++)
    {
        if(s[i]-48==j)
        count++;
    }
    printf("%d",count);
    count=0;
    }
    
    return 0;
}
