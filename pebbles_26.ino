#include <Crypto.h>
#include <SHA256.h>

#define HASH_SIZE 32
#define BLOCK_SIZE 64
#define OUTPUT_MAX 32

const byte SIGMA = 26;

char hex[64];
SHA256 hash;
byte bytearray_buffer[32];

const char pebble0[] PROGMEM = "810b2ded826a69f7194fc5a1166c9b8dfad59303ce4d74eb0df021338af12804";
const char pebble1[] PROGMEM = "5e7f77b3b7046e2b034bea699ca502564c1704566d985b3dd0bbb1a0f0ab54e7";
const char pebble2[] PROGMEM = "3b563f0ac22ce38784a7428798548d8d8ee648053e99804f6076f148162d69c7";
const char pebble3[] PROGMEM = "b0f08e74c3571040052eba10d577b1ce853e73815dc51f043336b75478cce5a7";
const char pebble4[] PROGMEM = "9c1cf0651f8fc795b208eca7dbfbc81cce19cc622b417c8024496cb9911c4a09";
const char pebble5[] PROGMEM = "0b01f249302c82dfe6903f5b92975cbca46e39a1df10a502621591b50ca01bdd";
const char pebble6[] PROGMEM = "faca232ad8f3dbf15fab90e02d0dce613364f6520081f1b26505c93e1a3c2c10";
const char pebble7[] PROGMEM = "015d06a3c3f310009c1ff3e358d14954d0e02064b738646291ad3af9ed818db9";
const char pebble8[] PROGMEM = "edf5a7ca6f11b47c4ba013107221c612ced03c5ad7a601b7ae722a7848def0d5";
const char pebble9[] PROGMEM = "2dd96cbb741ef9f6d8b2799cbda2b83db4b000989ccc0c1060fddb487df22ec4";
const char pebble10[] PROGMEM = "d6d35e5e452cc8a979687173c8e7b7dde36015e2bac2b9b17e0ed60b1fff2ed7";
const char pebble11[] PROGMEM = "df8a17364beb1ead3b8d81e98423f1d79ddd7fe99601c6cf30362068e9bfaae7";
const char pebble12[] PROGMEM = "12acc19d704a270908d0456abc486e61f36962bfe4f716a2980b12956fa721ee";
const char pebble13[] PROGMEM = "e3b639727a53b85e28ada35cbd61684852d40db8e23263b27bac56881cc6ecc5";
const char pebble14[] PROGMEM = "14475252e0e28f9bb1b63c22e4cbbc5d86c18c73e190cdaaeab6748d483c8976";
const char pebble15[] PROGMEM = "150b44622f07f644bd3d6e31894b4e84a813a10df26bf8124d7399066e9bb9d2";
const char pebble16[] PROGMEM = "a25e7c196f791399d592038675d314fe3891ed91ecf9143f3ee9c13f3e62f334";
const char pebble17[] PROGMEM = "0c6fa156eb8c57432a1f5d4c20ab008b8343b8c1f7b93ba51bc710e1855295a0";
const char pebble18[] PROGMEM = "2d17441ac63a588b206efd9025ff97dd7ab1aa23ebf4831911681a8393914a2c";
const char pebble19[] PROGMEM = "534b1cc5f7bfe96b0c70ac46193e22ada10539abf68ac4ffa81ec053ca20118c";
const char pebble20[] PROGMEM = "58171819b2b32d5b41a537e62a896f2274086d6c38f87e3d14c6e6e2d0be4ef8";
const char pebble21[] PROGMEM = "bbb367653598026c50bb57cae7ffbce9db26aabb1c514688c2924d76d61de275";
const char pebble22[] PROGMEM = "0d6e3ac647e6a2bf501e9c64e12c3b682b1274c640092bad3d7be25f6e4b7447";
const char pebble23[] PROGMEM = "29753ef8800e97b0b7fecfe345d8f0a78c949ed748dac4b79c735bca88d4e62d";
const char pebble24[] PROGMEM = "efd4aa45e99d634df75b3c366a3d305bcc36654ce42a2b2ccbf400baf733c59a";
const char pebble25[] PROGMEM = "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3";


const char* const initpebbles[] PROGMEM = {pebble0, pebble1, pebble2, pebble3, pebble4, pebble5, pebble6, pebble7, pebble8, pebble9, pebble10, pebble11, pebble12, pebble13, pebble14, pebble15, pebble16, pebble17, pebble18, pebble19, pebble20, pebble21, pebble22, pebble23, pebble24, pebble25};

char *btoh(char *dest, uint8_t *src, int len) {
  char *d = dest;
  while ( len-- ) sprintf(d, "%02x", (unsigned char)*src++), d += 2;
  return dest;
}

char* h(char* input) {
  uint8_t result[32];
  hash.reset();
  hash.update(input, strlen(input));
  hash.finalize(result, sizeof(result));

  return (btoh(hex, result, 32));
}

void hexCharacterStringToBytes_P(byte *byteArray, byte initPebbleNumber)
{
  char* ptr = (char *) pgm_read_word (&initpebbles [initPebbleNumber]);
  byte pebbleLength = sizeof(pebble0) - 1; // length of pebble0 less null terminator character
  bool oddLength = pebbleLength & 1;

  byte currentByte = 0;
  byte byteIndex = 0;

  for (byte charIndex = 0; charIndex < pebbleLength; charIndex++)
  {
    bool oddCharIndex = charIndex & 1;

    if (oddLength)
    {
      if (oddCharIndex)
      {
        currentByte = nibble(pgm_read_byte(ptr + charIndex)) << 4;
      }
      else
      {
        currentByte |= nibble(pgm_read_byte(ptr + charIndex));
        byteArray[byteIndex++] = currentByte;
        currentByte = 0;
      }
    }
    else
    {
      if (!oddCharIndex)
      {
        currentByte = nibble(pgm_read_byte(ptr + charIndex)) << 4;
      }
      else
      {
        currentByte |= nibble(pgm_read_byte(ptr + charIndex));
        byteArray[byteIndex++] = currentByte;
        currentByte = 0;
      }
    }
  }
}



void hexCharacterStringToBytes(byte *byteArray, char *hexString)
{
  bool oddLength = strlen(hexString) & 1;

  byte currentByte = 0;
  byte byteIndex = 0;

  for (byte charIndex = 0; charIndex < strlen(hexString); charIndex++)
  {
    bool oddCharIndex = charIndex & 1;

    if (oddLength)
    {
      if (oddCharIndex)
      {
        currentByte = nibble(hexString[charIndex]) << 4;
      }
      else
      {
        currentByte |= nibble(hexString[charIndex]);
        byteArray[byteIndex++] = currentByte;
        currentByte = 0;
      }
    }
    else
    {
      if (!oddCharIndex)
      {
        currentByte = nibble(hexString[charIndex]) << 4;
      }
      else
      {
        currentByte |= nibble(hexString[charIndex]);
        byteArray[byteIndex++] = currentByte;
        currentByte = 0;
      }
    }
  }
}

byte nibble(char c)
{
  if (c >= '0' && c <= '9')
    return c - '0';

  if (c >= 'a' && c <= 'f')
    return c - 'a' + 10;

  if (c >= 'A' && c <= 'F')
    return c - 'A' + 10;

  return 0;  // Not a valid hexadecimal character
}

void array_to_string(byte array[], byte len, char buffer[])
{
  for (unsigned int i = 0; i < len; i++)
  {
    byte nib1 = (array[i] >> 4) & 0x0F;
    byte nib2 = (array[i] >> 0) & 0x0F;
    buffer[i * 2 + 0] = nib1  < 0xA ? '0' + nib1  : 'a' + nib1  - 0xA;
    buffer[i * 2 + 1] = nib2  < 0xA ? '0' + nib2  : 'a' + nib2  - 0xA;
  }
  buffer[len * 2] = '\0';
}


//Pebble code


//Stop function
void stop()
{
  while (1);
}

typedef struct Pebble {
  byte StartIncr;
  byte DestIncr;
  unsigned long position;
  unsigned long destination;
  byte value[32];
};

void FindValue(struct Pebble pebble_List[])
{
  for (byte i = 1; i < SIGMA; i++)
  {
    if (pebble_List[i].position == pebble_List[0].position) {
      for (int j = 0; j < 32; j++) {
        bytearray_buffer[j] = pebble_List[i].value[j];
      }

    }
  }
}

int struct_cmp_by_destin(const void *a, const void *b)
{
  struct Pebble *ia = (struct Pebble *)a;
  struct Pebble *ib = (struct Pebble *)b;
  if (ia->destination == ib->destination) {
    return (0);
  } else if (ia->destination > ib->destination) {
    return (1);
  } else {
    return (-1);
  }
}

uint32_t Pow2(uint32_t ex) {
  return (uint32_t)1 << ex;
}

Pebble pebblelist[SIGMA];

void setup()
{
  Serial.begin(115200);


  for (byte i = 0; i < SIGMA; i++) {
    pebblelist[i].StartIncr = i + 1;
    pebblelist[i].DestIncr = (i + 2) ;
    pebblelist[i].position = Pow2(i + 1);
    pebblelist[i].destination = Pow2(i + 1);
  }

  for (byte i = 0; i < SIGMA; i++) {
    hexCharacterStringToBytes_P(pebblelist[i].value, i);
  }

  unsigned long currentposition = 0;

  char temp[64]  = "";
  char* hashoutput;
  unsigned long start = micros();
  while (currentposition <1000) {
    Serial.print("Hash ");
    Serial.println(currentposition);

    //1
    if (currentposition >= Pow2(SIGMA) ) {
      stop();
    }
    else {
      currentposition++ ;
    };
    //2
    for (byte i = 0; i < SIGMA; i++) {
      if (pebblelist[i].position != pebblelist[i].destination) {
        pebblelist[i].position = pebblelist[i].position - 2;
        array_to_string(pebblelist[i].value, 32, temp);
        hashoutput = h( h( temp ) );
        hexCharacterStringToBytes(pebblelist[i].value, hashoutput);
      };
    }
    char* output;
    //3
    if (currentposition % 2 == 1 ) {
      array_to_string(pebblelist[0].value, 32, temp);
      output =  h( temp );

    }
    else {

      array_to_string(pebblelist[0].value, 32, output);
      pebblelist[0].position = pebblelist[0].position + (3 * Pow2(pebblelist[0].StartIncr));
      pebblelist[0].destination = pebblelist[0].destination + Pow2(pebblelist[0].DestIncr);
      if (pebblelist[0].destination > Pow2(SIGMA) ) {
        pebblelist[0].destination = Pow2(SIGMA + 1);
        pebblelist[0].position = Pow2(SIGMA + 1);
      }
      else {
        FindValue(pebblelist);

        for (int i = 0; i < 32; i++) {
          pebblelist[0].value[i] = bytearray_buffer[i];
        }

      };
      qsort(pebblelist, sizeof(pebblelist) / sizeof(pebblelist[0]), sizeof(pebblelist[0]), struct_cmp_by_destin);
    };
    Serial.println(output);
  }
  unsigned long end = micros();
  unsigned long delta = end - start;
  Serial.println(delta);
}

void loop()
{
}
