#include <stdio.h>
#include "pico/stdlib.h"

int main() {

    // Initialize chosen serial port
    stdio_init_all();

    // Loop forever
    while (true) {
    
            // Echo serial input
            char c = getchar();
            putchar(c);
    }
}