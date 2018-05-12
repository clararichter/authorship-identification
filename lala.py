import pandas as pd

df1 = pd.DataFrame({'A': 0.2,
                      'B': 0.3,
                      'C': 0.1,
                      'D': 0.1},
                      index=[0])


df2 = pd.DataFrame({'A': 0.12,
                      'B': 0.33,
                      'C': 0.341,
                      'D': 0.3241},
                      index=[1])

df3 = pd.DataFrame({'A': 0.12,
                      'K': 0.3234,
                      'V': 0.324},
                      index=[1])


frames = [df1, df2, df3]

result = pd.concat()
print(result)
