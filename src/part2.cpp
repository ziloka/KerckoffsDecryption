// gcc src/part2.cpp -o part2
#include <stdio.h>
#include <unordered_map>
#include <string>
#include <map>

// {'4502': 'A', '53177': 'B', '946320122': 'C', '85053600': 'D', '7171031': 'E', '87445918': 'F', '4504': 'G', '692473': 'H', '20': 'I', '638440': 'J', '57643': 'K', '7004062': 'L', '52381': 'M', '930424404': 'N', '84524991': 'O', '89411894': 'P', '4254': 'Q', '376': 'R', '88527391': 'S', '23': 'T', '29': 'U', '361': 'V', '923921735': 'W', '4468': 'X', '636187': 'Y', '971559793': 'Z'}
// https://stackoverflow.com/questions/15151480/simple-dictionary-in-c

int main(int argc, char *argv[]) {

    std::unordered_map<std::string, std::string> codespacewords = {
            { 4, 3 },
            { 0, 2 }, { 2, 2 }, { 6, 2 }, { 8, 2 },
            { 1, 1 }, { 3, 1 }, { 5, 1 }, { 7, 1 }
    };

    printf("hello world!");
}