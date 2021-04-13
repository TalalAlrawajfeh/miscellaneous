/*
    Author: Talal H. Alrawajfeh
*/

#include <iostream>
#include "inertia_game.h"
#include <vector>
#include "matrix.h"

void printUsage()
{
    std::cout << "Please run the program with the following parameters:" << std::endl;
    std::cout << "    inertia_solver <game_type> <game_id>" << std::endl;
    std::cout << "game_type: 10x8, 15x12, 20x10, or custom" << std::endl;
    std::cout << "game_id: acquire from here https://www.chiark.greenend.org.uk" << std::endl;
}

int calculateTaxicabMetric(std::pair<int, int> firstPoint, std::pair<int, int> secondPoint)
{
    return abs(firstPoint.first - secondPoint.first) + abs(firstPoint.second - secondPoint.second);
}

std::pair<int, int> nextNearestGem(InertiaGame *game)
{
    std::pair<int, int> ballPosition = game->getBallPosition();
    Matrix<char> grid = game->getGrid();
    std::pair<int, int> dimensions = grid.getDimensions();

    int minDistance = dimensions.first + dimensions.second;
    int nearestGemRow = 0;
    int nearestGemColumn = 0;

    for (int i = 0; i < dimensions.first; i++)
    {
        for (int j = 0; j < dimensions.second; j++)
        {
            if (grid.getEntry(i, j) == 'g')
            {
                std::pair<int, int> gemPosition(i, j);
                int distance = calculateTaxicabMetric(ballPosition, gemPosition);
                if (distance < minDistance)
                {
                    minDistance = distance;
                    nearestGemRow = i;
                    nearestGemColumn = j;
                }
            }
        }
    }

    std::pair<int, int> nearestGem;
    if (minDistance < dimensions.first + dimensions.second + 1)
    {
        nearestGem.first = nearestGemRow;
        nearestGem.second = nearestGemColumn;
    }
    else
    {
        nearestGem.first = -1;
        nearestGem.second = -1;
    }
    return nearestGem;
}

int normalize(int number)
{
    if (number > 0)
    {
        return 1;
    }
    else if (number < 0)
    {
        return -1;
    }
    else
    {
        return 0;
    }
}

std::vector<MoveType> getMovesSortedByWeight(std::pair<int, int> ballPosition, std::pair<int, int> destination)
{
    int deltaY = normalize(ballPosition.first - destination.first);
    int deltaX = normalize(ballPosition.second - destination.second);

    std::vector<MoveType> moves(8);

    std::vector<std::pair<MoveType, int>> weightedMoves = {
        std::make_pair(NORTH, 8 * deltaY),
        std::make_pair(SOUTH, -8 * deltaY),
        std::make_pair(WEST, 7 * deltaX),
        std::make_pair(EAST, -7 * deltaX),
        std::make_pair(NORTH_WEST, 6 * deltaY + 6 * deltaX),
        std::make_pair(NORTH_EAST, 6 * deltaY + -5 * deltaX),
        std::make_pair(SOUTH_WEST, -6 * deltaY + 4 * deltaX),
        std::make_pair(SOUTH_EAST, -6 * deltaY - 3 * deltaX)};

    std::sort(weightedMoves.begin(), weightedMoves.end(),
              [](std::pair<MoveType, int> weightedMove1, std::pair<MoveType, int> weightedMove2) {
                  return weightedMove1.second > weightedMove2.second;
              });

    std::transform(weightedMoves.begin(), weightedMoves.end(), moves.begin(),
                   [](std::pair<MoveType, int> weightedMove) { return weightedMove.first; });

    return moves;
}

const char *moveTypeToString(MoveType moveType)
{
    switch (moveType)
    {
    case NORTH:
        return "NORTH";
    case SOUTH:
        return "SOUTH";
    case EAST:
        return "EAST";
    case WEST:
        return "WEST";
    case NORTH_EAST:
        return "NORTH_EAST";
    case NORTH_WEST:
        return "NORTH_WEST";
    case SOUTH_EAST:
        return "SOUTH_EAST";
    case SOUTH_WEST:
        return "SOUTH_WEST";
    }
    return "UNKNOWN";
}

void initializeVisits(Matrix<bool> visits)
{
    std::pair<int, int> dimensions = visits.getDimensions();
    for (int i = 0; i < dimensions.first; i++)
    {
        for (int j = 0; j < dimensions.second; j++)
        {
            visits.setEntry(i, j, false);
        }
    }
}

std::vector<MoveType> findPath(InertiaGame &game, std::pair<int, int> destination, Matrix<bool> visits)
{
    InertiaGame *currentGameState = new InertiaGame(game);
    Matrix<bool> *currentVisits = new Matrix<bool>(visits);
    std::vector<MoveType> moves = getMovesSortedByWeight(game.getBallPosition(), destination);

    std::vector<MoveType> result;

    for (auto move : moves)
    {
        if (!currentGameState->moveBall(move))
        {
            continue;
        }

        if (!currentGameState->gemExists(destination))
        {
            result.push_back(move);
            break;
        }

        std::pair<int, int> ballPosition = currentGameState->getBallPosition();
        if (!currentVisits->getEntry(ballPosition.first, ballPosition.second))
        {
            currentVisits->setEntry(ballPosition.first, ballPosition.second, true);
            std::vector<MoveType> path = findPath(*currentGameState, destination, *currentVisits);
            if (path.size() != 0)
            {
                path.insert(path.begin(), move);
                delete currentVisits;
                delete currentGameState;
                return path;
            }
        }

        delete currentVisits;
        currentVisits = new Matrix<bool>(visits);
        delete currentGameState;
        currentGameState = new InertiaGame(game);
    }

    delete currentVisits;
    delete currentGameState;
    return result;
}

void solveGame(InertiaGame &game)
{
    Matrix<bool> currentVisits(game.getGridHeight(), game.getGridWidth());
    initializeVisits(currentVisits);

    std::pair<int, int> position = game.getBallPosition();

    while (!game.isGameDone())
    {
        std::vector<MoveType> path = findPath(game, nextNearestGem(&game), currentVisits);
        for (auto move : path)
        {
            std::cout << moveTypeToString(move) << std::endl;
            game.moveBall(move);
        }
        position = game.getBallPosition();
    }
}

int main(int argc, char const *argv[])
{
    if (argc < 3)
    {
        printUsage();
    }
    else
    {
        InertiaGame game(argv[1], argv[2]);
        solveGame(game);
    }
    return 0;
}
