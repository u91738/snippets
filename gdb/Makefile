all: encrypt

encrypt: encrypt.c
	$(CC) -g -O2 $^ -lcrypto -o $@

.PHONY: clean

clean:
	rm -f encrypt
