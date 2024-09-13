#include <stdio.h>

int main() {
    int num = 10;
    int *ptr;

    ptr = &num;

    printf("El valor de num es: %d\n", num);
    printf("La dirección de num es: %p\n", &num);
    printf("El valor de ptr es: %p\n", ptr);
    printf("El valor al que apunta ptr es: %d\n", *ptr);

    return 0;
}