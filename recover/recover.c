#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Accept a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    // Open the memory card
    FILE *card = fopen(argv[1], "r");
    if (card == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // Create a buffer for a block of data
    uint8_t buffer[512];

    // While there's still data left to read from the memory card
    char filename[50];
    int i = 0;
    FILE *img = NULL;
    while (fread(&buffer, 1, 512, card) == 512)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // This is the start of a new JPEG
            if (img != NULL)
            {
                fclose(img);
            }

            sprintf(filename, "%03i.jpg", i);
            img = fopen(filename, "w");
            i++;
        }
        if (img != NULL)
        {
            fwrite(buffer, sizeof(uint8_t), 512, img);
        }
    }

    if (img != NULL)
    {
        fclose(img);
    }

    // Close the memory card file
    fclose(card);
    return 0;
}
