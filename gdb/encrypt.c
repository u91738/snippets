#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <assert.h>
#include <openssl/evp.h>

void hexdump(const uint8_t *v, size_t v_size) {
    for(size_t i  = 0; i < v_size; ++i)
        printf("%02X", v[i]);
    printf("\n");
}

const uint8_t key[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16};

int main() {
    EVP_CIPHER_CTX *ctx = EVP_CIPHER_CTX_new();
    assert(ctx);

    uint8_t iv[16] = {0};

    int ret = EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv);
    assert(ret == 1);

    int enc_len;
    const char plaintext[] = "something something";
    uint8_t ciphertext[32];
    ret = EVP_EncryptUpdate(ctx, ciphertext, &enc_len, plaintext, strlen(plaintext));
    assert(ret == 1);

    int fin_enc_len;
    ret = EVP_EncryptFinal_ex(ctx, ciphertext + enc_len, &fin_enc_len);
    assert(ret == 1);

    EVP_CIPHER_CTX_free(ctx);
    hexdump(ciphertext, enc_len + fin_enc_len);
}
