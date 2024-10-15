from cs50 import get_float


def main():
    kembalian = 0
    while True:
        if kembalian > 0:
            break
        kembalian = get_float("Change owed: ")
    calc_kembalian(kembalian)


def calc_kembalian(kembali):
    DULI = 25
    PULU = 10
    LIMA = 5
    SATU = 1

    kembali = kembali * 100
    hasil_bagi = 0
    jumlah_koin = 0
    sisa = 0

    hasil_bagi = kembali // DULI
    jumlah_koin = hasil_bagi
    sisa = kembali % DULI

    if sisa != 0:
        hasil_bagi = sisa // PULU
        jumlah_koin += hasil_bagi
        sisa = sisa % PULU

    if sisa != 0:
        hasil_bagi = sisa // LIMA
        jumlah_koin += hasil_bagi
        sisa = sisa % LIMA

    if sisa != 0:
        hasil_bagi = sisa // SATU
        jumlah_koin += hasil_bagi
        sisa = sisa % SATU

    print(jumlah_koin)


main()
