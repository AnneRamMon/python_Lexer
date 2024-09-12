#include <stdio.h>

int main() {
    int num1, num2;
    char g = 'g';

    printf("Ingrese el primer número: ");
    scanf("%d", &num1);

    printf("Ingrese el segundo número: ");
    scanf("%d", &num2);

    if (num1 > num2) {
        printf("%d es mayor que %d\n", num1, num2);
    } else if (num1 < num2) {
        printf("%d es menor que %d\n", num1, num2);
    } else {
        printf("Ambos números son iguales\n");
    }

    return 0;
}