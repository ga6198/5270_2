#include <iostream>
#include <des.h>
#include "modes.h"
#include "osrng.h"
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

    //for (size_t i = 0; i < plain.size(); i++)
    //    plain[i] = 'A' + (i % 26);

    cout << plain << endl;

    return 0;
}