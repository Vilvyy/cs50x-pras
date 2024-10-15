#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
} candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i].name, name) == 0)
        {
            candidates[i].votes += 1;
            return true;
        }
    }
    return false;
}

// Bubble sort to sort candidates by votes in descending order
void bubble_sort(void)
{
    for (int i = 0; i < candidate_count - 1; i++)
    {
        for (int j = 0; j < candidate_count - i - 1; j++)
        {
            if (candidates[j].votes < candidates[j + 1].votes)
            {
                // Swap if the current candidate has fewer votes than the next
                candidate temp = candidates[j];
                candidates[j] = candidates[j + 1];
                candidates[j + 1] = temp;
            }
        }
    }
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    // Sort candidates by votes using bubble sort
    bubble_sort();

    // Find the highest number of votes
    int highest_votes = candidates[0].votes;

    // Print the candidate(s) with the highest number of votes
    printf("%s\n", candidates[0].name);
    for (int i = 1; i < candidate_count; i++)
    {
        if (candidates[i].votes == highest_votes)
        {
            printf("%s\n", candidates[i].name);
        }
        else
        {
            return;
        }
    }
    return;
}
