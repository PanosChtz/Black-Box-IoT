#include <uECC.h>

extern "C" {
static int RNG(uint8_t *dest, unsigned size);
}

extern "C" {

static int RNG(uint8_t *dest, unsigned size) {

  while (size) {
    uint8_t val = 0;
    for (unsigned i = 0; i < 8; ++i) {
      int init = analogRead(0);
      int count = 0;
      while (analogRead(0) == init) {
        ++count;
      }
      
      if (count == 0) {
         val = (val << 1) | (init & 0x01);
      } else {
         val = (val << 1) | (count & 0x01);
      }
    }
    *dest = val;
    ++dest;
    --size;
  }
  return 1;
}

}  

void setup() {
  Serial.begin(115200);
  uECC_set_rng(&RNG);

  const struct uECC_Curve_t * curve = uECC_secp256k1();
  uint8_t private2[32];
  
  uint8_t public2[64];


  uint8_t signature[256];
  unsigned long a = micros();
  uECC_sign(private2, private2, 2048, signature, curve);
  unsigned long b = micros();
  Serial.print("Signed in "); Serial.println(b-a);
int counter = 0;
while (1) {

  
  uECC_sign(private2, private2, 2048, signature, curve);
  Serial.println(counter++);
}

}

void loop() {

}
