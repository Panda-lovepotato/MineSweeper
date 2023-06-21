#include <string>
#include <vector>
#include "MineSolver.h"
using namespace std;

void Split(const string& src, const string& separator, vector<string>& dest)
{
	string str = src;
	string substring;
	string::size_type start = 0, index;
	dest.clear();
	index = str.find_first_of(separator,start);
	do
	{
		if (index != string::npos)
		{    
			substring = str.substr(start,index-start );
			dest.push_back(substring);
			start =index+separator.size();
			index = str.find(separator,start);
			if (start == string::npos) break;
		}
	}while(index != string::npos);

	//the last part
	substring = str.substr(start);
	dest.push_back(substring);
}



int main(int argc, char **argv){
    int SquareNum_x = atoi(argv[1]);
    int SquareNum_y = atoi(argv[2]);
    int MineNum = atoi(argv[3]);
    vector <pair <int, int> > points;
    vector <vector <int> > board(SquareNum_x, vector <int> (SquareNum_y, -1));
    vector <vector <int> > his_board(SquareNum_y, vector <int> (SquareNum_x, -1));
    vector<string> VecStr;
    Split(argv[4], ",", VecStr);
    for (int i = 0; i < SquareNum_x; i++) {
		for (int j = 0; j < SquareNum_y; j++) {
			board[i][j] = atoi(VecStr[i*SquareNum_y+j].c_str());
            his_board[j][i] = board[i][j];
		}
	}
    MineSolver solver(SquareNum_y, SquareNum_x, MineNum);
	solver.GetCLKPoints(his_board, points);
    for (auto it : points) {
		printf("%d,%d\n", it.first, it.second);
	}

    return 0;
}