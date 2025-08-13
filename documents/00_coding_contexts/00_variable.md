# HOI4におけるVariableの使い方メモ

## variableってなんだ？

- 数学のxやyのような変数のこと。
- 様々な用途で使える。
- 特別なファイルは必要なく、`effect`や`trigger`の中で設定できる。
- `variable`コマンドを使うと名前付きの変数が誕生する。

例：

```hoi4
TUR = {
  set_variable = { var = var_name value = 10 }
}
```

この場合、トルコ（TUR）の`var_name`という変数は10になる。

## 可視化方法

- `localisation`の中で、以下のように書くことで表示できる：

```
[?var_name]
```

## variableコマンド一覧

### 基本系

```hoi4
set_variable = { var = var_name value = 0 }
```

- variableを新しく作成・初期化する。
- `on_startup`で実行しておくと便利。

```hoi4
set_variable = { var_name1 = var_name2 }
```

- var_name1 に var_name2 の値を代入する。

```hoi4
clear_variable = var_name
```

- 指定したvariableを削除（表示上は0になる）。

### 計算系

```hoi4
add_to_variable = { var = var_name value = 1 }
add_to_variable = { var1 = var2 }
```

- 値を加算（定数または他のvariable）。

```hoi4
subtract_from_variable = { var = var_name value = 1 }
subtract_from_variable = { var1 = var2 }
```

- 値を減算。

```hoi4
multiply_variable = { var = var_name value = 2 }
multiply_variable = { var1 = var2 }
```

- 値を乗算。

```hoi4
divide_variable = { var = var_name value = 2 }
divide_variable = { var1 = var2 }
```

- 値を除算。

### その他

```hoi4
clamp_variable = { var = var_name min = 0 max = 100 }
```

- 最小・最大値の制限。

```hoi4
round_variable = var_name
```

- 四捨五入。

```hoi4
set_variable = { var_name = random }
```

- ランダム（0〜1）な値を代入。

## Trigger系

```hoi4
check_variable = { var_name = 10 }
check_variable = { var_name > 10 }
check_variable = { var_name < 10 }
```

- 数値で比較。

```hoi4
check_variable = { var1 = var2 }
check_variable = { var1 > var2 }
check_variable = { var1 < var2 }
```

- 変数同士で比較。

```hoi4
check_variable = { var = var_name value = 10 compare = less_than }
check_variable = { var = var_name value = var_name_2 compare = less_than }
```

- より詳細な比較条件：
  - `less_than`
  - `less_than_or_equals`
  - `greater_than`
  - `greater_than_or_equals`
  - `equals`
  - `not_equals`

```hoi4
has_variable = var_name
```

- 変数の存在チェック（値は問わない）。
