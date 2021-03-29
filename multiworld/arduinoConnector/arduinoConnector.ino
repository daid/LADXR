/**
 * Arduino<->Gameboy Serial Multiworld connector
 * 
 * Link port pins:
 * Viewing the connector on the cable head on
 *       /-----------\
 *      / [1] [2] [3] \  
 *     /               \
 *     |  [4] [5] [6]  |
 *     +---------------+
 * (colors of wires in cable will vary)
 * 
 * Connect the following Arduino pins to an Gameboy link cable pins:
 * Arduino (Nano pin)    Link cable (Name on breakout board)
 * MISO (D12)         -> [2] (SI)
 * MOSI (D11)         -> [4] (SO)
 * SCK  (D13)         -> [3] (SC)
 * SS   (D10)         -> GND
 * GND                -> [6] (GND)
 * Do not connect the other link cable pins.
 */


void initSPI()
{
  SPCR = 0;
  pinMode(MISO, OUTPUT);
  SPCR = _BV(SPE) | _BV(CPOL) | _BV(CPHA);
  SPDR = 0xFF;
}

void setup() {
  Serial.begin(115200);
  initSPI();
}

//Transfer a byte and setup the next byte to transfer, with a timeout less then a frame time, so we can resolve framing errors.
int transferShortTimeout(uint8_t send) {
  auto t0 = millis();
  while(!(SPSR & _BV(SPIF)))
  {
    if (millis() - t0 > 5) return -1;
  }
  uint8_t data = SPDR;
  SPDR = send;
  return data;
}

//Transfer a byte and setup the next byte to transfer, with a timeout longer then a frame time.
int transfer(uint8_t send) {
  auto t0 = millis();
  while(!(SPSR & _BV(SPIF)))
  {
    if (millis() - t0 > 20) return -1;
  }
  uint8_t data = SPDR;
  SPDR = send;
  return data;
}

bool waitForSync()
{
  for(uint8_t timeout=0; timeout<10; timeout++)
  {
    int res = transferShortTimeout(0xFF);
    if (res == 0xE4)
    {
      res = transfer(0xFF);
      if (res == 0xE4) return true;
    }
    if (res == -1) initSPI();
  }
  return false;
}

int readMem(uint16_t addr)
{
  if (!waitForSync()) return -1;
  int res;
  res = transfer(0xD6);// >FF  <E4
  if (res != 0xE4) return -1;
  res = transfer(addr >> 8);// >D6  <E4
  if (res != 0xE4) return -1;
  res = transfer(addr);// >[H] <D0
  if (res != 0xD0) return -1;
  res = transfer(0xFF);// >[L] <D1
  if (res != 0xD1) return -1;
  res = transfer(0xFF);// >FF  <[DATA]
  return res;
}

bool writeMem(uint16_t addr, uint8_t value)
{
  if (!waitForSync()) return false;
  int res;
  res = transfer(0xD9);//     >FF  <E4
  if (res != 0xE4) return false;
  res = transfer(addr >> 8);//>D9  <E4
  if (res != 0xE4) return false;
  res = transfer(addr);  //   >[H]     <D8
  if (res != 0xD8) return false;
  res = transfer(~value);//   >[L]     <D9
  if (res != 0xD9) return false;
  res = transfer(value);//    >[^DATA] <DA
  if (res != 0xDA) return false;
  res = transfer(0xFF);//     >[DATA]  <DB
  if (res != 0xDB) return false;
  return res;
}

bool orMem(uint16_t addr, uint8_t value)
{
  if (!waitForSync()) return false;
  int res;
  res = transfer(0xDD);//     >FF  <E4
  if (res != 0xE4) return false;
  res = transfer(addr >> 8);//>DD  <E4
  if (res != 0xE4) return false;
  res = transfer(addr);  //   >[H]     <D8
  if (res != 0xD8) return false;
  res = transfer(~value);//   >[L]     <D9
  if (res != 0xD9) return false;
  res = transfer(value);//    >[^DATA] <DA
  if (res != 0xDA) return false;
  res = transfer(0xFF);//     >[DATA]  <DB
  if (res != 0xDB) return false;
  return res;
}

void loop() {
  uint16_t addr;
  switch(Serial.read())
  {
  case '!':
    Serial.print('!');
    break;
  case '?':
    if (waitForSync())
      Serial.print('K');
    else
      Serial.print('E');
    break;
  case 'R':
    while(Serial.available() < 2) {}
    addr = Serial.read() << 8;
    addr |= Serial.read();
    Serial.print(readMem(addr), HEX);
    break;
  case 'W':
    while(Serial.available() < 3) {}
    addr = Serial.read() << 8;
    addr |= Serial.read();
    if (writeMem(addr, Serial.read())) {
      Serial.print('K');
    } else {
      Serial.print('E');
    }
    break;
  case 'O':
    while(Serial.available() < 3) {}
    addr = Serial.read() << 8;
    addr |= Serial.read();
    if (orMem(addr, Serial.read())) {
      Serial.print('K');
    } else {
      Serial.print('E');
    }
    break;
  }
}
