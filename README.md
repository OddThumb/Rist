# `R` style `list` class in `Python`

- You can `Rist` class to create a list-like object in Python.
- It allows you to access elements by name, similar to R's named lists.
- Of course, it also supports access by index.
- Most easy way is to use attribute access.
- You can contain any type of object, including other `Rist` objects.


```python
import main
```

### Basic Usage


```python
import numpy as np
import pandas as pd

x = main.Rist(
    element0 = [i for i in range(50)],
    element1 = "hello",
    element2 = np.arange(20),
    element3 = pd.DataFrame([1,2,3])
)

```


```python
# Print the object
print(x)
```

    .(Rist)
        ├── .element0 (list)
        │   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
        ├── .element1 (str)
        │   'hello'
        ├── .element2 (ndarray)
        │   array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16,
        │          17, 18, 19])
        └── .element3 (DataFrame)
               0
            0  1
            1  2
            2  3


Get names and values


```python
# names, values
print(x.names)
print(x.values)
```

    ['element0', 'element1', 'element2', 'element3']
    [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49], 'hello', array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16,
           17, 18, 19]),    0
    0  1
    1  2
    2  3]


Set element by name or index


```python
x['element4'] = 5
print(x)
```

    .(Rist)
        ├── .element0 (list)
        │   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
        ├── .element1 (str)
        │   'hello'
        ├── .element2 (ndarray)
        │   array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16,
        │          17, 18, 19])
        ├── .element3 (DataFrame)
        │      0
        │   0  1
        │   1  2
        │   2  3
        └── .element4 (int)
            5



```python
x[5] = 0.5772
print(x)
```

    .(Rist)
        ├── .element0 (list)
        │   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
        ├── .element1 (str)
        │   'hello'
        ├── .element2 (ndarray)
        │   array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16,
        │          17, 18, 19])
        ├── .element3 (DataFrame)
        │      0
        │   0  1
        │   1  2
        │   2  3
        ├── .element4 (int)
        │   5
        └── .[5] (float)
            0.5772


If you try to set an element by index that does not exist, it will be created.
and the indices intervening will be filled with `None`.


```python
x[7] = 3.141592
print(x)
```

    .(Rist)
        ├── .element0 (list)
        │   [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
        ├── .element1 (str)
        │   'hello'
        ├── .element2 (ndarray)
        │   array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, 16,
        │          17, 18, 19])
        ├── .element3 (DataFrame)
        │      0
        │   0  1
        │   1  2
        │   2  3
        ├── .element4 (int)
        │   5
        ├── .[5] (float)
        │   0.5772
        ├── .[6] (NoneType)
        │   None
        └── .[7] (float)
            3.141592


## Accessing Methods

### Attribute

![AttributeAccess](images/Attribute.png)


```python
# Access by attribute access
print(x.element0)
print(x.element1)
print(x.element2)
print(x.element3)
```

### Name


```python
# Access by name
print(x['element0'])
print(x['element1'])
print(x['element2'])
print(x['element3'])
```

### Index


```python
# Access by index
print(x[0])
print(x[1])
print(x[2])
print(x[3])
```

## `Rist` in `Rist` in `Rist` ...


```python
Rist1 = main.Rist(
    Rist2 = main.Rist(
        Rist3 = main.Rist(
            string = "Hello World",
            df2    = pd.DataFrame({'Hello': [0,1,0], 'World': [1,0,1]})
        ),
        list2 = [2,3,5,7],
        arr1  = np.arange(5)
    ),
    list1 = [1,3,5,7],
    df1   = pd.DataFrame({'a': [1,2,3,4], 'b': [5,6,7,8]})
)
```


```python
print(Rist1)
```

## Add two `Rist`


```python
Rist_combined = x + Rist1
print(Rist_combined)
```

During adding, if the name already exists, it will raise an error.


```python
Rist_hasDupName = main.Rist(list1 = ['duplicated', 'name', 'not', 'allowed'])
Rist_combined2 = Rist1 + Rist_hasDupName
```

## Append an element into `Rist`


```python
Rist1.append(newobj = 'ImNoob')
```


```python
print(Rist1)
```

During appending, if the name already exists, it will raise an error.


```python
Rist1.append(list1 = ['duplicated', 'name', 'not', 'allowed'])
```
