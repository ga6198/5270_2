#include <iostream>
#include <des.h>
#include "files.h"
#include "modes.h"
#include "osrng.h"
#include "hex.h"
#include <assert.h>
using namespace std;
using namespace CryptoPP;
//using CryptoPP::DES;

/*
To see how a single bit of the plaintext / key affects the ciphertext bits in each round, list the output of each of the 16 rounds in the DES encryption, as shown in Figure 3.7, but ignorE the Intial Permutation block, the 32 - bit swap block and the Inverse Initial Permutation block, when
(1) m = 0x0, k = 0x2
(2) m = 0x2, k = 0x0
(3) m = 0x1, k = 0x2
where m is the plaintext and k is the key.
*/

int main()
{
    /*
    int m1 = 0x0;
    int m2 = 0x2;
    int m3 = 0x1;
    int k1 = 0x2;
    int k2 = 0x0;
    int k3 = 0x2;
    string plain1 = to_string(m1);
    string plain2 = to_string(m2);
    string plain3 = to_string(m3);
    string key1 = to_string(k1);
    string key2 = to_string(k2);
    string key3 = to_string(k3);

    cout << plain1 << endl;
    cout << plain2 << endl;
    cout << plain3 << endl;

    cout << key1 << endl;
    cout << key2 << endl;
    cout << key3 << endl;
    */

    //CBC_Mode<DES>::Encryption e;
    // DES des1 = DES();

    //CBC_Mode<DES>::Encryption e;

    //AutoSeededRandomPool prng;

    //SecByteBlock key(0x0, DES::DEFAULT_KEYLENGTH);
    //prng.GenerateBlock(key, key.size());

    /*
    byte key[DES::DEFAULT_KEYLENGTH];
    byte iv[DES::BLOCKSIZE];

    vector<byte> m1;
    vector<byte> ciphertext; //recover
    //string plain(64, 0x0);
    string plain = "00000000";
    //HexEncoder encoder(new FileSink(cout)

    memset(key, 0x2, sizeof(key));
    memset(iv, 0x0, sizeof(iv));

    CBC_Mode<DES>::Encryption e;
    e.SetKeyWithIV(key, sizeof(key), iv);
    */

    //for (size_t i = 0; i < plain.size(); i++)
    //    plain[i] = 'A' + (i % 26);

    //cout << plain << endl;

    //////////////////https://www.cryptopp.com/wiki/StringSink
    /*
    byte data[] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01 };
    string sink;

    HexEncoder encoder;
    encoder.Attach(new StringSink(sink));

    encoder.Put(data, sizeof(data));
    encoder.MessageEnd();

    cout << sink << endl;
    */

    /*
    byte key[AES::MAX_KEYLENGTH];
    byte iv[AES::BLOCKSIZE];
    //vector<byte> plain, cipher, recover;
    byte plain[] = { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01 };
    string hold;
    HexEncoder encoder(new StringSink(hold));

    memset(key, 0x00, sizeof(key));
    memset(iv, 0x00, sizeof(iv));


    HexEncoder enc(new FileSink(cout));

    //string str("Attack at dawn!");
    //std::copy(str.begin(), str.end(), std::back_inserter(plain));

    cout << "Plain text: ";
    encoder.Put(plain, sizeof(plain)); //enc.Put(plain.data(), plain.size());
    encoder.MessageEnd(); //enc.MessageEnd();
    cout << hold << endl;//cout << endl;
    */

    //transform text to bytes
    //string hexstring = "0000000000000000000000000000000000000000000000000000000000000000";
    string hexstring = "0x00";
    string decodedhex;

    StringSource ss(hexstring, true, new StringSink(decodedhex));
    const byte* data = reinterpret_cast<const byte*>(decodedhex.data());

    cout << data << endl;

    //string encodedKey = "1234567890123456789012345678901234567890123456789012345678901234";
    string encodedKey = "0000000000000000000000000000000000000000000000000000000000000000";
    string encodedIv = "1111111111222222222233333333334444444444555555555566666666667777";
    string encodedValues = "0000000000000000000000000000000000000000000000000000000000000000";
    string key, iv, values;

    StringSource ssk(encodedKey, true /*pumpAll*/,
        new HexDecoder(
            new StringSink(key)
        ) // HexDecoder
    ); // StringSource

    StringSource ssv(encodedIv, true /*pumpAll*/,
        new HexDecoder(
            new StringSink(iv)
        ) // HexDecoder
    ); // StringSource

    StringSource ssm(encodedValues, true /*pumpAll*/,
        new HexDecoder(
            new StringSink(values)
        ) // HexDecoder
    ); // StringSource

    //cout << key << "\n" << iv << endl;

    //CBC_Mode<DES>::Encryption encr;
    //encr.SetKeyWithIV(key.data())

    //key.data

    const byte* result_key = (const byte*)key.data();

    ECB_Mode<DES>::Encryption enc;
    //enc.SetKey(key, key.size());
    enc.SetKeyWithRounds(result_key, key.size(), 16);

    string cipher;


    return 0;
}