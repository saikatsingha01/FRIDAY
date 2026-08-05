# FRIDAY Randomized Stress Test Report

- **Date**: 2026-08-05 19:38:38
- **Seed**: 20260805
- **Target tests**: 1000 (unique messages, none repeated)
- **Tests completed**: 1000
- **Model**: llama3.2:3b (Ollama) | embeddings: nomic-embed-text
- **Concurrency**: 4 workers | analyze timeout 240s
- **Store**: redirected to scratch workspace (real data untouched)

## Summary

| Category | Tests | Pass | Fail | Error | Pass rate |
|---|---|---|---|---|---|
| A | 150 | 150 | 0 | 0 | 100.0% |
| B | 120 | 120 | 0 | 0 | 100.0% |
| C | 160 | 160 | 0 | 0 | 100.0% |
| D | 200 | 200 | 0 | 0 | 100.0% |
| E | 100 | 100 | 0 | 0 | 100.0% |
| F | 120 | 108 | 12 | 0 | 90.0% |
| G | 40 | 40 | 0 | 0 | 100.0% |
| H | 40 | 40 | 0 | 0 | 100.0% |
| R-sem | 30 | 30 | 0 | 0 | 100.0% |
| R-pro | 15 | 10 | 5 | 0 | 66.7% |
| R-epi | 15 | 15 | 0 | 0 | 100.0% |
| R-hist | 10 | 10 | 0 | 0 | 100.0% |
| **TOTAL** | 1000 | 983 | 17 | 0 | 98.3% |

## Test Results (every test)

| id | cat | message | expected | actual | result | issue |
|---|---|---|---|---|---|---|
| 0 | A | my favorite city is bogota | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 1 | A | my favorite city is jakarta | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 10 | A | my favorite book is project hail mary | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 100 | A | my favorite drink is sparkling water | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 101 | A | my favorite subject is law | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 102 | A | my favorite writer is george eliot | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 103 | A | my favorite city is toronto | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 104 | A | my favorite game is super mario odyssey | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 105 | A | my favorite dessert is beignets | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 106 | A | i am from prague | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 107 | A | i am from milan | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 108 | A | my favorite show is the umbrellas | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 109 | A | my favorite subject is network engineering | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 11 | A | my favorite book is anne of green gables | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 110 | A | my favorite book is beloved | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 111 | A | i work as a weaver | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 112 | A | my favorite animal is beetle | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 113 | A | my favorite subject is genetics | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 114 | A | my favorite game is breath of the wild | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 115 | A | i am from dubai | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 116 | A | my pet's name is max | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 117 | A | my favorite food is bhel puri | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 118 | A | i am from kathmandu | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 119 | A | my favorite hobby is rock climbing | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 12 | A | i am from kyoto | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 120 | A | my favorite hobby is crosswords | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 121 | A | my favorite game is zelda | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 122 | A | i am from stockholm | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 123 | A | my favorite game is stardew valley | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 124 | A | my favorite game is hades | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 125 | A | my favorite writer is haruki murakami | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 126 | A | my favorite sport is tennis | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 127 | A | my favorite hobby is card games | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 128 | A | my favorite show is the twilight zone | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 129 | A | my favorite game is forza horizon | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 13 | A | my favorite animal is seahorse | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 130 | A | my favorite hobby is dioramas | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 131 | A | my favorite drink is red wine | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 132 | A | i work as a librarian | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 133 | A | i am from hanoi | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 134 | A | my favorite book is sapiens | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 135 | A | i am from lima | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 136 | A | my favorite hobby is wine tasting | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 137 | A | my favorite music is bachata | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 138 | A | my pet's name is milo | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 139 | A | my favorite hobby is paddleboarding | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 14 | A | my favorite sport is ice hockey | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 140 | A | my favorite drink is buttermilk | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 141 | A | my favorite game is outer wilds | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 142 | A | my favorite drink is coffee | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 143 | A | my favorite show is stranger things | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 144 | A | my favorite food is calamari | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 145 | A | my favorite book is little women | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 146 | A | my favorite movie is inception | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 147 | A | my favorite animal is ant | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 148 | A | my favorite show is the bear | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 149 | A | my favorite movie is arrival | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 15 | A | my favorite show is parks and recreation | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 150 | B | my favorite breakfast is jambalaya | update (old value replaced by new) | seed=stored op=update status=stored v2_present=True old_present=True | PASS | old value still present alongside new |
| 151 | B | my favorite breakfast is moussaka | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 152 | B | my favorite breakfast is vindaloo | update (old value replaced by new) | seed=updated op=update status=stored v2_present=True old_present=True | PASS | old value still present alongside new |
| 153 | B | my favorite breakfast is nachos | update (old value replaced by new) | seed=needs_confirmation op=update status=updated v2_present=True old_present=False | PASS |  |
| 154 | B | my favorite breakfast is samosa | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 155 | B | my favorite breakfast is bhel puri | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 156 | B | my favorite breakfast is poha | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 157 | B | my favorite breakfast is dumplings | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 158 | B | my favorite breakfast is shepherd pie | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 159 | B | my favorite breakfast is pizza | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 16 | A | my favorite season is monsoon | store (durable casual fact persists) | op=update status=stored present=True | PASS |  |
| 160 | B | my favorite breakfast is kebabs -> now my favorite breakfast is nachos | update (old value replaced by new) | seed=stored op=update status=updated v2_present=True | PASS |  |
| 161 | B | my favorite breakfast is polenta | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 162 | B | my favorite breakfast is falafel | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 163 | B | my favorite breakfast is risotto | update (old value replaced by new) | seed=needs_confirmation op=update status=updated v2_present=True old_present=False | PASS |  |
| 164 | B | my favorite breakfast is pancakes -> now my favorite breakfast is coleslaw | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True | PASS |  |
| 165 | B | my favorite breakfast is biryani -> now my favorite breakfast is burrito | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True | PASS |  |
| 166 | B | my favorite breakfast is gnocchi | update (old value replaced by new) | seed=needs_confirmation op=update status=updated v2_present=True old_present=False | PASS |  |
| 167 | B | my favorite breakfast is burger | update (old value replaced by new) | seed=needs_confirmation op=update status=updated v2_present=True old_present=False | PASS |  |
| 168 | B | my favorite lunch is vindaloo | update (old value replaced by new) | seed=stored op=update status=updated v2_present=True old_present=False | PASS |  |
| 169 | B | my favorite lunch is samosa | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 17 | A | my favorite cuisine is hungarian | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 170 | B | my favorite lunch is calamari | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=False | PASS |  |
| 171 | B | my favorite lunch is risotto | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 172 | B | my favorite lunch is pancakes | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 173 | B | my favorite lunch is thai curry | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 174 | B | my favorite lunch is poutine | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 175 | B | my favorite lunch is sandwich | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 176 | B | my favorite lunch is gyoza | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 177 | B | my favorite lunch is lobster roll | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 178 | B | my favorite lunch is paella | update (old value replaced by new) | seed=ignored op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 179 | B | my favorite lunch is ceviche | update (old value replaced by new) | seed=needs_confirmation op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 18 | A | my favorite writer is astrid lindgren | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 180 | B | my favorite lunch is pizza | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 181 | B | my favorite lunch is bhel puri | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 182 | B | my favorite lunch is dumplings | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 183 | B | my favorite lunch is guacamole | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 184 | B | my favorite lunch is oysters | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 185 | B | my favorite dinner is bruschetta | update (old value replaced by new) | seed=needs_confirmation op=store status=stored v2_present=True old_present=True | PASS | old value still present alongside new |
| 186 | B | my favorite dinner is gumbo | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 187 | B | my favorite dinner is polenta | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 188 | B | my favorite dinner is palak paneer | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 189 | B | my favorite dinner is poha | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 19 | A | my favorite drink is frappe | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 190 | B | my favorite dinner is gnocchi | update (old value replaced by new) | seed=stored op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 191 | B | my favorite dinner is oysters | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 192 | B | my favorite dinner is dumplings -> now my favorite dinner is oysters | update (old value replaced by new) | seed=stored op=update status=updated v2_present=True | PASS |  |
| 193 | B | my favorite dinner is samosa | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 194 | B | my favorite dinner is burrito | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 195 | B | my favorite dinner is waffles | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 196 | B | my favorite dinner is jambalaya | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 197 | B | my favorite dinner is ramen | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 198 | B | my favorite dinner is pasta | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 199 | B | my favorite dinner is banh mi | update (old value replaced by new) | seed=needs_confirmation op=update status=updated v2_present=True old_present=False | PASS |  |
| 2 | A | my favorite subject is archaeology | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 20 | A | my favorite book is war and peace | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 200 | B | my favorite dinner is moussaka | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 201 | B | my favorite dinner is pierogi | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 202 | B | my favorite soup is dosa | update (old value replaced by new) | seed=stored op=update status=updated v2_present=True old_present=False | PASS |  |
| 203 | B | my favorite soup is kebabs | update (old value replaced by new) | seed=ignored op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 204 | B | my favorite soup is butter chicken | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 205 | B | my favorite soup is chow mein | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 206 | B | my favorite soup is mac and cheese | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 207 | B | my favorite soup is sandwich | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 208 | B | my favorite soup is ramen | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 209 | B | my favorite soup is waffles | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 21 | A | my favorite fruit is orange | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 210 | B | my favorite soup is palak paneer | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 211 | B | my favorite soup is idli | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 212 | B | my favorite soup is polenta | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 213 | B | my favorite soup is gyoza | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 214 | B | my favorite soup is samosa | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 215 | B | my favorite soup is vindaloo | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 216 | B | my favorite soup is dumplings | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 217 | B | my favorite soup is pancakes | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 218 | B | my favorite soup is shepherd pie | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 219 | B | my favorite pasta dish is samosa | update (old value replaced by new) | seed=stored op=update status=updated v2_present=True old_present=False | PASS |  |
| 22 | A | my favorite color is blush | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 220 | B | my favorite pasta dish is paratha | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 221 | B | my favorite pasta dish is pho | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 222 | B | my favorite pasta dish is moussaka | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 223 | B | my favorite pasta dish is ceviche | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 224 | B | my favorite pasta dish is paella | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 225 | B | my favorite pasta dish is jambalaya | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 226 | B | my favorite pasta dish is noodles | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 227 | B | my favorite pasta dish is palak paneer | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 228 | B | my favorite pasta dish is calamari | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 229 | B | my favorite pasta dish is onion rings | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 23 | A | my favorite food is fried rice | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 230 | B | my favorite pasta dish is shepherd pie | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 231 | B | my favorite pasta dish is gyoza -> now my favorite pasta dish is onion rings | update (old value replaced by new) | seed=stored op=update status=updated v2_present=True | PASS |  |
| 232 | B | my favorite pasta dish is kebabs | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 233 | B | my favorite pasta dish is polenta | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 234 | B | my favorite pasta dish is naan | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 235 | B | my favorite pasta dish is thai curry | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 236 | B | my favorite bread is korean bbq | update (old value replaced by new) | seed=stored op=update status=stored v2_present=True old_present=True | PASS | old value still present alongside new |
| 237 | B | my favorite bread is mac and cheese | update (old value replaced by new) | seed=stored op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 238 | B | my favorite bread is gyoza | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 239 | B | my favorite bread is empanadas | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 24 | A | i am from cairo | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 240 | B | my favorite bread is tamale | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 241 | B | my favorite bread is fried rice | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 242 | B | my favorite bread is paella | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 243 | B | my favorite bread is noodles | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 244 | B | my favorite bread is guacamole | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 245 | B | my favorite bread is lobster roll | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 246 | B | my favorite bread is coleslaw | update (old value replaced by new) | seed=ignored op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 247 | B | my favorite bread is palak paneer | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 248 | B | my favorite bread is dosa | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 249 | B | my favorite bread is paratha | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 25 | A | my favorite city is mexico city | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 250 | B | my favorite bread is chow mein | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 251 | B | my favorite bread is ceviche | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 252 | B | my favorite bread is ramen | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 253 | B | my favorite cheese is calamari | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 254 | B | my favorite cheese is pancakes | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 255 | B | my favorite cheese is waffles | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 256 | B | my favorite cheese is mac and cheese | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 257 | B | my favorite cheese is oysters | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 258 | B | my favorite cheese is curry | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 259 | B | my favorite cheese is empanadas | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 26 | A | my favorite cuisine is kerala | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 260 | B | my favorite cheese is samosa | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 261 | B | my favorite cheese is ramen | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 262 | B | my favorite cheese is sushi | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 263 | B | my favorite cheese is pasta | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 264 | B | my favorite cheese is gyoza | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 265 | B | my favorite cheese is naan | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 266 | B | my favorite cheese is lobster roll | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 267 | B | my favorite cheese is bhel puri | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 268 | B | my favorite cheese is biryani | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 269 | B | my favorite cheese is poutine | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 27 | A | my favorite sport is wrestling | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 270 | C | my favorite juice is rose lemonade | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 271 | C | my favorite juice is pineapple juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 272 | C | my favorite juice is limeade | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 273 | C | my favorite juice is cafe au lait | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 274 | C | my favorite juice is sparkling lemonade | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 275 | C | my favorite juice is mocha | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 276 | C | my favorite juice is apple cider | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 277 | C | my favorite juice is ale | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 278 | C | my favorite juice is beer | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 279 | C | my favorite juice is stout | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 28 | A | my favorite hobby is drumming | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 280 | C | my favorite juice is frappe | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 281 | C | my favorite juice is soda water | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 282 | C | my favorite juice is kombucha | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 283 | C | my favorite juice is black tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 284 | C | my favorite juice is yerba mate | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 285 | C | my favorite juice is grape juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 286 | C | my favorite juice is sparkling water | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 287 | C | my favorite juice is cherry soda | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 288 | C | my favorite juice is hibiscus tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 289 | C | my favorite juice is tonic water | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 29 | A | my favorite show is narcos | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 290 | C | my favorite juice is dirty chai | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 291 | C | my favorite juice is latte | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 292 | C | my favorite juice is salted lassi | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 293 | C | my favorite milkshake is mango lassi | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 294 | C | my favorite milkshake is cider | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 295 | C | my favorite milkshake is fresh lime soda | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 296 | C | my favorite milkshake is dirty chai | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 297 | C | my favorite milkshake is chai | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 298 | C | my favorite milkshake is watermelon juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 299 | C | my favorite milkshake is iced tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 3 | A | my favorite subject is psychiatry | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 30 | A | my favorite writer is agatha christie | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 300 | C | my favorite milkshake is bubble tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 301 | C | my favorite milkshake is cafe au lait | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 302 | C | my favorite milkshake is sugarcane juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 303 | C | my favorite milkshake is yerba mate | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 304 | C | my favorite milkshake is kombucha | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 305 | C | my favorite milkshake is green tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 306 | C | my favorite milkshake is americano | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 307 | C | my favorite milkshake is iced matcha | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 308 | C | my favorite milkshake is latte | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 309 | C | my favorite milkshake is cherry soda | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 31 | A | my favorite game is animal crossing | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 310 | C | my favorite milkshake is herbal tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 311 | C | my favorite milkshake is guava juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 312 | C | my favorite milkshake is sparkling water | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 313 | C | my favorite milkshake is rose wine | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 314 | C | my favorite milkshake is black tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 315 | C | my favorite milkshake is mango juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 316 | C | my favorite smoothie is dirty chai | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 317 | C | my favorite smoothie is lassi | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 318 | C | my favorite smoothie is rose lemonade | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 319 | C | my favorite smoothie is cider | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 32 | A | my pet's name is bella | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 320 | C | my favorite smoothie is prosecco | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 321 | C | my favorite smoothie is cappuccino | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 322 | C | my favorite smoothie is hot chocolate | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 323 | C | my favorite smoothie is mango lassi | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 324 | C | my favorite smoothie is espresso | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 325 | C | my favorite smoothie is ginger ale | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 326 | C | my favorite smoothie is apple cider | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 327 | C | my favorite smoothie is hot toddy | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 328 | C | my favorite smoothie is americano | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 329 | C | my favorite smoothie is orange juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 33 | A | my favorite subject is thermodynamics | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 330 | C | my favorite smoothie is bubble tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 331 | C | my favorite smoothie is badam milk | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 332 | C | my favorite smoothie is buttermilk | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 333 | C | my favorite smoothie is lemonade | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 334 | C | my favorite smoothie is sweet lassi | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 335 | C | my favorite smoothie is milkshake | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 336 | C | my favorite smoothie is peppermint tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 337 | C | my favorite smoothie is coconut water | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 338 | C | my favorite smoothie is masala chai | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 339 | C | my favorite tea is iced tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 34 | A | my favorite cuisine is cambodian | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 340 | C | my favorite tea is orange soda | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 341 | C | my favorite tea is apple juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 342 | C | my favorite tea is buttermilk | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 343 | C | my favorite tea is red wine | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 344 | C | my favorite tea is hibiscus tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 345 | C | my favorite tea is peppermint tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 346 | C | my favorite tea is yerba mate | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 347 | C | my favorite tea is mango lassi | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 348 | C | my favorite tea is hot toddy | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 349 | C | my favorite tea is beet juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 35 | A | my favorite fruit is pomelo | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 350 | C | my favorite tea is carrot juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 351 | C | my favorite tea is masala chai | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 352 | C | my favorite tea is pomegranate juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 353 | C | my favorite tea is green tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 354 | C | my favorite tea is root beer | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 355 | C | my favorite tea is chai | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 356 | C | my favorite tea is tonic water | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 357 | C | my favorite tea is jasmine tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 358 | C | my favorite tea is latte | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 359 | C | my favorite tea is fresh lime soda | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 36 | A | my favorite sport is archery | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 360 | C | my favorite tea is coffee | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 361 | C | my favorite tea is frappe | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 362 | C | my favorite soda is birch beer | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 363 | C | my favorite soda is falooda | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 364 | C | my favorite soda is cappuccino | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 365 | C | my favorite soda is badam milk | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 366 | C | my favorite soda is pineapple juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 367 | C | my favorite soda is espresso | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 368 | C | my favorite soda is masala chai | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 369 | C | my favorite soda is beer | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 37 | A | my favorite cuisine is mexican | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 370 | C | my favorite soda is eggnog | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 371 | C | my favorite soda is salted lassi | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 372 | C | my favorite soda is lassi | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 373 | C | my favorite soda is herbal tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 374 | C | my favorite soda is dirty chai | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 375 | C | my favorite soda is oolong | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 376 | C | my favorite soda is smoothie | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 377 | C | my favorite soda is coconut water | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 378 | C | my favorite soda is kombucha | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 379 | C | my favorite soda is affogato | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 38 | A | my favorite dessert is apple pie | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 380 | C | my favorite soda is mango lassi | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 381 | C | my favorite soda is ale | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 382 | C | my favorite soda is orange soda | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 383 | C | my favorite soda is cola | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 384 | C | my favorite soda is cherry soda | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 385 | C | my favorite shake is tonic water | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 386 | C | my favorite shake is green tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 387 | C | my favorite shake is cream soda | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 388 | C | my favorite shake is bubble tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 389 | C | my favorite shake is hot chocolate | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 39 | A | my favorite book is divergent | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 390 | C | my favorite shake is oolong | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 391 | C | my favorite shake is salted lassi | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 392 | C | my favorite shake is smoothie | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 393 | C | my favorite shake is flat white | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 394 | C | my favorite shake is pomegranate juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 395 | C | my favorite shake is black tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 396 | C | my favorite shake is orange juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 397 | C | my favorite shake is mango lassi | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 398 | C | my favorite shake is buttermilk | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 399 | C | my favorite shake is badam milk | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 4 | A | my favorite fruit is raspberry | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 40 | A | my favorite color is rust | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 400 | C | my favorite shake is white wine | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 401 | C | my favorite shake is guava juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 402 | C | my favorite shake is cold brew | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 403 | C | my favorite shake is carrot juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 404 | C | my favorite shake is rose lemonade | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 405 | C | my favorite shake is grape juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 406 | C | my favorite shake is herbal tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 407 | C | my favorite shake is kombucha | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 408 | C | my favorite mocktail is pineapple juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 409 | C | my favorite mocktail is sweet lassi | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 41 | A | my favorite hobby is backpacking | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 410 | C | my favorite mocktail is apple juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 411 | C | my favorite mocktail is stout | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 412 | C | my favorite mocktail is peppermint tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 413 | C | my favorite mocktail is falooda | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 414 | C | my favorite mocktail is iced chai | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 415 | C | my favorite mocktail is lassi | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 416 | C | my favorite mocktail is kombucha | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 417 | C | my favorite mocktail is iced matcha | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 418 | C | my favorite mocktail is birch beer | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 419 | C | my favorite mocktail is dirty chai | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 42 | A | i work as a psychologist | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 420 | C | my favorite mocktail is white wine | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 421 | C | my favorite mocktail is cranberry juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 422 | C | my favorite mocktail is masala chai | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 423 | C | my favorite mocktail is mango juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 424 | C | my favorite mocktail is coffee | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 425 | C | my favorite mocktail is red wine | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 426 | C | my favorite mocktail is espresso | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 427 | C | my favorite mocktail is hibiscus tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 428 | C | my favorite mocktail is beer | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 429 | C | my favorite mocktail is pomegranate juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 43 | A | my favorite movie is oppenheimer | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 430 | D | which is better, paella or tamale | no write | op=query | PASS |  |
| 431 | D | how far is amsterdam from barcelona | no write | op=None | PASS |  |
| 432 | D | do you know my favorite animal | no write | op=query | PASS |  |
| 433 | D | which is better, fried rice or biryani | no write | op=query | PASS |  |
| 434 | D | how far is singapore from berlin | no write | op=None | PASS |  |
| 435 | D | when was wto founded | no write | op=None | PASS |  |
| 436 | D | how far is stockholm from bogota | no write | op=None | PASS |  |
| 437 | D | how far is brussels from kathmandu | no write | op=None | PASS |  |
| 438 | D | how far is kathmandu from madrid | no write | op=None | PASS |  |
| 439 | D | which is better, gyoza or bruschetta | no write | op=query | PASS |  |
| 44 | A | i am from montevideo | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 440 | D | how far is rotterdam from florence | no write | op=None | PASS |  |
| 441 | D | which is better, thai curry or gumbo | no write | op=query | PASS |  |
| 442 | D | what do you think about job interview | no write | op=None | PASS |  |
| 443 | D | when was greenpeace founded | no write | op=None | PASS |  |
| 444 | D | how far is athens from dublin | no write | op=None | PASS |  |
| 445 | D | how far is nairobi from belfast | no write | op=None | PASS |  |
| 446 | D | how far is hanoi from copenhagen | no write | op=query | PASS |  |
| 447 | D | which is better, thai curry or korean bbq | no write | op=query | PASS |  |
| 448 | D | how far is venice from amsterdam | no write | op=None | PASS |  |
| 449 | D | what is the capital of sweden | no write | op=None | PASS |  |
| 45 | A | my pet's name is luna | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 450 | D | how far is seville from quito | no write | op=None | PASS |  |
| 451 | D | which is better, mac and cheese or pasta | no write | op=query | PASS |  |
| 452 | D | how far is singapore from manchester | no write | op=None | PASS |  |
| 453 | D | which is better, naan or palak paneer | no write | op=query | PASS |  |
| 454 | D | which is better, chow mein or pho | no write | op=query | PASS |  |
| 455 | D | you remember my favorite cuisine is german | no write | op=query | PASS |  |
| 456 | D | how far is belfast from casablanca | no write | op=None | PASS |  |
| 457 | D | how far is nairobi from oslo | no write | op=None | PASS |  |
| 458 | D | you remember my favorite game is dark souls 3 | no write | op=query | PASS |  |
| 459 | D | which is better, onion rings or naan | no write | op=query | PASS |  |
| 46 | A | my favorite sport is triathlon | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 460 | D | how far is dubai from berlin | no write | op=None | PASS |  |
| 461 | D | which is better, pasta or paella | no write | op=query | PASS |  |
| 462 | D | which is better, coleslaw or burger | no write | op=query | PASS |  |
| 463 | D | you remember my favorite animal is wombat | no write | op=query | PASS |  |
| 464 | D | which is better, momos or guacamole | no write | op=query | PASS |  |
| 465 | D | which is better, onion rings or gnocchi | no write | op=query | PASS |  |
| 466 | D | how far is stockholm from oslo | no write | op=None | PASS |  |
| 467 | D | which is better, ceviche or dumplings | no write | op=query | PASS |  |
| 468 | D | you remember my favorite game is portal | no write | op=query | PASS |  |
| 469 | D | how far is venice from edinburgh | no write | op=None | PASS |  |
| 47 | A | my favorite hobby is geocaching | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 470 | D | how far is paris from dublin | no write | op=None | PASS |  |
| 471 | D | how far is chennai from manila | no write | op=None | PASS |  |
| 472 | D | which is better, idli or shepherd pie | no write | op=query | PASS |  |
| 473 | D | which is better, vindaloo or biryani | no write | op=query | PASS |  |
| 474 | D | how far is belfast from rio de janeiro | no write | op=None | PASS |  |
| 475 | D | how far is copenhagen from edinburgh | no write | op=query | PASS |  |
| 476 | D | who wrote a song of ice and fire | no write | op=None | PASS |  |
| 477 | D | how far is athens from quito | no write | op=None | PASS |  |
| 478 | D | which is better, bhel puri or pancakes | no write | op=query | PASS |  |
| 479 | D | which is better, pierogi or banh mi | no write | op=query | PASS |  |
| 48 | A | my favorite food is momos | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 480 | D | how far is rotterdam from lisbon | no write | op=None | PASS |  |
| 481 | D | which is better, burrito or dumplings | no write | op=query | PASS |  |
| 482 | D | how far is warsaw from montevideo | no write | op=None | PASS |  |
| 483 | D | how far is toronto from seoul | no write | op=None | PASS |  |
| 484 | D | how far is barcelona from kathmandu | no write | op=None | PASS |  |
| 485 | D | who wrote moby dick | no write | op=None | PASS |  |
| 486 | D | how far is quito from zurich | no write | op=None | PASS |  |
| 487 | D | how far is zurich from toronto | no write | op=None | PASS |  |
| 488 | D | which is better, falafel or biryani | no write | op=query | PASS |  |
| 489 | D | how long does it take to cure bacon | no write | op=None | PASS |  |
| 49 | A | my birthday is in april | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 490 | D | how far is toronto from lisbon | no write | op=None | PASS |  |
| 491 | D | how far is seville from rotterdam | no write | op=None | PASS |  |
| 492 | D | how far is kyoto from vienna | no write | op=None | PASS |  |
| 493 | D | what do you think about podcast idea | no write | op=None | PASS |  |
| 494 | D | which is better, burrito or coleslaw | no write | op=query | PASS |  |
| 495 | D | which is better, coleslaw or paratha | no write | op=query | PASS |  |
| 496 | D | which is better, falafel or noodles | no write | op=query | PASS |  |
| 497 | D | you remember my favorite sport is snowboarding | no write | op=query | PASS |  |
| 498 | D | how far is copenhagen from vienna | no write | op=query | PASS |  |
| 499 | D | how does data structures work | no write | op=query | PASS |  |
| 5 | A | my favorite subject is pharmacy | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 50 | A | my favorite dessert is pecan pie | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 500 | D | which is better, hummus plate or kebabs | no write | op=query | PASS |  |
| 501 | D | you remember my favorite animal is shrimp | no write | op=query | PASS |  |
| 502 | D | which is better, burger or vindaloo | no write | op=query | PASS |  |
| 503 | D | how far is lagos from melbourne | no write | op=None | PASS |  |
| 504 | D | where can i buy tuba | no write | op=query | PASS |  |
| 505 | D | how far is cardiff from mexico city | no write | op=None | PASS |  |
| 506 | D | you remember my favorite color is charcoal | no write | op=query | PASS |  |
| 507 | D | how far is zurich from warsaw | no write | op=None | PASS |  |
| 508 | D | how far is lisbon from boston | no write | op=None | PASS |  |
| 509 | D | you remember my favorite animal is fox | no write | op=query | PASS |  |
| 51 | A | my favorite writer is virginia woolf | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 510 | D | which is better, risotto or korean bbq | no write | op=query | PASS |  |
| 511 | D | how far is madrid from oslo | no write | op=None | PASS |  |
| 512 | D | how far is tokyo from melbourne | no write | op=None | PASS |  |
| 513 | D | you remember my favorite drink is guava juice | no write | op=query | PASS |  |
| 514 | D | how far is sao paulo from warsaw | no write | op=None | PASS |  |
| 515 | D | how far is paris from copenhagen | no write | op=query | PASS |  |
| 516 | D | what is the capital of tunisia | no write | op=None | PASS |  |
| 517 | D | how far is seville from lima | no write | op=None | PASS |  |
| 518 | D | you remember my favorite game is half-life | no write | op=query | PASS |  |
| 519 | D | how far is capetown from rotterdam | no write | op=None | PASS |  |
| 52 | A | i work as a referee | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 520 | D | how far is lima from cardiff | no write | op=None | PASS |  |
| 521 | D | which is better, thai curry or naan | no write | op=query | PASS |  |
| 522 | D | how far is melbourne from mexico city | no write | op=None | PASS |  |
| 523 | D | which is better, butter chicken or paratha | no write | op=query | PASS |  |
| 524 | D | how far is mexico city from helsinki | no write | op=None | PASS |  |
| 525 | D | how far is seville from berlin | no write | op=None | PASS |  |
| 526 | D | who wrote the nightingale | no write | op=None | PASS |  |
| 527 | D | which is better, chow mein or falafel | no write | op=query | PASS |  |
| 528 | D | how far is zurich from manila | no write | op=None | PASS |  |
| 529 | D | is nachos healthy | no write | op=None | PASS |  |
| 53 | A | my favorite city is buenos aires | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 530 | D | is risotto healthy | no write | op=None | PASS |  |
| 531 | D | how far is kyoto from cardiff | no write | op=None | PASS |  |
| 532 | D | which is better, mac and cheese or idli | no write | op=query | PASS |  |
| 533 | D | you remember my favorite cuisine is tex-mex | no write | op=query | PASS |  |
| 534 | D | which is better, lobster roll or ramen | no write | op=query | PASS |  |
| 535 | D | which is better, pho or moussaka | no write | op=query | PASS |  |
| 536 | D | how far is santiago from rio de janeiro | no write | op=None | PASS |  |
| 537 | D | how far is buenos aires from stockholm | no write | op=None | PASS |  |
| 538 | D | can you explain compound interest to me | no write | op=query | PASS |  |
| 539 | D | you remember my favorite game is disco elysium | no write | op=query | PASS |  |
| 54 | A | my favorite game is valheim | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 540 | D | how far is nairobi from mumbai | no write | op=None | PASS |  |
| 541 | D | which is better, burrito or risotto | no write | op=query | PASS |  |
| 542 | D | how far is capetown from seoul | no write | op=None | PASS |  |
| 543 | D | you remember my favorite drink is cappuccino | no write | op=query | PASS |  |
| 544 | D | why is the sky blue | no write | op=None | PASS |  |
| 545 | D | which is better, ratatouille or paella | no write | op=query | PASS |  |
| 546 | D | where can i buy cable | no write | op=query | PASS |  |
| 547 | D | you remember my favorite writer is leo tolstoy | no write | op=query | PASS |  |
| 548 | D | how far is manchester from milan | no write | op=None | PASS |  |
| 549 | D | how far is rotterdam from athens | no write | op=None | PASS |  |
| 55 | A | my favorite writer is amitav ghosh | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 550 | D | what is greenhouse effect | no write | op=None | PASS |  |
| 551 | D | how far is mumbai from budapest | no write | op=None | PASS |  |
| 552 | D | which is better, poutine or hummus plate | no write | op=query | PASS |  |
| 553 | D | how far is lima from edinburgh | no write | op=None | PASS |  |
| 554 | D | how far is melbourne from florence | no write | op=None | PASS |  |
| 555 | D | which is better, ceviche or polenta | no write | op=query | PASS |  |
| 556 | D | which is better, guacamole or curry | no write | op=query | PASS |  |
| 557 | D | which is better, fried rice or pancakes | no write | op=query | PASS |  |
| 558 | D | which is better, gumbo or dumplings | no write | op=query | PASS |  |
| 559 | D | you remember my favorite show is fleabag | no write | op=query | PASS |  |
| 56 | A | my favorite music is baroque | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 560 | D | how far is bogota from manchester | no write | op=None | PASS |  |
| 561 | D | how far is delhi from chennai | no write | op=None | PASS |  |
| 562 | D | which is better, dumplings or pizza | no write | op=query | PASS |  |
| 563 | D | which is better, risotto or pizza | no write | op=query | PASS |  |
| 564 | D | which is better, shepherd pie or naan | no write | op=query | PASS |  |
| 565 | D | how far is rome from dublin | no write | op=None | PASS |  |
| 566 | D | where can i buy soundbar | no write | op=query | PASS |  |
| 567 | D | how far is lima from helsinki | no write | op=None | PASS |  |
| 568 | D | which is better, calamari or poha | no write | op=query | PASS |  |
| 569 | D | what time is it in delhi | no write | op=None | PASS |  |
| 57 | A | my favorite hobby is reading | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 570 | D | which is better, samosa or fried rice | no write | op=query | PASS |  |
| 571 | D | which is better, momos or paratha | no write | op=query | PASS |  |
| 572 | D | can you explain climate change to me | no write | op=query | PASS |  |
| 573 | D | which is better, biryani or burger | no write | op=query | PASS |  |
| 574 | D | which is better, pancakes or paratha | no write | op=query | PASS |  |
| 575 | D | which is better, poutine or ratatouille | no write | op=query | PASS |  |
| 576 | D | how far is lima from manila | no write | op=None | PASS |  |
| 577 | D | you remember my favorite drink is hot toddy | no write | op=query | PASS |  |
| 578 | D | what time is it in toronto | no write | op=None | PASS |  |
| 579 | D | which is better, dosa or dosa | no write | op=query | PASS |  |
| 58 | A | my favorite food is ramen | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 580 | D | you remember my favorite food is biryani | no write | op=query | PASS |  |
| 581 | D | which is better, risotto or ratatouille | no write | op=query | PASS |  |
| 582 | D | you remember my favorite drink is milk coffee | no write | op=query | PASS |  |
| 583 | D | how far is rome from nairobi | no write | op=None | PASS |  |
| 584 | D | you remember my favorite subject is biology | no write | op=query | PASS |  |
| 585 | D | which is better, poutine or tacos | no write | op=query | PASS |  |
| 586 | D | which is better, waffles or poutine | no write | op=query | PASS |  |
| 587 | D | how far is venice from nairobi | no write | op=None | PASS |  |
| 588 | D | how far is toronto from seville | no write | op=None | PASS |  |
| 589 | D | how far is sao paulo from tokyo | no write | op=None | PASS |  |
| 59 | A | i am from melbourne | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 590 | D | which is better, korean bbq or gumbo | no write | op=query | PASS |  |
| 591 | D | what is gdp | no write | op=None | PASS |  |
| 592 | D | you remember my favorite dessert is bread pudding | no write | op=query | PASS |  |
| 593 | D | which is better, biryani or fried rice | no write | op=query | PASS |  |
| 594 | D | which is better, waffles or nachos | no write | op=query | PASS |  |
| 595 | D | how far is prague from amsterdam | no write | op=None | PASS |  |
| 596 | D | you remember my favorite show is arcane | no write | op=query | PASS |  |
| 597 | D | which is better, sandwich or paratha | no write | op=query | PASS |  |
| 598 | D | how far is boston from cardiff | no write | op=None | PASS |  |
| 599 | D | you remember my favorite music is techno | no write | op=query | PASS |  |
| 6 | A | my favorite color is seafoam | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 60 | A | my favorite book is the bell jar | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 600 | D | how far is amsterdam from stockholm | no write | op=None | PASS |  |
| 601 | D | you remember my favorite fruit is muskmelon | no write | op=query | PASS |  |
| 602 | D | what is the weather like in florence | no write | op=None | PASS |  |
| 603 | D | which is better, palak paneer or dumplings | no write | op=query | PASS |  |
| 604 | D | which is better, vindaloo or paratha | no write | op=query | PASS |  |
| 605 | D | you remember my favorite game is animal crossing | no write | op=query | PASS |  |
| 606 | D | how far is berlin from hanoi | no write | op=None | PASS |  |
| 607 | D | you remember my favorite animal is dolphin | no write | op=query | PASS |  |
| 608 | D | which is better, guacamole or ratatouille | no write | op=query | PASS |  |
| 609 | D | you remember my favorite game is tears of the kingdom | no write | op=query | PASS |  |
| 61 | A | my favorite color is caramel | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 610 | D | which is better, biryani or sandwich | no write | op=query | PASS |  |
| 611 | D | how far is milan from cairo | no write | op=None | PASS |  |
| 612 | D | how far is brussels from vienna | no write | op=None | PASS |  |
| 613 | D | how far is belfast from florence | no write | op=None | PASS |  |
| 614 | D | how far is casablanca from brussels | no write | op=None | PASS |  |
| 615 | D | which is better, falafel or guacamole | no write | op=query | PASS |  |
| 616 | D | what does idiosyncrasy mean | no write | op=None | PASS |  |
| 617 | D | you remember my favorite hobby is woodworking | no write | op=query | PASS |  |
| 618 | D | what does alacrity mean | no write | op=None | PASS |  |
| 619 | D | how far is manchester from berlin | no write | op=None | PASS |  |
| 62 | A | my favorite food is palak paneer | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 620 | D | which is better, dumplings or dumplings | no write | op=query | PASS |  |
| 621 | D | when was bandai namco founded | no write | op=None | PASS |  |
| 622 | D | how far is milan from boston | no write | op=None | PASS |  |
| 623 | D | how far is cardiff from barcelona | no write | op=None | PASS |  |
| 624 | D | how far is lima from dubai | no write | op=None | PASS |  |
| 625 | D | which is better, ratatouille or banh mi | no write | op=query | PASS |  |
| 626 | D | how far is santiago from helsinki | no write | op=None | PASS |  |
| 627 | D | which is better, naan or curry | no write | op=query | PASS |  |
| 628 | D | how far is bangkok from florence | no write | op=None | PASS |  |
| 629 | D | when was the linux foundation founded | no write | op=None | PASS |  |
| 63 | A | my favorite book is the handmaid tale | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 630 | E | what did we talk about regarding painting class | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 631 | E | recap what we discussed about garden layout | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 632 | E | did we work on ui design together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 633 | E | anything from our chat about fitness routine | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 634 | E | did we work on fitness routine together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 635 | E | did we work on language learning together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 636 | E | what did we talk about regarding bug hunting | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 637 | E | remind me what we planned for marketing campaign | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 638 | E | what did we talk about regarding study group | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 639 | E | anything from our chat about marketing campaign | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 64 | A | my favorite hobby is calligraphy | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 640 | E | recap what we discussed about road trip plan | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 641 | E | anything from our chat about book club | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 642 | E | what did we talk about regarding python project | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 643 | E | remind me what we planned for resume building | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 644 | E | what did we talk about regarding exam preparation | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 645 | E | remind me what we planned for twitch stream | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 646 | E | anything from our chat about python project | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 647 | E | anything from our chat about home office setup | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 648 | E | did we work on machine learning model together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 649 | E | recap what we discussed about cooking class | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 65 | A | my favorite sport is fencing | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 650 | E | anything from our chat about performance tuning | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 651 | E | did we work on salary negotiation together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 652 | E | remind me what we planned for investment plan | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 653 | E | anything from our chat about internship application | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 654 | E | what did we talk about regarding budget plan | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 655 | E | recap what we discussed about bike repair | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 656 | E | anything from our chat about product idea | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 657 | E | did we work on start-up pitch together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 658 | E | what did we talk about regarding photography trip | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 659 | E | did we work on photography trip together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 66 | A | my favorite drink is pomegranate juice | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 660 | E | did we work on newsletter together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 661 | E | what did we talk about regarding visa process | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 662 | E | did we work on app prototype together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 663 | E | anything from our chat about bike repair | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 664 | E | did we work on science fair together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 665 | E | remind me what we planned for game jam | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 666 | E | recap what we discussed about book club | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 667 | E | what did we talk about regarding side hustle | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 668 | E | did we work on resume building together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 669 | E | remind me what we planned for marathon training | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 67 | A | my favorite fruit is gooseberry | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 670 | E | what did we talk about regarding rust project | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 671 | E | remind me what we planned for app prototype | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 672 | E | anything from our chat about photography trip | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 673 | E | remind me what we planned for job interview | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 674 | E | what did we talk about regarding start-up pitch | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 675 | E | recap what we discussed about streaming setup | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 676 | E | what did we talk about regarding product idea | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 677 | E | what did we talk about regarding meal prep | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 678 | E | recap what we discussed about travel itinerary | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 679 | E | recap what we discussed about marathon training | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 68 | A | my favorite animal is salamander | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 680 | E | anything from our chat about data analysis project | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 681 | E | recap what we discussed about twitch stream | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 682 | E | what did we talk about regarding research paper | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 683 | E | did we work on side hustle together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 684 | E | anything from our chat about apartment hunting | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 685 | E | remind me what we planned for meal prep | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 686 | E | recap what we discussed about python project | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 687 | E | remind me what we planned for garden layout | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 688 | E | anything from our chat about debate prep | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 689 | E | what did we talk about regarding job interview | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 69 | A | my favorite color is purple | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 690 | E | remind me what we planned for kitchen renovation | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 691 | E | anything from our chat about side hustle | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 692 | E | recap what we discussed about newsletter | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 693 | E | remind me what we planned for study group | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 694 | E | recap what we discussed about visa process | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 695 | E | anything from our chat about gaming setup | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 696 | E | anything from our chat about group project | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 697 | E | did we work on movie night together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 698 | E | what did we talk about regarding marathon training | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 699 | E | anything from our chat about api integration | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 7 | A | my pet's name is kaju | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 70 | A | my favorite dessert is kulfi | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 700 | E | what did we talk about regarding apartment hunting | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 701 | E | recap what we discussed about fitness routine | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 702 | E | what did we talk about regarding research internship | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 703 | E | recap what we discussed about resume building | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 704 | E | remind me what we planned for group project | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 705 | E | recap what we discussed about code refactor | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 706 | E | remind me what we planned for debate prep | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 707 | E | what did we talk about regarding ui design | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 708 | E | recap what we discussed about podcast idea | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 709 | E | did we work on group project together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 71 | A | my favorite color is silver | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 710 | E | anything from our chat about youtube channel | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 711 | E | did we work on tax filing together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 712 | E | recap what we discussed about homework help | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 713 | E | remind me what we planned for home office setup | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 714 | E | remind me what we planned for youtube channel | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 715 | E | remind me what we planned for podcast idea | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 716 | E | what did we talk about regarding science fair | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 717 | E | did we work on rust project together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 718 | E | remind me what we planned for hackathon | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 719 | E | remind me what we planned for tax filing | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 72 | A | my favorite color is forest | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 720 | E | remind me what we planned for rust project | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 721 | E | recap what we discussed about thesis | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 722 | E | what did we talk about regarding book club | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 723 | E | anything from our chat about business plan | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 724 | E | remind me what we planned for book club | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 725 | E | did we work on meal prep together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 726 | E | anything from our chat about road trip plan | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 727 | E | anything from our chat about job interview | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 728 | E | anything from our chat about website redesign | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 729 | E | did we work on code refactor together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 73 | A | my favorite game is slay the spire | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 730 | F | no wait, i prefer cola for my favorite coffee | context-aware write or safe follow-up | op=update status=stored fact='My favorite coffee is cola' | PASS |  |
| 731 | F | no wait, i prefer sweet lassi for my favorite coffee | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite editor is PyCharm' | FAIL | context update not applied: status=needs_clarification |
| 732 | F | actually my favorite coffee is now badam milk | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is badam milk' | PASS |  |
| 733 | F | now my favorite coffee is taro milk tea | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is taro milk tea' | PASS |  |
| 734 | F | now my favorite coffee is birch beer | context-aware write or safe follow-up | op=update status=stored fact='My favorite coffee is birch beer' | PASS |  |
| 735 | F | now my favorite coffee is buttermilk | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is buttermilk' | PASS |  |
| 736 | F | actually my favorite coffee is now green tea | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is green tea' | PASS |  |
| 737 | F | actually my favorite coffee is now herbal tea | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is herbal tea' | PASS |  |
| 738 | F | actually my favorite coffee is now kombucha | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is kombucha' | PASS |  |
| 739 | F | no wait, i prefer bubble tea for my favorite coffee | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite editor is PyCharm' | FAIL | context update not applied: status=needs_clarification |
| 74 | A | my favorite sport is cross country skiing | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 740 | F | no wait, i prefer kesar milk for my favorite coffee | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite editor is PyCharm' | FAIL | context update not applied: status=needs_clarification |
| 741 | F | actually my favorite coffee is now orange juice | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is orange juice' | PASS |  |
| 742 | F | no wait, i prefer grape juice for my favorite coffee | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite editor is PyCharm' | FAIL | context update not applied: status=needs_clarification |
| 743 | F | no wait, i prefer stout for my favorite coffee | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite editor is PyCharm' | FAIL | context update not applied: status=needs_clarification |
| 744 | F | actually my favorite coffee is now coffee | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite editor is PyCharm' | FAIL | context update not applied: status=needs_clarification |
| 745 | F | no wait, i prefer dirty chai for my favorite coffee | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite editor is PyCharm' | FAIL | context update not applied: status=needs_clarification |
| 746 | F | actually my favorite coffee is now mango lassi | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is mango lassi' | PASS |  |
| 747 | F | actually my favorite coffee is now eggnog | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is eggnog' | PASS |  |
| 748 | F | now my favorite pastry is panna cotta | context-aware write or safe follow-up | op=update status=stored fact='My favorite pastry is panna cotta' | PASS |  |
| 749 | F | no wait, i prefer pavlova for my favorite pastry | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is pavlova' | PASS |  |
| 75 | A | my favorite fruit is nectarine | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 750 | F | now my favorite pastry is donuts | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is donuts' | PASS |  |
| 751 | F | now my favorite pastry is chocolate cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is chocolate cake' | PASS |  |
| 752 | F | no wait, i prefer angel food cake for my favorite pastry | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is angel food cake' | PASS |  |
| 753 | F | no wait, i prefer bread pudding for my favorite pastry | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is bread pudding' | PASS |  |
| 754 | F | no wait, i prefer mishti doi for my favorite pastry | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is mishti doi' | PASS |  |
| 755 | F | no wait, i prefer sandesh for my favorite pastry | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is sandesh' | PASS |  |
| 756 | F | no wait, i prefer crepes for my favorite pastry | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is crepes' | PASS |  |
| 757 | F | now my favorite pastry is mango pudding | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is mango pudding' | PASS |  |
| 758 | F | actually my favorite pastry is now pound cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is pound cake' | PASS |  |
| 759 | F | no wait, i prefer sponge cake for my favorite pastry | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is sponge cake' | PASS |  |
| 76 | A | my favorite food is samosa | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 760 | F | no wait, i prefer mousse for my favorite pastry | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is mousse' | PASS |  |
| 761 | F | no wait, i prefer brownie sundae for my favorite pastry | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is brownie sundae' | PASS |  |
| 762 | F | actually my favorite pastry is now macarons | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is macarons' | PASS |  |
| 763 | F | now my favorite pastry is rasgulla | context-aware write or safe follow-up | op=update status=stored fact='My favorite pastry is rasgulla' | PASS |  |
| 764 | F | now my favorite pastry is brownies | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is brownies' | PASS |  |
| 765 | F | now my favorite pastry is beignets | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is beignets' | PASS |  |
| 766 | F | actually my favorite cake is now pound cake | context-aware write or safe follow-up | op=update status=stored fact='My favorite cake is pound cake' | PASS |  |
| 767 | F | now my favorite cake is apple pie | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is apple pie' | PASS |  |
| 768 | F | now my favorite cake is caramel custard | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is caramel custard' | PASS |  |
| 769 | F | actually my favorite cake is now pumpkin pie | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is pumpkin pie' | PASS |  |
| 77 | A | my favorite cuisine is vietnamese | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 770 | F | no wait, i prefer angel food cake for my favorite cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is angel food cake' | PASS |  |
| 771 | F | actually my favorite cake is now crepes | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is crepes' | PASS |  |
| 772 | F | actually my favorite cake is now jalebi | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is jalebi' | PASS |  |
| 773 | F | no wait, i prefer cheesecake for my favorite cake | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite editor is PyCharm' | FAIL | context update not applied: status=needs_clarification |
| 774 | F | no wait, i prefer laddu for my favorite cake | context-aware write or safe follow-up | op=update status=stored fact='My favorite cake is laddu' | PASS |  |
| 775 | F | now my favorite cake is macarons | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite editor is PyCharm' | FAIL | context update not applied: status=needs_clarification |
| 776 | F | no wait, i prefer donuts for my favorite cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is donuts' | PASS |  |
| 777 | F | no wait, i prefer phirni for my favorite cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is phirni' | PASS |  |
| 778 | F | now my favorite cake is red velvet cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is red velvet cake' | PASS |  |
| 779 | F | now my favorite cake is baklava | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is baklava' | PASS |  |
| 78 | A | i work as a accountant | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 780 | F | actually my favorite cake is now carrot cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is carrot cake' | PASS |  |
| 781 | F | no wait, i prefer tiramisu for my favorite cake | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite editor is PyCharm' | FAIL | context update not applied: status=needs_clarification |
| 782 | F | now my favorite cake is coconut barfi | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is coconut barfi' | PASS |  |
| 783 | F | actually my favorite cake is now brownie sundae | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is brownie sundae' | PASS |  |
| 784 | F | now my favorite candy is pound cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is pound cake' | PASS |  |
| 785 | F | now my favorite candy is mango pudding | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is mango pudding' | PASS |  |
| 786 | F | actually my favorite candy is now brownie sundae | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is brownie sundae' | PASS |  |
| 787 | F | now my favorite candy is sandesh | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is sandesh' | PASS |  |
| 788 | F | no wait, i prefer pecan pie for my favorite candy | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is pecan pie' | PASS |  |
| 789 | F | actually my favorite candy is now rasmalai | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is rasmalai' | PASS |  |
| 79 | A | my favorite drink is guava juice | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 790 | F | no wait, i prefer mishti doi for my favorite candy | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is mishti doi' | PASS |  |
| 791 | F | now my favorite candy is mousse | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is mousse' | PASS |  |
| 792 | F | actually my favorite candy is now angel food cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is angel food cake' | PASS |  |
| 793 | F | no wait, i prefer panna cotta for my favorite candy | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite editor is PyCharm' | FAIL | context update not applied: status=needs_clarification |
| 794 | F | now my favorite candy is macaron tower | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is macaron tower' | PASS |  |
| 795 | F | now my favorite candy is pavlova | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is pavlova' | PASS |  |
| 796 | F | now my favorite candy is red velvet cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is pound cake' | FAIL | context update not applied: status=updated |
| 797 | F | now my favorite candy is creme brulee | context-aware write or safe follow-up | op=update status=updated fact='my favorite candy is creme brulee' | PASS |  |
| 798 | F | actually my favorite candy is now jalebi | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is now Jalebi' | PASS |  |
| 799 | F | actually my favorite candy is now kulfi | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is kulfi' | PASS |  |
| 8 | A | my favorite food is gnocchi | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 80 | A | my pet's name is pepper | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 800 | F | no wait, i prefer truffles for my favorite candy | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is truffles' | PASS |  |
| 801 | F | now my favorite candy is fudge | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is fudge' | PASS |  |
| 802 | F | yeah, makes sense | context-aware write or safe follow-up | op=None | PASS |  |
| 803 | F | please continue | context-aware write or safe follow-up | op=store fact='I need help with my cardiology homework' | PASS | followup auto-wrote (review): op=store fact='I need help with my cardiology homework' |
| 804 | F | so, so what about it | context-aware write or safe follow-up | op=store fact='I am planning a trip to Lima' | PASS | followup auto-wrote (review): op=store fact='I am planning a trip to Lima' |
| 805 | F | so what about it | context-aware write or safe follow-up | op=store fact='negotiation' | PASS | followup auto-wrote (review): op=store fact='negotiation' |
| 806 | F | yeah, yes you tell me | context-aware write or safe follow-up | op=store fact='I am planning a trip to Manila' | PASS | followup auto-wrote (review): op=store fact='I am planning a trip to Manila' |
| 807 | F | yeah, fine | context-aware write or safe follow-up | op=store fact='I study B.Tech' | PASS | followup auto-wrote (review): op=store fact='I study B.Tech' |
| 808 | F | continue | context-aware write or safe follow-up | op=None | PASS |  |
| 809 | F | go on then | context-aware write or safe follow-up | op=store fact='You are working on your salary negotiation' | PASS | followup auto-wrote (review): op=store fact='You are working on your salary negotiation' |
| 81 | A | my favorite game is hellblade | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 810 | F | yeah, go ahead | context-aware write or safe follow-up | op=None | PASS |  |
| 811 | F | yeah, please continue | context-aware write or safe follow-up | op=query | PASS |  |
| 812 | F | and then what | context-aware write or safe follow-up | op=None | PASS |  |
| 813 | F | okay, fine | context-aware write or safe follow-up | op=None | PASS |  |
| 814 | F | okay, so | context-aware write or safe follow-up | op=None | PASS |  |
| 815 | F | okay, continue | context-aware write or safe follow-up | op=store fact='I am working on my bike repair' | PASS | followup auto-wrote (review): op=store fact='I am working on my bike repair' |
| 816 | F | fine | context-aware write or safe follow-up | op=store | PASS |  |
| 817 | F | okay, yes you tell me | context-aware write or safe follow-up | op=update fact='My favorite editor is PyCharm' | PASS | followup auto-wrote (review): op=update fact='My favorite editor is PyCharm' |
| 818 | F | yeah, yes please | context-aware write or safe follow-up | op=store fact='I want to update the conversation topic' | PASS | followup auto-wrote (review): op=store fact='I want to update the conversation topic' |
| 819 | F | so, yes you tell me | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 82 | A | i work as a electrician | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 820 | F | okay | context-aware write or safe follow-up | op=None | PASS |  |
| 821 | F | makes sense | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 822 | F | ok then | context-aware write or safe follow-up | op=update fact='I plan a trip to Zurich' | PASS | followup auto-wrote (review): op=update fact='I plan a trip to Zurich' |
| 823 | F | yeah, go on then | context-aware write or safe follow-up | op=None | PASS |  |
| 824 | F | okay, tell me more | context-aware write or safe follow-up | op=query | PASS |  |
| 825 | F | yes you tell me | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 826 | F | okay, go on | context-aware write or safe follow-up | op=store fact='I am thinking about chow mein for dinner' | PASS | followup auto-wrote (review): op=store fact='I am thinking about chow mein for dinner' |
| 827 | F | yeah, got it, go on | context-aware write or safe follow-up | op=update fact='My favorite editor is PyCharm' | PASS | followup auto-wrote (review): op=update fact='My favorite editor is PyCharm' |
| 828 | F | okay, proceed | context-aware write or safe follow-up | op=None | PASS |  |
| 829 | F | okay, right | context-aware write or safe follow-up | op=None | PASS |  |
| 83 | A | my favorite music is afrobeat | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 830 | F | okay, okay go | context-aware write or safe follow-up | op=update fact='My favorite editor is PyCharm' | PASS | followup auto-wrote (review): op=update fact='My favorite editor is PyCharm' |
| 831 | F | yeah, so | context-aware write or safe follow-up | op=None | PASS |  |
| 832 | F | you were saying | context-aware write or safe follow-up | op=store fact='I study B.Tech' | PASS | followup auto-wrote (review): op=store fact='I study B.Tech' |
| 833 | F | yeah, right, go ahead | context-aware write or safe follow-up | op=update fact='My favorite editor is PyCharm' | PASS | followup auto-wrote (review): op=update fact='My favorite editor is PyCharm' |
| 834 | F | so, go on then | context-aware write or safe follow-up | op=None | PASS |  |
| 835 | F | okay, you were saying | context-aware write or safe follow-up | op=update fact='My favorite editor is PyCharm' | PASS | followup auto-wrote (review): op=update fact='My favorite editor is PyCharm' |
| 836 | F | so, tell me | context-aware write or safe follow-up | op=query | PASS |  |
| 837 | F | okay, sure thing | context-aware write or safe follow-up | op=None | PASS |  |
| 838 | F | yeah, yeah go ahead | context-aware write or safe follow-up | op=None | PASS |  |
| 839 | F | go ahead | context-aware write or safe follow-up | op=update fact='My favorite editor is PyCharm' | PASS | followup auto-wrote (review): op=update fact='My favorite editor is PyCharm' |
| 84 | A | i am from berlin | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 840 | F | okay, make sense, continue | context-aware write or safe follow-up | op=store fact='i am planning a trip to delhi' | PASS | followup auto-wrote (review): op=store fact='i am planning a trip to delhi' |
| 841 | F | so, and then | context-aware write or safe follow-up | op=store | PASS |  |
| 842 | F | so, right | context-aware write or safe follow-up | op=None | PASS |  |
| 843 | F | so | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 844 | F | okay, please continue | context-aware write or safe follow-up | op=store fact='i need help with my geography homework' | PASS | followup auto-wrote (review): op=store fact='i need help with my geography homework' |
| 845 | F | okay, okay | context-aware write or safe follow-up | op=None | PASS |  |
| 846 | F | yeah, and then what | context-aware write or safe follow-up | op=store fact='Florence' | PASS | followup auto-wrote (review): op=store fact='Florence' |
| 847 | F | yeah, yes, go on | context-aware write or safe follow-up | op=store fact='I am thinking about vindaloo for dinner' | PASS | followup auto-wrote (review): op=store fact='I am thinking about vindaloo for dinner' |
| 848 | F | okay, interesting | context-aware write or safe follow-up | op=store fact='I study B.Tech' | PASS | followup auto-wrote (review): op=store fact='I study B.Tech' |
| 849 | F | yeah, alright | context-aware write or safe follow-up | op=None | PASS |  |
| 85 | A | my favorite hobby is billiards | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 850 | G | yeah, enough for today | no write (session/meta) | op=None es=True | PASS |  |
| 851 | G | hmm, set that aside | no write (session/meta) | op=None es=False | PASS |  |
| 852 | G | um, good night | no write (session/meta) | op=None es=None | PASS |  |
| 853 | G | so, exit | no write (session/meta) | op=None es=True | PASS |  |
| 854 | G | hmm, i am going to rest | no write (session/meta) | op=None es=True | PASS |  |
| 855 | G | um, i am going to rest | no write (session/meta) | op=None es=True | PASS |  |
| 856 | G | um, this session is over | no write (session/meta) | op=None es=True | PASS |  |
| 857 | G | yeah, okay i am done | no write (session/meta) | op=None es=True | PASS |  |
| 858 | G | thats enough for me today | no write (session/meta) | op=None es=True | PASS |  |
| 859 | G | um, stop listening | no write (session/meta) | op=None es=False | PASS |  |
| 86 | A | my favorite color is mint | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 860 | G | um, skip this topic | no write (session/meta) | op=None es=False | PASS |  |
| 861 | G | um, forget this topic | no write (session/meta) | op=None es=False | PASS |  |
| 862 | G | yeah, shelve this topic | no write (session/meta) | op=None es=False | PASS |  |
| 863 | G | yeah, set that aside | no write (session/meta) | op=None es=False | PASS |  |
| 864 | G | okay, this session is over | no write (session/meta) | op=None es=False | PASS |  |
| 865 | G | so, thats enough for me today | no write (session/meta) | op=None es=True | PASS |  |
| 866 | G | so, i need to rest now | no write (session/meta) | op=None es=False | PASS |  |
| 867 | G | um, time to sleep | no write (session/meta) | op=None es=True | PASS |  |
| 868 | G | hmm, i'm turning in for the night | no write (session/meta) | op=None es=True | PASS |  |
| 869 | G | um, shelve this topic | no write (session/meta) | op=None es=False | PASS |  |
| 87 | A | my favorite book is to kill a mockingbird | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 870 | G | hmm, lets change the subject | no write (session/meta) | op=None es=False | PASS |  |
| 871 | G | okay, that topic is over | no write (session/meta) | op=None es=False | PASS |  |
| 872 | G | moving on | no write (session/meta) | op=None es=False | PASS |  |
| 873 | G | um, on a different note | no write (session/meta) | op=None es=False | PASS |  |
| 874 | G | hmm, miss this topic | no write (session/meta) | op=None es=False | PASS |  |
| 875 | G | yeah, we're done here | no write (session/meta) | op=None es=False | PASS |  |
| 876 | G | okay, lets switch topics | no write (session/meta) | op=None es=False | PASS |  |
| 877 | G | miss this topic | no write (session/meta) | op=None es=False | PASS |  |
| 878 | G | hmm, stop the session | no write (session/meta) | op=None es=False | PASS |  |
| 879 | G | yeah, that's it for now | no write (session/meta) | op=None es=True | PASS |  |
| 88 | A | my favorite book is educated | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 880 | G | um, lets move past this | no write (session/meta) | op=None es=False | PASS |  |
| 881 | G | lets call it a day | no write (session/meta) | op=None es=True | PASS |  |
| 882 | G | so, stop the session | no write (session/meta) | op=None es=False | PASS |  |
| 883 | G | so, time to sleep | no write (session/meta) | op=None es=True | PASS |  |
| 884 | G | um, exit | no write (session/meta) | op=None es=True | PASS |  |
| 885 | G | so, lets change the subject | no write (session/meta) | op=None es=False | PASS |  |
| 886 | G | power down | no write (session/meta) | op=None es=True | PASS |  |
| 887 | G | okay, stop listening | no write (session/meta) | op=forget es=False | PASS |  |
| 888 | G | yeah, i am done | no write (session/meta) | op=None es=True | PASS |  |
| 889 | G | yeah, this session is over | no write (session/meta) | op=None es=False | PASS |  |
| 89 | A | my favorite movie is the matrix | store (durable casual fact persists) | op=update status=stored present=True | PASS |  |
| 890 | H | my favorite music genre is minimalism | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 891 | H | my favorite music genre is folk | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 892 | H | my favorite music genre is highlife | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 893 | H | my favorite music genre is noise | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 894 | H | my favorite music genre is drum and bass | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 895 | H | my favorite music genre is disco | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 896 | H | my favorite music genre is house | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 897 | H | my favorite playlist is drum and bass | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 898 | H | my favorite playlist is blues | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 899 | H | my favorite playlist is folk | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 9 | A | my favorite sport is figure skating | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 90 | A | i work as a glassblower | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 900 | H | my favorite playlist is math rock | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 901 | H | my favorite playlist is r&b | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 902 | H | my favorite playlist is qawwali | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 903 | H | my favorite playlist is ska | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 904 | H | my favorite singer is flamenco | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 905 | H | my favorite singer is punk | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 906 | H | my favorite singer is bachata | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 907 | H | my favorite singer is folk | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 908 | H | my favorite singer is minimalism | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 909 | H | my favorite singer is afrobeat | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 91 | A | my favorite subject is meteorology | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 910 | H | my favorite singer is celtic | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 911 | H | my favorite composer is blues | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 912 | H | my favorite composer is lo-fi | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 913 | H | my favorite composer is gospel | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 914 | H | my favorite composer is soul | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 915 | H | my favorite composer is new wave | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 916 | H | my favorite composer is hip hop | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 917 | H | my favorite composer is bossa nova | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 918 | H | my favorite album is lo-fi | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 919 | H | my favorite album is baroque | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 92 | A | my favorite fruit is tamarind | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 920 | H | my favorite album is ghazal | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 921 | H | my favorite album is trip hop | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 922 | H | my favorite album is rock | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 923 | H | my favorite album is reggaeton | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 924 | H | my favorite lyricist is qawwali | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 925 | H | my favorite lyricist is salsa | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 926 | H | my favorite lyricist is rockabilly | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 927 | H | my favorite lyricist is noise | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 928 | H | my favorite lyricist is blues | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 929 | H | my favorite lyricist is pop | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 93 | A | my favorite city is capetown | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 930 | R-sem | my favorite appetizer is pho | retrieved (semantic) | use_memory=True results=1 hit='pho' | PASS |  |
| 931 | R-sem | my favorite appetizer is lasagna | retrieved (semantic) | use_memory=True results=1 hit='lasagna' | PASS |  |
| 932 | R-sem | my favorite appetizer is onion rings | retrieved (semantic) | use_memory=True results=1 hit='onion rings' | PASS |  |
| 933 | R-sem | my favorite appetizer is empanadas | retrieved (semantic) | use_memory=True results=1 hit='empanadas' | PASS |  |
| 934 | R-sem | my favorite appetizer is moussaka | retrieved (semantic) | use_memory=True results=1 hit='moussaka' | PASS |  |
| 935 | R-sem | my favorite salad is idli | retrieved (semantic) | use_memory=True results=1 hit='idli' | PASS |  |
| 936 | R-sem | my favorite salad is sandwich | retrieved (semantic) | use_memory=True results=1 hit='sandwich' | PASS |  |
| 937 | R-sem | my favorite salad is pasta | retrieved (semantic) | use_memory=True results=1 hit='pasta' | PASS |  |
| 938 | R-sem | my favorite salad is risotto | retrieved (semantic) | use_memory=True results=1 hit='risotto' | PASS |  |
| 939 | R-sem | my favorite salad is poutine | retrieved (semantic) | use_memory=True results=1 hit='poutine' | PASS |  |
| 94 | A | my favorite food is kebabs | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 940 | R-sem | my favorite sauce is ramen | retrieved (semantic) | use_memory=True results=1 hit='ramen' | PASS |  |
| 941 | R-sem | my favorite sauce is butter chicken | retrieved (semantic) | use_memory=True results=1 hit='butter chicken' | PASS |  |
| 942 | R-sem | my favorite sauce is chow mein | retrieved (semantic) | use_memory=True results=1 hit='chow mein' | PASS |  |
| 943 | R-sem | my favorite sauce is poha | retrieved (semantic) | use_memory=True results=1 hit='poha' | PASS |  |
| 944 | R-sem | my favorite sauce is gyoza | retrieved (semantic) | use_memory=True results=1 hit='gyoza' | PASS |  |
| 945 | R-sem | my favorite dip is polenta | retrieved (semantic) | use_memory=True results=1 hit='polenta' | PASS |  |
| 946 | R-sem | my favorite dip is biryani | retrieved (semantic) | use_memory=True results=1 hit='biryani' | PASS |  |
| 947 | R-sem | my favorite dip is hot pot | retrieved (semantic) | use_memory=True results=1 hit='hot pot' | PASS |  |
| 948 | R-sem | my favorite dip is waffles | retrieved (semantic) | use_memory=True results=1 hit='waffles' | PASS |  |
| 949 | R-sem | my favorite dip is coleslaw | retrieved (semantic) | use_memory=True results=1 hit='coleslaw' | PASS |  |
| 95 | A | i am from dublin | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 950 | R-sem | my favorite spread is sushi | retrieved (semantic) | use_memory=True results=1 hit='sushi' | PASS |  |
| 951 | R-sem | my favorite spread is dumplings | retrieved (semantic) | use_memory=True results=1 hit='dumplings' | PASS |  |
| 952 | R-sem | my favorite spread is hot pot | retrieved (semantic) | use_memory=True results=1 hit='hot pot' | PASS |  |
| 953 | R-sem | my favorite spread is samosa | retrieved (semantic) | use_memory=True results=1 hit='samosa' | PASS |  |
| 954 | R-sem | my favorite spread is guacamole | retrieved (semantic) | use_memory=True results=1 hit='guacamole' | PASS |  |
| 955 | R-sem | my favorite side dish is moussaka | retrieved (semantic) | use_memory=True results=1 hit='moussaka' | PASS |  |
| 956 | R-sem | my favorite side dish is paella | retrieved (semantic) | use_memory=True results=1 hit='paella' | PASS |  |
| 957 | R-sem | my favorite side dish is poutine | retrieved (semantic) | use_memory=True results=1 hit='poutine' | PASS |  |
| 958 | R-sem | my favorite side dish is paratha | retrieved (semantic) | use_memory=True results=1 hit='paratha' | PASS |  |
| 959 | R-sem | my favorite side dish is pizza | retrieved (semantic) | use_memory=True results=1 hit='pizza' | PASS |  |
| 96 | A | my favorite drink is grape soda | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 960 | R-pro | my name is tofu | retrieved (profile) | results=1 | PASS |  |
| 961 | R-pro | my name is chip | retrieved (profile) | results=1 | PASS |  |
| 962 | R-pro | my name is mango | retrieved (profile) | use_memory=True results=0 | FAIL | profile query did not return stored fact |
| 963 | R-pro | my name is jack | retrieved (profile) | results=1 | PASS |  |
| 964 | R-pro | my name is waffle | retrieved (profile) | use_memory=True results=0 | FAIL | profile query did not return stored fact |
| 965 | R-pro | my name is kaju | retrieved (profile) | results=1 | PASS |  |
| 966 | R-pro | my name is ginger | retrieved (profile) | results=1 | PASS |  |
| 967 | R-pro | my name is bailey | retrieved (profile) | results=1 | PASS |  |
| 968 | R-pro | my name is sadie | retrieved (profile) | use_memory=True results=0 | FAIL | profile query did not return stored fact |
| 969 | R-pro | my name is molly | retrieved (profile) | results=1 | PASS |  |
| 97 | A | my favorite city is helsinki | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 970 | R-pro | my name is buddy | retrieved (profile) | use_memory=True results=0 | FAIL | profile query did not return stored fact |
| 971 | R-pro | my name is taco | retrieved (profile) | results=1 | PASS |  |
| 972 | R-pro | my name is luna | retrieved (profile) | results=1 | PASS |  |
| 973 | R-pro | my name is misty | retrieved (profile) | use_memory=True results=0 | FAIL | profile query did not return stored fact |
| 974 | R-pro | my name is bella | retrieved (profile) | results=1 | PASS |  |
| 975 | R-epi | recap what we discussed about study group | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 976 | R-epi | recap what we discussed about investment plan | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 977 | R-epi | recap what we discussed about gaming setup | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 978 | R-epi | recap what we discussed about bug hunting | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 979 | R-epi | recap what we discussed about science fair | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 98 | A | my favorite fruit is watermelon | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 980 | R-epi | recap what we discussed about painting class | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 981 | R-epi | recap what we discussed about game jam | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 982 | R-epi | recap what we discussed about database migration | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 983 | R-epi | recap what we discussed about job interview | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 984 | R-epi | recap what we discussed about app prototype | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 985 | R-epi | recap what we discussed about chess bot | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 986 | R-epi | recap what we discussed about budget plan | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 987 | R-epi | recap what we discussed about debate prep | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 988 | R-epi | recap what we discussed about internship application | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 989 | R-epi | recap what we discussed about data analysis project | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 99 | A | i am from capetown | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 990 | R-hist | my favorite seasoning is coleslaw | retrieved (history) | hist=1 | PASS |  |
| 991 | R-hist | my favorite seasoning is noodles | retrieved (history) | hist=1 | PASS |  |
| 992 | R-hist | my favorite seasoning is dumplings | retrieved (history) | hist=1 | PASS |  |
| 993 | R-hist | my favorite seasoning is pierogi | retrieved (history) | hist=1 | PASS |  |
| 994 | R-hist | my favorite seasoning is chow mein | retrieved (history) | hist=1 | PASS |  |
| 995 | R-hist | my favorite condiment is ramen | retrieved (history) | hist=1 | PASS |  |
| 996 | R-hist | my favorite condiment is burger | retrieved (history) | hist=1 | PASS |  |
| 997 | R-hist | my favorite condiment is lobster roll | retrieved (history) | hist=1 | PASS |  |
| 998 | R-hist | my favorite condiment is coleslaw | retrieved (history) | hist=1 | PASS |  |
| 999 | R-hist | my favorite condiment is dumplings | retrieved (history) | hist=1 | PASS |  |

## Issues Found

17 failing/erroring test(s):

- **#731** [F] "no wait, i prefer sweet lassi for my favorite coffee" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite editor is PyCharm'; issue: context update not applied: status=needs_clarification
- **#739** [F] "no wait, i prefer bubble tea for my favorite coffee" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite editor is PyCharm'; issue: context update not applied: status=needs_clarification
- **#740** [F] "no wait, i prefer kesar milk for my favorite coffee" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite editor is PyCharm'; issue: context update not applied: status=needs_clarification
- **#742** [F] "no wait, i prefer grape juice for my favorite coffee" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite editor is PyCharm'; issue: context update not applied: status=needs_clarification
- **#743** [F] "no wait, i prefer stout for my favorite coffee" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite editor is PyCharm'; issue: context update not applied: status=needs_clarification
- **#744** [F] "actually my favorite coffee is now coffee" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite editor is PyCharm'; issue: context update not applied: status=needs_clarification
- **#745** [F] "no wait, i prefer dirty chai for my favorite coffee" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite editor is PyCharm'; issue: context update not applied: status=needs_clarification
- **#773** [F] "no wait, i prefer cheesecake for my favorite cake" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite editor is PyCharm'; issue: context update not applied: status=needs_clarification
- **#775** [F] "now my favorite cake is macarons" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite editor is PyCharm'; issue: context update not applied: status=needs_clarification
- **#781** [F] "no wait, i prefer tiramisu for my favorite cake" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite editor is PyCharm'; issue: context update not applied: status=needs_clarification
- **#793** [F] "no wait, i prefer panna cotta for my favorite candy" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite editor is PyCharm'; issue: context update not applied: status=needs_clarification
- **#796** [F] "now my favorite candy is red velvet cake" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite candy is pound cake'; issue: context update not applied: status=updated
- **#962** [R-pro] "my name is mango" — expected: retrieved (profile); actual: use_memory=True results=0; issue: profile query did not return stored fact
- **#964** [R-pro] "my name is waffle" — expected: retrieved (profile); actual: use_memory=True results=0; issue: profile query did not return stored fact
- **#968** [R-pro] "my name is sadie" — expected: retrieved (profile); actual: use_memory=True results=0; issue: profile query did not return stored fact
- **#970** [R-pro] "my name is buddy" — expected: retrieved (profile); actual: use_memory=True results=0; issue: profile query did not return stored fact
- **#973** [R-pro] "my name is misty" — expected: retrieved (profile); actual: use_memory=True results=0; issue: profile query did not return stored fact
