#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

string cypher(string text, int cypherKey);

int main(int argc, string argv[])
{
    if (argc <= 0)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    else if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    for (int i = 0, n = strlen(argv[1]); i < n; i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }

    int key = atoi(argv[1]);
    string plainText = get_string("plaintext: ");
    string encryptedText = cypher(plainText, key);
    printf("ciphertext: %s\n", encryptedText);
}

string cypher(string text, int cypherKey)
{
    int lengthText = strlen(text);
    int key = cypherKey % 26;

    for (int i = 0; i < lengthText; i++)
    {
        if (isupper(text[i]))
        {
            text[i] = ((text[i] - 'A' + key) % 26) + 'A';
        }
        else if (islower(text[i]))
        {
            text[i] = ((text[i] - 'a' + key) % 26) + 'a';
        }
    }

    return text;
}
