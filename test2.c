#include <stdio.h>

int main() {
    int a = 5;
    int b = 10;
    int c = 15;

    // Operador &&
    if (a > 0 && b > 0) {
        printf("Ambas variables son mayores que cero\n");
    }

    // Operador ||
    if (a > 0 || b > 0) {
        printf("Al menos una de las variables es mayor que cero\n");
    }

    // Operador <=
    if (a <= b) {
        printf("a es menor o igual que b\n");
    }

    // Operador >=
    if (c >= b) {
        printf("c es mayor o igual que b\n");
    }

    // Operador ++
    a++;
    printf("El valor de a después de incrementarlo es: %d\n", a);

    // Operador --
    c--;
    printf("El valor de c después de decrementarlo es: %d\n", c);

    return 0;
}