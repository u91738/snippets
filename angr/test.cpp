#include <cstdlib>
#include <cstring>
#include <algorithm>
#include <array>
#include <charconv>
#include <fstream>
#include <iostream>
#include <memory>
#include <string>


void somefunc(const std::string &s)
{
    int i = 0;
    std::from_chars(s.data(), s.data() + s.size(), i);
    if(i >= 0 && i < 10) {
        std::cout << "print i" << std::endl;
        std::cout << "i: " << i << std::endl;
    } else if (i >= 10 && i < 20) {
        printf("user-controlled format string\n");
        printf(s.c_str(), i);
    } else if (i >= 20 && i < 30) {
        std::string buf('-', 20);
        std::cout << "heap buffer overflow buf size: " << buf.size() << " s_size: " << s.size() << std::endl;
        std::copy(s.cbegin(), s.cend(), buf.begin());
        std::cout << buf << std::endl;
    } else {
        std::array<char, 20> buf;
        std::cout << "stack buffer overflow buf size: " << buf.size() << " s_size: " << s.size() << std::endl;
        std::copy(s.cbegin(), s.cend(), buf.begin());
        buf[buf.size() - 1] = 0;
        std::cout << buf.data() << std::endl;
    }
}


int main(int argc, char **argv)
{
    char s[1024];
    // angr seems to have issues with iostream
    if(argc == 1) {
        fgets(s, sizeof(s), stdin);
    } else {
        FILE * f = fopen(argv[1], "rb");
        if(f) {
            fgets(s, sizeof(s), f);
            fclose(f);
        } else {
            return 1;
        }
    }

    std::string str = s;
    somefunc(str);
    return 0;
}
