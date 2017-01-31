#include <stdio.h>

#define IsBitSet(val, bit) ((val) & (1 << (bit)))

static inline void native_cpuid(unsigned int *eax, unsigned int *ebx,
                                unsigned int *ecx, unsigned int *edx) {
        /* ecx is often an input as well as an output. */
        asm volatile("cpuid"
            : "=a" (*eax),
              "=b" (*ebx),
              "=c" (*ecx),
              "=d" (*edx) 
            : "0" (*eax), "2" (*ecx));
}

int main()
{
  unsigned int a, b, c, d, i;

  // check Intel MPX bit (EAX=07H, ECX=0H), bit 14 in EBX
  // this indicates that the CPU supports MPX
  a = 0x7; b = c = d = 0;
  native_cpuid(&a, &b, &c, &d);
  printf("[00] Intel MPX bit:    %c\n", IsBitSet(b, 14) ? '1' : '0');

  // check XCR0 bits -- BNDREGS and BNDCSR
  // instead of XCR0 we can use CPUID: (EAX=0DH, ECX=0), bits 3 and 4
  // these two bits indicate that OS supports MPX
  a = 0xD; b = c = d = 0;
  native_cpuid(&a, &b, &c, &d);
  printf("[01] XCR0 BNDREGS bit: %c\n", IsBitSet(a, 3) ? '1' : '0');
  printf("[02] XCR0 BNDCSR  bit: %c\n", IsBitSet(a, 4) ? '1' : '0');

  return 0;
}
