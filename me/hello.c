#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // get input from user
    string name = get_string("What is your name?\n");
    // output
    printf("Hello, %s\n", name);
}
