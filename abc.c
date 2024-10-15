#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // get input from user
    int hits = get_int("Hits: ");
    int baseDMG = 100;
    int bonusDMG = 50;
    int totalBonusDMG = 0;

    if (hits == 1)
    {
        printf("100\n");
        return 0;
    }
    else
    {
        for (int i = 0; i < hits - 1; i++)
        {
            totalBonusDMG += bonusDMG;
            bonusDMG += 50;
        }
        int totalDMG = (hits * baseDMG) + totalBonusDMG;
        printf("%i\n", totalDMG);
        return 0;
    }
}
