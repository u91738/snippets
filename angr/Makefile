CFLAGS=-g -O2 -Wall
CXXFLAGS=-g -O2 -Wall --std=c++17

SANITIZERS=-fsanitize=address \
           -fsanitize=leak \
           -fsanitize=undefined \
           -fsanitize=bounds-strict \
           -fstack-protector-all

all: test test-san testpp testpp-san

test: test.c
	$(CC) $(CFLAGS) $^ -o $@

test-san: test.c
	$(CC) $(CFLAGS) $(SANITIZERS) $^ -o $@

testpp: test.cpp
	$(CXX) $(CXXFLAGS) $^ -o $@

testpp-san: test.cpp
	$(CXX) $(CXXFLAGS) $(SANITIZERS) $^ -o $@

clean:
	rm -f test test-san testpp testpp-san
