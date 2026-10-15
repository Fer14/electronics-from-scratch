# Boolean Algebra

> Three operations, AND, OR and NOT, are enough to describe every decision a digital circuit can make.

**Type:** Learn
**Prerequisites:** Phase 14 (Digital Logic), Lesson 01 (Analog vs Digital), Lesson 02 (Binary Numbers)
**Time:** ~75 minutes

## Words You'll Meet

| Word | Plain meaning | Everyday picture |
|---|---|---|
| Boolean variable | A name that can only be 0 (false) or 1 (true) | "Is the door open?" with a yes/no answer |
| Boolean algebra | Rules for combining true/false values, like school algebra for yes/no answers | Grammar rules for "and", "or", "not" |
| AND | Output is 1 only when every input is 1 | A bank vault that opens only when both keys are turned |
| OR | Output is 1 when at least one input is 1 | A doorbell with a button at the front and the back: either rings it |
| NOT | Output is the opposite of the input | A "door open" warning light that is on when the door is not closed |
| Truth table | A table listing the output for every possible combination of inputs | A full menu with a price for every combo |
| Expression | A formula built from variables and operations, like `a·b + c'` | A recipe written in shorthand |
| Literal | A variable or its opposite: `a` or `a'` | One ingredient, plain or "without" |
| Product term (minterm) | Several literals ANDed together | "Only if it's Saturday AND sunny AND I'm free" |
| Sum of products (SOP) | Product terms ORed together | A list of separate situations, any of which triggers the action |
| De Morgan's laws | Rules that swap AND and OR when you push a NOT through them | "Not (tea or coffee)" means "no tea and no coffee" |
| Karnaugh map | A grid that arranges a truth table so terms that can merge sit next to each other | A seating chart that puts friends side by side |

## Learning Objectives

- Write the truth tables of AND, OR and NOT and read the symbols `·`, `+` and `'`.
- Use the main laws of Boolean algebra (identity, null, idempotent, complement, commutative, associative, distributive, absorption) to simplify expressions.
- Apply De Morgan's laws to push a NOT through an AND or an OR.
- Turn any truth table into a sum-of-products expression.
- Simplify a 3-variable function with a Karnaugh map.
- Check that two expressions are equal by comparing their truth tables with the simulator.

## The Problem

You are designing the controller of a greenhouse fan. The rules from the gardener are: "Run the fan if it is daytime and too hot, or if it is daytime and too humid." Three sensors give you three bits: `a` (too hot), `b` (daytime), `c` (too humid). You need a circuit whose output `y` is 1 exactly when the rule says so.

You could wire it straight from the sentence: two AND gates and an OR gate. But is that the cheapest circuit? Is "daytime and (hot or humid)" the same thing, with one gate fewer? What if your parts drawer only has NAND chips? What if the rules come as a table of 8 cases instead of a sentence?

In 1854 the English mathematician George Boole published a way to calculate with "true" and "false" as if they were numbers. In 1937 a young engineer named Claude Shannon showed, in his master's thesis, that Boole's algebra describes exactly what networks of relay switches do. Since then, Boolean algebra has been the language for designing, simplifying and checking every digital circuit. This lesson teaches it.

## The Physics

Boolean algebra is mathematics, but each operation maps onto something physical you already know:

- **AND is switches in series.** A lamp wired through two switches in series lights only when switch A **and** switch B are closed. One open switch breaks the loop (Phase 02, Lesson 04).
- **OR is switches in parallel.** With two switches side by side, closing A **or** B (or both) gives the current a path.
- **NOT is a switch that is closed when its control is off.** A transistor pulling an output down to ground when its input is high does exactly that (Phase 12, Lesson 05).

```
  AND: series                      OR: parallel

  +V ---/ A ---/ B --- lamp       +V ---+--/ A --+--- lamp
                                        |        |
                                        +--/ B --+
```

Shannon's insight was that these three switch arrangements, nested inside each other, can build any logical function, and that Boole's algebra lets you simplify the network before you build it. In Lesson 05 we will see that a CMOS gate is literally a series and parallel arrangement of transistor switches.

## The Concept

### Variables and the three operations

A Boolean variable takes only two values, 0 and 1. We write the three basic operations like this:

| Operation | Written | Read aloud | Rule |
|---|---|---|---|
| AND | `a·b` or `ab` | "a and b" | 1 only if both are 1 |
| OR | `a + b` | "a or b" | 1 if at least one is 1 |
| NOT | `a'` (also written with a bar over `a`) | "not a" or "a bar" | flips 0 and 1 |

The `+` here is **not** ordinary addition: in Boolean algebra `1 + 1 = 1` (true or true is true). The symbols were chosen because AND behaves a lot like multiplication (anything times 0 is 0) and OR somewhat like addition. When you see `+` in this phase, read it as "or".

Their truth tables, rows in binary counting order:

```
 a b | a·b       a b | a+b       a | a'
 ----+----       ----+----       --+---
 0 0 |  0        0 0 |  0        0 | 1
 0 1 |  0        0 1 |  1        1 | 0
 1 0 |  0        1 0 |  1
 1 1 |  1        1 1 |  1
```

Order of operations, like in school algebra: NOT first, then AND, then OR. So `a + b·c'` means `a + (b·(c'))`.

### Truth tables: the complete description

With n inputs there are 2^n input combinations (Lesson 02), so a truth table has 2^n rows. For the greenhouse fan, with three inputs, that is 8 rows. Go through the rule "daytime and hot, or daytime and humid" row by row:

```
 row  a b c | y    why
  0   0 0 0 | 0    night
  1   0 0 1 | 0    night
  2   0 1 0 | 0    day, but neither hot nor humid
  3   0 1 1 | 1    day and humid
  4   1 0 0 | 0    night
  5   1 0 1 | 0    night
  6   1 1 0 | 1    day and hot
  7   1 1 1 | 1    day, hot and humid
```

The truth table is the final authority. Two expressions are equal if and only if they have the same truth table. With only 8 rows, you can always check by brute force, and our simulator will do exactly that.

### The laws

Each law below is true for every value of the variables. You can prove any of them by checking its truth table, which is a good exercise. The ones marked "new" have no counterpart in ordinary algebra.

| Law | AND form | OR form |
|---|---|---|
| Identity | `a·1 = a` | `a + 0 = a` |
| Null (domination) | `a·0 = 0` | `a + 1 = 1` (new) |
| Idempotent (new) | `a·a = a` | `a + a = a` |
| Complement (new) | `a·a' = 0` | `a + a' = 1` |
| Double negation | `(a')' = a` | |
| Commutative | `a·b = b·a` | `a + b = b + a` |
| Associative | `(a·b)·c = a·(b·c)` | `(a + b) + c = a + (b + c)` |
| Distributive | `a·(b + c) = a·b + a·c` | `a + b·c = (a + b)·(a + c)` (new) |
| Absorption (new) | `a·(a + b) = a` | `a + a·b = a` |

Read a few out loud with a picture:

- `a + 1 = 1`: "a or true is true". A doorbell with one button stuck pressed always rings.
- `a·a' = 0`: "a and not a is false". The door cannot be both open and closed.
- `a + a·b = a`: "a, or a and b, is just a". If you go out whenever it is sunny, the extra rule "also go out when sunny and warm" changes nothing.

Proof of absorption by truth table, so you see how it is done:

```
 a b | a·b | a + a·b | a
 ----+-----+---------+---
 0 0 |  0  |    0    | 0
 0 1 |  0  |    0    | 0
 1 0 |  0  |    1    | 1
 1 1 |  1  |    1    | 1
```

The last two columns match in every row, so the law holds.

### Simplifying the greenhouse rule

The sentence gave us

```
y = a·b + b·c
```

Use commutativity to write `a·b = b·a`, then the distributive law backwards (factor out `b`, just like `3x + 3y = 3(x + y)`):

```
y = b·a + b·c = b·(a + c)
```

"Daytime, and (hot or humid)". The first form needs two AND gates and one OR gate (3 gates); the second needs one OR and one AND (2 gates). Same truth table, one gate less. That is what simplification buys: fewer gates means less area on the chip, less power and often less delay (Phase 20 measures all three).

### De Morgan's laws

Augustus De Morgan, a friend of Boole, noticed how NOT interacts with AND and OR:

```
(a·b)' = a' + b'        "not (a and b)"  equals  "not a, or not b"
(a + b)' = a'·b'        "not (a or b)"   equals  "not a, and not b"
```

Everyday check: "It is not true that I had tea and coffee" means at least one of them I did not have. "I had neither tea nor coffee", which is "not (tea or coffee)", means no tea and no coffee.

Proof of the first law by truth table:

```
 a b | a·b | (a·b)' | a' | b' | a' + b'
 ----+-----+--------+----+----+--------
 0 0 |  0  |   1    | 1  | 1  |   1
 0 1 |  0  |   1    | 1  | 0  |   1
 1 0 |  0  |   1    | 0  | 1  |   1
 1 1 |  1  |   0    | 0  | 0  |   0
```

The recipe to remember: **to push a NOT through a bracket, flip every AND to OR (and every OR to AND), and NOT every variable.** It works for any number of variables: `(a·b·c)' = a' + b' + c'`.

### Why De Morgan matters in hardware

In Lesson 05 you will see that the cheapest gates to build in CMOS are not AND and OR but **NAND** ("not and", `(a·b)'`) and **NOR** ("not or", `(a+b)'`). De Morgan lets you rewrite any AND/OR design into NANDs. Take the greenhouse rule in its sum-of-products form and apply double negation, then De Morgan on the outer OR:

```
y = a·b + b·c
  = ((a·b + b·c)')'              double negation changes nothing
  = ((a·b)' · (b·c)')'           De Morgan: (X + Y)' = X'·Y'
  = NAND( NAND(a, b), NAND(b, c) )
```

Three NAND gates, no AND or OR at all. This trick, "a sum of products is a NAND of NANDs", works for every sum of products. In the lab of this lesson you build exactly this.

### From truth table to expression: sum of products

What if you are given only a table, with no sentence? There is a mechanical recipe that always works:

1. Find every row where the output is 1.
2. For each such row, write a product term that is 1 **only** on that row: use the variable plain if its value in the row is 1, with a NOT if its value is 0. This term is called a **minterm**.
3. OR all those minterms together.

For the greenhouse table, the 1 rows are 3 (`a=0,b=1,c=1`), 6 (`1,1,0`) and 7 (`1,1,1`):

```
row 3: a'·b·c
row 6: a·b·c'
row 7: a·b·c

y = a'·b·c + a·b·c' + a·b·c
```

Check row 3: `a'·b·c` with a=0, b=1, c=1 gives 1·1·1 = 1. Check row 2 (a=0, b=1, c=0): `a'·b·c` = 1·1·0 = 0, `a·b·c'` = 0, `a·b·c` = 0, so y = 0. Correct.

This expression is correct but long: three 3-input ANDs and a 3-input OR. Simplify with the laws:

```
y = a'·b·c + a·b·c' + a·b·c
  = a'·b·c + a·b·c + a·b·c' + a·b·c      idempotent: a·b·c + a·b·c = a·b·c, so we may duplicate it
  = b·c·(a' + a) + a·b·(c' + c)          distributive, factoring
  = b·c·1 + a·b·1                        complement: a' + a = 1
  = b·c + a·b
  = b·(a + c)
```

The duplication trick in the second line is legal because of the idempotent law and is the key move in hand simplification: reuse a term to combine with two neighbours.

### Karnaugh maps: seeing the simplification

Doing algebra by hand is error-prone. In 1953 Maurice Karnaugh proposed drawing the truth table as a grid in which **neighbouring cells differ in exactly one variable**. Two neighbouring 1s can then be merged into one shorter term, because `X·c + X·c' = X`.

For three variables, put `a` on the rows and `b c` on the columns, in the order 00, 01, 11, 10 (not 00, 01, 10, 11). This order, called Gray code, changes one bit at a time, also between the last and the first column, so the map wraps around like a cylinder.

```
            bc
          00   01   11   10
        +----+----+----+----+
  a = 0 |  0 |  0 |  1 |  0 |
        +----+----+----+----+
  a = 1 |  0 |  0 |  1 |  1 |
        +----+----+----+----+
```

Now circle groups of adjacent 1s, in sizes 1, 2, 4 or 8 (powers of two), as large as possible, until every 1 is in at least one group:

- The column `bc = 11` has 1s in both rows: a group of 2. Inside it, `a` changes and `b=1, c=1` stay. The group is `b·c`.
- The row `a = 1`, columns `11` and `10`: a group of 2. Inside it, `c` changes and `a=1, b=1` stay. The group is `a·b`.

So `y = b·c + a·b`, the same result as the algebra, found by looking. Each doubling of a group size removes one more variable from its term: a single cell has 3 literals, a pair 2, a group of 4 just 1.

Karnaugh maps are practical up to 4 variables (a 4x4 grid). Beyond that, engineers use computer programs (the Quine-McCluskey method, and today the logic synthesis tools of Phase 20) that do the same job automatically.

### Don't-care conditions

Sometimes some input combinations can never happen, or we do not care what the output is for them. For example, a digit from 0 to 9 stored in 4 bits never takes the patterns 10 to 15. Mark those cells with an X in the map and treat each X as a 0 or a 1, whichever makes the groups bigger. This often simplifies circuits a lot (Lesson 06 uses it for a display decoder).

### Equivalent expressions, different circuits

Here are three ways to build the greenhouse fan, all with the same truth table:

```
SOP from the sentence:      y = a·b + b·c                3 gates: AND, AND, OR
Factored:                   y = b·(a + c)                2 gates: OR, AND
NAND-NAND:                  y = NAND(NAND(a,b), NAND(b,c)) 3 gates, all NAND
```

Boolean algebra does not tell you which is "best". That depends on what gates you have, how fast they are and how much area they take. It tells you which ones are **correct**, and gives you the moves to get from one to another.

## Build It

The script `code/main.py` builds the greenhouse fan three ways in our logic simulator, checks that all three have the same truth table, proves De Morgan's laws by brute force and rebuilds the expression from the table.

### Step 1: A circuit in `sim.logic`

A `LogicCircuit` is a list of named wires and the gates that drive them. Each gate method takes the **output wire first**, then its input wires.

```python
from sim.logic import LogicCircuit

def greenhouse_sop():
    lc = LogicCircuit("a·b + b·c")
    lc.inputs("a", "b", "c")
    lc.and_("ab", "a", "b")
    lc.and_("bc", "b", "c")
    lc.or_("y", "ab", "bc")
    lc.outputs("y")
    return lc
```

The method names `and_`, `or_`, `not_` end in an underscore because `and`, `or` and `not` are reserved words in Python. `nand`, `nor` and `xor` need no underscore.

### Step 2: The other two circuits

```python
def greenhouse_factored():
    lc = LogicCircuit("b·(a + c)")
    lc.inputs("a", "b", "c")
    lc.or_("a_or_c", "a", "c")
    lc.and_("y", "b", "a_or_c")
    lc.outputs("y")
    return lc


def greenhouse_nand():
    lc = LogicCircuit("NAND(NAND(a,b), NAND(b,c))")
    lc.inputs("a", "b", "c")
    lc.nand("n1", "a", "b")
    lc.nand("n2", "b", "c")
    lc.nand("y", "n1", "n2")
    lc.outputs("y")
    return lc
```

### Step 3: Compare truth tables

`lc.truth_table()` tries every input combination in binary counting order and returns one dictionary per row. We pull out the `y` column of each circuit and compare.

```python
def column(lc, output):
    return [row[output] for row in lc.truth_table(outputs=[output])]

circuits = [greenhouse_sop(), greenhouse_factored(), greenhouse_nand()]
for lc in circuits:
    print(lc.name, column(lc, "y"), lc.gate_count(), lc.counts())
```

Output:

```
  a·b + b·c                    y column = [0, 0, 0, 1, 0, 0, 1, 1]  gates = 3  {'and': 2, 'or': 1, 'dff': 0}
  b·(a + c)                    y column = [0, 0, 0, 1, 0, 0, 1, 1]  gates = 2  {'or': 1, 'and': 1, 'dff': 0}
  NAND(NAND(a,b), NAND(b,c))   y column = [0, 0, 0, 1, 0, 0, 1, 1]  gates = 3  {'nand': 3, 'dff': 0}
  all three have the same truth table: True
```

Three different circuits, one function. (`dff` counts memory elements, which we meet in Phase 15; here there are none.)

### Step 4: De Morgan by brute force

We build both sides of each law in one circuit and compare their columns:

```python
def de_morgan():
    lc = LogicCircuit("De Morgan")
    lc.inputs("a", "b")
    lc.nand("not_both", "a", "b")
    lc.not_("na", "a")
    lc.not_("nb", "b")
    lc.or_("na_or_nb", "na", "nb")
    lc.nor("neither", "a", "b")
    lc.and_("na_and_nb", "na", "nb")
    lc.outputs("not_both", "na_or_nb", "neither", "na_and_nb")
    return lc
```

The script prints `(a·b)' == a' + b' : True` and `(a+b)' == a'·b' : True`. With two inputs, four rows are a complete proof.

### Step 5: From a truth table to an expression

The minterm recipe, in code: for every row with output 1, write each variable plain if its bit is 1 and with a `'` if it is 0, join with `·`, then join the terms with `+`.

```python
def sum_of_products(names, outputs):
    terms = []
    for bits, out in zip(product((0, 1), repeat=len(names)), outputs):
        if out:
            terms.append("·".join(n if b else n + "'" for n, b in zip(names, bits)))
    return " + ".join(terms)
```

It prints `y = a'·b·c + a·b·c' + a·b·c`, exactly the expression we derived by hand, and then the Karnaugh map in Gray-code column order:

```
          bc=00 bc=01 bc=11 bc=10
    a=0     0     0     1     0
    a=1     0     0     1     1
```

Run it:

```bash
uv run python phases/14-digital-logic/03-boolean-algebra/code/main.py
```

## Use It

- **Programming.** Every `if` statement with `and`, `or`, `not` in Python is Boolean algebra. De Morgan is how you rewrite `not (x > 0 and y > 0)` as `x <= 0 or y <= 0`.
- **Logic synthesis.** Chip designers write behaviour in a hardware description language (Verilog, VHDL). A synthesis tool turns it into Boolean equations, simplifies them with methods descended from Karnaugh and Quine-McCluskey, and maps them onto the gates of a standard cell library (Phase 20, Lesson 11).
- **Search engines and databases.** Queries like `"cat" AND NOT "dog"` are Boolean expressions over the set of documents.
- **Safety interlocks.** A press machine runs only if both of the operator's hands are on two separate buttons (AND), and stops if any emergency button is pressed (OR of the stop buttons, then NOT). Safety standards require these to be designed and checked as Boolean functions.
- **74HC chips.** A 74HC08 has four 2-input AND gates, a 74HC32 four 2-input ORs, a 74HC04 six NOTs. A greenhouse controller made from them takes one 74HC08 and one 74HC32, or one 74HC00 (four NANDs) using the NAND-NAND form.

## Try It in the Lab

The lab task "Greenhouse fan from NAND gates" gives you three empty gate slots wired as two first-level gates (one looking at `a` and `b`, the other at `b` and `c`) feeding one second-level gate. Your parts drawer has NAND, NOR and XOR gates, but no AND or OR. Fill the slots so the fan output matches the gardener's rule for all 8 input combinations.

Think about: which expression from this lesson uses only one kind of gate? What does De Morgan's law say about a NAND that receives two NAND outputs?

## Common Mistakes

- **Reading `+` as arithmetic.** In Boolean algebra `1 + 1 = 1`. There is no carry and no 2.
- **Forgetting to flip the operator in De Morgan.** `(a·b)'` is `a' + b'`, not `a'·b'`. Negating each variable without swapping AND/OR is the most common error in this whole topic.
- **Putting the NOT on the wrong thing.** `a'·b'` (not a, and not b) is different from `(a·b)'` (not both). Check with the row a=1, b=0: the first gives 0, the second gives 1.
- **Using natural binary order on a Karnaugh map.** Columns must go 00, 01, 11, 10, otherwise neighbours differ in two bits and your groups are wrong.
- **Making groups that are not powers of two, or not rectangles.** A group of 3 cells does not correspond to a single product term.
- **Assuming the shortest expression is the best circuit.** Fewer literals usually helps, but the available gate types (NAND only?), the delay and the wiring also matter.

## Exercises

1. Prove `a + a'·b = a + b` with a truth table. Then explain it in words with an everyday example.
2. Use De Morgan to write `(a + b'·c)'` without any NOT over a bracket.
3. A 3-input function is 1 on rows 1, 3, 5 and 7 (a, b, c in binary counting order). Write its sum of products and simplify it. What does the function depend on?
4. Draw the Karnaugh map of `y = a'·b'·c' + a'·b'·c + a·b'·c' + a·b'·c` and simplify. (Hint: 4 cells in one group.)
5. The **majority** function of three inputs is 1 when at least two inputs are 1. Write its truth table, its sum of products, and simplify it with a Karnaugh map to `a·b + b·c + a·c`. How many 2-input NAND gates would the NAND-NAND form need if you only had 2-input gates? (Hint: a 3-input OR needs to be split.)

## Key Terms

| Term | What people say | What it actually means |
|---|---|---|
| Boolean algebra | "Logic math" | An algebra on {0, 1} with AND, OR, NOT and laws like De Morgan and absorption |
| Truth table | "The table of all cases" | The output listed for all 2^n input combinations; the complete definition of a combinational function |
| Sum of products | "OR of ANDs" | An expression made of product terms joined by OR; any truth table can be written this way |
| Minterm | "One row as a formula" | A product of all variables, each plain or negated, that is 1 on exactly one row |
| De Morgan's laws | "Break the bar, change the sign" | `(a·b)' = a' + b'` and `(a+b)' = a'·b'` |
| Karnaugh map | "K-map" | A Gray-coded grid of the truth table where adjacent 1s merge into simpler product terms |
| Don't care | "X" | An output value we may choose freely because that input never happens or does not matter |

## Further Reading

- Claude E. Shannon, *A Symbolic Analysis of Relay and Switching Circuits*, MIT master's thesis (1937; published in Transactions of the AIEE, 1938).
- M. Morris Mano and Michael D. Ciletti, *Digital Design*, Chapters 2-3 (Boolean algebra and gate-level minimization, including map methods).
- All About Circuits, *Digital* textbook (Vol. IV), chapters "Boolean Algebra" and "Karnaugh Mapping".
- Charles Petzold, *Code*, chapter on logic and switches, for the history from Boole to Shannon.
