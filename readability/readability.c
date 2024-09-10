#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

float avgLetters(string word);
float avgSents(string word);
int countIndex(float averageLetters, float averageSentences);

int main(void)
{
    string text = get_string("Text: ");
    float avgLetter = avgLetters(text);
    float avgSent = avgSents(text);
    int grade = countIndex(avgLetter, avgSent);

    if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (grade > 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}

float avgLetters(string word)
{
    int textLength = strlen(word);
    float realTextLength = 0;
    float totalNumWords = 0;
    for (int i = 0; i <= textLength; i++)
    {
        // count the number of letters
        if (toupper(word[i]) >= 65 && toupper(word[i]) <= 90)
        {
            realTextLength++;
        }

        // count the total number of words
        if (word[i] == 32)
        {
            totalNumWords++;
        }
        else if (word[i] == 0)
        {
            totalNumWords++;
        }
    }
    float avgLetters = (realTextLength / totalNumWords) * 100.0;
    return avgLetters;
}

float avgSents(string word)
{
    int textLength = strlen(word);
    float totalSent = 0;
    float totalNumWords = 0;
    for (int i = 0; i <= textLength; i++)
    {
        // count the number of sentences
        // condition to check for exclamation points "!"
        if (word[i] == 33)
        {
            totalSent++;
        }
        // condition to check for question marks "?"
        else if (word[i] == 63)
        {
            totalSent++;
        }
        // condition to check for full stops "."
        else if (word[i] == 46)
        {
            totalSent++;
        }

        // count the total number of words
        if (word[i] == 32)
        {
            totalNumWords++;
        }
        else if (word[i] == 0)
        {
            totalNumWords++;
        }
    }
    float avgSent = (totalSent / totalNumWords) * 100.0;
    return avgSent;
}

int countIndex(float averageLetters, float averageSentences)
{
    float index = 0.0588 * averageLetters - 0.296 * averageSentences - 15.8;
    int grade = round(index);
    if (index < 1)
    {
        return 0;
    }
    else
    {
        return grade;
    }
}
