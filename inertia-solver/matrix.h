/*
    Author: Talal H. Alrawajfeh
*/

#ifndef __MATRIX_H__
#define __MATRIX_H__

#include <iostream>
#include <stdexcept>

template <typename T>
class Matrix
{
  private:
    int rows;
    int columns;
    T **entries;

    inline void initializeDimensions(int rows, int columns);
    inline void initializeEntries();
    inline bool rowExists(int row) const noexcept;
    inline bool columnExists(int column) const noexcept;
    inline bool bothRowAndColumnExist(int row, int column) const noexcept;

  public:
    Matrix(int rows, int columns)
    {
        if (rows < 0 || columns < 0)
        {
            initializeDimensions(0, 0);
            this->entries = nullptr;
        }
        else
        {
            initializeDimensions(rows, columns);
            initializeEntries();
        }
    }

    Matrix(const std::pair<int, int> &dimensions)
    {
        Matrix(dimensions.first, dimensions.second);
    }

    Matrix(const Matrix<T> &matrix)
    {
        std::pair<int, int> dimensions = matrix.getDimensions();
        initializeDimensions(dimensions.first, dimensions.second);
        initializeEntries();
        for (int i = 0; i < rows; i++)
        {
            for (int j = 0; j < columns; j++)
            {
                entries[i][j] = matrix.getEntry(i, j);
            }
        }
    }

    std::pair<int, int> getDimensions() const noexcept;
    bool areEntriesEmpty() const noexcept;
    Matrix<T> &loadEntries(T **entries);
    Matrix<T> &setEntry(int row, int column, T entry) noexcept;
    T getEntry(int row, int column) const noexcept;

    Matrix<T> &operator=(const Matrix<T> &);
};

template <typename T>
inline void Matrix<T>::initializeDimensions(int rows, int columns)
{
    this->rows = rows;
    this->columns = columns;
}

template <typename T>
inline void Matrix<T>::initializeEntries()
{
    this->entries = new T *[this->rows];
    for (int i = 0; i < this->rows; i++)
    {
        this->entries[i] = new T[this->columns];
    }
}

template <typename T>
inline bool Matrix<T>::rowExists(int row) const noexcept
{
    return row >= 0 && row < this->rows;
}

template <typename T>
inline bool Matrix<T>::columnExists(int column) const noexcept
{
    return column >= 0 && column < this->columns;
}

template <typename T>
inline bool Matrix<T>::bothRowAndColumnExist(int row, int column) const noexcept
{
    return rowExists(row) && columnExists(column);
}

template <typename E>
inline void ensureEqualDimensions(const Matrix<E> &first, const Matrix<E> &second)
{
    std::pair<int, int> firstDimensions = first.getDimensions();
    std::pair<int, int> secondDimensions = second.getDimensions();

    if (firstDimensions.first != secondDimensions.first || firstDimensions.second != secondDimensions.second)
    {
        throw std::runtime_error("Matrices have invalid dimensions for summation");
    }
}

template <typename T>
std::pair<int, int> Matrix<T>::getDimensions() const noexcept
{
    std::pair<int, int> pair(this->rows, this->columns);
    pair.second = this->columns;
    return pair;
}

template <typename T>
bool Matrix<T>::areEntriesEmpty() const noexcept
{
    return nullptr == this->entries;
}

template <typename T>
Matrix<T> &Matrix<T>::loadEntries(T **entries)
{
    for (int i = 0; i < this->rows; i++)
    {
        for (int j = 0; j < this->columns; j++)
        {
            this->entries[i][j] = entries[i][j];
        }
    }
    return *this;
}

template <typename T>
Matrix<T> &Matrix<T>::setEntry(int row, int column, T entry) noexcept
{
    if (bothRowAndColumnExist(row, column))
    {
        this->entries[row][column] = entry;
    }
    return *this;
}

template <typename T>
T Matrix<T>::getEntry(int row, int column) const noexcept
{
    if (bothRowAndColumnExist(row, column))
    {
        return this->entries[row][column];
    }
    return 0;
}

template <typename T>
Matrix<T> &Matrix<T>::operator=(const Matrix<T> &matrix)
{
    Matrix<T> ret(matrix);
    return ret;
}

#endif /* __MATRIX_H__ */