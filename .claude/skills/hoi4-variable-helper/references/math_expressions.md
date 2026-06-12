# HOI4 Math Expressions

Math expressions are inline formulas accepted by normal and temporary variable effects, except `modulo_variable` and `clamp_variable`. Use them instead of staging many temp variables when a value is calculated once.

## Shape

An expression starts with `value = ...`, then applies statements in order.

```
set_variable = {
    mobile_units = {
        value = num_cavalry
        add = num_motorized
        add = num_mechanized
    }
}
```

Expressions use fixed-point arithmetic. In boolean contexts, `0.0` is false and any other value is true. Comparison operators return `1.0` for true and `0.0` for false. If parsing fails, the runtime value becomes `0.0`.

## Operators

```
multiply = x
add = x
subtract = x
divide = x
min = x
max = x
clamp = { min = 0 max = 100 }
greater_than = x
less_than = x
greater_than_or_equals = x
less_than_or_equals = x
equals = x
not_equals = x
round = yes
```

Statements can take literal values, variables, data tokens such as `modifier@x`, script constants, and nested expressions.

```
set_variable = {
    industrial_score = {
        value = resource_produced@steel
        multiply = 0.45
        add = { value = resource_produced@oil multiply = 0.70 }
        add = { value = modifier@industrial_capacity_factory add = 1 multiply = num_of_factories }
    }
}
```

## Conditionals

`if` and `else` blocks modify the accumulator. `limit` is itself a math expression; nonzero is true.

```
set_variable = {
    policy_score = {
        value = base_score
        if = {
            limit = { value = stability greater_than = 0.6 }
            add = 10
        }
        else = {
            subtract = 5
        }
    }
}
```

## Collection Iteration

`every_collection` switches scope to each element of a named collection and applies statements to the accumulator.

```
set_variable = {
    non_capitulated_major_factories = {
        value = 0
        every_collection = {
            named_collection = non_capitulated_majors
            add = num_of_factories
        }
    }
}
```

Use collections for live, unordered membership. Use arrays when order, stable indices, or sorting matter.
