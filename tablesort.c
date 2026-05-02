#include<stdio.h>
#include<stdlib.h>

struct node{
    char name[10];
    int points;
    float nrr;

};

void insertionsort(struct node team[])
{ for(int i=1;i<10;i++)
    {
        struct node key=team[i];
        int j= i-1;
        while(j>=0 && (team[j].points<key.points|| (team[j].points==key.points && team[j].nrr<key.nrr)))
        {
            team[j+1]=team[j];
            j--;
            
        }
        team[j+1]=key;
    }
    
}

int main()
{
   struct node team[10]={
   {"CSK",6,-0.121},
   {"KKR",5,-0.751},
   {"RCB",12,1.420},
   
   {"LSG",4,-1.106},

   {"GT",10,-0.192},
   {"DC",8,-0.895},
   {"PBKS",13,1.043},
   {"RR",12,0.510},
   {"MI",4,-0.784},
   {"SRH",12,0.832},
   
     
   };

   insertionsort(team);
   printf("Team \t Points \t NRR \n");
   for(int i=0;i<10;i++)
   { 
    printf("%s \t %d \t %.3f \n",team[i].name,team[i].points,team[i].nrr);

   }
   return 0;
}
