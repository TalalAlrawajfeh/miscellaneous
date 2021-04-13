/*
    Author: Talal H. Alrawajfeh
*/

#ifndef __INERTIA_GAME_H__
#define __INERTIA_GAME_H__

#include <iostream>
#include <string>
#include <regex>
#include "matrix.h"

enum MoveType
{
    NONE,
    NORTH,
    SOUTH,
    EAST,
    WEST,
    NORTH_EAST,
    NORTH_WEST,
    SOUTH_EAST,
    SOUTH_WEST
};

class InertiaGame
{
  private:
    const std::regex GAME_TYPE_REGEX = std::regex("([0-9]+)x([0-9]+)");

    std::string gameId;
    std::string gameType;
    int gridWidth;
    int gridHeight;
    std::pair<int, int> ballPosition;

    char **grid;

    void parseGameType();
    void allocateGrid();
    void dealocateGrid();
    void fillGrid();
    void setBallPosition();

  public:
    InertiaGame(std::string gameType, std::string gameId);
    InertiaGame(char *gameType, char *gameId);
    InertiaGame(const InertiaGame &game);

    ~InertiaGame();

    std::string getGameId() const;
    std::string getGameType() const;

    int getGridWidth() const;
    int getGridHeight() const;

    char **copyGrid() const;

    std::pair<int, int> getBallPosition() const;
    Matrix<char> getGrid() const;

    bool moveBall(MoveType moveType);
    bool isGameDone();
    int numberOfGemsLeft();
    bool gemExists(std::pair<int, int> gemPosition);

    void printGrid();
};

InertiaGame::InertiaGame(std::string gameType, std::string gameId)
{
    this->gameType = gameType;
    this->gameId = gameId;

    parseGameType();
    allocateGrid();
    fillGrid();
    setBallPosition();
}

InertiaGame::InertiaGame(char *gameType, char *gameId)
{
    InertiaGame(std::string(gameId), std::string(gameType));
}

InertiaGame::InertiaGame(const InertiaGame &game)
{
    this->gameId = game.getGameId();
    this->gameType = game.getGameType();
    this->gridWidth = game.getGridWidth();
    this->gridHeight = game.getGridHeight();
    this->ballPosition = game.getBallPosition();
    this->grid = game.copyGrid();
}

std::string InertiaGame::getGameId() const
{
    return this->gameId;
}

std::string InertiaGame::getGameType() const
{
    return this->gameType;
}

int InertiaGame::getGridWidth() const
{
    return this->gridWidth;
}

int InertiaGame::getGridHeight() const
{
    return this->gridHeight;
}

InertiaGame::~InertiaGame()
{
    dealocateGrid();
}

void InertiaGame::parseGameType()
{
    std::smatch match;
    std::regex_search(this->gameType, match, this->GAME_TYPE_REGEX);

    this->gridWidth = std::stoi(match[1]);
    this->gridHeight = std::stoi(match[2]);
}

void InertiaGame::allocateGrid()
{
    this->grid = new char *[this->gridHeight];
    for (int i = 0; i < this->gridHeight; i++)
    {
        this->grid[i] = new char[this->gridWidth];
    }
}

void InertiaGame::dealocateGrid()
{
    for (int i = 0; i < this->gridHeight; i++)
    {
        delete this->grid[i];
    }
    delete this->grid;
}

void InertiaGame::fillGrid()
{
    for (int i = 0; i < this->gridHeight; i++)
    {
        for (int j = 0; j < this->gridWidth; j++)
        {
            int pos = i * this->gridWidth + j;
            this->grid[i][j] = this->gameId[pos];
        }
    }
}

std::pair<int, int> InertiaGame::getBallPosition() const
{
    return this->ballPosition;
}

void InertiaGame::setBallPosition()
{
    for (int i = 0; i < this->gridHeight; i++)
    {
        for (int j = 0; j < this->gridWidth; j++)
        {
            if (this->grid[i][j] == 'S')
            {
                this->grid[i][j] = 's';
                this->ballPosition = std::pair<int, int>(i, j);
                return;
            }
        }
    }
    this->ballPosition = std::pair<int, int>(-1, -1);
}

char **InertiaGame::copyGrid() const
{
    char **gridCopy = new char *[this->gridHeight];
    for (int i = 0; i < this->gridHeight; i++)
    {
        gridCopy[i] = new char[this->gridWidth];
        for (int j = 0; j < this->gridWidth; j++)
        {
            gridCopy[i][j] = this->grid[i][j];
        }
    }
    return gridCopy;
}

bool InertiaGame::isGameDone()
{
    for (int i = 0; i < this->gridHeight; i++)
    {
        for (int j = 0; j < this->gridWidth; j++)
        {
            if (grid[i][j] == 'g')
            {
                return false;
            }
        }
    }
    return true;
}

int InertiaGame::numberOfGemsLeft()
{
    int gems = 0;
    for (int i = 0; i < this->gridHeight; i++)
    {
        for (int j = 0; j < this->gridWidth; j++)
        {
            if (grid[i][j] == 'g')
            {
                gems++;
            }
        }
    }
    return gems;
}

bool InertiaGame::moveBall(MoveType moveType)
{
    if (moveType == NONE)
    {
        return false;
    }

    int deltaY;
    int deltaX;

    switch (moveType)
    {
    case NORTH:
        deltaY = -1;
        deltaX = 0;
        break;
    case SOUTH:
        deltaY = 1;
        deltaX = 0;
        break;
    case EAST:
        deltaY = 0;
        deltaX = 1;
        break;
    case WEST:
        deltaY = 0;
        deltaX = -1;
        break;
    case NORTH_EAST:
        deltaY = -1;
        deltaX = 1;
        break;
    case NORTH_WEST:
        deltaY = -1;
        deltaX = -1;
        break;
    case SOUTH_EAST:
        deltaY = 1;
        deltaX = 1;
        break;
    case SOUTH_WEST:
        deltaY = 1;
        deltaX = -1;
        break;
    }

    int i = ballPosition.first + deltaY;
    int j = ballPosition.second + deltaX;

    if (i < 0 || i >= gridHeight || j < 0 || j >= gridWidth)
    {
        return false;
    }

    while (i >= 0 && i < gridHeight && j >= 0 && j < gridWidth)
    {
        if (grid[i][j] == 's' || grid[i][j] == 'w')
        {
            break;
        }
        else if (grid[i][j] == 'm')
        {
            return false;
        }

        i += deltaY;
        j += deltaX;
    }

    i = ballPosition.first + deltaY;
    j = ballPosition.second + deltaX;

    while (i >= 0 && i < gridHeight && j >= 0 && j < gridWidth)
    {
        if (grid[i][j] == 's')
        {
            break;
        }
        else if (grid[i][j] == 'w')
        {
            i -= deltaY;
            j -= deltaX;
            break;
        }
        else if (grid[i][j] == 'g')
        {
            grid[i][j] = 'b';
        }

        i += deltaY;
        j += deltaX;
    }

    if (i < 0 || i >= gridHeight || j < 0 || j >= gridWidth)
    {
        i -= deltaY;
        j -= deltaX;
    }

    if (i == ballPosition.first && j == ballPosition.second)
    {
        return false;
    }

    ballPosition.first = i;
    ballPosition.second = j;

    return true;
}

bool InertiaGame::gemExists(std::pair<int, int> gemPosition)
{
    if (grid[gemPosition.first][gemPosition.second] == 'g')
    {
        return true;
    }
    return false;
}

void InertiaGame::printGrid()
{
    std::cout << "Grid:" << std::endl;
    for (int i = 0; i < gridHeight; i++)
    {
        for (int j = 0; j < gridWidth; j++)
        {
            std::cout << grid[i][j] << " ";
        }
        std::cout << std::endl;
    }
    std::cout << std::endl
              << "Current Position: ("
              << ballPosition.first
              << ", "
              << ballPosition.second
              << ")"
              << std::endl;
}

Matrix<char> InertiaGame::getGrid() const
{
    Matrix<char> gridMatrix(gridHeight, gridWidth);
    gridMatrix.loadEntries(grid);
    return gridMatrix;
}

#endif /* __INERTIA_GAME_H__ */