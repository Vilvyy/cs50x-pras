#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int skor1(string word);
int skor2(string word);
void cekSkor(int word1, int word2);

int main(void)
{
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    int score1 = skor1(word1), score2 = skor2(word2);

    cekSkor(score1, score2);
}

int skor1(string word)
{
    int skor = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        if (toupper(word[i]) - 65 >= 0 && toupper(word[i]) - 65 <= 25)
        {
            skor += POINTS[toupper(word[i]) - 65];
        }
    }
    return skor;
}

int skor2(string word)
{
    int skor = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        if (toupper(word[i]) - 65 >= 0 && toupper(word[i]) - 65 <= 25)
        {
            skor += POINTS[toupper(word[i]) - 65];
        }
    }
    return skor;
}

void cekSkor(int word1, int word2)
{
    if (word1 > word2)
    {
        printf("Player 1 wins!\n");
    }
    else if (word1 < word2)
    {
        printf("Player 2 wins!\n");
    }
    else if (word1 == word2)
    {
        printf("Tie!\n");
    }
    else
    {
        printf("Error\n");
    }
}
