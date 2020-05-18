#include <stdio.h>

int main()
{
  char ch;
  char s[10];
  char sen[100];
  
  scanf("%c%*c",&ch);
  scanf("%s%*c",s);
  scanf("%n");
  scanf("%[\^n]",sen);
  printf("%c\n%s\n%s",ch,s,sen);
return 0;
}
