#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    int n = argc - 1;
    if (n == 0) {
        printf("Usage: %s <num1> <num2> ... <numN>\n", argv[0]);
        return 1;
    }

    int arr[n];
    for (int i = 0; i < n; i++) {
        arr[i] = atoi(argv[i + 1]);
    }

    printf("%d", find_largest(arr, n));
    return 0;
}

int find_largest(int arr[], int n) {
    int max = arr[0];
    for (int i = 0; i < n; i++) { 
        if (arr[i] > max)
            max = arr[i];
    }
    return max;
}
