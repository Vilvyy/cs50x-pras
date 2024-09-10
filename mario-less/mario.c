#include <cs50.h>
#include <stdio.h>

void triangle(int b);

int main(void)
{
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n <= 0);
    triangle(n);
}

void triangle(int b)
{
    for (int a = 0; a < b; a++)
    {
        for (int d = 0; d <= a; d++)
        {
            printf("#");
        }
        printf("\n");
    }
}
