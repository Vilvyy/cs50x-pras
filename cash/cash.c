#include <cs50.h>
#include <math.h>
#include <stdio.h>

int const duli = 25;
int const pulu = 10;
int const lima = 5;
int const satu = 1;

int hasil_bagi;
int jumlah_koin;
int sisa;

void kembalian(int change);

int main(void)
{
    int c;
    do
    {
        c = get_int("Change owed: ");
    }
    while (c <= 0);
    kembalian(c);
}

void kembalian(int change)
{

    hasil_bagi = change / duli;
    jumlah_koin = hasil_bagi;
    sisa = change % duli;

    if (sisa != 0)
    {
        hasil_bagi = sisa / pulu;
        jumlah_koin = jumlah_koin + hasil_bagi;
        sisa = sisa % pulu;
    }

    if (sisa != 0)
    {
        hasil_bagi = sisa / lima;
        jumlah_koin = jumlah_koin + hasil_bagi;
        sisa = sisa % lima;
    }

    if (sisa != 0)
    {
        hasil_bagi = sisa / satu;
        jumlah_koin = jumlah_koin + hasil_bagi;
        sisa = sisa % satu;
    }
    printf("%i\n", jumlah_koin);
}
