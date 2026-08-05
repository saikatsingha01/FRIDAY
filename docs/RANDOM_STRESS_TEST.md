# FRIDAY Randomized Stress Test Report

- **Date**: 2026-08-05 09:58:33
- **Seed**: 20260804
- **Target tests**: 5000 (unique messages, none repeated)
- **Tests completed**: 5000
- **Model**: llama3.2:3b (Ollama) | embeddings: nomic-embed-text
- **Concurrency**: 4 workers | analyze timeout 240s
- **Store**: redirected to scratch workspace (real data untouched)

## Summary

| Category | Tests | Pass | Fail | Error | Pass rate |
|---|---|---|---|---|---|
| A | 1000 | 928 | 72 | 0 | 92.8% |
| B | 400 | 293 | 107 | 0 | 73.2% |
| C | 400 | 165 | 235 | 0 | 41.2% |
| D | 1850 | 1845 | 5 | 0 | 99.7% |
| E | 300 | 187 | 113 | 0 | 62.3% |
| F | 350 | 226 | 119 | 5 | 64.6% |
| G | 300 | 279 | 20 | 1 | 93.0% |
| H | 250 | 250 | 0 | 0 | 100.0% |
| R-sem | 60 | 41 | 19 | 0 | 68.3% |
| R-pro | 30 | 22 | 8 | 0 | 73.3% |
| R-epi | 30 | 30 | 0 | 0 | 100.0% |
| R-hist | 30 | 11 | 19 | 0 | 36.7% |
| **TOTAL** | 5000 | 4277 | 717 | 6 | 85.5% |

## Test Results (every test)

| id | cat | message | expected | actual | result | issue |
|---|---|---|---|---|---|---|
| 0 | A | my favorite hobby is ballroom dancing | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 1 | A | my favorite subject is software testing | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 10 | A | my favorite game is demon souls | store (durable casual fact persists) | op=store status=needs_clarification fact="My favorite game is Demon's Souls" | FAIL | store did not persist: status=needs_clarification present=False |
| 100 | A | my favorite book is beloved | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1000 | B | my favorite breakfast is fried rice | update (old value replaced by new) | seed=stored op=update status=updated v2_present=True old_present=False | PASS |  |
| 1001 | B | my favorite breakfast is pizza | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1002 | B | my favorite breakfast is samosa | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1003 | B | my favorite breakfast is poutine | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1004 | B | my favorite breakfast is coleslaw | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1005 | B | my favorite breakfast is bruschetta | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1006 | B | my favorite breakfast is empanadas | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1007 | B | my favorite breakfast is noodles | update (old value replaced by new) | seed=needs_clarification op=store status=updated v2_present=True old_present=False | PASS |  |
| 1008 | B | my favorite breakfast is pierogi | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1009 | B | my favorite breakfast is sandwich | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 101 | A | my favorite hobby is reading | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1010 | B | my favorite breakfast is burrito | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite breakfast is pho' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1011 | B | my favorite breakfast is dosa | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1012 | B | my favorite breakfast is risotto | update (old value replaced by new) | seed=needs_clarification op=store status=updated v2_present=True old_present=False | PASS |  |
| 1013 | B | my favorite breakfast is waffles | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1014 | B | my favorite breakfast is mac and cheese | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1015 | B | my favorite breakfast is palak paneer | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1016 | B | my favorite breakfast is paratha | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1017 | B | my favorite breakfast is poha | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite breakfast is burrito' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1018 | B | my favorite breakfast is ceviche | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1019 | B | my favorite breakfast is shepherd pie | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 102 | A | my favorite dessert is banana bread | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1020 | B | my favorite breakfast is gnocchi | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1021 | B | my favorite breakfast is pasta | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1022 | B | my favorite breakfast is bhel puri | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1023 | B | my favorite breakfast is oysters | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1024 | B | my favorite breakfast is jambalaya | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1025 | B | my favorite breakfast is nachos | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1026 | B | my favorite breakfast is thai curry | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1027 | B | my favorite breakfast is onion rings | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1028 | B | my favorite breakfast is pancakes | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1029 | B | my favorite breakfast is ramen | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 103 | A | my favorite animal is porcupine | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1030 | B | my favorite breakfast is pho | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1031 | B | my favorite breakfast is momos | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1032 | B | my favorite breakfast is tamale | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1033 | B | my favorite breakfast is kebabs | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1034 | B | my favorite breakfast is biryani | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1035 | B | my favorite breakfast is lasagna | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1036 | B | my favorite breakfast is hot pot | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1037 | B | my favorite breakfast is gumbo | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1038 | B | my favorite breakfast is banh mi | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1039 | B | my favorite breakfast is sushi | update (old value replaced by new) | seed=needs_clarification op=store status=updated v2_present=True old_present=False | PASS |  |
| 104 | A | my favorite drink is frappe | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is frappe' | FAIL | store did not persist: status=needs_clarification present=False |
| 1040 | B | my favorite breakfast is dumplings | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1041 | B | my favorite breakfast is idli | update (old value replaced by new) | seed=needs_clarification op=store status=updated v2_present=True old_present=False | PASS |  |
| 1042 | B | my favorite breakfast is polenta | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1043 | B | my favorite breakfast is calamari | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1044 | B | my favorite breakfast is moussaka | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1045 | B | my favorite breakfast is vindaloo | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1046 | B | my favorite breakfast is naan | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1047 | B | my favorite breakfast is korean bbq | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1048 | B | my favorite breakfast is hummus plate | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1049 | B | my favorite breakfast is burger | update (old value replaced by new) | seed=needs_clarification op=store status=updated v2_present=True old_present=False | PASS |  |
| 105 | A | my favorite hobby is pottery class | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1050 | B | my favorite breakfast is gyoza | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite breakfast is coleslaw' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1051 | B | my favorite breakfast is lobster roll | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1052 | B | my favorite breakfast is paella | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1053 | B | my favorite breakfast is butter chicken | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1054 | B | my favorite breakfast is chow mein | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1055 | B | my favorite breakfast is tacos | update (old value replaced by new) | seed=needs_clarification op=store status=updated v2_present=True old_present=False | PASS |  |
| 1056 | B | my favorite breakfast is falafel | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1057 | B | my favorite breakfast is curry | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1058 | B | my favorite lunch is ceviche | update (old value replaced by new) | seed=needs_clarification op=update status=stored v2_present=True old_present=False | PASS |  |
| 1059 | B | my favorite lunch is onion rings | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 106 | A | my favorite subject is ethics | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1060 | B | my favorite lunch is butter chicken | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1061 | B | my favorite lunch is dumplings | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1062 | B | my favorite lunch is samosa | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1063 | B | my favorite lunch is gnocchi | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=False | PASS |  |
| 1064 | B | my favorite lunch is palak paneer | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=False | PASS |  |
| 1065 | B | my favorite lunch is empanadas | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=False | PASS |  |
| 1066 | B | my favorite lunch is sushi | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=False | PASS |  |
| 1067 | B | my favorite lunch is guacamole | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1068 | B | my favorite lunch is falafel | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1069 | B | my favorite lunch is mac and cheese | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 107 | A | my favorite sport is mountain biking | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1070 | B | my favorite lunch is pierogi | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1071 | B | my favorite lunch is dosa | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1072 | B | my favorite lunch is naan | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1073 | B | my favorite lunch is oysters | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=False | PASS |  |
| 1074 | B | my favorite lunch is paratha | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1075 | B | my favorite lunch is poha | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1076 | B | my favorite lunch is sandwich | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=False | PASS |  |
| 1077 | B | my favorite lunch is risotto | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1078 | B | my favorite lunch is gyoza | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1079 | B | my favorite lunch is hummus plate | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 108 | A | my favorite drink is oolong | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is oolong' | FAIL | store did not persist: status=needs_clarification present=False |
| 1080 | B | my favorite lunch is pho | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1081 | B | my favorite lunch is ratatouille | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1082 | B | my favorite lunch is burrito | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1083 | B | my favorite lunch is bhel puri | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1084 | B | my favorite lunch is idli | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1085 | B | my favorite lunch is kebabs | update (old value replaced by new) | seed=ignored op=store status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1086 | B | my favorite lunch is jambalaya | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1087 | B | my favorite lunch is tacos | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1088 | B | my favorite lunch is tamale | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1089 | B | my favorite lunch is polenta | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 109 | A | my favorite drink is kesar milk | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is kesar milk' | FAIL | store did not persist: status=needs_clarification present=False |
| 1090 | B | my favorite lunch is pancakes | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1091 | B | my favorite lunch is vindaloo | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1092 | B | my favorite lunch is lobster roll | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1093 | B | my favorite lunch is chow mein | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1094 | B | my favorite lunch is fried rice | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1095 | B | my favorite lunch is ramen | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1096 | B | my favorite lunch is paella | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1097 | B | my favorite lunch is gumbo | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1098 | B | my favorite lunch is pasta | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1099 | B | my favorite lunch is nachos | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 11 | A | my favorite animal is hamster | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 110 | A | my favorite book is catch 22 | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite book is Catch-22' | FAIL | store did not persist: status=needs_clarification present=False |
| 1100 | B | my favorite lunch is waffles | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1101 | B | my favorite lunch is shepherd pie | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1102 | B | my favorite lunch is coleslaw | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1103 | B | my favorite lunch is moussaka | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1104 | B | my favorite lunch is pizza | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1105 | B | my favorite lunch is calamari | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1106 | B | my favorite lunch is banh mi | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1107 | B | my favorite lunch is lasagna | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1108 | B | my favorite lunch is biryani | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1109 | B | my favorite lunch is poutine | update (old value replaced by new) | op=update status=ignored fact='My favorite lunch is biryani' | FAIL | update not applied: seed=updated status=ignored v2_present=True |
| 111 | A | my favorite music is k-pop | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1110 | B | my favorite lunch is bruschetta | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1111 | B | my favorite lunch is hot pot | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1112 | B | my favorite lunch is korean bbq | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1113 | B | my favorite lunch is momos | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1114 | B | my favorite lunch is curry | update (old value replaced by new) | seed=needs_clarification op=store status=updated v2_present=True old_present=False | PASS |  |
| 1115 | B | my favorite dinner is mac and cheese | update (old value replaced by new) | seed=stored op=update status=updated v2_present=True old_present=False | PASS |  |
| 1116 | B | my favorite dinner is dumplings | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=False | PASS |  |
| 1117 | B | my favorite dinner is butter chicken | update (old value replaced by new) | seed=needs_clarification op=store status=updated v2_present=True old_present=False | PASS |  |
| 1118 | B | my favorite dinner is ceviche | update (old value replaced by new) | seed=needs_clarification op=store status=updated v2_present=True old_present=False | PASS |  |
| 1119 | B | my favorite dinner is burrito | update (old value replaced by new) | seed=needs_clarification op=store status=updated v2_present=True old_present=False | PASS |  |
| 112 | A | my favorite city is singapore | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1120 | B | my favorite dinner is lasagna | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1121 | B | my favorite dinner is empanadas | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1122 | B | my favorite dinner is calamari | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1123 | B | my favorite dinner is waffles | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1124 | B | my favorite dinner is risotto | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1125 | B | my favorite dinner is vindaloo | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1126 | B | my favorite dinner is shepherd pie | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1127 | B | my favorite dinner is gnocchi | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1128 | B | my favorite dinner is hummus plate | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1129 | B | my favorite dinner is sandwich | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 113 | A | my favorite music is noise | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1130 | B | my favorite dinner is biryani | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1131 | B | my favorite dinner is pho | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1132 | B | my favorite dinner is pierogi | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1133 | B | my favorite dinner is guacamole | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1134 | B | my favorite dinner is korean bbq | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1135 | B | my favorite dinner is moussaka | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1136 | B | my favorite dinner is onion rings | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1137 | B | my favorite dinner is gyoza | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1138 | B | my favorite dinner is pancakes | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1139 | B | my favorite dinner is falafel | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 114 | A | my favorite color is powder | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite color is powder' | FAIL | store did not persist: status=needs_clarification present=False |
| 1140 | B | my favorite dinner is sushi | update (old value replaced by new) | seed=needs_clarification op=store status=updated v2_present=True old_present=False | PASS |  |
| 1141 | B | my favorite dinner is chow mein | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1142 | B | my favorite dinner is tamale | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1143 | B | my favorite dinner is tacos | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1144 | B | my favorite dinner is hot pot | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1145 | B | my favorite dinner is fried rice | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1146 | B | my favorite dinner is polenta | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1147 | B | my favorite dinner is jambalaya | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1148 | B | my favorite dinner is palak paneer | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1149 | B | my favorite dinner is samosa | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 115 | A | my favorite drink is taro milk tea | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is taro milk tea' | FAIL | store did not persist: status=needs_clarification present=False |
| 1150 | B | my favorite dinner is poutine | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1151 | B | my favorite dinner is oysters | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1152 | B | my favorite dinner is nachos | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1153 | B | my favorite dinner is pasta | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1154 | B | my favorite dinner is gumbo | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1155 | B | my favorite dinner is banh mi | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1156 | B | my favorite dinner is idli | update (old value replaced by new) | seed=needs_clarification op=store status=updated v2_present=True old_present=False | PASS |  |
| 1157 | B | my favorite dinner is ratatouille | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1158 | B | my favorite dinner is naan | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1159 | B | my favorite dinner is pizza | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 116 | A | my favorite cuisine is soul food | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1160 | B | my favorite dinner is dosa | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1161 | B | my favorite dinner is thai curry | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1162 | B | my favorite dinner is coleslaw | update (old value replaced by new) | seed=needs_clarification op=store status=updated v2_present=True old_present=False | PASS |  |
| 1163 | B | my favorite dinner is momos | update (old value replaced by new) | seed=needs_clarification op=store status=updated v2_present=True old_present=False | PASS |  |
| 1164 | B | my favorite dinner is paella | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1165 | B | my favorite dinner is curry | update (old value replaced by new) | seed=needs_clarification op=store status=updated v2_present=True old_present=False | PASS |  |
| 1166 | B | my favorite dinner is lobster roll | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1167 | B | my favorite dinner is ramen | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1168 | B | my favorite dinner is bruschetta | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1169 | B | my favorite dinner is burger | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 117 | A | my favorite animal is wolf | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1170 | B | my favorite dinner is paratha | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1171 | B | my favorite dinner is kebabs | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1172 | B | my favorite soup is naan | update (old value replaced by new) | seed=stored op=update status=updated v2_present=True old_present=False | PASS |  |
| 1173 | B | my favorite soup is ramen | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1174 | B | my favorite soup is falafel | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1175 | B | my favorite soup is ceviche | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1176 | B | my favorite soup is samosa | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1177 | B | my favorite soup is curry | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1178 | B | my favorite soup is waffles | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1179 | B | my favorite soup is chow mein | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 118 | A | my favorite animal is ferret | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1180 | B | my favorite soup is empanadas | update (old value replaced by new) | seed=ignored op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1181 | B | my favorite soup is vindaloo | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1182 | B | my favorite soup is pierogi | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1183 | B | my favorite soup is gumbo | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1184 | B | my favorite soup is lobster roll | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1185 | B | my favorite soup is korean bbq | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite soup is idli' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1186 | B | my favorite soup is coleslaw | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1187 | B | my favorite soup is tamale | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1188 | B | my favorite soup is pizza | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1189 | B | my favorite soup is biryani | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 119 | A | i work as a librarian | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 1190 | B | my favorite soup is butter chicken | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1191 | B | my favorite soup is moussaka | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1192 | B | my favorite soup is ratatouille | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1193 | B | my favorite soup is pancakes | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1194 | B | my favorite soup is pasta | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1195 | B | my favorite soup is noodles | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1196 | B | my favorite soup is momos | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1197 | B | my favorite soup is oysters | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1198 | B | my favorite soup is mac and cheese | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite soup is burrito' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1199 | B | my favorite soup is paratha | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite soup is waffles' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 12 | A | my favorite city is lima | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 120 | A | my favorite book is dune | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1200 | B | my favorite soup is gnocchi | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1201 | B | my favorite soup is paella | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1202 | B | my favorite soup is tacos | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1203 | B | my favorite soup is gyoza | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite soup is tacos' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1204 | B | my favorite soup is bhel puri | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1205 | B | my favorite soup is risotto | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1206 | B | my favorite soup is bruschetta | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1207 | B | my favorite soup is burrito | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1208 | B | my favorite soup is palak paneer | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1209 | B | my favorite soup is kebabs | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite soup is sandwich' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 121 | A | my favorite book is the martian | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1210 | B | my favorite soup is hot pot | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1211 | B | my favorite soup is poutine | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1212 | B | my favorite soup is calamari | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1213 | B | my favorite soup is sushi | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1214 | B | my favorite soup is dumplings | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1215 | B | my favorite soup is banh mi | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite soup is burger' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1216 | B | my favorite soup is polenta | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1217 | B | my favorite soup is fried rice | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1218 | B | my favorite soup is burger | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1219 | B | my favorite soup is shepherd pie | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 122 | A | my favorite game is fallout 4 | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1220 | B | my favorite soup is nachos | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite soup is pancakes' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1221 | B | my favorite soup is onion rings | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1222 | B | my favorite soup is pho | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1223 | B | my favorite soup is sandwich | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite soup is kebabs' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=True |
| 1224 | B | my favorite soup is guacamole | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1225 | B | my favorite soup is lasagna | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1226 | B | my favorite soup is idli | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1227 | B | my favorite soup is hummus plate | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1228 | B | my favorite soup is thai curry | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1229 | B | my favorite pasta dish is pancakes | update (old value replaced by new) | seed=needs_clarification op=update status=stored v2_present=True old_present=False | PASS |  |
| 123 | A | my favorite writer is charles dickens | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1230 | B | my favorite pasta dish is shepherd pie | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite pasta dish is dumplings' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=True |
| 1231 | B | my favorite pasta dish is sushi | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1232 | B | my favorite pasta dish is ramen | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite pasta dish is nachos' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1233 | B | my favorite pasta dish is ceviche | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1234 | B | my favorite pasta dish is waffles | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite pasta dish is dosa' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1235 | B | my favorite pasta dish is butter chicken | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite pasta dish is idli' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1236 | B | my favorite pasta dish is poha | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1237 | B | my favorite pasta dish is gumbo | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1238 | B | my favorite pasta dish is oysters | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite pasta dish is tamale' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1239 | B | my favorite pasta dish is kebabs | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite pasta dish is sushi' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 124 | A | my favorite music is pop | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1240 | B | my favorite pasta dish is hot pot | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1241 | B | my favorite pasta dish is curry | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1242 | B | my favorite pasta dish is pho | update (old value replaced by new) | seed=needs_clarification op=store status=updated v2_present=True old_present=False | PASS |  |
| 1243 | B | my favorite pasta dish is chow mein | update (old value replaced by new) | seed=updated op=store status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1244 | B | my favorite pasta dish is burger | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite pasta dish is tacos' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1245 | B | my favorite pasta dish is coleslaw | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite pasta dish is samosa' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1246 | B | my favorite pasta dish is gnocchi | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1247 | B | my favorite pasta dish is naan | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1248 | B | my favorite pasta dish is onion rings | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite pasta dish is momos' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1249 | B | my favorite pasta dish is pizza | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 125 | A | i am from bangkok | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 1250 | B | my favorite pasta dish is calamari | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite pasta dish is naan' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1251 | B | my favorite pasta dish is vindaloo | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1252 | B | my favorite pasta dish is biryani | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1253 | B | my favorite pasta dish is falafel | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite pasta dish is pancakes' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1254 | B | my favorite pasta dish is banh mi | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1255 | B | my favorite pasta dish is sandwich | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1256 | B | my favorite pasta dish is burrito | update (old value replaced by new) | op=update status=ignored fact='My favorite pasta dish is falafel' | FAIL | update not applied: seed=needs_clarification status=ignored v2_present=True |
| 1257 | B | my favorite pasta dish is tacos | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite pasta dish is sandwich' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1258 | B | my favorite pasta dish is mac and cheese | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite pasta dish is burrito' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1259 | B | my favorite pasta dish is risotto | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite pasta dish is curry' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 126 | A | my favorite city is vienna | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1260 | B | my favorite pasta dish is idli | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1261 | B | my favorite pasta dish is dosa | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1262 | B | my favorite pasta dish is hummus plate | update (old value replaced by new) | op=update status=ignored fact='My favorite pasta dish is risotto' | FAIL | update not applied: seed=needs_clarification status=ignored v2_present=True |
| 1263 | B | my favorite pasta dish is lasagna | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1264 | B | my favorite pasta dish is pierogi | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1265 | B | my favorite pasta dish is paratha | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1266 | B | my favorite pasta dish is tamale | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite pasta dish is coleslaw' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1267 | B | my favorite pasta dish is guacamole | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1268 | B | my favorite pasta dish is pasta | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1269 | B | my favorite pasta dish is thai curry | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 127 | A | my favorite food is curry | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1270 | B | my favorite pasta dish is lobster roll | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1271 | B | my favorite pasta dish is polenta | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1272 | B | my favorite pasta dish is bruschetta | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite pasta dish is onion rings' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1273 | B | my favorite pasta dish is poutine | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1274 | B | my favorite pasta dish is empanadas | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite pasta dish is waffles' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1275 | B | my favorite pasta dish is samosa | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1276 | B | my favorite pasta dish is nachos | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1277 | B | my favorite pasta dish is momos | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1278 | B | my favorite pasta dish is paella | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1279 | B | my favorite pasta dish is gyoza | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 128 | A | my favorite subject is mathematics | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1280 | B | my favorite pasta dish is fried rice | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1281 | B | my favorite pasta dish is palak paneer | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite pasta dish is kebabs' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=True |
| 1282 | B | my favorite pasta dish is moussaka | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite pasta dish is noodles' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1283 | B | my favorite pasta dish is ratatouille | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite pasta dish is burger' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1284 | B | my favorite pasta dish is korean bbq | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite pasta dish is oysters' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1285 | B | my favorite pasta dish is noodles | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1286 | B | my favorite bread is kebabs | update (old value replaced by new) | seed=needs_clarification op=update status=stored v2_present=True old_present=True | PASS | old value still present alongside new |
| 1287 | B | my favorite bread is noodles | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is coleslaw' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1288 | B | my favorite bread is pancakes | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is gumbo' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1289 | B | my favorite bread is pierogi | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 129 | A | my favorite game is stray | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1290 | B | my favorite bread is thai curry | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1291 | B | my favorite bread is risotto | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is pancakes' | FAIL | update not applied: seed=ignored status=needs_clarification v2_present=False |
| 1292 | B | my favorite bread is chow mein | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1293 | B | my favorite bread is onion rings | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1294 | B | my favorite bread is curry | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1295 | B | my favorite bread is poutine | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1296 | B | my favorite bread is coleslaw | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is burrito' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1297 | B | my favorite bread is biryani | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is calamari' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1298 | B | my favorite bread is tamale | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1299 | B | my favorite bread is korean bbq | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is nachos' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 13 | A | my favorite color is lavender | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 130 | A | my favorite fruit is raspberry | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1300 | B | my favorite bread is oysters | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1301 | B | my favorite bread is samosa | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1302 | B | my favorite bread is jambalaya | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1303 | B | my favorite bread is paratha | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is dumplings' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=True |
| 1304 | B | my favorite bread is butter chicken | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1305 | B | my favorite bread is gyoza | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1306 | B | my favorite bread is lasagna | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is pasta' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=True |
| 1307 | B | my favorite bread is naan | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is jambalaya' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1308 | B | my favorite bread is vindaloo | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is Korean BBQ' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1309 | B | my favorite bread is falafel | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is gyoza' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 131 | A | my favorite sport is javelin | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1310 | B | my favorite bread is bruschetta | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1311 | B | my favorite bread is tacos | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1312 | B | my favorite bread is shepherd pie | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1313 | B | my favorite bread is waffles | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is oysters' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1314 | B | my favorite bread is pho | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1315 | B | my favorite bread is ceviche | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is sandwich' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1316 | B | my favorite bread is gumbo | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1317 | B | my favorite bread is gnocchi | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite food is tacos' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1318 | B | my favorite bread is banh mi | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1319 | B | my favorite bread is hot pot | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 132 | A | my favorite dessert is profiteroles | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1320 | B | my favorite bread is moussaka | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is pho' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1321 | B | my favorite bread is palak paneer | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is sushi' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1322 | B | my favorite bread is empanadas | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1323 | B | my favorite bread is mac and cheese | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is waffles' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1324 | B | my favorite bread is idli | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is noodles' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=True |
| 1325 | B | my favorite bread is pizza | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is idli' | FAIL | update not applied: seed=ignored status=needs_clarification v2_present=True |
| 1326 | B | my favorite bread is pasta | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is hummus plate' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=True |
| 1327 | B | my favorite bread is sushi | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is hot pot' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1328 | B | my favorite bread is polenta | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is momos' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1329 | B | my favorite bread is ratatouille | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 133 | A | my favorite cuisine is afghan | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1330 | B | my favorite bread is ramen | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is lobster roll' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1331 | B | my favorite bread is burrito | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is burger' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1332 | B | my favorite bread is calamari | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is chow mein' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1333 | B | my favorite bread is bhel puri | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1334 | B | my favorite bread is dumplings | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is poutine' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1335 | B | my favorite bread is fried rice | update (old value replaced by new) | seed=stored op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1336 | B | my favorite bread is hummus plate | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1337 | B | my favorite bread is poha | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is fried rice' | FAIL | update not applied: seed=ignored status=needs_clarification v2_present=True |
| 1338 | B | my favorite bread is nachos | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1339 | B | my favorite bread is sandwich | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is samosa' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 134 | A | my favorite food is banh mi | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1340 | B | my favorite bread is dosa | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is tamale' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1341 | B | my favorite bread is lobster roll | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1342 | B | my favorite bread is paella | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite bread is gnocchi' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1343 | B | my favorite cheese is idli | update (old value replaced by new) | seed=needs_clarification op=update status=stored v2_present=True old_present=False | PASS |  |
| 1344 | B | my favorite cheese is poutine | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1345 | B | my favorite cheese is curry | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is Thai Curry' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1346 | B | my favorite cheese is gyoza | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is burger' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1347 | B | my favorite cheese is gnocchi | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is pasta' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1348 | B | my favorite cheese is chow mein | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is momos' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1349 | B | my favorite cheese is moussaka | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 135 | A | my favorite game is doom | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 1350 | B | my favorite cheese is tamale | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is waffles' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1351 | B | my favorite cheese is momos | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is hot pot' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1352 | B | my favorite cheese is nachos | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=False | PASS |  |
| 1353 | B | my favorite cheese is poha | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is hummus plate' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=True |
| 1354 | B | my favorite cheese is banh mi | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is curry' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1355 | B | my favorite cheese is vindaloo | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is jambalaya' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1356 | B | my favorite cheese is ratatouille | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is pho' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1357 | B | my favorite cheese is burrito | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1358 | B | my favorite cheese is bhel puri | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is tacos' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1359 | B | my favorite cheese is shepherd pie | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is coleslaw' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 136 | A | my favorite music is post rock | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1360 | B | my favorite cheese is risotto | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is vindaloo' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=True |
| 1361 | B | my favorite cheese is kebabs | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1362 | B | my favorite cheese is waffles | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1363 | B | my favorite cheese is ceviche | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1364 | B | my favorite cheese is hot pot | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is chow mein' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1365 | B | my favorite cheese is jambalaya | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is burrito' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1366 | B | my favorite cheese is lobster roll | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is ramen' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1367 | B | my favorite cheese is sandwich | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is sushi' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1368 | B | my favorite cheese is guacamole | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is poha' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1369 | B | my favorite cheese is tacos | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is idli' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 137 | A | i work as a plumber | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 1370 | B | my favorite cheese is samosa | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is fried rice' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=True |
| 1371 | B | my favorite cheese is calamari | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is oysters' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1372 | B | my favorite cheese is onion rings | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is biryani' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1373 | B | my favorite cheese is burger | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is nachos' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1374 | B | my favorite cheese is falafel | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is gyoza' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1375 | B | my favorite cheese is dumplings | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1376 | B | my favorite cheese is thai curry | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is pancakes' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1377 | B | my favorite cheese is dosa | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1378 | B | my favorite cheese is paratha | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is ceviche' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1379 | B | my favorite cheese is oysters | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is gumbo' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 138 | A | my favorite book is the secret garden | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1380 | B | my favorite cheese is paella | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is onion rings' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1381 | B | my favorite cheese is biryani | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is lobster roll' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=True |
| 1382 | B | my favorite cheese is pancakes | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is gnocchi' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1383 | B | my favorite cheese is hummus plate | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is samosa' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1384 | B | my favorite cheese is pierogi | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is tamale' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1385 | B | my favorite cheese is noodles | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is dosa' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=True |
| 1386 | B | my favorite cheese is pasta | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is noodles' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1387 | B | my favorite cheese is pizza | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is banh mi' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=False |
| 1388 | B | my favorite cheese is coleslaw | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1389 | B | my favorite cheese is pho | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is dumplings' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 139 | A | my favorite movie is la la land | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1390 | B | my favorite cheese is ramen | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1391 | B | my favorite cheese is sushi | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is naan' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1392 | B | my favorite cheese is korean bbq | update (old value replaced by new) | seed=needs_clarification op=update status=updated v2_present=True old_present=False | PASS |  |
| 1393 | B | my favorite cheese is bruschetta | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is Korean BBQ' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1394 | B | my favorite cheese is mac and cheese | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is sandwich' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=True |
| 1395 | B | my favorite cheese is butter chicken | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1396 | B | my favorite cheese is fried rice | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is bhel puri' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 1397 | B | my favorite cheese is palak paneer | update (old value replaced by new) | seed=updated op=update status=updated v2_present=True old_present=True | PASS | old value still present alongside new |
| 1398 | B | my favorite cheese is lasagna | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is kebabs' | FAIL | update not applied: seed=updated status=needs_clarification v2_present=True |
| 1399 | B | my favorite cheese is empanadas | update (old value replaced by new) | op=update status=needs_clarification fact='My favorite cheese is falafel' | FAIL | update not applied: seed=needs_clarification status=needs_clarification v2_present=False |
| 14 | A | my favorite drink is grape juice | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 140 | A | i work as a actor | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 1400 | C | my favorite juice is smoothie | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1401 | C | my favorite juice is latte | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1402 | C | my favorite juice is cola | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1403 | C | my favorite juice is milk coffee | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1404 | C | my favorite juice is cafe au lait | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1405 | C | my favorite juice is soda water | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1406 | C | my favorite juice is kombucha | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1407 | C | my favorite juice is buttermilk | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1408 | C | my favorite juice is hot chocolate | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1409 | C | my favorite juice is birch beer | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 141 | A | my birthday is in november | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 1410 | C | my favorite juice is pineapple juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1411 | C | my favorite juice is flat white | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1412 | C | my favorite juice is pomegranate juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1413 | C | my favorite juice is beet juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1414 | C | my favorite juice is bubble tea | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1415 | C | my favorite juice is sparkling lemonade | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1416 | C | my favorite juice is oolong | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1417 | C | my favorite juice is peppermint tea | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1418 | C | my favorite juice is sweet lassi | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1419 | C | my favorite juice is prosecco | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 142 | A | my favorite music is minimalism | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1420 | C | my favorite juice is black tea | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1421 | C | my favorite juice is sparkling water | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1422 | C | my favorite juice is hibiscus tea | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1423 | C | my favorite juice is orange juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1424 | C | my favorite juice is hot toddy | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1425 | C | my favorite juice is cherry soda | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1426 | C | my favorite juice is cider | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1427 | C | my favorite juice is watermelon juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1428 | C | my favorite juice is red wine | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1429 | C | my favorite juice is sugarcane juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 143 | A | my favorite fruit is sugar apple | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1430 | C | my favorite juice is limeade | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1431 | C | my favorite juice is cranberry juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1432 | C | my favorite juice is americano | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1433 | C | my favorite juice is iced chai | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1434 | C | my favorite juice is masala chai | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1435 | C | my favorite juice is guava juice | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1436 | C | my favorite juice is eggnog | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1437 | C | my favorite juice is mocha | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1438 | C | my favorite juice is ginger ale | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1439 | C | my favorite juice is white wine | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 144 | A | my favorite drink is cold brew | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is cold brew' | FAIL | store did not persist: status=needs_clarification present=False |
| 1440 | C | my favorite juice is mango lassi | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1441 | C | my favorite juice is orange soda | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1442 | C | my favorite juice is coconut water | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1443 | C | my favorite juice is cappuccino | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1444 | C | my favorite juice is taro milk tea | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1445 | C | my favorite juice is grape soda | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1446 | C | my favorite juice is mead | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1447 | C | my favorite juice is root beer | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1448 | C | my favorite juice is yerba mate | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1449 | C | my favorite juice is badam milk | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 145 | A | my favorite subject is artificial intelligence | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1450 | C | my favorite juice is carrot juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1451 | C | my favorite juice is matcha | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1452 | C | my favorite juice is lassi | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1453 | C | my favorite juice is cold brew | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1454 | C | my favorite juice is mango juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1455 | C | my favorite juice is jasmine tea | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1456 | C | my favorite juice is rose milk | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1457 | C | my favorite juice is tonic water | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1458 | C | my favorite milkshake is rose wine | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1459 | C | my favorite milkshake is soda water | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 146 | A | my favorite hobby is beekeeping | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1460 | C | my favorite milkshake is guava juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1461 | C | my favorite milkshake is rose lemonade | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1462 | C | my favorite milkshake is tomato juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1463 | C | my favorite milkshake is hot toddy | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1464 | C | my favorite milkshake is limeade | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1465 | C | my favorite milkshake is dirty chai | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1466 | C | my favorite milkshake is birch beer | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1467 | C | my favorite milkshake is sparkling lemonade | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1468 | C | my favorite milkshake is cider | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1469 | C | my favorite milkshake is tonic water | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 147 | A | my favorite writer is mario vargas llosa | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1470 | C | my favorite milkshake is lemonade | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1471 | C | my favorite milkshake is mate | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1472 | C | my favorite milkshake is white wine | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1473 | C | my favorite milkshake is apple cider | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1474 | C | my favorite milkshake is iced matcha | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1475 | C | my favorite milkshake is frappe | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1476 | C | my favorite milkshake is milk coffee | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1477 | C | my favorite milkshake is pomegranate juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1478 | C | my favorite milkshake is root beer | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1479 | C | my favorite milkshake is ale | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 148 | A | my favorite sport is curling | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1480 | C | my favorite milkshake is mango juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1481 | C | my favorite milkshake is pineapple juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1482 | C | my favorite milkshake is mead | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1483 | C | my favorite milkshake is stout | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1484 | C | my favorite milkshake is bubble tea | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1485 | C | my favorite milkshake is buttermilk | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1486 | C | my favorite milkshake is watermelon juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1487 | C | my favorite milkshake is kesar milk | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1488 | C | my favorite milkshake is flat white | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1489 | C | my favorite milkshake is salted lassi | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 149 | A | my favorite drink is latte | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is latte' | FAIL | store did not persist: status=needs_clarification present=False |
| 1490 | C | my favorite milkshake is falooda | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1491 | C | my favorite milkshake is black tea | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1492 | C | my favorite milkshake is carrot juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1493 | C | my favorite milkshake is beet juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1494 | C | my favorite milkshake is cream soda | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1495 | C | my favorite milkshake is grape soda | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1496 | C | my favorite milkshake is taro milk tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1497 | C | my favorite milkshake is matcha | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1498 | C | my favorite milkshake is cappuccino | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1499 | C | my favorite milkshake is yerba mate | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 15 | A | my favorite food is fried rice | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 150 | A | my favorite season is monsoon | store (durable casual fact persists) | op=update status=stored present=True | PASS |  |
| 1500 | C | my favorite milkshake is americano | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1501 | C | my favorite milkshake is mocha | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1502 | C | my favorite milkshake is oolong | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1503 | C | my favorite milkshake is coconut water | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1504 | C | my favorite milkshake is cola | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1505 | C | my favorite milkshake is iced tea | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1506 | C | my favorite milkshake is beer | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1507 | C | my favorite milkshake is sangria | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1508 | C | my favorite milkshake is cold brew | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1509 | C | my favorite milkshake is cafe au lait | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 151 | A | i am from dubai | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 1510 | C | my favorite milkshake is prosecco | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1511 | C | my favorite milkshake is orange soda | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1512 | C | my favorite milkshake is peppermint tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1513 | C | my favorite milkshake is orange juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1514 | C | my favorite milkshake is hibiscus tea | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1515 | C | my favorite smoothie is peppermint tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1516 | C | my favorite smoothie is black tea | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1517 | C | my favorite smoothie is lassi | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1518 | C | my favorite smoothie is mead | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1519 | C | my favorite smoothie is badam milk | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 152 | A | my favorite city is rotterdam | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1520 | C | my favorite smoothie is iced tea | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1521 | C | my favorite smoothie is cranberry juice | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1522 | C | my favorite smoothie is jasmine tea | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1523 | C | my favorite smoothie is sweet lassi | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1524 | C | my favorite smoothie is cider | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1525 | C | my favorite smoothie is iced chai | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1526 | C | my favorite smoothie is grape juice | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1527 | C | my favorite smoothie is cold brew | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1528 | C | my favorite smoothie is sparkling lemonade | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1529 | C | my favorite smoothie is watermelon juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 153 | A | my favorite color is citrine | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1530 | C | my favorite smoothie is ale | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1531 | C | my favorite smoothie is sparkling water | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1532 | C | my favorite smoothie is chai | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1533 | C | my favorite smoothie is latte | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1534 | C | my favorite smoothie is yerba mate | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1535 | C | my favorite smoothie is cream soda | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1536 | C | my favorite smoothie is oolong | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1537 | C | my favorite smoothie is limeade | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1538 | C | my favorite smoothie is pineapple juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1539 | C | my favorite smoothie is grape soda | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 154 | A | i am from oslo | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 1540 | C | my favorite smoothie is coconut water | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1541 | C | my favorite smoothie is flat white | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1542 | C | my favorite smoothie is soda water | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1543 | C | my favorite smoothie is masala chai | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1544 | C | my favorite smoothie is cola | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1545 | C | my favorite smoothie is cafe au lait | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1546 | C | my favorite smoothie is beet juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1547 | C | my favorite smoothie is kombucha | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1548 | C | my favorite smoothie is hot toddy | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1549 | C | my favorite smoothie is apple cider | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 155 | A | i am from budapest | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 1550 | C | my favorite smoothie is stout | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1551 | C | my favorite smoothie is herbal tea | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1552 | C | my favorite smoothie is carrot juice | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1553 | C | my favorite smoothie is coffee | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1554 | C | my favorite smoothie is cappuccino | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1555 | C | my favorite smoothie is rose wine | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1556 | C | my favorite smoothie is hibiscus tea | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1557 | C | my favorite smoothie is hot chocolate | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1558 | C | my favorite smoothie is salted lassi | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1559 | C | my favorite smoothie is iced matcha | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 156 | A | my favorite cuisine is chinese | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1560 | C | my favorite smoothie is americano | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1561 | C | my favorite smoothie is dirty chai | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1562 | C | my favorite smoothie is tomato juice | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1563 | C | my favorite smoothie is apple juice | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1564 | C | my favorite smoothie is orange juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1565 | C | my favorite smoothie is green tea | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1566 | C | my favorite smoothie is orange soda | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1567 | C | my favorite smoothie is taro milk tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1568 | C | my favorite smoothie is guava juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1569 | C | my favorite smoothie is eggnog | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 157 | A | my favorite writer is jk rowling | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1570 | C | my favorite smoothie is mocha | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1571 | C | my favorite smoothie is affogato | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1572 | C | my favorite tea is lemonade | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1573 | C | my favorite tea is red wine | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1574 | C | my favorite tea is sparkling water | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1575 | C | my favorite tea is lassi | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1576 | C | my favorite tea is cold brew | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1577 | C | my favorite tea is sangria | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1578 | C | my favorite tea is pineapple juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1579 | C | my favorite tea is herbal tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 158 | A | my favorite sport is handball | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1580 | C | my favorite tea is mocha | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1581 | C | my favorite tea is cappuccino | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1582 | C | my favorite tea is oolong | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1583 | C | my favorite tea is dirty chai | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1584 | C | my favorite tea is orange juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1585 | C | my favorite tea is badam milk | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1586 | C | my favorite tea is kombucha | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1587 | C | my favorite tea is taro milk tea | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1588 | C | my favorite tea is hot chocolate | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1589 | C | my favorite tea is birch beer | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 159 | A | my favorite hobby is card games | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1590 | C | my favorite tea is carrot juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1591 | C | my favorite tea is green tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1592 | C | my favorite tea is americano | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1593 | C | my favorite tea is prosecco | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1594 | C | my favorite tea is beet juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1595 | C | my favorite tea is bubble tea | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1596 | C | my favorite tea is sparkling lemonade | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1597 | C | my favorite tea is cream soda | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1598 | C | my favorite tea is black tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1599 | C | my favorite tea is mead | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 16 | A | my favorite color is crimson | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 160 | A | my favorite animal is octopus | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1600 | C | my favorite tea is cherry soda | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1601 | C | my favorite tea is hibiscus tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1602 | C | my favorite tea is guava juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1603 | C | my favorite tea is iced chai | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1604 | C | my favorite tea is ale | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1605 | C | my favorite tea is grape juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1606 | C | my favorite tea is frappe | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1607 | C | my favorite tea is watermelon juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1608 | C | my favorite tea is fresh lime soda | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1609 | C | my favorite tea is soda water | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 161 | A | my favorite game is splatoon | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1610 | C | my favorite tea is peppermint tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1611 | C | my favorite tea is jasmine tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1612 | C | my favorite tea is cider | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1613 | C | my favorite tea is sweet lassi | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1614 | C | my favorite tea is tomato juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1615 | C | my favorite tea is rose lemonade | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1616 | C | my favorite tea is smoothie | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1617 | C | my favorite tea is kesar milk | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1618 | C | my favorite tea is chai | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1619 | C | my favorite tea is stout | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 162 | A | my pet's name is pickles | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1620 | C | my favorite tea is beer | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1621 | C | my favorite tea is iced tea | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1622 | C | my favorite tea is grape soda | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1623 | C | my favorite tea is tonic water | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1624 | C | my favorite tea is sugarcane juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1625 | C | my favorite tea is orange soda | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1626 | C | my favorite tea is mango juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1627 | C | my favorite tea is flat white | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1628 | C | my favorite tea is falooda | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1629 | C | my favorite soda is peppermint tea | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 163 | A | my favorite color is bronze | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1630 | C | my favorite soda is flat white | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1631 | C | my favorite soda is root beer | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1632 | C | my favorite soda is herbal tea | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1633 | C | my favorite soda is beer | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1634 | C | my favorite soda is pineapple juice | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1635 | C | my favorite soda is kesar milk | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1636 | C | my favorite soda is cherry soda | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1637 | C | my favorite soda is coffee | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1638 | C | my favorite soda is cider | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1639 | C | my favorite soda is coconut water | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 164 | A | my favorite dessert is mochi | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1640 | C | my favorite soda is iced tea | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1641 | C | my favorite soda is latte | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1642 | C | my favorite soda is ginger ale | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1643 | C | my favorite soda is pomegranate juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1644 | C | my favorite soda is green tea | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1645 | C | my favorite soda is salted lassi | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1646 | C | my favorite soda is cold brew | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1647 | C | my favorite soda is matcha | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1648 | C | my favorite soda is rose lemonade | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1649 | C | my favorite soda is red wine | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 165 | A | i work as a physicist | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 1650 | C | my favorite soda is americano | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1651 | C | my favorite soda is tomato juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1652 | C | my favorite soda is grape juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1653 | C | my favorite soda is sparkling lemonade | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1654 | C | my favorite soda is mead | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1655 | C | my favorite soda is frappe | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1656 | C | my favorite soda is sangria | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1657 | C | my favorite soda is chamomile | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1658 | C | my favorite soda is falooda | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1659 | C | my favorite soda is sweet lassi | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 166 | A | my favorite sport is tennis | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1660 | C | my favorite soda is tonic water | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1661 | C | my favorite soda is rose wine | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1662 | C | my favorite soda is soda water | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1663 | C | my favorite soda is iced chai | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1664 | C | my favorite soda is masala chai | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1665 | C | my favorite soda is kombucha | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1666 | C | my favorite soda is taro milk tea | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1667 | C | my favorite soda is smoothie | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1668 | C | my favorite soda is orange juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1669 | C | my favorite soda is ale | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 167 | A | my favorite music is hindustani | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1670 | C | my favorite soda is birch beer | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1671 | C | my favorite soda is apple juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1672 | C | my favorite soda is hibiscus tea | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1673 | C | my favorite soda is grape soda | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1674 | C | my favorite soda is yerba mate | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1675 | C | my favorite soda is cafe au lait | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1676 | C | my favorite soda is rose milk | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1677 | C | my favorite soda is mango juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1678 | C | my favorite soda is eggnog | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1679 | C | my favorite soda is lemonade | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 168 | A | my favorite color is maroon | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 1680 | C | my favorite soda is bubble tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1681 | C | my favorite soda is oolong | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1682 | C | my favorite soda is white wine | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1683 | C | my favorite soda is cranberry juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1684 | C | my favorite soda is mango lassi | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1685 | C | my favorite soda is sparkling water | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1686 | C | my favorite shake is americano | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1687 | C | my favorite shake is guava juice | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1688 | C | my favorite shake is buttermilk | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1689 | C | my favorite shake is rose lemonade | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 169 | A | my favorite music is blues | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1690 | C | my favorite shake is milk coffee | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1691 | C | my favorite shake is latte | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1692 | C | my favorite shake is apple juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1693 | C | my favorite shake is espresso | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1694 | C | my favorite shake is grape juice | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1695 | C | my favorite shake is sugarcane juice | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1696 | C | my favorite shake is chai | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1697 | C | my favorite shake is mocha | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1698 | C | my favorite shake is root beer | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1699 | C | my favorite shake is pomegranate juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 17 | A | my favorite cuisine is bbq | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 170 | A | my favorite book is native son | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1700 | C | my favorite shake is pineapple juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1701 | C | my favorite shake is mango lassi | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1702 | C | my favorite shake is chamomile | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1703 | C | my favorite shake is lassi | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1704 | C | my favorite shake is beer | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1705 | C | my favorite shake is soda water | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1706 | C | my favorite shake is tonic water | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1707 | C | my favorite shake is ale | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1708 | C | my favorite shake is ginger ale | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1709 | C | my favorite shake is kesar milk | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 171 | A | my favorite music is hip hop | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 1710 | C | my favorite shake is badam milk | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1711 | C | my favorite shake is red wine | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1712 | C | my favorite shake is lemonade | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1713 | C | my favorite shake is sangria | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1714 | C | my favorite shake is mead | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1715 | C | my favorite shake is smoothie | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1716 | C | my favorite shake is beet juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1717 | C | my favorite shake is cafe au lait | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1718 | C | my favorite shake is yerba mate | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1719 | C | my favorite shake is coconut water | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 172 | A | my favorite subject is geometry | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1720 | C | my favorite shake is iced chai | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1721 | C | my favorite shake is limeade | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1722 | C | my favorite shake is dirty chai | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1723 | C | my favorite shake is jasmine tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1724 | C | my favorite shake is flat white | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1725 | C | my favorite shake is black tea | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1726 | C | my favorite shake is rose milk | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1727 | C | my favorite shake is coffee | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1728 | C | my favorite shake is frappe | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1729 | C | my favorite shake is cranberry juice | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 173 | A | my favorite season is summer | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 1730 | C | my favorite shake is salted lassi | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1731 | C | my favorite shake is kombucha | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1732 | C | my favorite shake is stout | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1733 | C | my favorite shake is orange soda | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1734 | C | my favorite shake is green tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1735 | C | my favorite shake is fresh lime soda | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1736 | C | my favorite shake is falooda | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1737 | C | my favorite shake is masala chai | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1738 | C | my favorite shake is white wine | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1739 | C | my favorite shake is birch beer | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 174 | A | my pet's name is molly | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1740 | C | my favorite shake is cappuccino | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1741 | C | my favorite shake is mate | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1742 | C | my favorite shake is iced matcha | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1743 | C | my favorite mocktail is chamomile | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1744 | C | my favorite mocktail is salted lassi | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1745 | C | my favorite mocktail is birch beer | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1746 | C | my favorite mocktail is latte | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1747 | C | my favorite mocktail is orange soda | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1748 | C | my favorite mocktail is matcha | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1749 | C | my favorite mocktail is cafe au lait | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 175 | A | my favorite movie is the imitation game | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1750 | C | my favorite mocktail is white wine | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1751 | C | my favorite mocktail is carrot juice | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1752 | C | my favorite mocktail is cranberry juice | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1753 | C | my favorite mocktail is badam milk | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1754 | C | my favorite mocktail is cola | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1755 | C | my favorite mocktail is taro milk tea | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1756 | C | my favorite mocktail is milkshake | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1757 | C | my favorite mocktail is espresso | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1758 | C | my favorite mocktail is frappe | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1759 | C | my favorite mocktail is limeade | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 176 | A | my favorite subject is psychiatry | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1760 | C | my favorite mocktail is cappuccino | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1761 | C | my favorite mocktail is coconut water | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1762 | C | my favorite mocktail is peppermint tea | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1763 | C | my favorite mocktail is sugarcane juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1764 | C | my favorite mocktail is herbal tea | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1765 | C | my favorite mocktail is stout | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1766 | C | my favorite mocktail is rose wine | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1767 | C | my favorite mocktail is rose lemonade | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1768 | C | my favorite mocktail is grape soda | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1769 | C | my favorite mocktail is iced tea | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 177 | A | my favorite writer is ray bradbury | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1770 | C | my favorite mocktail is hibiscus tea | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1771 | C | my favorite mocktail is dirty chai | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1772 | C | my favorite mocktail is cold brew | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1773 | C | my favorite mocktail is mead | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1774 | C | my favorite mocktail is guava juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1775 | C | my favorite mocktail is tonic water | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1776 | C | my favorite mocktail is cream soda | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1777 | C | my favorite mocktail is orange juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1778 | C | my favorite mocktail is americano | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1779 | C | my favorite mocktail is smoothie | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 178 | A | my favorite book is a thousand splendid suns | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1780 | C | my favorite mocktail is mango juice | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1781 | C | my favorite mocktail is beer | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1782 | C | my favorite mocktail is sparkling water | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1783 | C | my favorite mocktail is cherry soda | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1784 | C | my favorite mocktail is soda water | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1785 | C | my favorite mocktail is lassi | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1786 | C | my favorite mocktail is jasmine tea | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1787 | C | my favorite mocktail is red wine | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 1788 | C | my favorite mocktail is rose milk | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1789 | C | my favorite mocktail is iced chai | forget (op=forget and fact removed) | op=forget status=deleted | PASS |  |
| 179 | A | my favorite music is reggae | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1790 | C | my favorite mocktail is watermelon juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1791 | C | my favorite mocktail is beet juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1792 | C | my favorite mocktail is buttermilk | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1793 | C | my favorite mocktail is grape juice | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1794 | C | my favorite mocktail is lemonade | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1795 | C | my favorite mocktail is tomato juice | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1796 | C | my favorite mocktail is apple juice | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1797 | C | my favorite mocktail is pineapple juice | forget (op=forget and fact removed) | op=forget status=not_found | PASS | decisioning correct; target not found |
| 1798 | C | my favorite mocktail is prosecco | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 1799 | C | my favorite mocktail is falooda | forget (op=forget and fact removed) | op=forget status=needs_clarification | FAIL | forget gate failed: status=needs_clarification |
| 18 | A | my favorite fruit is apple | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 180 | A | my favorite music is world music | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1800 | D | how far is rome from sao paulo | no write | op=None | PASS |  |
| 1801 | D | how far is brussels from manila | no write | op=None | PASS |  |
| 1802 | D | how far is delhi from caracas | no write | op=None | PASS |  |
| 1803 | D | which is better, noodles or palak paneer | no write | op=query | PASS |  |
| 1804 | D | which is better, dosa or sandwich | no write | op=query | PASS |  |
| 1805 | D | which is better, hummus plate or poha | no write | op=query | PASS |  |
| 1806 | D | how far is madrid from capetown | no write | op=None | PASS |  |
| 1807 | D | how far is brussels from edinburgh | no write | op=None | PASS |  |
| 1808 | D | which is better, dumplings or tamale | no write | op=query | PASS |  |
| 1809 | D | you remember my favorite sport is athletics | no write | op=query | PASS |  |
| 181 | A | i work as a marketer | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 1810 | D | which is better, polenta or fried rice | no write | op=query | PASS |  |
| 1811 | D | which is better, vindaloo or waffles | no write | op=query | PASS |  |
| 1812 | D | how far is paris from quito | no write | op=None | PASS |  |
| 1813 | D | which is better, falafel or ramen | no write | op=query | PASS |  |
| 1814 | D | how far is tokyo from brussels | no write | op=None | PASS |  |
| 1815 | D | you remember my favorite sport is track cycling | no write | op=query | PASS |  |
| 1816 | D | which is better, sushi or guacamole | no write | op=query | PASS |  |
| 1817 | D | how long does it take to brew beer | no write | op=None | PASS |  |
| 1818 | D | which is better, pancakes or gnocchi | no write | op=query | PASS |  |
| 1819 | D | which is better, paella or waffles | no write | op=query | PASS |  |
| 182 | A | my favorite subject is virology | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1820 | D | how far is nairobi from cairo | no write | op=None | PASS |  |
| 1821 | D | which is better, hummus plate or momos | no write | op=query | PASS |  |
| 1822 | D | which is better, paella or burger | no write | op=query | PASS |  |
| 1823 | D | you remember my favorite sport is badminton | no write | op=query | PASS |  |
| 1824 | D | how far is madrid from hanoi | no write | op=None | PASS |  |
| 1825 | D | can you explain diffraction to me | no write | op=query | PASS |  |
| 1826 | D | where can i buy record | no write | op=query | PASS |  |
| 1827 | D | how far is prague from brussels | no write | op=None | PASS |  |
| 1828 | D | how far is edinburgh from kathmandu | no write | op=None | PASS |  |
| 1829 | D | you remember my favorite color is forest | no write | op=query | PASS |  |
| 183 | A | my favorite city is toronto | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1830 | D | you remember my favorite color is emerald | no write | op=query | PASS |  |
| 1831 | D | how far is hanoi from oslo | no write | op=None | PASS |  |
| 1832 | D | which is better, korean bbq or paratha | no write | op=query | PASS |  |
| 1833 | D | how far is amsterdam from chennai | no write | op=None | PASS |  |
| 1834 | D | how far is boston from vienna | no write | op=None | PASS |  |
| 1835 | D | which is better, sandwich or pho | no write | op=query | PASS |  |
| 1836 | D | you remember my favorite color is ochre | no write | op=query | PASS |  |
| 1837 | D | how far is barcelona from bangkok | no write | op=None | PASS |  |
| 1838 | D | which is better, ramen or fried rice | no write | op=query | PASS |  |
| 1839 | D | how far is lisbon from bogota | no write | op=None | PASS |  |
| 184 | A | my favorite drink is cola | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is cola' | FAIL | store did not persist: status=needs_clarification present=False |
| 1840 | D | you remember my favorite movie is pulp fiction | no write | op=query | PASS |  |
| 1841 | D | which is better, pasta or pho | no write | op=query | PASS |  |
| 1842 | D | can you explain tsunamis to me | no write | op=query | PASS |  |
| 1843 | D | is tamale healthy | no write | op=None | PASS |  |
| 1844 | D | which is better, lobster roll or thai curry | no write | op=query | PASS |  |
| 1845 | D | which is better, hummus plate or samosa | no write | op=query | PASS |  |
| 1846 | D | which is better, gumbo or curry | no write | op=query | PASS |  |
| 1847 | D | what is refraction | no write | op=None | PASS |  |
| 1848 | D | what is the capital of bangladesh | no write | op=None | PASS |  |
| 1849 | D | how far is lagos from lisbon | no write | op=None | PASS |  |
| 185 | A | my favorite food is gnocchi | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1850 | D | which is better, waffles or thai curry | no write | op=query | PASS |  |
| 1851 | D | how far is helsinki from delhi | no write | op=None | PASS |  |
| 1852 | D | how far is lima from quito | no write | op=None | PASS |  |
| 1853 | D | which is better, gyoza or butter chicken | no write | op=query | PASS |  |
| 1854 | D | how far is barcelona from belfast | no write | op=None | PASS |  |
| 1855 | D | which is better, ramen or butter chicken | no write | op=query | PASS |  |
| 1856 | D | is burger healthy | no write | op=None | PASS |  |
| 1857 | D | how far is warsaw from helsinki | no write | op=None | PASS |  |
| 1858 | D | which is better, oysters or gyoza | no write | op=query | PASS |  |
| 1859 | D | how far is chennai from madrid | no write | op=None | PASS |  |
| 186 | A | my pet's name is buddy | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1860 | D | which is better, mac and cheese or paratha | no write | op=query | PASS |  |
| 1861 | D | how far is berlin from cardiff | no write | op=None | PASS |  |
| 1862 | D | what is the weather like in toronto | no write | op=None | PASS |  |
| 1863 | D | how far is kathmandu from santiago | no write | op=None | PASS |  |
| 1864 | D | how far is rome from manila | no write | op=None | PASS |  |
| 1865 | D | you remember my favorite city is rio de janeiro | no write | op=query | PASS |  |
| 1866 | D | which is better, butter chicken or mac and cheese | no write | op=query | PASS |  |
| 1867 | D | which is better, moussaka or ratatouille | no write | op=query | PASS |  |
| 1868 | D | which is better, shepherd pie or burger | no write | op=query | PASS |  |
| 1869 | D | how far is dubai from sao paulo | no write | op=None | PASS |  |
| 187 | A | my favorite subject is philosophy | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1870 | D | which is better, dumplings or risotto | no write | op=query | PASS |  |
| 1871 | D | which is better, waffles or coleslaw | no write | op=query | PASS |  |
| 1872 | D | how far is manchester from lagos | no write | op=None | PASS |  |
| 1873 | D | you remember my favorite food is polenta | no write | op=query | PASS |  |
| 1874 | D | how far is mumbai from capetown | no write | op=None | PASS |  |
| 1875 | D | how far is chennai from dubai | no write | op=None | PASS |  |
| 1876 | D | you remember my favorite writer is james baldwin | no write | op=query | PASS |  |
| 1877 | D | which is better, lobster roll or sushi | no write | op=query | PASS |  |
| 1878 | D | you remember my favorite animal is shark | no write | op=query | PASS |  |
| 1879 | D | how far is montevideo from lima | no write | op=None | PASS |  |
| 188 | A | my favorite book is the nightingale | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1880 | D | which is better, pho or poha | no write | op=query | PASS |  |
| 1881 | D | which is better, oysters or poha | no write | op=query | PASS |  |
| 1882 | D | which is better, risotto or falafel | no write | op=query | PASS |  |
| 1883 | D | which is better, bhel puri or burger | no write | op=query | PASS |  |
| 1884 | D | which is better, hummus plate or shepherd pie | no write | op=query | PASS |  |
| 1885 | D | how far is chennai from melbourne | no write | op=None | PASS |  |
| 1886 | D | which is better, bhel puri or poha | no write | op=query | PASS |  |
| 1887 | D | which is better, guacamole or onion rings | no write | op=query | PASS |  |
| 1888 | D | how far is venice from mexico city | no write | op=None | PASS |  |
| 1889 | D | how far is bogota from cairo | no write | op=None | PASS |  |
| 189 | A | my favorite hobby is caving | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1890 | D | you remember my favorite book is the handmaid tale | no write | op=query | PASS |  |
| 1891 | D | which is better, chow mein or biryani | no write | op=query | PASS |  |
| 1892 | D | which is better, gyoza or sandwich | no write | op=query | PASS |  |
| 1893 | D | what do you think about pet adoption | no write | op=None | PASS |  |
| 1894 | D | how far is caracas from prague | no write | op=None | PASS |  |
| 1895 | D | how far is rome from jakarta | no write | op=None | PASS |  |
| 1896 | D | how far is copenhagen from chennai | no write | op=query | PASS |  |
| 1897 | D | how far is berlin from dubai | no write | op=None | PASS |  |
| 1898 | D | which is better, noodles or samosa | no write | op=query | PASS |  |
| 1899 | D | which is better, guacamole or tacos | no write | op=query | PASS |  |
| 19 | A | my favorite animal is beaver | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 190 | A | my favorite book is invisible man | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1900 | D | which is better, sushi or tacos | no write | op=query | PASS |  |
| 1901 | D | you remember my favorite animal is owl | no write | op=query | PASS |  |
| 1902 | D | how far is vienna from bogota | no write | op=None | PASS |  |
| 1903 | D | which is better, samosa or vindaloo | no write | op=query | PASS |  |
| 1904 | D | what is the weather like in chennai | no write | op=None | PASS |  |
| 1905 | D | who wrote a song of ice and fire | no write | op=None | PASS |  |
| 1906 | D | which is better, banh mi or waffles | no write | op=query | PASS |  |
| 1907 | D | which is better, vindaloo or bruschetta | no write | op=query | PASS |  |
| 1908 | D | you remember my favorite writer is ray bradbury | no write | op=query | PASS |  |
| 1909 | D | which is better, guacamole or gumbo | no write | op=query | PASS |  |
| 191 | A | my favorite game is slay the spire | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1910 | D | you remember my favorite cuisine is mexican | no write | op=query | PASS |  |
| 1911 | D | how far is dubai from oslo | no write | op=None | PASS |  |
| 1912 | D | how far is quito from paris | no write | op=None | PASS |  |
| 1913 | D | which is better, paratha or butter chicken | no write | op=query | PASS |  |
| 1914 | D | how far is santiago from lima | no write | op=None | PASS |  |
| 1915 | D | which is better, coleslaw or bhel puri | no write | op=query | PASS |  |
| 1916 | D | how far is tokyo from buenos aires | no write | op=None | PASS |  |
| 1917 | D | which is better, gumbo or dumplings | no write | op=query | PASS |  |
| 1918 | D | you remember my favorite food is paratha | no write | op=query | PASS |  |
| 1919 | D | how far is cairo from capetown | no write | op=None | PASS |  |
| 192 | A | my favorite sport is athletics | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1920 | D | which is better, pierogi or nachos | no write | op=query | PASS |  |
| 1921 | D | how far is madrid from boston | no write | op=None | PASS |  |
| 1922 | D | which is better, empanadas or pho | no write | op=query | PASS |  |
| 1923 | D | how far is cardiff from mumbai | no write | op=None | PASS |  |
| 1924 | D | which is better, hummus plate or paella | no write | op=query | PASS |  |
| 1925 | D | how far is stockholm from amsterdam | no write | op=None | PASS |  |
| 1926 | D | how far is cairo from seoul | no write | op=None | PASS |  |
| 1927 | D | what does eudaemonia mean | no write | op=None | PASS |  |
| 1928 | D | how far is nairobi from seville | no write | op=None | PASS |  |
| 1929 | D | which is better, ratatouille or samosa | no write | op=query | PASS |  |
| 193 | A | my favorite movie is the social network | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1930 | D | which is better, pancakes or idli | no write | op=query | PASS |  |
| 1931 | D | which is better, risotto or guacamole | no write | op=query | PASS |  |
| 1932 | D | how far is oslo from athens | no write | op=None | PASS |  |
| 1933 | D | how far is helsinki from nairobi | no write | op=None | PASS |  |
| 1934 | D | how far is rio de janeiro from helsinki | no write | op=None | PASS |  |
| 1935 | D | which is better, kebabs or idli | no write | op=query | PASS |  |
| 1936 | D | which is better, guacamole or paratha | no write | op=query | PASS |  |
| 1937 | D | you remember my favorite book is the alchemist | no write | op=query | PASS |  |
| 1938 | D | which is better, pancakes or palak paneer | no write | op=query | PASS |  |
| 1939 | D | which is better, waffles or tamale | no write | op=query | PASS |  |
| 194 | A | my favorite drink is ale | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is ale' | FAIL | store did not persist: status=needs_clarification present=False |
| 1940 | D | how far is zurich from bangkok | no write | op=None | PASS |  |
| 1941 | D | you remember my favorite dessert is jalebi | no write | op=query | PASS |  |
| 1942 | D | how far is manila from caracas | no write | op=None | PASS |  |
| 1943 | D | which is better, poutine or burger | no write | op=query | PASS |  |
| 1944 | D | which is better, paratha or curry | no write | op=query | PASS |  |
| 1945 | D | how far is venice from nairobi | no write | op=None | PASS |  |
| 1946 | D | what time is it in cardiff | no write | op=None | PASS |  |
| 1947 | D | how long does it take to make pretzels | no write | op=None | PASS |  |
| 1948 | D | which is better, kebabs or risotto | no write | op=query | PASS |  |
| 1949 | D | how far is milan from budapest | no write | op=None | PASS |  |
| 195 | A | my favorite color is honey | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1950 | D | which is better, sushi or noodles | no write | op=query | PASS |  |
| 1951 | D | which is better, tamale or banh mi | no write | op=query | PASS |  |
| 1952 | D | which is better, gnocchi or burger | no write | op=query | PASS |  |
| 1953 | D | how far is milan from manila | no write | op=None | PASS |  |
| 1954 | D | which is better, tacos or polenta | no write | op=query | PASS |  |
| 1955 | D | which is better, lasagna or banh mi | no write | op=query | PASS |  |
| 1956 | D | which is better, ratatouille or pizza | no write | op=query | PASS |  |
| 1957 | D | you remember my favorite fruit is tamarind | no write | op=query | PASS |  |
| 1958 | D | which is better, gyoza or hot pot | no write | op=query | PASS |  |
| 1959 | D | which is better, naan or biryani | no write | op=query | PASS |  |
| 196 | A | my favorite show is lost | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1960 | D | which is better, onion rings or gnocchi | no write | op=query | PASS |  |
| 1961 | D | which is better, poha or empanadas | no write | op=query | PASS |  |
| 1962 | D | how far is tokyo from edinburgh | no write | op=None | PASS |  |
| 1963 | D | how far is casablanca from dubai | no write | op=None | PASS |  |
| 1964 | D | which is better, coleslaw or idli | no write | op=query | PASS |  |
| 1965 | D | how far is milan from copenhagen | no write | op=query | PASS |  |
| 1966 | D | which is better, risotto or dumplings | no write | op=query | PASS |  |
| 1967 | D | which is better, fried rice or poutine | no write | op=query | PASS |  |
| 1968 | D | how far is melbourne from chennai | no write | op=None | PASS |  |
| 1969 | D | you remember my favorite writer is amitav ghosh | no write | op=query | PASS |  |
| 197 | A | my favorite book is moby dick | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1970 | D | which is better, sushi or lobster roll | no write | op=query | PASS |  |
| 1971 | D | how far is kyoto from rotterdam | no write | op=None | PASS |  |
| 1972 | D | which is better, butter chicken or idli | no write | op=query | PASS |  |
| 1973 | D | which is better, paratha or calamari | no write | op=query | PASS |  |
| 1974 | D | which is better, paratha or risotto | no write | op=query | PASS |  |
| 1975 | D | how far is copenhagen from dublin | no write | op=query | PASS |  |
| 1976 | D | how far is zurich from tokyo | no write | op=None | PASS |  |
| 1977 | D | which is better, pizza or jambalaya | no write | op=query | PASS |  |
| 1978 | D | which is better, dumplings or pasta | no write | op=query | PASS |  |
| 1979 | D | how far is copenhagen from quito | no write | op=query | PASS |  |
| 198 | A | my favorite animal is echidna | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 1980 | D | you remember my favorite fruit is lime | no write | op=query | PASS |  |
| 1981 | D | how far is seville from athens | no write | op=None | PASS |  |
| 1982 | D | which is better, risotto or moussaka | no write | op=query | PASS |  |
| 1983 | D | how far is montevideo from zurich | no write | op=None | PASS |  |
| 1984 | D | do you know my favorite show | no write | op=query | PASS |  |
| 1985 | D | which is better, coleslaw or calamari | no write | op=query | PASS |  |
| 1986 | D | which is better, samosa or sushi | no write | op=query | PASS |  |
| 1987 | D | how far is prague from prague | no write | op=None | PASS |  |
| 1988 | D | which is better, momos or banh mi | no write | op=query | PASS |  |
| 1989 | D | which is better, butter chicken or biryani | no write | op=query | PASS |  |
| 199 | A | my favorite color is cobalt | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 1990 | D | you remember my favorite movie is avatar | no write | op=query | PASS |  |
| 1991 | D | you remember my favorite game is valheim | no write | op=query | PASS |  |
| 1992 | D | how far is zurich from singapore | no write | op=None | PASS |  |
| 1993 | D | how far is mexico city from kathmandu | no write | op=None | PASS |  |
| 1994 | D | how far is kyoto from singapore | no write | op=None | PASS |  |
| 1995 | D | how far is madrid from rome | no write | op=None | PASS |  |
| 1996 | D | which is better, ramen or samosa | no write | op=query | PASS |  |
| 1997 | D | you remember my favorite movie is the matrix | no write | op=query | PASS |  |
| 1998 | D | how far is oslo from bangkok | no write | op=None | PASS |  |
| 1999 | D | what is inflation | no write | op=None | PASS |  |
| 2 | A | my favorite dessert is beignets | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 20 | A | my favorite animal is owl | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 200 | A | my favorite drink is orange juice | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2000 | D | can you explain climate change to me | no write | op=query | PASS |  |
| 2001 | D | how far is venice from florence | no write | op=None | PASS |  |
| 2002 | D | how far is cairo from budapest | no write | op=None | PASS |  |
| 2003 | D | how far is chennai from venice | no write | op=None | PASS |  |
| 2004 | D | which is better, dumplings or idli | no write | op=query | PASS |  |
| 2005 | D | you remember my favorite book is the hunger games | no write | op=query | PASS |  |
| 2006 | D | where can i buy a usb drive | no write | op=query | PASS |  |
| 2007 | D | how long does it take to renew a passport | no write | op=query | PASS |  |
| 2008 | D | how far is seville from boston | no write | op=None | PASS |  |
| 2009 | D | how far is oslo from vienna | no write | op=None | PASS |  |
| 201 | A | i work as a recruiter | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 2010 | D | how far is cairo from nairobi | no write | op=None | PASS |  |
| 2011 | D | how far is mumbai from toronto | no write | op=None | PASS |  |
| 2012 | D | how far is stockholm from casablanca | no write | op=None | PASS |  |
| 2013 | D | how far is berlin from paris | no write | op=None | PASS |  |
| 2014 | D | which is better, chow mein or pierogi | no write | op=query | PASS |  |
| 2015 | D | you remember my favorite hobby is metalworking | no write | op=query | PASS |  |
| 2016 | D | which is better, momos or onion rings | no write | op=query | PASS |  |
| 2017 | D | you remember my favorite hobby is ballroom dancing | no write | op=query | PASS |  |
| 2018 | D | how far is dublin from capetown | no write | op=None | PASS |  |
| 2019 | D | which is better, risotto or kebabs | no write | op=query | PASS |  |
| 202 | A | my favorite drink is apple cider | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is apple cider' | FAIL | store did not persist: status=needs_clarification present=False |
| 2020 | D | what is cloud computing | no write | op=None | PASS |  |
| 2021 | D | which is better, dosa or butter chicken | no write | op=query | PASS |  |
| 2022 | D | how far is santiago from delhi | no write | op=None | PASS |  |
| 2023 | D | how far is toronto from mumbai | no write | op=None | PASS |  |
| 2024 | D | which is better, korean bbq or pancakes | no write | op=query | PASS |  |
| 2025 | D | which is better, polenta or burrito | no write | op=query | PASS |  |
| 2026 | D | how far is seville from zurich | no write | op=None | PASS |  |
| 2027 | D | which is better, paratha or dosa | no write | op=query | PASS |  |
| 2028 | D | which is better, ratatouille or falafel | no write | op=query | PASS |  |
| 2029 | D | which is better, falafel or paella | no write | op=query | PASS |  |
| 203 | A | my favorite show is mad men | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2030 | D | which is better, momos or shepherd pie | no write | op=query | PASS |  |
| 2031 | D | how far is montevideo from dubai | no write | op=None | PASS |  |
| 2032 | D | how far is brussels from mumbai | no write | op=None | PASS |  |
| 2033 | D | what is the weather like in santiago | no write | op=None | PASS |  |
| 2034 | D | how far is melbourne from buenos aires | no write | op=None | PASS |  |
| 2035 | D | which is better, biryani or waffles | no write | op=query | PASS |  |
| 2036 | D | which is better, idli or sushi | no write | op=query | PASS |  |
| 2037 | D | is paella healthy | no write | op=None | PASS |  |
| 2038 | D | which is better, gyoza or polenta | no write | op=query | PASS |  |
| 2039 | D | how far is delhi from singapore | no write | op=None | PASS |  |
| 204 | A | my favorite show is money heist | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2040 | D | which is better, ceviche or samosa | no write | op=query | PASS |  |
| 2041 | D | how far is berlin from montevideo | no write | op=None | PASS |  |
| 2042 | D | which is better, mac and cheese or fried rice | no write | op=query | PASS |  |
| 2043 | D | which is better, guacamole or dumplings | no write | op=query | PASS |  |
| 2044 | D | which is better, korean bbq or nachos | no write | op=query | PASS |  |
| 2045 | D | which is better, empanadas or idli | no write | op=query | PASS |  |
| 2046 | D | which is better, falafel or poutine | no write | op=query | PASS |  |
| 2047 | D | which is better, idli or polenta | no write | op=query | PASS |  |
| 2048 | D | which is better, burger or moussaka | no write | op=query | PASS |  |
| 2049 | D | which is better, lobster roll or poha | no write | op=query | PASS |  |
| 205 | A | my favorite city is cairo | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2050 | D | which is better, paratha or pizza | no write | op=query | PASS |  |
| 2051 | D | which is better, burger or fried rice | no write | op=query | PASS |  |
| 2052 | D | how far is casablanca from oslo | no write | op=None | PASS |  |
| 2053 | D | how far is tokyo from athens | no write | op=None | PASS |  |
| 2054 | D | which is better, ceviche or tamale | no write | op=query | PASS |  |
| 2055 | D | how far is manila from mexico city | no write | op=None | PASS |  |
| 2056 | D | how far is vienna from milan | no write | op=None | PASS |  |
| 2057 | D | do you know my favorite drink | no write | op=query | PASS |  |
| 2058 | D | which is better, korean bbq or palak paneer | no write | op=query | PASS |  |
| 2059 | D | which is better, jambalaya or curry | no write | op=query | PASS |  |
| 206 | A | my favorite fruit is grapefruit | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2060 | D | which is better, burger or momos | no write | op=query | PASS |  |
| 2061 | D | which is better, burrito or lasagna | no write | op=query | PASS |  |
| 2062 | D | which is better, samosa or jambalaya | no write | op=query | PASS |  |
| 2063 | D | which is better, pasta or poutine | no write | op=query | PASS |  |
| 2064 | D | which is better, naan or korean bbq | no write | op=query | PASS |  |
| 2065 | D | which is better, ratatouille or sushi | no write | op=query | PASS |  |
| 2066 | D | which is better, gnocchi or calamari | no write | op=query | PASS |  |
| 2067 | D | which is better, guacamole or samosa | no write | op=query | PASS |  |
| 2068 | D | which is better, gumbo or chow mein | no write | op=query | PASS |  |
| 2069 | D | which is better, naan or ratatouille | no write | op=query | PASS |  |
| 207 | A | my favorite animal is squirrel | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2070 | D | which is better, thai curry or pancakes | no write | op=query | PASS |  |
| 2071 | D | you remember my favorite food is nachos | no write | op=query | PASS |  |
| 2072 | D | how far is capetown from quito | no write | op=None | PASS |  |
| 2073 | D | how far is dublin from kyoto | no write | op=None | PASS |  |
| 2074 | D | which is better, biryani or butter chicken | no write | op=query | PASS |  |
| 2075 | D | you remember my favorite dessert is truffles | no write | op=query | PASS |  |
| 2076 | D | which is better, tacos or calamari | no write | op=query | PASS |  |
| 2077 | D | which is better, pho or pho | no write | op=query | PASS |  |
| 2078 | D | how far is singapore from helsinki | no write | op=None | PASS |  |
| 2079 | D | which is better, momos or hummus plate | no write | op=query | PASS |  |
| 208 | A | my favorite food is waffles | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2080 | D | how far is kathmandu from buenos aires | no write | op=None | PASS |  |
| 2081 | D | how far is lisbon from hanoi | no write | op=None | PASS |  |
| 2082 | D | how far is prague from rome | no write | op=None | PASS |  |
| 2083 | D | you remember my favorite cuisine is mughlai | no write | op=query | PASS |  |
| 2084 | D | which is better, sandwich or jambalaya | no write | op=query | PASS |  |
| 2085 | D | how far is belfast from zurich | no write | op=None | PASS |  |
| 2086 | D | how far is venice from santiago | no write | op=None | PASS |  |
| 2087 | D | how far is cairo from seville | no write | op=None | PASS |  |
| 2088 | D | which is better, nachos or samosa | no write | op=query | PASS |  |
| 2089 | D | can you explain blockchain to me | no write | op=query | PASS |  |
| 209 | A | my favorite game is stardew valley | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2090 | D | which is better, shepherd pie or noodles | no write | op=query | PASS |  |
| 2091 | D | how far is boston from nairobi | no write | op=None | PASS |  |
| 2092 | D | you remember my favorite book is beloved | no write | op=query | PASS |  |
| 2093 | D | which is better, fried rice or bhel puri | no write | op=query | PASS |  |
| 2094 | D | which is better, burrito or ramen | no write | op=query | PASS |  |
| 2095 | D | do you know my favorite movie | no write | op=query | PASS |  |
| 2096 | D | you remember my favorite sport is archery | no write | op=query | PASS |  |
| 2097 | D | which is better, calamari or ceviche | no write | op=query | PASS |  |
| 2098 | D | you remember my favorite sport is discus | no write | op=query | PASS |  |
| 2099 | D | how far is buenos aires from buenos aires | no write | op=None | PASS |  |
| 21 | A | my favorite drink is birch beer | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is birch beer' | FAIL | store did not persist: status=needs_clarification present=False |
| 210 | A | my favorite drink is coffee | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is coffee' | FAIL | store did not persist: status=needs_clarification present=False |
| 2100 | D | what do you think about data analysis project | no write | op=query | PASS |  |
| 2101 | D | how far is budapest from buenos aires | no write | op=None | PASS |  |
| 2102 | D | what time is it in dubai | no write | op=None | PASS |  |
| 2103 | D | how far is budapest from milan | no write | op=None | PASS |  |
| 2104 | D | which is better, sushi or sushi | no write | op=query | PASS |  |
| 2105 | D | how far is kyoto from delhi | no write | op=None | PASS |  |
| 2106 | D | what is the weather like in amsterdam | no write | op=None | PASS |  |
| 2107 | D | which is better, nachos or polenta | no write | op=query | PASS |  |
| 2108 | D | which is better, hot pot or pizza | no write | op=query | PASS |  |
| 2109 | D | which is better, pasta or curry | no write | op=query | PASS |  |
| 211 | A | my favorite drink is green tea | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2110 | D | how far is sao paulo from dubai | no write | op=None | PASS |  |
| 2111 | D | which is better, pizza or lasagna | no write | op=query | PASS |  |
| 2112 | D | which is better, butter chicken or korean bbq | no write | op=query | PASS |  |
| 2113 | D | you remember my favorite sport is ice hockey | no write | op=query | PASS |  |
| 2114 | D | which is better, gnocchi or dumplings | no write | op=query | PASS |  |
| 2115 | D | which is better, hot pot or pho | no write | op=query | PASS |  |
| 2116 | D | how far is tokyo from melbourne | no write | op=None | PASS |  |
| 2117 | D | how far is amsterdam from quito | no write | op=None | PASS |  |
| 2118 | D | which is better, lobster roll or empanadas | no write | op=query | PASS |  |
| 2119 | D | when was github founded | no write | op=None | PASS |  |
| 212 | A | my favorite sport is shot put | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2120 | D | which is better, bhel puri or moussaka | no write | op=query | PASS |  |
| 2121 | D | how far is rotterdam from kathmandu | no write | op=None | PASS |  |
| 2122 | D | how far is cairo from helsinki | no write | op=None | PASS |  |
| 2123 | D | you remember my favorite subject is sociology | no write | op=query | PASS |  |
| 2124 | D | which is better, biryani or dosa | no write | op=query | PASS |  |
| 2125 | D | how far is amsterdam from lima | no write | op=None | PASS |  |
| 2126 | D | how far is singapore from lisbon | no write | op=None | PASS |  |
| 2127 | D | how far is vienna from casablanca | no write | op=None | PASS |  |
| 2128 | D | how far is kyoto from brussels | no write | op=None | PASS |  |
| 2129 | D | how far is delhi from florence | no write | op=None | PASS |  |
| 213 | A | my favorite writer is emily dickinson | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2130 | D | which is better, dosa or samosa | no write | op=query | PASS |  |
| 2131 | D | which is better, chow mein or burrito | no write | op=query | PASS |  |
| 2132 | D | which is better, butter chicken or sushi | no write | op=query | PASS |  |
| 2133 | D | how far is chennai from delhi | no write | op=None | PASS |  |
| 2134 | D | which is better, chow mein or vindaloo | no write | op=query | PASS |  |
| 2135 | D | how far is manchester from stockholm | no write | op=None | PASS |  |
| 2136 | D | how far is oslo from cairo | no write | op=None | PASS |  |
| 2137 | D | what do you think about painting class | no write | op=None | PASS |  |
| 2138 | D | which is better, gumbo or idli | no write | op=query | PASS |  |
| 2139 | D | which is better, palak paneer or jambalaya | no write | op=query | PASS |  |
| 214 | A | my favorite city is prague | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2140 | D | which is better, poutine or thai curry | no write | op=query | PASS |  |
| 2141 | D | which is better, gyoza or bruschetta | no write | op=query | PASS |  |
| 2142 | D | you remember my favorite food is pancakes | no write | op=query | PASS |  |
| 2143 | D | how far is delhi from sao paulo | no write | op=None | PASS |  |
| 2144 | D | which is better, pancakes or tamale | no write | op=query | PASS |  |
| 2145 | D | which is better, lasagna or burger | no write | op=query | PASS |  |
| 2146 | D | how far is budapest from casablanca | no write | op=None | PASS |  |
| 2147 | D | you remember my favorite music is trip hop | no write | op=query | PASS |  |
| 2148 | D | how far is prague from lima | no write | op=None | PASS |  |
| 2149 | D | you remember my favorite city is zurich | no write | op=query | PASS |  |
| 215 | A | my favorite writer is toni morrison | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2150 | D | how far is paris from warsaw | no write | op=None | PASS |  |
| 2151 | D | which is better, tamale or pho | no write | op=query | PASS |  |
| 2152 | D | which is better, palak paneer or korean bbq | no write | op=query | PASS |  |
| 2153 | D | what is the weather like in stockholm | no write | op=None | PASS |  |
| 2154 | D | which is better, poutine or pancakes | no write | op=query | PASS |  |
| 2155 | D | which is better, noodles or oysters | no write | op=query | PASS |  |
| 2156 | D | how far is milan from toronto | no write | op=None | PASS |  |
| 2157 | D | how far is sao paulo from seoul | no write | op=None | PASS |  |
| 2158 | D | which is better, calamari or gnocchi | no write | op=query | PASS |  |
| 2159 | D | what is the capital of china | no write | op=None | PASS |  |
| 216 | A | my favorite food is dosa | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2160 | D | how far is kathmandu from boston | no write | op=None | PASS |  |
| 2161 | D | you remember my favorite city is lagos | no write | op=query | PASS |  |
| 2162 | D | how far is manila from hanoi | no write | op=None | PASS |  |
| 2163 | D | how far is athens from belfast | no write | op=None | PASS |  |
| 2164 | D | how far is prague from cardiff | no write | op=None | PASS |  |
| 2165 | D | which is better, palak paneer or falafel | no write | op=query | PASS |  |
| 2166 | D | how far is rome from caracas | no write | op=None | PASS |  |
| 2167 | D | which is better, burrito or curry | no write | op=query | PASS |  |
| 2168 | D | which is better, nachos or calamari | no write | op=query | PASS |  |
| 2169 | D | which is better, empanadas or pierogi | no write | op=query | PASS |  |
| 217 | A | my favorite book is the hobbit | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2170 | D | how far is chennai from athens | no write | op=None | PASS |  |
| 2171 | D | when was greenpeace founded | no write | op=None | PASS |  |
| 2172 | D | which is better, jambalaya or noodles | no write | op=query | PASS |  |
| 2173 | D | how far is stockholm from tokyo | no write | op=None | PASS |  |
| 2174 | D | how far is delhi from rotterdam | no write | op=None | PASS |  |
| 2175 | D | how far is hanoi from melbourne | no write | op=None | PASS |  |
| 2176 | D | how does compound interest work | no write | op=query | PASS |  |
| 2177 | D | which is better, kebabs or sandwich | no write | op=query | PASS |  |
| 2178 | D | how far is mumbai from dublin | no write | op=None | PASS |  |
| 2179 | D | how far is oslo from boston | no write | op=None | PASS |  |
| 218 | A | my favorite drink is limeade | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is limeade' | FAIL | store did not persist: status=needs_clarification present=False |
| 2180 | D | how does magnetism work | no write | op=query | PASS |  |
| 2181 | D | when was cd projekt founded | no write | op=None | PASS |  |
| 2182 | D | which is better, noodles or gyoza | no write | op=query | PASS |  |
| 2183 | D | who wrote the color purple | no write | op=None | PASS |  |
| 2184 | D | how far is nairobi from berlin | no write | op=None | PASS |  |
| 2185 | D | which is better, palak paneer or naan | no write | op=query | PASS |  |
| 2186 | D | how far is rotterdam from madrid | no write | op=None | PASS |  |
| 2187 | D | which is better, momos or thai curry | no write | op=query | PASS |  |
| 2188 | D | which is better, bhel puri or ratatouille | no write | op=query | PASS |  |
| 2189 | D | which is better, tamale or naan | no write | op=query | PASS |  |
| 219 | A | my favorite movie is the hobbit | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2190 | D | which is better, gnocchi or naan | no write | op=query | PASS |  |
| 2191 | D | which is better, sandwich or thai curry | no write | op=query | PASS |  |
| 2192 | D | how far is helsinki from milan | no write | op=None | PASS |  |
| 2193 | D | you remember my favorite city is milan | no write | op=query | PASS |  |
| 2194 | D | how far is edinburgh from rotterdam | no write | op=None | PASS |  |
| 2195 | D | how far is boston from lisbon | no write | op=None | PASS |  |
| 2196 | D | how far is budapest from amsterdam | no write | op=None | PASS |  |
| 2197 | D | which is better, poutine or ramen | no write | op=query | PASS |  |
| 2198 | D | how far is lima from oslo | no write | op=None | PASS |  |
| 2199 | D | which is better, noodles or fried rice | no write | op=query | PASS |  |
| 22 | A | my favorite sport is long jump | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 220 | A | my favorite animal is panda | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2200 | D | give me advice about blog post | no write | op=store conf=1.0 | FAIL | no-write message produced a write: op=store fact='I need advice on a blog post' |
| 2201 | D | which is better, onion rings or momos | no write | op=query | PASS |  |
| 2202 | D | how far is athens from casablanca | no write | op=None | PASS |  |
| 2203 | D | how far is melbourne from dublin | no write | op=None | PASS |  |
| 2204 | D | you remember my favorite music is indie | no write | op=query | PASS |  |
| 2205 | D | how far is budapest from manila | no write | op=None | PASS |  |
| 2206 | D | which is better, gumbo or jambalaya | no write | op=query | PASS |  |
| 2207 | D | how far is rome from zurich | no write | op=None | PASS |  |
| 2208 | D | which is better, tamale or ratatouille | no write | op=query | PASS |  |
| 2209 | D | which is better, thai curry or thai curry | no write | op=query | PASS |  |
| 221 | A | my favorite show is friends | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2210 | D | how far is singapore from bogota | no write | op=None | PASS |  |
| 2211 | D | which is better, sushi or curry | no write | op=query | PASS |  |
| 2212 | D | you remember my favorite food is pasta | no write | op=query | PASS |  |
| 2213 | D | which is better, onion rings or naan | no write | op=query | PASS |  |
| 2214 | D | which is better, momos or kebabs | no write | op=query | PASS |  |
| 2215 | D | you remember my favorite drink is latte | no write | op=query | PASS |  |
| 2216 | D | which is better, bhel puri or bhel puri | no write | op=query | PASS |  |
| 2217 | D | which is better, ceviche or lobster roll | no write | op=query | PASS |  |
| 2218 | D | how far is edinburgh from manchester | no write | op=None | PASS |  |
| 2219 | D | which is better, palak paneer or noodles | no write | op=query | PASS |  |
| 222 | A | my favorite animal is raccoon | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2220 | D | you remember my favorite sport is skeleton | no write | op=query | PASS |  |
| 2221 | D | how far is kyoto from vienna | no write | op=None | PASS |  |
| 2222 | D | how does gravity work | no write | op=query | PASS |  |
| 2223 | D | which is better, onion rings or pancakes | no write | op=query | PASS |  |
| 2224 | D | which is better, gnocchi or jambalaya | no write | op=query | PASS |  |
| 2225 | D | which is better, poutine or lobster roll | no write | op=query | PASS |  |
| 2226 | D | which is better, moussaka or pancakes | no write | op=query | PASS |  |
| 2227 | D | can you explain magnetism to me | no write | op=query | PASS |  |
| 2228 | D | which is better, dumplings or sandwich | no write | op=query | PASS |  |
| 2229 | D | you remember my favorite music is bluegrass | no write | op=query | PASS |  |
| 223 | A | my favorite cuisine is sri lankan | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2230 | D | which is better, idli or pancakes | no write | op=query | PASS |  |
| 2231 | D | how far is sao paulo from cardiff | no write | op=None | PASS |  |
| 2232 | D | how far is toronto from montevideo | no write | op=None | PASS |  |
| 2233 | D | how far is cardiff from dubai | no write | op=None | PASS |  |
| 2234 | D | how far is dublin from mexico city | no write | op=None | PASS |  |
| 2235 | D | how far is boston from paris | no write | op=None | PASS |  |
| 2236 | D | which is better, korean bbq or idli | no write | op=query | PASS |  |
| 2237 | D | how far is athens from kyoto | no write | op=None | PASS |  |
| 2238 | D | how far is amsterdam from madrid | no write | op=None | PASS |  |
| 2239 | D | how far is oslo from paris | no write | op=None | PASS |  |
| 224 | A | my favorite music is afrobeat | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2240 | D | you remember my favorite drink is apple cider | no write | op=query | PASS |  |
| 2241 | D | you remember my favorite fruit is pomelo | no write | op=query | PASS |  |
| 2242 | D | which is better, waffles or paella | no write | op=query | PASS |  |
| 2243 | D | which is better, sandwich or nachos | no write | op=query | PASS |  |
| 2244 | D | how far is warsaw from sao paulo | no write | op=None | PASS |  |
| 2245 | D | which is better, jambalaya or thai curry | no write | op=query | PASS |  |
| 2246 | D | how far is vienna from capetown | no write | op=None | PASS |  |
| 2247 | D | how far is caracas from boston | no write | op=None | PASS |  |
| 2248 | D | you remember my favorite drink is sweet lassi | no write | op=query | PASS |  |
| 2249 | D | how far is delhi from nairobi | no write | op=None | PASS |  |
| 225 | A | my favorite writer is maya angelou | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2250 | D | you remember my favorite city is quito | no write | op=query | PASS |  |
| 2251 | D | how long does it take to fix a bike | no write | op=None | PASS |  |
| 2252 | D | what is the capital of turkey | no write | op=None | PASS |  |
| 2253 | D | you remember my favorite food is paella | no write | op=query | PASS |  |
| 2254 | D | how far is warsaw from barcelona | no write | op=None | PASS |  |
| 2255 | D | how far is capetown from paris | no write | op=None | PASS |  |
| 2256 | D | which is better, pizza or falafel | no write | op=query | PASS |  |
| 2257 | D | how far is belfast from prague | no write | op=None | PASS |  |
| 2258 | D | which is better, burrito or pierogi | no write | op=query | PASS |  |
| 2259 | D | how far is chennai from santiago | no write | op=None | PASS |  |
| 226 | A | my favorite movie is no country for old men | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2260 | D | you remember my favorite dessert is mishti doi | no write | op=query | PASS |  |
| 2261 | D | you remember my favorite writer is jrr tolkien | no write | op=query | PASS |  |
| 2262 | D | how far is boston from mexico city | no write | op=None | PASS |  |
| 2263 | D | which is better, paella or gnocchi | no write | op=query | PASS |  |
| 2264 | D | where can i buy a cooling pad | no write | op=query | PASS |  |
| 2265 | D | how far is prague from hanoi | no write | op=None | PASS |  |
| 2266 | D | which is better, risotto or gumbo | no write | op=query | PASS |  |
| 2267 | D | how far is seoul from singapore | no write | op=None | PASS |  |
| 2268 | D | how far is mumbai from venice | no write | op=None | PASS |  |
| 2269 | D | how far is paris from belfast | no write | op=None | PASS |  |
| 227 | A | my favorite music is bossa nova | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2270 | D | which is better, paella or tacos | no write | op=query | PASS |  |
| 2271 | D | give me advice about presentation | no write | op=store conf=1.0 | FAIL | no-write message produced a write: op=store fact='I need advice on a presentation' |
| 2272 | D | which is better, risotto or ceviche | no write | op=query | PASS |  |
| 2273 | D | which is better, samosa or chow mein | no write | op=query | PASS |  |
| 2274 | D | which is better, nachos or pierogi | no write | op=query | PASS |  |
| 2275 | D | can you explain smart contracts to me | no write | op=query | PASS |  |
| 2276 | D | what time is it in edinburgh | no write | op=None | PASS |  |
| 2277 | D | which is better, burger or sandwich | no write | op=query | PASS |  |
| 2278 | D | what is the capital of cuba | no write | op=None | PASS |  |
| 2279 | D | how far is jakarta from lima | no write | op=None | PASS |  |
| 228 | A | i am from kyoto | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 2280 | D | which is better, palak paneer or polenta | no write | op=query | PASS |  |
| 2281 | D | you remember my favorite show is the witcher | no write | op=query | PASS |  |
| 2282 | D | how far is buenos aires from belfast | no write | op=None | PASS |  |
| 2283 | D | which is better, calamari or noodles | no write | op=query | PASS |  |
| 2284 | D | which is better, naan or guacamole | no write | op=query | PASS |  |
| 2285 | D | which is better, tacos or hot pot | no write | op=query | PASS |  |
| 2286 | D | how far is oslo from edinburgh | no write | op=None | PASS |  |
| 2287 | D | how far is florence from warsaw | no write | op=None | PASS |  |
| 2288 | D | which is better, vindaloo or poutine | no write | op=query | PASS |  |
| 2289 | D | what does quixotic mean | no write | op=None | PASS |  |
| 229 | A | my favorite writer is charlotte bronte | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite writer is Charlotte Bronté' | FAIL | store did not persist: status=needs_clarification present=False |
| 2290 | D | how far is prague from berlin | no write | op=None | PASS |  |
| 2291 | D | how far is venice from caracas | no write | op=None | PASS |  |
| 2292 | D | which is better, tamale or noodles | no write | op=query | PASS |  |
| 2293 | D | you remember my favorite game is rocket league | no write | op=query | PASS |  |
| 2294 | D | how far is paris from florence | no write | op=None | PASS |  |
| 2295 | D | how far is berlin from chennai | no write | op=None | PASS |  |
| 2296 | D | which is better, shepherd pie or momos | no write | op=query | PASS |  |
| 2297 | D | which is better, empanadas or coleslaw | no write | op=query | PASS |  |
| 2298 | D | how far is sao paulo from stockholm | no write | op=None | PASS |  |
| 2299 | D | which is better, vindaloo or dosa | no write | op=query | PASS |  |
| 23 | A | my favorite drink is cider | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is cider' | FAIL | store did not persist: status=needs_clarification present=False |
| 230 | A | my favorite movie is oppenheimer | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2300 | D | which is better, samosa or calamari | no write | op=query | PASS |  |
| 2301 | D | how long does it take to wash the car | no write | op=None | PASS |  |
| 2302 | D | which is better, tacos or gumbo | no write | op=query | PASS |  |
| 2303 | D | how far is oslo from quito | no write | op=None | PASS |  |
| 2304 | D | how far is dublin from boston | no write | op=None | PASS |  |
| 2305 | D | you remember my favorite music is chamber | no write | op=query | PASS |  |
| 2306 | D | how far is dubai from amsterdam | no write | op=None | PASS |  |
| 2307 | D | how far is milan from dubai | no write | op=None | PASS |  |
| 2308 | D | which is better, risotto or gyoza | no write | op=query | PASS |  |
| 2309 | D | how far is lagos from mexico city | no write | op=None | PASS |  |
| 231 | A | my favorite fruit is blueberry | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2310 | D | how far is cardiff from paris | no write | op=None | PASS |  |
| 2311 | D | how far is dublin from lagos | no write | op=None | PASS |  |
| 2312 | D | how far is capetown from belfast | no write | op=None | PASS |  |
| 2313 | D | what is the capital of indonesia | no write | op=None | PASS |  |
| 2314 | D | which is better, ratatouille or poutine | no write | op=query | PASS |  |
| 2315 | D | which is better, vindaloo or gyoza | no write | op=query | PASS |  |
| 2316 | D | how far is santiago from chennai | no write | op=None | PASS |  |
| 2317 | D | which is better, vindaloo or kebabs | no write | op=query | PASS |  |
| 2318 | D | which is better, tamale or fried rice | no write | op=query | PASS |  |
| 2319 | D | which is better, hummus plate or naan | no write | op=query | PASS |  |
| 232 | A | my favorite animal is koala | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2320 | D | you remember my favorite fruit is cranberry | no write | op=query | PASS |  |
| 2321 | D | how far is seville from sao paulo | no write | op=None | PASS |  |
| 2322 | D | how far is oslo from prague | no write | op=None | PASS |  |
| 2323 | D | how far is hanoi from belfast | no write | op=None | PASS |  |
| 2324 | D | which is better, moussaka or ramen | no write | op=query | PASS |  |
| 2325 | D | how far is rio de janeiro from zurich | no write | op=None | PASS |  |
| 2326 | D | how far is milan from helsinki | no write | op=None | PASS |  |
| 2327 | D | which is better, banh mi or shepherd pie | no write | op=query | PASS |  |
| 2328 | D | which is better, momos or sandwich | no write | op=query | PASS |  |
| 2329 | D | which is better, jambalaya or sandwich | no write | op=query | PASS |  |
| 233 | A | my favorite animal is gecko | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2330 | D | which is better, pancakes or sandwich | no write | op=query | PASS |  |
| 2331 | D | how far is barcelona from prague | no write | op=None | PASS |  |
| 2332 | D | how far is hanoi from quito | no write | op=None | PASS |  |
| 2333 | D | how far is zurich from madrid | no write | op=None | PASS |  |
| 2334 | D | how far is brussels from seoul | no write | op=None | PASS |  |
| 2335 | D | how far is toronto from venice | no write | op=None | PASS |  |
| 2336 | D | you remember my favorite hobby is kayaking | no write | op=query | PASS |  |
| 2337 | D | you remember my favorite writer is mario vargas llosa | no write | op=query | PASS |  |
| 2338 | D | how far is vienna from paris | no write | op=None | PASS |  |
| 2339 | D | you remember my favorite drink is mango juice | no write | op=query | PASS |  |
| 234 | A | my favorite dessert is cinnamon roll | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2340 | D | how far is athens from santiago | no write | op=None | PASS |  |
| 2341 | D | how far is edinburgh from nairobi | no write | op=None | PASS |  |
| 2342 | D | how far is caracas from berlin | no write | op=None | PASS |  |
| 2343 | D | you remember my favorite color is gold | no write | op=query | PASS |  |
| 2344 | D | which is better, lasagna or coleslaw | no write | op=query | PASS |  |
| 2345 | D | how far is helsinki from rotterdam | no write | op=None | PASS |  |
| 2346 | D | can you explain the big bang to me | no write | op=query | PASS |  |
| 2347 | D | how far is cardiff from kathmandu | no write | op=None | PASS |  |
| 2348 | D | which is better, waffles or idli | no write | op=query | PASS |  |
| 2349 | D | how far is rio de janeiro from manchester | no write | op=None | PASS |  |
| 235 | A | my favorite drink is cafe au lait | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2350 | D | which is better, pancakes or kebabs | no write | op=query | PASS |  |
| 2351 | D | which is better, dumplings or paella | no write | op=query | PASS |  |
| 2352 | D | which is better, gnocchi or momos | no write | op=query | PASS |  |
| 2353 | D | which is better, calamari or curry | no write | op=query | PASS |  |
| 2354 | D | you remember my favorite music is drum and bass | no write | op=query | PASS |  |
| 2355 | D | who wrote the little prince | no write | op=None | PASS |  |
| 2356 | D | how far is tokyo from barcelona | no write | op=None | PASS |  |
| 2357 | D | which is better, pancakes or ramen | no write | op=query | PASS |  |
| 2358 | D | when was the gnu project founded | no write | op=query | PASS |  |
| 2359 | D | which is better, burger or pancakes | no write | op=query | PASS |  |
| 236 | A | my favorite color is burgundy | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2360 | D | how far is seoul from dublin | no write | op=None | PASS |  |
| 2361 | D | you remember my favorite animal is guinea | no write | op=query | PASS |  |
| 2362 | D | you remember my favorite game is divinity original sin 2 | no write | op=query | PASS |  |
| 2363 | D | you remember my favorite fruit is grapefruit | no write | op=query | PASS |  |
| 2364 | D | what do you think about insurance plan | no write | op=None | PASS |  |
| 2365 | D | which is better, dosa or sushi | no write | op=query | PASS |  |
| 2366 | D | which is better, oysters or gumbo | no write | op=query | PASS |  |
| 2367 | D | which is better, ramen or biryani | no write | op=query | PASS |  |
| 2368 | D | which is better, fried rice or nachos | no write | op=query | PASS |  |
| 2369 | D | how far is delhi from capetown | no write | op=None | PASS |  |
| 237 | A | i am from dublin | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 2370 | D | you remember my favorite cuisine is italian | no write | op=query | PASS |  |
| 2371 | D | which is better, onion rings or paratha | no write | op=query | PASS |  |
| 2372 | D | which is better, risotto or curry | no write | op=query | PASS |  |
| 2373 | D | how far is lima from amsterdam | no write | op=None | PASS |  |
| 2374 | D | which is better, paratha or pierogi | no write | op=query | PASS |  |
| 2375 | D | how far is brussels from cairo | no write | op=None | PASS |  |
| 2376 | D | how far is buenos aires from delhi | no write | op=None | PASS |  |
| 2377 | D | which is better, ceviche or paratha | no write | op=query | PASS |  |
| 2378 | D | you remember my favorite city is stockholm | no write | op=query | PASS |  |
| 2379 | D | which is better, naan or gumbo | no write | op=query | PASS |  |
| 238 | A | my favorite city is brussels | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2380 | D | which is better, momos or curry | no write | op=query | PASS |  |
| 2381 | D | how far is kyoto from lima | no write | op=None | PASS |  |
| 2382 | D | which is better, paratha or hot pot | no write | op=query | PASS |  |
| 2383 | D | how far is warsaw from delhi | no write | op=None | PASS |  |
| 2384 | D | which is better, tacos or pho | no write | op=query | PASS |  |
| 2385 | D | which is better, lobster roll or ratatouille | no write | op=query | PASS |  |
| 2386 | D | how far is sao paulo from warsaw | no write | op=None | PASS |  |
| 2387 | D | how far is toronto from rio de janeiro | no write | op=None | PASS |  |
| 2388 | D | how far is toronto from manila | no write | op=None | PASS |  |
| 2389 | D | you remember my favorite show is love death robots | no write | op=query | PASS |  |
| 239 | A | my favorite show is veep | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2390 | D | how far is kyoto from paris | no write | op=None | PASS |  |
| 2391 | D | how far is manila from milan | no write | op=None | PASS |  |
| 2392 | D | which is better, shepherd pie or ratatouille | no write | op=query | PASS |  |
| 2393 | D | which is better, tacos or sandwich | no write | op=query | PASS |  |
| 2394 | D | which is better, mac and cheese or poha | no write | op=query | PASS |  |
| 2395 | D | you remember my favorite dessert is rice pudding | no write | op=query | PASS |  |
| 2396 | D | which is better, pho or empanadas | no write | op=query | PASS |  |
| 2397 | D | which is better, thai curry or tamale | no write | op=query | PASS |  |
| 2398 | D | which is better, moussaka or poha | no write | op=query | PASS |  |
| 2399 | D | which is better, lobster roll or bruschetta | no write | op=query | PASS |  |
| 24 | A | my favorite city is buenos aires | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 240 | A | my favorite city is barcelona | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2400 | D | how far is rio de janeiro from delhi | no write | op=None | PASS |  |
| 2401 | D | how far is budapest from bogota | no write | op=None | PASS |  |
| 2402 | D | is coleslaw healthy | no write | op=None | PASS |  |
| 2403 | D | you remember my favorite sport is formula one | no write | op=query | PASS |  |
| 2404 | D | which is better, guacamole or burrito | no write | op=query | PASS |  |
| 2405 | D | how far is rio de janeiro from kyoto | no write | op=None | PASS |  |
| 2406 | D | how far is oslo from capetown | no write | op=None | PASS |  |
| 2407 | D | which is better, sushi or oysters | no write | op=query | PASS |  |
| 2408 | D | how far is florence from lagos | no write | op=None | PASS |  |
| 2409 | D | can you explain relativity to me | no write | op=query | PASS |  |
| 241 | A | my favorite animal is chameleon | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2410 | D | how far is tokyo from nairobi | no write | op=None | PASS |  |
| 2411 | D | when was the red cross founded | no write | op=None | PASS |  |
| 2412 | D | you remember my favorite subject is environmental science | no write | op=query | PASS |  |
| 2413 | D | which is better, noodles or dosa | no write | op=query | PASS |  |
| 2414 | D | you remember my favorite cuisine is argentine | no write | op=query | PASS |  |
| 2415 | D | which is better, burger or ramen | no write | op=query | PASS |  |
| 2416 | D | which is better, bhel puri or samosa | no write | op=query | PASS |  |
| 2417 | D | how far is dublin from budapest | no write | op=None | PASS |  |
| 2418 | D | how far is helsinki from toronto | no write | op=None | PASS |  |
| 2419 | D | which is better, ramen or korean bbq | no write | op=query | PASS |  |
| 242 | A | my favorite dessert is carrot cake | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2420 | D | how far is bangkok from chennai | no write | op=None | PASS |  |
| 2421 | D | which is better, onion rings or polenta | no write | op=query | PASS |  |
| 2422 | D | you remember my favorite animal is toad | no write | op=query | PASS |  |
| 2423 | D | which is better, onion rings or dosa | no write | op=query | PASS |  |
| 2424 | D | how does the carbon cycle work | no write | op=query | PASS |  |
| 2425 | D | you remember my favorite game is red dead redemption 2 | no write | op=query | PASS |  |
| 2426 | D | how far is bangkok from manila | no write | op=None | PASS |  |
| 2427 | D | who wrote divergent | no write | op=None | PASS |  |
| 2428 | D | which is better, gumbo or tacos | no write | op=query | PASS |  |
| 2429 | D | you remember my favorite show is the expanse | no write | op=query | PASS |  |
| 243 | A | my favorite show is love death robots | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2430 | D | which is better, nachos or coleslaw | no write | op=query | PASS |  |
| 2431 | D | which is better, hot pot or onion rings | no write | op=query | PASS |  |
| 2432 | D | how far is prague from athens | no write | op=None | PASS |  |
| 2433 | D | how far is bangkok from santiago | no write | op=None | PASS |  |
| 2434 | D | how far is madrid from kyoto | no write | op=None | PASS |  |
| 2435 | D | is vindaloo healthy | no write | op=None | PASS |  |
| 2436 | D | which is better, empanadas or butter chicken | no write | op=query | PASS |  |
| 2437 | D | how far is rio de janeiro from manila | no write | op=None | PASS |  |
| 2438 | D | which is better, poha or waffles | no write | op=query | PASS |  |
| 2439 | D | which is better, oysters or burrito | no write | op=query | PASS |  |
| 244 | A | my favorite fruit is muskmelon | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2440 | D | how far is rotterdam from seville | no write | op=None | PASS |  |
| 2441 | D | which is better, poha or oysters | no write | op=query | PASS |  |
| 2442 | D | how far is helsinki from hanoi | no write | op=None | PASS |  |
| 2443 | D | how far is santiago from sao paulo | no write | op=None | PASS |  |
| 2444 | D | which is better, guacamole or coleslaw | no write | op=query | PASS |  |
| 2445 | D | you remember my favorite drink is cranberry juice | no write | op=query | PASS |  |
| 2446 | D | which is better, falafel or dosa | no write | op=query | PASS |  |
| 2447 | D | which is better, vindaloo or ramen | no write | op=query | PASS |  |
| 2448 | D | how far is zurich from belfast | no write | op=None | PASS |  |
| 2449 | D | which is better, sandwich or biryani | no write | op=query | PASS |  |
| 245 | A | my favorite food is hot pot | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2450 | D | how far is singapore from chennai | no write | op=None | PASS |  |
| 2451 | D | how far is casablanca from singapore | no write | op=None | PASS |  |
| 2452 | D | which is better, biryani or pancakes | no write | op=query | PASS |  |
| 2453 | D | which is better, risotto or korean bbq | no write | op=query | PASS |  |
| 2454 | D | how far is manila from athens | no write | op=None | PASS |  |
| 2455 | D | which is better, lasagna or chow mein | no write | op=query | PASS |  |
| 2456 | D | which is better, fried rice or onion rings | no write | op=query | PASS |  |
| 2457 | D | how far is sao paulo from brussels | no write | op=None | PASS |  |
| 2458 | D | which is better, dosa or mac and cheese | no write | op=query | PASS |  |
| 2459 | D | which is better, noodles or ramen | no write | op=query | PASS |  |
| 246 | A | my favorite fruit is rambutan | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2460 | D | what time is it in chennai | no write | op=None | PASS |  |
| 2461 | D | how does scrum work | no write | op=query | PASS |  |
| 2462 | D | which is better, biryani or poha | no write | op=query | PASS |  |
| 2463 | D | which is better, vindaloo or tacos | no write | op=query | PASS |  |
| 2464 | D | which is better, pho or hot pot | no write | op=query | PASS |  |
| 2465 | D | which is better, naan or empanadas | no write | op=query | PASS |  |
| 2466 | D | how far is casablanca from mexico city | no write | op=None | PASS |  |
| 2467 | D | which is better, jambalaya or tacos | no write | op=query | PASS |  |
| 2468 | D | you remember my favorite color is blue | no write | op=query | PASS |  |
| 2469 | D | how far is rotterdam from prague | no write | op=None | PASS |  |
| 247 | A | my favorite movie is schindler list | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2470 | D | which is better, thai curry or oysters | no write | op=query | PASS |  |
| 2471 | D | how far is capetown from seoul | no write | op=None | PASS |  |
| 2472 | D | how far is kyoto from mexico city | no write | op=None | PASS |  |
| 2473 | D | which is better, ramen or ramen | no write | op=query | PASS |  |
| 2474 | D | which is better, ceviche or hummus plate | no write | op=query | PASS |  |
| 2475 | D | how far is lagos from santiago | no write | op=None | PASS |  |
| 2476 | D | which is better, vindaloo or pierogi | no write | op=query | PASS |  |
| 2477 | D | how far is mumbai from quito | no write | op=None | PASS |  |
| 2478 | D | how far is paris from madrid | no write | op=None | PASS |  |
| 2479 | D | you remember my favorite color is purple | no write | op=query | PASS |  |
| 248 | A | my favorite game is gta v | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2480 | D | how far is delhi from warsaw | no write | op=None | PASS |  |
| 2481 | D | how far is florence from casablanca | no write | op=None | PASS |  |
| 2482 | D | which is better, noodles or kebabs | no write | op=query | PASS |  |
| 2483 | D | is hot pot healthy | no write | op=None | PASS |  |
| 2484 | D | which is better, kebabs or oysters | no write | op=query | PASS |  |
| 2485 | D | how far is singapore from oslo | no write | op=None | PASS |  |
| 2486 | D | how far is florence from capetown | no write | op=None | PASS |  |
| 2487 | D | which is better, samosa or ceviche | no write | op=query | PASS |  |
| 2488 | D | how far is milan from hanoi | no write | op=None | PASS |  |
| 2489 | D | which is better, tamale or sushi | no write | op=query | PASS |  |
| 249 | A | my favorite fruit is lychee | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2490 | D | which is better, butter chicken or pancakes | no write | op=query | PASS |  |
| 2491 | D | how far is manila from bangkok | no write | op=None | PASS |  |
| 2492 | D | how far is prague from kathmandu | no write | op=None | PASS |  |
| 2493 | D | which is better, onion rings or calamari | no write | op=query | PASS |  |
| 2494 | D | you remember my favorite food is ceviche | no write | op=query | PASS |  |
| 2495 | D | you remember my favorite game is slay the spire | no write | op=query | PASS |  |
| 2496 | D | how far is singapore from manila | no write | op=None | PASS |  |
| 2497 | D | which is better, noodles or hot pot | no write | op=query | PASS |  |
| 2498 | D | how far is bangkok from seville | no write | op=None | PASS |  |
| 2499 | D | which is better, dumplings or bruschetta | no write | op=query | PASS |  |
| 25 | A | my favorite city is sao paulo | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 250 | A | my favorite hobby is stargazing | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2500 | D | how far is dublin from dubai | no write | op=None | PASS |  |
| 2501 | D | which is better, pierogi or pasta | no write | op=query | PASS |  |
| 2502 | D | which is better, onion rings or empanadas | no write | op=query | PASS |  |
| 2503 | D | which is better, moussaka or pierogi | no write | op=query | PASS |  |
| 2504 | D | which is better, korean bbq or bhel puri | no write | op=query | PASS |  |
| 2505 | D | you remember my favorite writer is f scott fitzgerald | no write | op=query | PASS |  |
| 2506 | D | which is better, ramen or pizza | no write | op=query | PASS |  |
| 2507 | D | which is better, pizza or vindaloo | no write | op=query | PASS |  |
| 2508 | D | how far is edinburgh from rio de janeiro | no write | op=None | PASS |  |
| 2509 | D | how far is rio de janeiro from florence | no write | op=None | PASS |  |
| 251 | A | my favorite subject is mechanics | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2510 | D | you remember my favorite food is tamale | no write | op=query | PASS |  |
| 2511 | D | how far is caracas from dubai | no write | op=None | PASS |  |
| 2512 | D | which is better, naan or palak paneer | no write | op=query | PASS |  |
| 2513 | D | which is better, oysters or paratha | no write | op=query | PASS |  |
| 2514 | D | you remember my favorite hobby is paddleboarding | no write | op=query | PASS |  |
| 2515 | D | how far is kathmandu from seoul | no write | op=None | PASS |  |
| 2516 | D | which is better, ramen or palak paneer | no write | op=query | PASS |  |
| 2517 | D | which is better, sandwich or calamari | no write | op=query | PASS |  |
| 2518 | D | which is better, risotto or burrito | no write | op=query | PASS |  |
| 2519 | D | you remember my favorite sport is canoeing | no write | op=query | PASS |  |
| 252 | A | i am from toronto | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 2520 | D | which is better, poha or moussaka | no write | op=query | PASS |  |
| 2521 | D | how far is tokyo from lima | no write | op=None | PASS |  |
| 2522 | D | what is the capital of india | no write | op=None | PASS |  |
| 2523 | D | how far is boston from cairo | no write | op=None | PASS |  |
| 2524 | D | you remember my favorite fruit is kumquat | no write | op=query | PASS |  |
| 2525 | D | you remember my favorite food is burger | no write | op=query | PASS |  |
| 2526 | D | can you explain compilers to me | no write | op=query | PASS |  |
| 2527 | D | which is better, paratha or dumplings | no write | op=query | PASS |  |
| 2528 | D | how far is lima from cardiff | no write | op=None | PASS |  |
| 2529 | D | which is better, pho or banh mi | no write | op=query | PASS |  |
| 253 | A | my favorite color is teal | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2530 | D | which is better, poha or paratha | no write | op=query | PASS |  |
| 2531 | D | how far is bogota from athens | no write | op=None | PASS |  |
| 2532 | D | which is better, naan or tamale | no write | op=query | PASS |  |
| 2533 | D | how far is paris from rio de janeiro | no write | op=None | PASS |  |
| 2534 | D | how far is mumbai from kathmandu | no write | op=None | PASS |  |
| 2535 | D | which is better, falafel or thai curry | no write | op=query | PASS |  |
| 2536 | D | which is better, ramen or burrito | no write | op=query | PASS |  |
| 2537 | D | how far is madrid from santiago | no write | op=None | PASS |  |
| 2538 | D | how does recursion work | no write | op=query | PASS |  |
| 2539 | D | you remember my favorite sport is windsurfing | no write | op=query | PASS |  |
| 254 | A | my favorite city is berlin | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2540 | D | how far is santiago from casablanca | no write | op=None | PASS |  |
| 2541 | D | you remember my favorite subject is logic | no write | op=query | PASS |  |
| 2542 | D | you remember my favorite hobby is bread baking | no write | op=query | PASS |  |
| 2543 | D | which is better, tacos or pancakes | no write | op=query | PASS |  |
| 2544 | D | how far is madrid from cardiff | no write | op=None | PASS |  |
| 2545 | D | what do you think about kitchen renovation | no write | op=None | PASS |  |
| 2546 | D | how far is capetown from hanoi | no write | op=None | PASS |  |
| 2547 | D | which is better, polenta or ceviche | no write | op=query | PASS |  |
| 2548 | D | how far is prague from santiago | no write | op=None | PASS |  |
| 2549 | D | which is better, jambalaya or samosa | no write | op=query | PASS |  |
| 255 | A | my favorite food is jambalaya | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2550 | D | which is better, dosa or tacos | no write | op=query | PASS |  |
| 2551 | D | how far is quito from boston | no write | op=None | PASS |  |
| 2552 | D | which is better, noodles or bruschetta | no write | op=query | PASS |  |
| 2553 | D | which is better, risotto or oysters | no write | op=query | PASS |  |
| 2554 | D | give me advice about twitch stream | no write | op=query | PASS |  |
| 2555 | D | which is better, palak paneer or sandwich | no write | op=query | PASS |  |
| 2556 | D | how far is buenos aires from helsinki | no write | op=None | PASS |  |
| 2557 | D | which is better, pho or pierogi | no write | op=query | PASS |  |
| 2558 | D | how far is florence from montevideo | no write | op=None | PASS |  |
| 2559 | D | which is better, gumbo or hot pot | no write | op=query | PASS |  |
| 256 | A | my favorite movie is the sixth sense | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2560 | D | which is better, chow mein or naan | no write | op=query | PASS |  |
| 2561 | D | how far is seoul from toronto | no write | op=None | PASS |  |
| 2562 | D | which is better, falafel or tamale | no write | op=query | PASS |  |
| 2563 | D | which is better, poha or thai curry | no write | op=query | PASS |  |
| 2564 | D | which is better, lasagna or ramen | no write | op=query | PASS |  |
| 2565 | D | which is better, oysters or vindaloo | no write | op=query | PASS |  |
| 2566 | D | which is better, oysters or samosa | no write | op=query | PASS |  |
| 2567 | D | how far is venice from bangkok | no write | op=None | PASS |  |
| 2568 | D | which is better, lobster roll or korean bbq | no write | op=query | PASS |  |
| 2569 | D | how far is vienna from chennai | no write | op=None | PASS |  |
| 257 | A | my favorite show is euphoria | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2570 | D | how far is bangkok from bangkok | no write | op=None | PASS |  |
| 2571 | D | how far is delhi from boston | no write | op=None | PASS |  |
| 2572 | D | which is better, mac and cheese or calamari | no write | op=query | PASS |  |
| 2573 | D | which is better, lobster roll or risotto | no write | op=query | PASS |  |
| 2574 | D | which is better, biryani or polenta | no write | op=query | PASS |  |
| 2575 | D | how far is madrid from seoul | no write | op=None | PASS |  |
| 2576 | D | you remember my favorite food is sushi | no write | op=query | PASS |  |
| 2577 | D | how far is prague from quito | no write | op=None | PASS |  |
| 2578 | D | which is better, oysters or mac and cheese | no write | op=query | PASS |  |
| 2579 | D | how far is venice from jakarta | no write | op=None | PASS |  |
| 258 | A | i am from lagos | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 2580 | D | how far is berlin from oslo | no write | op=None | PASS |  |
| 2581 | D | how far is lagos from buenos aires | no write | op=None | PASS |  |
| 2582 | D | can you explain statistics to me | no write | op=query | PASS |  |
| 2583 | D | which is better, sandwich or polenta | no write | op=query | PASS |  |
| 2584 | D | what is the weather like in montevideo | no write | op=None | PASS |  |
| 2585 | D | how far is kyoto from berlin | no write | op=None | PASS |  |
| 2586 | D | which is better, poha or risotto | no write | op=query | PASS |  |
| 2587 | D | how far is mumbai from santiago | no write | op=None | PASS |  |
| 2588 | D | which is better, chow mein or bhel puri | no write | op=query | PASS |  |
| 2589 | D | how far is nairobi from budapest | no write | op=None | PASS |  |
| 259 | A | my favorite city is milan | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2590 | D | which is better, poha or curry | no write | op=query | PASS |  |
| 2591 | D | how far is brussels from paris | no write | op=None | PASS |  |
| 2592 | D | you remember my favorite cuisine is andhra | no write | op=query | PASS |  |
| 2593 | D | which is better, sushi or burrito | no write | op=query | PASS |  |
| 2594 | D | which is better, curry or waffles | no write | op=query | PASS |  |
| 2595 | D | which is better, bhel puri or kebabs | no write | op=query | PASS |  |
| 2596 | D | how far is kathmandu from seville | no write | op=None | PASS |  |
| 2597 | D | how far is seville from capetown | no write | op=None | PASS |  |
| 2598 | D | how far is boston from melbourne | no write | op=None | PASS |  |
| 2599 | D | which is better, shepherd pie or bhel puri | no write | op=query | PASS |  |
| 26 | A | my favorite movie is saving private ryan | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 260 | A | my favorite subject is statistics | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2600 | D | how far is nairobi from capetown | no write | op=None | PASS |  |
| 2601 | D | which is better, sushi or samosa | no write | op=query | PASS |  |
| 2602 | D | which is better, thai curry or sushi | no write | op=query | PASS |  |
| 2603 | D | you remember my favorite color is periwinkle | no write | op=query | PASS |  |
| 2604 | D | which is better, samosa or korean bbq | no write | op=query | PASS |  |
| 2605 | D | how far is kyoto from athens | no write | op=None | PASS |  |
| 2606 | D | which is better, waffles or risotto | no write | op=query | PASS |  |
| 2607 | D | how far is warsaw from dubai | no write | op=None | PASS |  |
| 2608 | D | which is better, momos or ceviche | no write | op=query | PASS |  |
| 2609 | D | which is better, paella or korean bbq | no write | op=query | PASS |  |
| 261 | A | my favorite fruit is clementine | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2610 | D | how far is jakarta from oslo | no write | op=None | PASS |  |
| 2611 | D | which is better, ceviche or ceviche | no write | op=query | PASS |  |
| 2612 | D | what does ephemeral mean | no write | op=None | PASS |  |
| 2613 | D | which is better, naan or moussaka | no write | op=query | PASS |  |
| 2614 | D | which is better, risotto or vindaloo | no write | op=query | PASS |  |
| 2615 | D | how far is bangkok from tokyo | no write | op=None | PASS |  |
| 2616 | D | you remember my favorite season is spring | no write | op=query | PASS |  |
| 2617 | D | how far is brussels from copenhagen | no write | op=query | PASS |  |
| 2618 | D | how far is copenhagen from delhi | no write | op=query | PASS |  |
| 2619 | D | which is better, naan or vindaloo | no write | op=query | PASS |  |
| 262 | A | i am from chennai | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 2620 | D | you remember my favorite city is belfast | no write | op=query | PASS |  |
| 2621 | D | how far is milan from paris | no write | op=None | PASS |  |
| 2622 | D | how far is santiago from paris | no write | op=None | PASS |  |
| 2623 | D | who wrote the grapes of wrath | no write | op=None | PASS |  |
| 2624 | D | how far is bogota from prague | no write | op=None | PASS |  |
| 2625 | D | which is better, guacamole or momos | no write | op=query | PASS |  |
| 2626 | D | how far is kathmandu from belfast | no write | op=None | PASS |  |
| 2627 | D | you remember my favorite food is curry | no write | op=query | PASS |  |
| 2628 | D | you remember my favorite movie is the shape of water | no write | op=query | PASS |  |
| 2629 | D | how far is berlin from boston | no write | op=None | PASS |  |
| 263 | A | my favorite movie is the revenant | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2630 | D | how far is brussels from tokyo | no write | op=None | PASS |  |
| 2631 | D | which is better, butter chicken or thai curry | no write | op=query | PASS |  |
| 2632 | D | which is better, kebabs or coleslaw | no write | op=query | PASS |  |
| 2633 | D | how far is belfast from athens | no write | op=None | PASS |  |
| 2634 | D | what is the weather like in milan | no write | op=None | PASS |  |
| 2635 | D | how far is paris from sao paulo | no write | op=None | PASS |  |
| 2636 | D | which is better, mac and cheese or curry | no write | op=query | PASS |  |
| 2637 | D | which is better, banh mi or lobster roll | no write | op=query | PASS |  |
| 2638 | D | you remember my favorite hobby is stamp collecting | no write | op=query | PASS |  |
| 2639 | D | how far is cardiff from zurich | no write | op=None | PASS |  |
| 264 | A | my favorite cuisine is russian | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2640 | D | which is better, thai curry or guacamole | no write | op=query | PASS |  |
| 2641 | D | how far is manchester from rome | no write | op=None | PASS |  |
| 2642 | D | how far is toronto from bogota | no write | op=None | PASS |  |
| 2643 | D | you remember my favorite subject is psychology | no write | op=query | PASS |  |
| 2644 | D | which is better, gumbo or calamari | no write | op=query | PASS |  |
| 2645 | D | how far is kathmandu from helsinki | no write | op=None | PASS |  |
| 2646 | D | give me advice about hackathon | no write | op=store conf=1.0 | FAIL | no-write message produced a write: op=store fact='I want to know about hackathons' |
| 2647 | D | which is better, chow mein or chow mein | no write | op=query | PASS |  |
| 2648 | D | how far is caracas from dublin | no write | op=None | PASS |  |
| 2649 | D | how far is sao paulo from milan | no write | op=None | PASS |  |
| 265 | A | my favorite subject is film studies | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2650 | D | what do you think about travel itinerary | no write | op=None | PASS |  |
| 2651 | D | which is better, gnocchi or thai curry | no write | op=query | PASS |  |
| 2652 | D | how far is lima from chennai | no write | op=None | PASS |  |
| 2653 | D | how far is stockholm from cardiff | no write | op=None | PASS |  |
| 2654 | D | how far is amsterdam from vienna | no write | op=None | PASS |  |
| 2655 | D | what is the weather like in rome | no write | op=None | PASS |  |
| 2656 | D | how far is warsaw from dublin | no write | op=None | PASS |  |
| 2657 | D | which is better, tacos or kebabs | no write | op=query | PASS |  |
| 2658 | D | how far is santiago from copenhagen | no write | op=query | PASS |  |
| 2659 | D | how far is dublin from montevideo | no write | op=None | PASS |  |
| 266 | A | my favorite dessert is laddu | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2660 | D | which is better, lobster roll or gumbo | no write | op=query | PASS |  |
| 2661 | D | how far is madrid from manila | no write | op=None | PASS |  |
| 2662 | D | how far is rome from dublin | no write | op=None | PASS |  |
| 2663 | D | which is better, gyoza or pancakes | no write | op=query | PASS |  |
| 2664 | D | which is better, hot pot or burrito | no write | op=query | PASS |  |
| 2665 | D | which is better, pho or shepherd pie | no write | op=query | PASS |  |
| 2666 | D | how far is seville from edinburgh | no write | op=None | PASS |  |
| 2667 | D | which is better, pasta or mac and cheese | no write | op=query | PASS |  |
| 2668 | D | who wrote lord of the flies | no write | op=None | PASS |  |
| 2669 | D | which is better, kebabs or tacos | no write | op=query | PASS |  |
| 267 | A | i am from santiago | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 2670 | D | which is better, biryani or biryani | no write | op=query | PASS |  |
| 2671 | D | how far is helsinki from bangkok | no write | op=None | PASS |  |
| 2672 | D | what is supply and demand | no write | op=None | PASS |  |
| 2673 | D | which is better, jambalaya or ramen | no write | op=query | PASS |  |
| 2674 | D | how far is casablanca from berlin | no write | op=None | PASS |  |
| 2675 | D | which is better, korean bbq or guacamole | no write | op=query | PASS |  |
| 2676 | D | which is better, calamari or tacos | no write | op=query | PASS |  |
| 2677 | D | which is better, tacos or paratha | no write | op=query | PASS |  |
| 2678 | D | which is better, guacamole or polenta | no write | op=query | PASS |  |
| 2679 | D | how far is melbourne from milan | no write | op=None | PASS |  |
| 268 | A | my pet's name is sadie | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2680 | D | how far is capetown from rotterdam | no write | op=None | PASS |  |
| 2681 | D | how far is lisbon from lisbon | no write | op=None | PASS |  |
| 2682 | D | how far is manila from tokyo | no write | op=None | PASS |  |
| 2683 | D | how far is sao paulo from edinburgh | no write | op=None | PASS |  |
| 2684 | D | how far is lisbon from buenos aires | no write | op=None | PASS |  |
| 2685 | D | how long does it take to unclog a drain | no write | op=None | PASS |  |
| 2686 | D | you remember my favorite hobby is sudoku | no write | op=query | PASS |  |
| 2687 | D | can you explain agile to me | no write | op=query | PASS |  |
| 2688 | D | which is better, polenta or bhel puri | no write | op=query | PASS |  |
| 2689 | D | how far is madrid from amsterdam | no write | op=None | PASS |  |
| 269 | A | i am from paris | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 2690 | D | you remember my favorite city is mexico city | no write | op=query | PASS |  |
| 2691 | D | how far is edinburgh from bogota | no write | op=None | PASS |  |
| 2692 | D | you remember my favorite subject is music theory | no write | op=query | PASS |  |
| 2693 | D | which is better, poutine or nachos | no write | op=query | PASS |  |
| 2694 | D | you remember my favorite dessert is creme brulee | no write | op=query | PASS |  |
| 2695 | D | how far is hanoi from dublin | no write | op=None | PASS |  |
| 2696 | D | which is better, ramen or pho | no write | op=query | PASS |  |
| 2697 | D | how does serverless work | no write | op=query | PASS |  |
| 2698 | D | what is the capital of panama | no write | op=None | PASS |  |
| 2699 | D | how far is toronto from belfast | no write | op=None | PASS |  |
| 27 | A | my favorite food is calamari | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 270 | A | my favorite sport is volleyball | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2700 | D | which is better, mac and cheese or naan | no write | op=query | PASS |  |
| 2701 | D | which is better, poutine or coleslaw | no write | op=query | PASS |  |
| 2702 | D | how far is copenhagen from oslo | no write | op=query | PASS |  |
| 2703 | D | you remember my favorite drink is buttermilk | no write | op=query | PASS |  |
| 2704 | D | how long does it take to mow the lawn | no write | op=None | PASS |  |
| 2705 | D | which is better, calamari or moussaka | no write | op=query | PASS |  |
| 2706 | D | how far is manchester from lima | no write | op=None | PASS |  |
| 2707 | D | how far is quito from sao paulo | no write | op=None | PASS |  |
| 2708 | D | how far is seoul from prague | no write | op=None | PASS |  |
| 2709 | D | which is better, biryani or palak paneer | no write | op=query | PASS |  |
| 271 | A | my favorite hobby is kayaking | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2710 | D | which is better, empanadas or poha | no write | op=query | PASS |  |
| 2711 | D | how far is prague from chennai | no write | op=None | PASS |  |
| 2712 | D | you remember my favorite color is cobalt | no write | op=query | PASS |  |
| 2713 | D | which is better, ratatouille or dosa | no write | op=query | PASS |  |
| 2714 | D | which is better, vindaloo or moussaka | no write | op=query | PASS |  |
| 2715 | D | which is better, kebabs or noodles | no write | op=query | PASS |  |
| 2716 | D | which is better, mac and cheese or tamale | no write | op=query | PASS |  |
| 2717 | D | which is better, burger or ceviche | no write | op=query | PASS |  |
| 2718 | D | which is better, paella or gyoza | no write | op=query | PASS |  |
| 2719 | D | how far is bogota from belfast | no write | op=None | PASS |  |
| 272 | A | my favorite city is bogota | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2720 | D | which is better, burger or paratha | no write | op=query | PASS |  |
| 2721 | D | how far is capetown from athens | no write | op=None | PASS |  |
| 2722 | D | you remember my favorite game is splatoon | no write | op=query | PASS |  |
| 2723 | D | how far is jakarta from budapest | no write | op=None | PASS |  |
| 2724 | D | you remember my favorite food is hummus plate | no write | op=query | PASS |  |
| 2725 | D | how far is buenos aires from casablanca | no write | op=None | PASS |  |
| 2726 | D | you remember my favorite animal is lobster | no write | op=query | PASS |  |
| 2727 | D | you remember my favorite animal is pig | no write | op=query | PASS |  |
| 2728 | D | how far is rome from rome | no write | op=None | PASS |  |
| 2729 | D | you remember my favorite food is bhel puri | no write | op=query | PASS |  |
| 273 | A | my favorite game is monster hunter | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2730 | D | which is better, hummus plate or noodles | no write | op=query | PASS |  |
| 2731 | D | how far is buenos aires from prague | no write | op=None | PASS |  |
| 2732 | D | how far is lisbon from athens | no write | op=None | PASS |  |
| 2733 | D | how far is santiago from stockholm | no write | op=None | PASS |  |
| 2734 | D | which is better, shepherd pie or jambalaya | no write | op=query | PASS |  |
| 2735 | D | how does electricity work | no write | op=query | PASS |  |
| 2736 | D | how far is rio de janeiro from barcelona | no write | op=None | PASS |  |
| 2737 | D | you remember my favorite animal is clownfish | no write | op=query | PASS |  |
| 2738 | D | what is quarantine | no write | op=None | PASS |  |
| 2739 | D | how far is toronto from toronto | no write | op=None | PASS |  |
| 274 | A | my favorite music is trance | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2740 | D | which is better, noodles or momos | no write | op=query | PASS |  |
| 2741 | D | you remember my favorite dessert is cheesecake | no write | op=query | PASS |  |
| 2742 | D | where can i buy a laptop stand | no write | op=query | PASS |  |
| 2743 | D | you remember my favorite show is curb your enthusiasm | no write | op=query | PASS |  |
| 2744 | D | which is better, thai curry or butter chicken | no write | op=query | PASS |  |
| 2745 | D | which is better, momos or gyoza | no write | op=query | PASS |  |
| 2746 | D | which is better, mac and cheese or ceviche | no write | op=query | PASS |  |
| 2747 | D | how far is tokyo from copenhagen | no write | op=query | PASS |  |
| 2748 | D | how far is oslo from manchester | no write | op=None | PASS |  |
| 2749 | D | which is better, mac and cheese or guacamole | no write | op=query | PASS |  |
| 275 | A | my favorite movie is the departed | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2750 | D | how far is belfast from seville | no write | op=None | PASS |  |
| 2751 | D | which is better, oysters or idli | no write | op=query | PASS |  |
| 2752 | D | which is better, hot pot or waffles | no write | op=query | PASS |  |
| 2753 | D | what is the capital of nepal | no write | op=None | PASS |  |
| 2754 | D | how far is zurich from kyoto | no write | op=None | PASS |  |
| 2755 | D | how far is warsaw from stockholm | no write | op=None | PASS |  |
| 2756 | D | which is better, dumplings or mac and cheese | no write | op=query | PASS |  |
| 2757 | D | which is better, ceviche or ramen | no write | op=query | PASS |  |
| 2758 | D | how far is brussels from boston | no write | op=None | PASS |  |
| 2759 | D | which is better, waffles or curry | no write | op=query | PASS |  |
| 276 | A | my favorite animal is crocodile | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2760 | D | which is better, bhel puri or nachos | no write | op=query | PASS |  |
| 2761 | D | which is better, poha or hummus plate | no write | op=query | PASS |  |
| 2762 | D | how far is quito from venice | no write | op=None | PASS |  |
| 2763 | D | you remember my favorite game is stray | no write | op=query | PASS |  |
| 2764 | D | how far is manchester from quito | no write | op=None | PASS |  |
| 2765 | D | give me advice about branding | no write | op=None | PASS |  |
| 2766 | D | how far is dubai from rotterdam | no write | op=None | PASS |  |
| 2767 | D | which is better, tacos or nachos | no write | op=query | PASS |  |
| 2768 | D | how far is jakarta from athens | no write | op=None | PASS |  |
| 2769 | D | which is better, tamale or pizza | no write | op=query | PASS |  |
| 277 | A | my favorite show is the last of us | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2770 | D | which is better, lobster roll or hummus plate | no write | op=query | PASS |  |
| 2771 | D | how far is madrid from cairo | no write | op=None | PASS |  |
| 2772 | D | how far is kyoto from quito | no write | op=None | PASS |  |
| 2773 | D | you remember my favorite fruit is pomegranate | no write | op=query | PASS |  |
| 2774 | D | how far is casablanca from tokyo | no write | op=None | PASS |  |
| 2775 | D | how far is santiago from quito | no write | op=None | PASS |  |
| 2776 | D | which is better, jambalaya or onion rings | no write | op=query | PASS |  |
| 2777 | D | how far is buenos aires from boston | no write | op=None | PASS |  |
| 2778 | D | you remember my favorite color is lavender | no write | op=query | PASS |  |
| 2779 | D | which is better, gnocchi or bhel puri | no write | op=query | PASS |  |
| 278 | A | my favorite fruit is apricot | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2780 | D | you remember my favorite drink is chamomile | no write | op=query | PASS |  |
| 2781 | D | how far is delhi from santiago | no write | op=None | PASS |  |
| 2782 | D | you remember my favorite show is dark | no write | op=query | PASS |  |
| 2783 | D | which is better, curry or pancakes | no write | op=query | PASS |  |
| 2784 | D | how far is stockholm from edinburgh | no write | op=None | PASS |  |
| 2785 | D | you remember my favorite sport is football | no write | op=query | PASS |  |
| 2786 | D | how far is nairobi from kathmandu | no write | op=None | PASS |  |
| 2787 | D | which is better, banh mi or coleslaw | no write | op=query | PASS |  |
| 2788 | D | how far is vienna from nairobi | no write | op=None | PASS |  |
| 2789 | D | which is better, lobster roll or pizza | no write | op=query | PASS |  |
| 279 | A | my favorite drink is watermelon juice | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is watermelon juice' | FAIL | store did not persist: status=needs_clarification present=False |
| 2790 | D | which is better, korean bbq or poha | no write | op=query | PASS |  |
| 2791 | D | what time is it in barcelona | no write | op=None | PASS |  |
| 2792 | D | how far is amsterdam from bogota | no write | op=None | PASS |  |
| 2793 | D | which is better, coleslaw or sushi | no write | op=query | PASS |  |
| 2794 | D | how far is paris from kyoto | no write | op=None | PASS |  |
| 2795 | D | how far is athens from melbourne | no write | op=None | PASS |  |
| 2796 | D | how far is oslo from budapest | no write | op=None | PASS |  |
| 2797 | D | which is better, polenta or jambalaya | no write | op=query | PASS |  |
| 2798 | D | which is better, samosa or samosa | no write | op=query | PASS |  |
| 2799 | D | which is better, polenta or noodles | no write | op=query | PASS |  |
| 28 | A | my favorite hobby is mushroom foraging | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 280 | A | my favorite book is project hail mary | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2800 | D | which is better, dosa or risotto | no write | op=query | PASS |  |
| 2801 | D | how far is seoul from edinburgh | no write | op=None | PASS |  |
| 2802 | D | what do you think about research paper | no write | op=None | PASS |  |
| 2803 | D | how far is boston from rotterdam | no write | op=None | PASS |  |
| 2804 | D | what is operating systems | no write | op=None | PASS |  |
| 2805 | D | how far is buenos aires from vienna | no write | op=None | PASS |  |
| 2806 | D | which is better, dumplings or moussaka | no write | op=query | PASS |  |
| 2807 | D | how far is toronto from nairobi | no write | op=None | PASS |  |
| 2808 | D | how far is chennai from cairo | no write | op=None | PASS |  |
| 2809 | D | how far is prague from cairo | no write | op=None | PASS |  |
| 281 | A | my favorite show is industry | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2810 | D | how far is lisbon from casablanca | no write | op=None | PASS |  |
| 2811 | D | which is better, burrito or falafel | no write | op=query | PASS |  |
| 2812 | D | which is better, tacos or momos | no write | op=query | PASS |  |
| 2813 | D | how does greenhouse effect work | no write | op=query | PASS |  |
| 2814 | D | you remember my favorite food is shepherd pie | no write | op=query | PASS |  |
| 2815 | D | how far is caracas from mexico city | no write | op=None | PASS |  |
| 2816 | D | how far is santiago from edinburgh | no write | op=None | PASS |  |
| 2817 | D | which is better, pho or palak paneer | no write | op=query | PASS |  |
| 2818 | D | which is better, calamari or onion rings | no write | op=query | PASS |  |
| 2819 | D | how far is sao paulo from kathmandu | no write | op=None | PASS |  |
| 282 | A | my favorite game is portal 2 | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2820 | D | what do you think about homework help | no write | op=query | PASS |  |
| 2821 | D | which is better, korean bbq or pho | no write | op=query | PASS |  |
| 2822 | D | can you explain dark matter to me | no write | op=query | PASS |  |
| 2823 | D | how far is capetown from rome | no write | op=None | PASS |  |
| 2824 | D | how far is florence from manchester | no write | op=None | PASS |  |
| 2825 | D | what time is it in kathmandu | no write | op=None | PASS |  |
| 2826 | D | which is better, fried rice or chow mein | no write | op=query | PASS |  |
| 2827 | D | you remember my favorite show is lost | no write | op=query | PASS |  |
| 2828 | D | which is better, momos or palak paneer | no write | op=query | PASS |  |
| 2829 | D | how far is amsterdam from santiago | no write | op=None | PASS |  |
| 283 | A | my favorite city is capetown | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2830 | D | how far is capetown from bogota | no write | op=None | PASS |  |
| 2831 | D | how far is bangkok from cairo | no write | op=None | PASS |  |
| 2832 | D | which is better, sushi or onion rings | no write | op=query | PASS |  |
| 2833 | D | how far is singapore from mumbai | no write | op=None | PASS |  |
| 2834 | D | how far is casablanca from budapest | no write | op=None | PASS |  |
| 2835 | D | how far is budapest from tokyo | no write | op=None | PASS |  |
| 2836 | D | how far is chennai from copenhagen | no write | op=query | PASS |  |
| 2837 | D | how far is budapest from kyoto | no write | op=None | PASS |  |
| 2838 | D | which is better, bhel puri or pizza | no write | op=query | PASS |  |
| 2839 | D | you remember my favorite fruit is boysenberry | no write | op=query | PASS |  |
| 284 | A | my favorite drink is smoothie | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is smoothie' | FAIL | store did not persist: status=needs_clarification present=False |
| 2840 | D | how far is lisbon from manila | no write | op=None | PASS |  |
| 2841 | D | you remember my favorite dessert is funnel cake | no write | op=query | PASS |  |
| 2842 | D | you remember my favorite drink is guava juice | no write | op=query | PASS |  |
| 2843 | D | are you great | no write | op=None | PASS |  |
| 2844 | D | you remember my favorite food is naan | no write | op=query | PASS |  |
| 2845 | D | can you explain the immune system to me | no write | op=query | PASS |  |
| 2846 | D | which is better, biryani or sushi | no write | op=query | PASS |  |
| 2847 | D | which is better, momos or empanadas | no write | op=query | PASS |  |
| 2848 | D | you remember my favorite writer is ernest cline | no write | op=query | PASS |  |
| 2849 | D | which is better, dumplings or pancakes | no write | op=query | PASS |  |
| 285 | A | my favorite fruit is mandarin | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2850 | D | how far is lisbon from madrid | no write | op=None | PASS |  |
| 2851 | D | what is greenhouse effect | no write | op=None | PASS |  |
| 2852 | D | you remember my favorite color is coral | no write | op=query | PASS |  |
| 2853 | D | which is better, calamari or gumbo | no write | op=query | PASS |  |
| 2854 | D | how far is nairobi from seoul | no write | op=None | PASS |  |
| 2855 | D | which is better, pasta or vindaloo | no write | op=query | PASS |  |
| 2856 | D | you remember my favorite movie is moonlight | no write | op=query | PASS |  |
| 2857 | D | which is better, bhel puri or butter chicken | no write | op=query | PASS |  |
| 2858 | D | which is better, sandwich or burrito | no write | op=query | PASS |  |
| 2859 | D | which is better, bruschetta or oysters | no write | op=query | PASS |  |
| 286 | A | my favorite dessert is coconut barfi | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2860 | D | which is better, fried rice or falafel | no write | op=query | PASS |  |
| 2861 | D | how far is madrid from quito | no write | op=None | PASS |  |
| 2862 | D | you remember my favorite movie is parasite | no write | op=query | PASS |  |
| 2863 | D | which is better, shepherd pie or dosa | no write | op=query | PASS |  |
| 2864 | D | which is better, shepherd pie or onion rings | no write | op=query | PASS |  |
| 2865 | D | which is better, pierogi or fried rice | no write | op=query | PASS |  |
| 2866 | D | which is better, lasagna or fried rice | no write | op=query | PASS |  |
| 2867 | D | which is better, falafel or moussaka | no write | op=query | PASS |  |
| 2868 | D | which is better, oysters or oysters | no write | op=query | PASS |  |
| 2869 | D | which is better, moussaka or noodles | no write | op=query | PASS |  |
| 287 | A | my favorite dessert is pecan pie | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2870 | D | which is better, paella or lobster roll | no write | op=query | PASS |  |
| 2871 | D | how far is paris from nairobi | no write | op=None | PASS |  |
| 2872 | D | you remember my favorite city is kathmandu | no write | op=query | PASS |  |
| 2873 | D | how far is prague from toronto | no write | op=None | PASS |  |
| 2874 | D | which is better, shepherd pie or waffles | no write | op=query | PASS |  |
| 2875 | D | how far is lagos from florence | no write | op=None | PASS |  |
| 2876 | D | how far is casablanca from manila | no write | op=None | PASS |  |
| 2877 | D | which is better, banh mi or poutine | no write | op=query | PASS |  |
| 2878 | D | how far is brussels from venice | no write | op=None | PASS |  |
| 2879 | D | which is better, paratha or poutine | no write | op=query | PASS |  |
| 288 | A | my favorite book is the sound and the fury | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2880 | D | how far is zurich from nairobi | no write | op=None | PASS |  |
| 2881 | D | how far is manchester from vienna | no write | op=None | PASS |  |
| 2882 | D | which is better, banh mi or thai curry | no write | op=query | PASS |  |
| 2883 | D | which is better, naan or sandwich | no write | op=query | PASS |  |
| 2884 | D | how far is sao paulo from belfast | no write | op=None | PASS |  |
| 2885 | D | how far is jakarta from nairobi | no write | op=None | PASS |  |
| 2886 | D | how far is mumbai from lisbon | no write | op=None | PASS |  |
| 2887 | D | how far is manila from florence | no write | op=None | PASS |  |
| 2888 | D | how does the internet work | no write | op=query | PASS |  |
| 2889 | D | how far is melbourne from athens | no write | op=None | PASS |  |
| 289 | A | my favorite food is gyoza | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2890 | D | which is better, thai curry or nachos | no write | op=None | PASS |  |
| 2891 | D | how far is stockholm from rio de janeiro | no write | op=None | PASS |  |
| 2892 | D | which is better, banh mi or guacamole | no write | op=query | PASS |  |
| 2893 | D | how far is quito from stockholm | no write | op=None | PASS |  |
| 2894 | D | you remember my favorite animal is hare | no write | op=query | PASS |  |
| 2895 | D | which is better, curry or lasagna | no write | op=query | PASS |  |
| 2896 | D | how far is melbourne from melbourne | no write | op=None | PASS |  |
| 2897 | D | which is better, korean bbq or thai curry | no write | op=query | PASS |  |
| 2898 | D | how far is warsaw from quito | no write | op=None | PASS |  |
| 2899 | D | which is better, bruschetta or ramen | no write | op=query | PASS |  |
| 29 | A | my favorite cuisine is sichuan | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 290 | A | my favorite subject is linguistics | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2900 | D | how far is boston from sao paulo | no write | op=None | PASS |  |
| 2901 | D | how far is boston from delhi | no write | op=None | PASS |  |
| 2902 | D | which is better, polenta or hot pot | no write | op=query | PASS |  |
| 2903 | D | how far is capetown from melbourne | no write | op=None | PASS |  |
| 2904 | D | you remember my favorite drink is orange soda | no write | op=query | PASS |  |
| 2905 | D | which is better, gumbo or waffles | no write | op=query | PASS |  |
| 2906 | D | how far is paris from delhi | no write | op=None | PASS |  |
| 2907 | D | you remember my favorite game is outer wilds | no write | op=query | PASS |  |
| 2908 | D | which is better, lobster roll or lobster roll | no write | op=query | PASS |  |
| 2909 | D | how far is copenhagen from rotterdam | no write | op=query | PASS |  |
| 291 | A | my favorite cuisine is austrian | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2910 | D | how far is florence from kathmandu | no write | op=None | PASS |  |
| 2911 | D | which is better, jambalaya or momos | no write | op=query | PASS |  |
| 2912 | D | how far is kyoto from kathmandu | no write | op=None | PASS |  |
| 2913 | D | how far is zurich from amsterdam | no write | op=None | PASS |  |
| 2914 | D | how far is nairobi from nairobi | no write | op=None | PASS |  |
| 2915 | D | what is the water cycle | no write | op=None | PASS |  |
| 2916 | D | how far is venice from tokyo | no write | op=None | PASS |  |
| 2917 | D | how far is manila from seville | no write | op=None | PASS |  |
| 2918 | D | which is better, idli or burrito | no write | op=query | PASS |  |
| 2919 | D | which is better, pierogi or dosa | no write | op=query | PASS |  |
| 292 | A | my favorite movie is the dark knight | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2920 | D | how far is seoul from brussels | no write | op=None | PASS |  |
| 2921 | D | which is better, pierogi or mac and cheese | no write | op=query | PASS |  |
| 2922 | D | you remember my favorite fruit is muskmelon | no write | op=query | PASS |  |
| 2923 | D | you remember my favorite movie is no country for old men | no write | op=query | PASS |  |
| 2924 | D | how far is copenhagen from buenos aires | no write | op=query | PASS |  |
| 2925 | D | how far is belfast from chennai | no write | op=None | PASS |  |
| 2926 | D | how far is capetown from copenhagen | no write | op=query | PASS |  |
| 2927 | D | you remember my favorite subject is statistics | no write | op=query | PASS |  |
| 2928 | D | how far is rotterdam from montevideo | no write | op=None | PASS |  |
| 2929 | D | which is better, paella or pierogi | no write | op=query | PASS |  |
| 293 | A | my favorite food is butter chicken | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2930 | D | how far is buenos aires from berlin | no write | op=None | PASS |  |
| 2931 | D | how far is berlin from kathmandu | no write | op=None | PASS |  |
| 2932 | D | which is better, oysters or empanadas | no write | op=query | PASS |  |
| 2933 | D | how far is kyoto from tokyo | no write | op=None | PASS |  |
| 2934 | D | you remember my favorite drink is cider | no write | op=query | PASS |  |
| 2935 | D | what does sonder mean | no write | op=None | PASS |  |
| 2936 | D | how far is barcelona from florence | no write | op=None | PASS |  |
| 2937 | D | which is better, onion rings or nachos | no write | op=query | PASS |  |
| 2938 | D | which is better, dumplings or waffles | no write | op=query | PASS |  |
| 2939 | D | when was nintendo founded | no write | op=None | PASS |  |
| 294 | A | i am from vienna | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 2940 | D | which is better, ramen or noodles | no write | op=query | PASS |  |
| 2941 | D | which is better, onion rings or moussaka | no write | op=query | PASS |  |
| 2942 | D | which is better, korean bbq or poutine | no write | op=query | PASS |  |
| 2943 | D | how far is cairo from quito | no write | op=None | PASS |  |
| 2944 | D | how far is berlin from capetown | no write | op=None | PASS |  |
| 2945 | D | you remember my favorite book is the little prince | no write | op=query | PASS |  |
| 2946 | D | how far is nairobi from rome | no write | op=None | PASS |  |
| 2947 | D | how far is copenhagen from dubai | no write | op=query | PASS |  |
| 2948 | D | which is better, hot pot or moussaka | no write | op=query | PASS |  |
| 2949 | D | which is better, pizza or polenta | no write | op=query | PASS |  |
| 295 | A | my favorite drink is sweet lassi | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is sweet lassi' | FAIL | store did not persist: status=needs_clarification present=False |
| 2950 | D | which is better, dosa or falafel | no write | op=query | PASS |  |
| 2951 | D | which is better, fried rice or waffles | no write | op=query | PASS |  |
| 2952 | D | you remember my favorite writer is pablo neruda | no write | op=query | PASS |  |
| 2953 | D | how far is vienna from lima | no write | op=None | PASS |  |
| 2954 | D | what is the capital of thailand | no write | op=None | PASS |  |
| 2955 | D | how does photosynthesis work | no write | op=query | PASS |  |
| 2956 | D | how far is seville from seville | no write | op=None | PASS |  |
| 2957 | D | you remember my favorite music is disco | no write | op=query | PASS |  |
| 2958 | D | you remember my favorite game is cyberpunk 2077 | no write | op=query | PASS |  |
| 2959 | D | what is gdp | no write | op=None | PASS |  |
| 296 | A | my favorite food is naan | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2960 | D | you remember my favorite movie is the sixth sense | no write | op=query | PASS |  |
| 2961 | D | how far is sao paulo from madrid | no write | op=None | PASS |  |
| 2962 | D | which is better, coleslaw or onion rings | no write | op=query | PASS |  |
| 2963 | D | which is better, burrito or dosa | no write | op=query | PASS |  |
| 2964 | D | how far is brussels from manchester | no write | op=None | PASS |  |
| 2965 | D | how far is oslo from florence | no write | op=None | PASS |  |
| 2966 | D | you remember my favorite game is cuphead | no write | op=query | PASS |  |
| 2967 | D | how far is kathmandu from cardiff | no write | op=None | PASS |  |
| 2968 | D | which is better, pasta or hot pot | no write | op=query | PASS |  |
| 2969 | D | which is better, chow mein or samosa | no write | op=query | PASS |  |
| 297 | A | my favorite hobby is gardening | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2970 | D | which is better, burrito or biryani | no write | op=query | PASS |  |
| 2971 | D | how far is paris from kathmandu | no write | op=None | PASS |  |
| 2972 | D | you remember my favorite animal is newt | no write | op=query | PASS |  |
| 2973 | D | which is better, gyoza or paratha | no write | op=query | PASS |  |
| 2974 | D | how far is boston from quito | no write | op=None | PASS |  |
| 2975 | D | which is better, paella or vindaloo | no write | op=query | PASS |  |
| 2976 | D | which is better, guacamole or pho | no write | op=query | PASS |  |
| 2977 | D | which is better, gyoza or burrito | no write | op=query | PASS |  |
| 2978 | D | you remember my favorite subject is optics | no write | op=query | PASS |  |
| 2979 | D | how long does it take to fix a leak | no write | op=None | PASS |  |
| 298 | A | my favorite fruit is strawberry | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 2980 | D | which is better, ratatouille or korean bbq | no write | op=query | PASS |  |
| 2981 | D | which is better, ratatouille or coleslaw | no write | op=query | PASS |  |
| 2982 | D | how far is montevideo from amsterdam | no write | op=None | PASS |  |
| 2983 | D | which is better, dosa or ratatouille | no write | op=query | PASS |  |
| 2984 | D | how far is chennai from budapest | no write | op=None | PASS |  |
| 2985 | D | which is better, bruschetta or polenta | no write | op=query | PASS |  |
| 2986 | D | which is better, korean bbq or ramen | no write | op=query | PASS |  |
| 2987 | D | which is better, samosa or pizza | no write | op=query | PASS |  |
| 2988 | D | which is better, risotto or onion rings | no write | op=query | PASS |  |
| 2989 | D | which is better, calamari or paratha | no write | op=query | PASS |  |
| 299 | A | my favorite color is fuchsia | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 2990 | D | how far is rome from belfast | no write | op=None | PASS |  |
| 2991 | D | which is better, coleslaw or naan | no write | op=query | PASS |  |
| 2992 | D | which is better, palak paneer or coleslaw | no write | op=query | PASS |  |
| 2993 | D | what is the capital of tanzania | no write | op=None | PASS |  |
| 2994 | D | which is better, sandwich or waffles | no write | op=query | PASS |  |
| 2995 | D | how far is dubai from hanoi | no write | op=None | PASS |  |
| 2996 | D | which is better, poha or onion rings | no write | op=query | PASS |  |
| 2997 | D | how far is hanoi from prague | no write | op=None | PASS |  |
| 2998 | D | which is better, pho or vindaloo | no write | op=query | PASS |  |
| 2999 | D | which is better, noodles or tacos | no write | op=query | PASS |  |
| 3 | A | my favorite movie is everything everywhere all at once | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 30 | A | my favorite animal is pig | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 300 | A | my favorite show is better call saul | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3000 | D | how far is stockholm from brussels | no write | op=None | PASS |  |
| 3001 | D | where can i buy an | no write | op=query | PASS |  |
| 3002 | D | which is better, poutine or shepherd pie | no write | op=query | PASS |  |
| 3003 | D | which is better, curry or noodles | no write | op=query | PASS |  |
| 3004 | D | which is better, hummus plate or risotto | no write | op=query | PASS |  |
| 3005 | D | which is better, vindaloo or paella | no write | op=query | PASS |  |
| 3006 | D | how far is delhi from chennai | no write | op=None | PASS |  |
| 3007 | D | which is better, sandwich or mac and cheese | no write | op=query | PASS |  |
| 3008 | D | which is better, chow mein or tamale | no write | op=query | PASS |  |
| 3009 | D | you remember my favorite music is hindustani | no write | op=query | PASS |  |
| 301 | A | my favorite music is ska | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3010 | D | how far is lima from buenos aires | no write | op=None | PASS |  |
| 3011 | D | how far is oslo from helsinki | no write | op=None | PASS |  |
| 3012 | D | who wrote atomic habits | no write | op=None | PASS |  |
| 3013 | D | where can i buy scanner | no write | op=query | PASS |  |
| 3014 | D | how far is tokyo from berlin | no write | op=None | PASS |  |
| 3015 | D | who wrote the old man and the sea | no write | op=None | PASS |  |
| 3016 | D | how far is montevideo from toronto | no write | op=None | PASS |  |
| 3017 | D | how far is berlin from lagos | no write | op=None | PASS |  |
| 3018 | D | how far is barcelona from stockholm | no write | op=None | PASS |  |
| 3019 | D | how far is boston from belfast | no write | op=None | PASS |  |
| 302 | A | my favorite show is curb your enthusiasm | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3020 | D | how far is quito from cairo | no write | op=None | PASS |  |
| 3021 | D | which is better, risotto or fried rice | no write | op=query | PASS |  |
| 3022 | D | which is better, samosa or pho | no write | op=query | PASS |  |
| 3023 | D | which is better, pierogi or lobster roll | no write | op=query | PASS |  |
| 3024 | D | how far is santiago from toronto | no write | op=None | PASS |  |
| 3025 | D | how far is florence from bogota | no write | op=None | PASS |  |
| 3026 | D | you remember my favorite color is orange | no write | op=query | PASS |  |
| 3027 | D | what is compilers | no write | op=None | PASS |  |
| 3028 | D | how far is warsaw from seville | no write | op=None | PASS |  |
| 3029 | D | how far is lagos from manila | no write | op=None | PASS |  |
| 303 | A | my favorite sport is e-sports | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 3030 | D | you remember my favorite movie is the departed | no write | op=query | PASS |  |
| 3031 | D | how far is mexico city from brussels | no write | op=None | PASS |  |
| 3032 | D | which is better, hummus plate or nachos | no write | op=query | PASS |  |
| 3033 | D | which is better, pancakes or bruschetta | no write | op=query | PASS |  |
| 3034 | D | how far is caracas from stockholm | no write | op=None | PASS |  |
| 3035 | D | which is better, pizza or kebabs | no write | op=query | PASS |  |
| 3036 | D | how far is venice from athens | no write | op=None | PASS |  |
| 3037 | D | which is better, naan or bruschetta | no write | op=query | PASS |  |
| 3038 | D | which is better, calamari or banh mi | no write | op=query | PASS |  |
| 3039 | D | how far is stockholm from boston | no write | op=None | PASS |  |
| 304 | A | my favorite cuisine is jamaican | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3040 | D | which is better, moussaka or tamale | no write | op=query | PASS |  |
| 3041 | D | which is better, waffles or burrito | no write | op=query | PASS |  |
| 3042 | D | how far is capetown from berlin | no write | op=None | PASS |  |
| 3043 | D | which is better, poha or poutine | no write | op=query | PASS |  |
| 3044 | D | how far is nairobi from mumbai | no write | op=None | PASS |  |
| 3045 | D | how far is capetown from singapore | no write | op=None | PASS |  |
| 3046 | D | you remember my favorite hobby is robotics | no write | op=query | PASS |  |
| 3047 | D | which is better, shepherd pie or lobster roll | no write | op=query | PASS |  |
| 3048 | D | you remember my favorite drink is green tea | no write | op=query | PASS |  |
| 3049 | D | how far is seoul from manila | no write | op=None | PASS |  |
| 305 | A | my favorite cuisine is goan | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3050 | D | how far is hanoi from tokyo | no write | op=None | PASS |  |
| 3051 | D | when was oculus founded | no write | op=None | PASS |  |
| 3052 | D | how far is rome from rio de janeiro | no write | op=None | PASS |  |
| 3053 | D | how far is seoul from seville | no write | op=None | PASS |  |
| 3054 | D | which is better, naan or lasagna | no write | op=query | PASS |  |
| 3055 | D | which is better, pizza or coleslaw | no write | op=query | PASS |  |
| 3056 | D | how far is prague from tokyo | no write | op=None | PASS |  |
| 3057 | D | which is better, bruschetta or sandwich | no write | op=query | PASS |  |
| 3058 | D | how far is florence from dublin | no write | op=None | PASS |  |
| 3059 | D | how far is montevideo from manila | no write | op=None | PASS |  |
| 306 | A | my favorite subject is literature | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3060 | D | which is better, burger or tacos | no write | op=query | PASS |  |
| 3061 | D | which is better, bruschetta or naan | no write | op=query | PASS |  |
| 3062 | D | how far is manila from paris | no write | op=None | PASS |  |
| 3063 | D | how far is warsaw from rome | no write | op=None | PASS |  |
| 3064 | D | how far is sao paulo from lagos | no write | op=None | PASS |  |
| 3065 | D | how far is casablanca from dublin | no write | op=None | PASS |  |
| 3066 | D | which is better, ramen or shepherd pie | no write | op=query | PASS |  |
| 3067 | D | how far is barcelona from caracas | no write | op=None | PASS |  |
| 3068 | D | give me advice about science fair | no write | op=query | PASS |  |
| 3069 | D | which is better, samosa or oysters | no write | op=query | PASS |  |
| 307 | A | my favorite animal is salamander | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3070 | D | which is better, paratha or thai curry | no write | op=query | PASS |  |
| 3071 | D | how far is rio de janeiro from copenhagen | no write | op=query | PASS |  |
| 3072 | D | which is better, poha or burrito | no write | op=query | PASS |  |
| 3073 | D | how far is lagos from berlin | no write | op=None | PASS |  |
| 3074 | D | how far is dublin from madrid | no write | op=None | PASS |  |
| 3075 | D | which is better, jambalaya or ceviche | no write | op=query | PASS |  |
| 3076 | D | which is better, pho or noodles | no write | op=query | PASS |  |
| 3077 | D | how far is budapest from barcelona | no write | op=None | PASS |  |
| 3078 | D | how far is budapest from toronto | no write | op=None | PASS |  |
| 3079 | D | how far is edinburgh from toronto | no write | op=None | PASS |  |
| 308 | A | my favorite food is idli | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3080 | D | which is better, guacamole or pancakes | no write | op=query | PASS |  |
| 3081 | D | which is better, paella or burrito | no write | op=query | PASS |  |
| 3082 | D | which is better, pancakes or curry | no write | op=query | PASS |  |
| 3083 | D | how far is edinburgh from boston | no write | op=None | PASS |  |
| 3084 | D | which is better, bruschetta or vindaloo | no write | op=query | PASS |  |
| 3085 | D | can you explain devops to me | no write | op=query | PASS |  |
| 3086 | D | you remember my favorite dessert is apple pie | no write | op=query | PASS |  |
| 3087 | D | which is better, butter chicken or gumbo | no write | op=query | PASS |  |
| 3088 | D | how far is hanoi from barcelona | no write | op=None | PASS |  |
| 3089 | D | you remember my favorite food is tacos | no write | op=query | PASS |  |
| 309 | A | my favorite show is community | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3090 | D | you remember my favorite sport is luge | no write | op=query | PASS |  |
| 3091 | D | how far is lima from rome | no write | op=None | PASS |  |
| 3092 | D | which is better, fried rice or butter chicken | no write | op=query | PASS |  |
| 3093 | D | you remember my favorite sport is high jump | no write | op=query | PASS |  |
| 3094 | D | which is better, kebabs or poutine | no write | op=query | PASS |  |
| 3095 | D | how far is dubai from caracas | no write | op=None | PASS |  |
| 3096 | D | how far is barcelona from venice | no write | op=None | PASS |  |
| 3097 | D | which is better, paratha or palak paneer | no write | op=query | PASS |  |
| 3098 | D | what do you think about tax filing | no write | op=None | PASS |  |
| 3099 | D | which is better, idli or coleslaw | no write | op=None | PASS |  |
| 31 | A | my favorite color is periwinkle | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 310 | A | i work as a athlete | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 3100 | D | you remember my favorite cuisine is southern indian | no write | op=query | PASS |  |
| 3101 | D | how far is brussels from delhi | no write | op=None | PASS |  |
| 3102 | D | how far is kyoto from cairo | no write | op=None | PASS |  |
| 3103 | D | how far is dublin from florence | no write | op=None | PASS |  |
| 3104 | D | how far is chennai from amsterdam | no write | op=None | PASS |  |
| 3105 | D | what time is it in zurich | no write | op=None | PASS |  |
| 3106 | D | which is better, polenta or lobster roll | no write | op=query | PASS |  |
| 3107 | D | how far is delhi from stockholm | no write | op=None | PASS |  |
| 3108 | D | how far is prague from milan | no write | op=None | PASS |  |
| 3109 | D | which is better, naan or calamari | no write | op=query | PASS |  |
| 311 | A | my favorite city is seville | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3110 | D | how far is zurich from rotterdam | no write | op=None | PASS |  |
| 3111 | D | which is better, lasagna or vindaloo | no write | op=query | PASS |  |
| 3112 | D | which is better, gyoza or shepherd pie | no write | op=query | PASS |  |
| 3113 | D | how far is caracas from buenos aires | no write | op=None | PASS |  |
| 3114 | D | when was openai founded | no write | op=None | PASS |  |
| 3115 | D | which is better, paratha or sandwich | no write | op=query | PASS |  |
| 3116 | D | how far is edinburgh from paris | no write | op=None | PASS |  |
| 3117 | D | which is better, sushi or momos | no write | op=query | PASS |  |
| 3118 | D | which is better, idli or gyoza | no write | op=query | PASS |  |
| 3119 | D | which is better, palak paneer or waffles | no write | op=query | PASS |  |
| 312 | A | my favorite drink is tonic water | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3120 | D | how far is stockholm from helsinki | no write | op=None | PASS |  |
| 3121 | D | how far is amsterdam from prague | no write | op=None | PASS |  |
| 3122 | D | which is better, dumplings or noodles | no write | op=query | PASS |  |
| 3123 | D | which is better, oysters or falafel | no write | op=query | PASS |  |
| 3124 | D | which is better, nachos or falafel | no write | op=query | PASS |  |
| 3125 | D | how far is nairobi from tokyo | no write | op=None | PASS |  |
| 3126 | D | which is better, palak paneer or chow mein | no write | op=query | PASS |  |
| 3127 | D | how far is madrid from sao paulo | no write | op=None | PASS |  |
| 3128 | D | how far is boston from capetown | no write | op=None | PASS |  |
| 3129 | D | which is better, coleslaw or bruschetta | no write | op=query | PASS |  |
| 313 | A | my favorite cuisine is italian | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3130 | D | which is better, thai curry or lasagna | no write | op=query | PASS |  |
| 3131 | D | how far is casablanca from athens | no write | op=None | PASS |  |
| 3132 | D | which is better, jambalaya or polenta | no write | op=query | PASS |  |
| 3133 | D | how does dark matter work | no write | op=query | PASS |  |
| 3134 | D | how far is madrid from vienna | no write | op=None | PASS |  |
| 3135 | D | how far is casablanca from warsaw | no write | op=None | PASS |  |
| 3136 | D | which is better, idli or biryani | no write | op=query | PASS |  |
| 3137 | D | you remember my favorite show is sherlock | no write | op=query | PASS |  |
| 3138 | D | which is better, shepherd pie or ceviche | no write | op=query | PASS |  |
| 3139 | D | how far is rome from florence | no write | op=None | PASS |  |
| 314 | A | my favorite dessert is barfi | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3140 | D | which is better, polenta or paratha | no write | op=query | PASS |  |
| 3141 | D | which is better, tamale or curry | no write | op=query | PASS |  |
| 3142 | D | how far is bangkok from sao paulo | no write | op=None | PASS |  |
| 3143 | D | which is better, burger or gumbo | no write | op=query | PASS |  |
| 3144 | D | how far is rotterdam from bangkok | no write | op=None | PASS |  |
| 3145 | D | how far is lima from lagos | no write | op=None | PASS |  |
| 3146 | D | how far is montevideo from rotterdam | no write | op=None | PASS |  |
| 3147 | D | how far is buenos aires from nairobi | no write | op=None | PASS |  |
| 3148 | D | which is better, dosa or curry | no write | op=query | PASS |  |
| 3149 | D | which is better, calamari or tamale | no write | op=query | PASS |  |
| 315 | A | my favorite drink is sparkling water | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3150 | D | which is better, tacos or idli | no write | op=query | PASS |  |
| 3151 | D | how far is kathmandu from budapest | no write | op=None | PASS |  |
| 3152 | D | which is better, naan or bhel puri | no write | op=query | PASS |  |
| 3153 | D | which is better, gnocchi or kebabs | no write | op=query | PASS |  |
| 3154 | D | how far is vienna from sao paulo | no write | op=None | PASS |  |
| 3155 | D | how far is oslo from rio de janeiro | no write | op=None | PASS |  |
| 3156 | D | which is better, oysters or jambalaya | no write | op=query | PASS |  |
| 3157 | D | which is better, tacos or tamale | no write | op=query | PASS |  |
| 3158 | D | which is better, coleslaw or burrito | no write | op=query | PASS |  |
| 3159 | D | which is better, noodles or moussaka | no write | op=query | PASS |  |
| 316 | A | my favorite writer is aldous huxley | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3160 | D | how far is tokyo from seoul | no write | op=None | PASS |  |
| 3161 | D | how far is seoul from zurich | no write | op=None | PASS |  |
| 3162 | D | how far is caracas from delhi | no write | op=None | PASS |  |
| 3163 | D | how far is stockholm from copenhagen | no write | op=query | PASS |  |
| 3164 | D | you remember my favorite cuisine is turkish | no write | op=query | PASS |  |
| 3165 | D | which is better, korean bbq or burrito | no write | op=query | PASS |  |
| 3166 | D | which is better, onion rings or sandwich | no write | op=query | PASS |  |
| 3167 | D | how far is jakarta from manchester | no write | op=None | PASS |  |
| 3168 | D | which is better, noodles or ceviche | no write | op=query | PASS |  |
| 3169 | D | you remember my favorite cuisine is mediterranean | no write | op=query | PASS |  |
| 317 | A | my favorite game is satisfactory | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3170 | D | who wrote to kill a mockingbird | no write | op=None | PASS |  |
| 3171 | D | which is better, biryani or mac and cheese | no write | op=query | PASS |  |
| 3172 | D | how far is quito from copenhagen | no write | op=query | PASS |  |
| 3173 | D | how far is mexico city from seoul | no write | op=None | PASS |  |
| 3174 | D | how far is chennai from bangkok | no write | op=None | PASS |  |
| 3175 | D | which is better, ramen or ceviche | no write | op=query | PASS |  |
| 3176 | D | which is better, curry or burrito | no write | op=query | PASS |  |
| 3177 | D | which is better, nachos or bhel puri | no write | op=query | PASS |  |
| 3178 | D | how far is vienna from brussels | no write | op=None | PASS |  |
| 3179 | D | how far is dublin from dublin | no write | op=None | PASS |  |
| 318 | A | my favorite animal is kangaroo | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3180 | D | what do you think about study group | no write | op=None | PASS |  |
| 3181 | D | you remember my favorite city is warsaw | no write | op=query | PASS |  |
| 3182 | D | which is better, burger or hummus plate | no write | op=query | PASS |  |
| 3183 | D | how far is florence from oslo | no write | op=None | PASS |  |
| 3184 | D | which is better, ramen or falafel | no write | op=query | PASS |  |
| 3185 | D | which is better, calamari or pizza | no write | op=query | PASS |  |
| 3186 | D | which is better, guacamole or fried rice | no write | op=query | PASS |  |
| 3187 | D | you remember my favorite game is fire emblem | no write | op=query | PASS |  |
| 3188 | D | how far is bangkok from rome | no write | op=None | PASS |  |
| 3189 | D | how far is caracas from warsaw | no write | op=None | PASS |  |
| 319 | A | my favorite book is the alchemist | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3190 | D | which is better, oysters or tamale | no write | op=query | PASS |  |
| 3191 | D | how far is oslo from sao paulo | no write | op=None | PASS |  |
| 3192 | D | which is better, paella or pizza | no write | op=query | PASS |  |
| 3193 | D | which is better, samosa or fried rice | no write | op=query | PASS |  |
| 3194 | D | which is better, curry or ceviche | no write | op=query | PASS |  |
| 3195 | D | how far is chennai from dublin | no write | op=None | PASS |  |
| 3196 | D | who wrote brave new world | no write | op=None | PASS |  |
| 3197 | D | which is better, pasta or ratatouille | no write | op=query | PASS |  |
| 3198 | D | how far is cairo from sao paulo | no write | op=None | PASS |  |
| 3199 | D | how far is nairobi from montevideo | no write | op=None | PASS |  |
| 32 | A | my favorite food is risotto | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 320 | A | my favorite drink is cherry soda | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is cherry soda' | FAIL | store did not persist: status=needs_clarification present=False |
| 3200 | D | how far is melbourne from quito | no write | op=None | PASS |  |
| 3201 | D | which is better, burrito or mac and cheese | no write | op=query | PASS |  |
| 3202 | D | which is better, moussaka or sandwich | no write | op=query | PASS |  |
| 3203 | D | which is better, pierogi or butter chicken | no write | op=query | PASS |  |
| 3204 | D | which is better, hummus plate or waffles | no write | op=query | PASS |  |
| 3205 | D | you remember my favorite drink is coconut water | no write | op=query | PASS |  |
| 3206 | D | how far is manchester from lisbon | no write | op=None | PASS |  |
| 3207 | D | which is better, tacos or onion rings | no write | op=query | PASS |  |
| 3208 | D | how far is chennai from vienna | no write | op=None | PASS |  |
| 3209 | D | how far is mexico city from sao paulo | no write | op=None | PASS |  |
| 321 | A | i am from berlin | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 3210 | D | which is better, idli or empanadas | no write | op=query | PASS |  |
| 3211 | D | how far is lagos from budapest | no write | op=None | PASS |  |
| 3212 | D | which is better, polenta or burger | no write | op=query | PASS |  |
| 3213 | D | how far is dubai from seville | no write | op=None | PASS |  |
| 3214 | D | how far is oslo from madrid | no write | op=None | PASS |  |
| 3215 | D | which is better, pasta or korean bbq | no write | op=query | PASS |  |
| 3216 | D | how long does it take to design a logo | no write | op=None | PASS |  |
| 3217 | D | how far is lagos from rio de janeiro | no write | op=None | PASS |  |
| 3218 | D | which is better, noodles or banh mi | no write | op=query | PASS |  |
| 3219 | D | you remember my favorite drink is kombucha | no write | op=query | PASS |  |
| 322 | A | i am from milan | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 3220 | D | which is better, momos or chow mein | no write | op=query | PASS |  |
| 3221 | D | how far is cairo from rotterdam | no write | op=None | PASS |  |
| 3222 | D | which is better, risotto or samosa | no write | op=query | PASS |  |
| 3223 | D | how far is milan from mexico city | no write | op=None | PASS |  |
| 3224 | D | who wrote project hail mary | no write | op=query | PASS |  |
| 3225 | D | which is better, samosa or banh mi | no write | op=query | PASS |  |
| 3226 | D | which is better, gnocchi or poha | no write | op=query | PASS |  |
| 3227 | D | what does ikigai mean | no write | op=None | PASS |  |
| 3228 | D | which is better, shepherd pie or lasagna | no write | op=query | PASS |  |
| 3229 | D | how far is copenhagen from toronto | no write | op=query | PASS |  |
| 323 | A | my favorite movie is a quiet place | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite movie is A Quiet Place' | FAIL | store did not persist: status=needs_clarification present=False |
| 3230 | D | you remember my favorite writer is yann martel | no write | op=query | PASS |  |
| 3231 | D | how far is amsterdam from belfast | no write | op=None | PASS |  |
| 3232 | D | which is better, risotto or pho | no write | op=query | PASS |  |
| 3233 | D | how far is kathmandu from barcelona | no write | op=None | PASS |  |
| 3234 | D | which is better, momos or burger | no write | op=query | PASS |  |
| 3235 | D | how far is belfast from cairo | no write | op=None | PASS |  |
| 3236 | D | which is better, vindaloo or curry | no write | op=query | PASS |  |
| 3237 | D | which is better, korean bbq or hummus plate | no write | op=query | PASS |  |
| 3238 | D | you remember my favorite sport is diving | no write | op=query | PASS |  |
| 3239 | D | which is better, sandwich or pizza | no write | op=query | PASS |  |
| 324 | A | my favorite food is lasagna | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3240 | D | can you explain algorithms to me | no write | op=query | PASS |  |
| 3241 | D | how far is sao paulo from quito | no write | op=None | PASS |  |
| 3242 | D | how far is milan from capetown | no write | op=None | PASS |  |
| 3243 | D | what is the capital of bhutan | no write | op=None | PASS |  |
| 3244 | D | how far is casablanca from manchester | no write | op=None | PASS |  |
| 3245 | D | which is better, fried rice or gnocchi | no write | op=query | PASS |  |
| 3246 | D | which is better, pizza or banh mi | no write | op=query | PASS |  |
| 3247 | D | which is better, kebabs or banh mi | no write | op=query | PASS |  |
| 3248 | D | which is better, calamari or kebabs | no write | op=query | PASS |  |
| 3249 | D | which is better, gnocchi or curry | no write | op=query | PASS |  |
| 325 | A | my favorite book is where the crawdads sing | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3250 | D | how far is copenhagen from caracas | no write | op=query | PASS |  |
| 3251 | D | which is better, sandwich or noodles | no write | op=query | PASS |  |
| 3252 | D | how far is rio de janeiro from athens | no write | op=None | PASS |  |
| 3253 | D | which is better, calamari or hot pot | no write | op=query | PASS |  |
| 3254 | D | which is better, tacos or banh mi | no write | op=query | PASS |  |
| 3255 | D | which is better, onion rings or kebabs | no write | op=query | PASS |  |
| 3256 | D | how far is florence from venice | no write | op=None | PASS |  |
| 3257 | D | you remember my favorite book is moby dick | no write | op=query | PASS |  |
| 3258 | D | which is better, waffles or gyoza | no write | op=query | PASS |  |
| 3259 | D | which is better, pho or sandwich | no write | op=query | PASS |  |
| 326 | A | i am from montevideo | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 3260 | D | you remember my favorite animal is echidna | no write | op=query | PASS |  |
| 3261 | D | how far is stockholm from seville | no write | op=None | PASS |  |
| 3262 | D | how far is sao paulo from casablanca | no write | op=None | PASS |  |
| 3263 | D | which is better, kebabs or calamari | no write | op=query | PASS |  |
| 3264 | D | how far is seoul from hanoi | no write | op=None | PASS |  |
| 3265 | D | how far is rotterdam from stockholm | no write | op=None | PASS |  |
| 3266 | D | which is better, hummus plate or bhel puri | no write | op=query | PASS |  |
| 3267 | D | how far is budapest from vienna | no write | op=None | PASS |  |
| 3268 | D | you remember my favorite dessert is rasgulla | no write | op=query | PASS |  |
| 3269 | D | which is better, korean bbq or sushi | no write | op=query | PASS |  |
| 327 | A | my favorite subject is geography | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3270 | D | how far is belfast from rome | no write | op=None | PASS |  |
| 3271 | D | which is better, empanadas or poutine | no write | op=query | PASS |  |
| 3272 | D | what do you think about group project | no write | op=query | PASS |  |
| 3273 | D | which is better, onion rings or vindaloo | no write | op=query | PASS |  |
| 3274 | D | how does antibiotics work | no write | op=query | PASS |  |
| 3275 | D | which is better, tacos or gnocchi | no write | op=query | PASS |  |
| 3276 | D | which is better, lasagna or paella | no write | op=query | PASS |  |
| 3277 | D | how far is warsaw from brussels | no write | op=None | PASS |  |
| 3278 | D | how far is cardiff from milan | no write | op=None | PASS |  |
| 3279 | D | how far is prague from copenhagen | no write | op=query | PASS |  |
| 328 | A | my favorite dessert is cheesecake | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3280 | D | how far is brussels from hanoi | no write | op=None | PASS |  |
| 3281 | D | how far is stockholm from toronto | no write | op=None | PASS |  |
| 3282 | D | you remember my favorite subject is genetics | no write | op=query | PASS |  |
| 3283 | D | you remember my favorite cuisine is soul food | no write | op=query | PASS |  |
| 3284 | D | which is better, pancakes or lobster roll | no write | op=query | PASS |  |
| 3285 | D | how far is vienna from buenos aires | no write | op=None | PASS |  |
| 3286 | D | which is better, hot pot or fried rice | no write | op=query | PASS |  |
| 3287 | D | which is better, mac and cheese or samosa | no write | op=query | PASS |  |
| 3288 | D | how far is manchester from delhi | no write | op=None | PASS |  |
| 3289 | D | which is better, hummus plate or lobster roll | no write | op=query | PASS |  |
| 329 | A | my favorite city is amsterdam | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3290 | D | which is better, banh mi or falafel | no write | op=query | PASS |  |
| 3291 | D | how far is amsterdam from mumbai | no write | op=None | PASS |  |
| 3292 | D | you remember my favorite movie is a quiet place | no write | op=query | PASS |  |
| 3293 | D | which is better, risotto or pasta | no write | op=query | PASS |  |
| 3294 | D | how far is helsinki from paris | no write | op=None | PASS |  |
| 3295 | D | you remember my favorite dessert is pecan pie | no write | op=query | PASS |  |
| 3296 | D | which is better, lobster roll or nachos | no write | op=query | PASS |  |
| 3297 | D | which is better, falafel or coleslaw | no write | op=query | PASS |  |
| 3298 | D | which is better, sushi or dosa | no write | op=query | PASS |  |
| 3299 | D | how far is berlin from mexico city | no write | op=None | PASS |  |
| 33 | A | my favorite city is belfast | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 330 | A | my pet's name is pebbles | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3300 | D | how far is stockholm from capetown | no write | op=None | PASS |  |
| 3301 | D | which is better, moussaka or moussaka | no write | op=query | PASS |  |
| 3302 | D | how far is buenos aires from cairo | no write | op=None | PASS |  |
| 3303 | D | which is better, thai curry or hot pot | no write | op=query | PASS |  |
| 3304 | D | how far is tokyo from oslo | no write | op=None | PASS |  |
| 3305 | D | which is better, hot pot or lasagna | no write | op=query | PASS |  |
| 3306 | D | how far is edinburgh from lima | no write | op=None | PASS |  |
| 3307 | D | how far is milan from oslo | no write | op=None | PASS |  |
| 3308 | D | which is better, paratha or chow mein | no write | op=query | PASS |  |
| 3309 | D | you remember my favorite dessert is lamington | no write | op=query | PASS |  |
| 331 | A | my favorite color is chestnut | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3310 | D | can you explain dna to me | no write | op=query | PASS |  |
| 3311 | D | which is better, hummus plate or hot pot | no write | op=query | PASS |  |
| 3312 | D | which is better, moussaka or burrito | no write | op=query | PASS |  |
| 3313 | D | which is better, ramen or calamari | no write | op=query | PASS |  |
| 3314 | D | how far is melbourne from kyoto | no write | op=None | PASS |  |
| 3315 | D | which is better, dumplings or dumplings | no write | op=query | PASS |  |
| 3316 | D | where can i buy printer | no write | op=query | PASS |  |
| 3317 | D | which is better, fried rice or calamari | no write | op=query | PASS |  |
| 3318 | D | what is the capital of spain | no write | op=None | PASS |  |
| 3319 | D | which is better, lasagna or gyoza | no write | op=query | PASS |  |
| 332 | A | my favorite music is rockabilly | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3320 | D | which is better, pasta or bhel puri | no write | op=query | PASS |  |
| 3321 | D | you remember my favorite book is the sound and the fury | no write | op=query | PASS |  |
| 3322 | D | how far is bogota from rotterdam | no write | op=None | PASS |  |
| 3323 | D | how far is paris from santiago | no write | op=None | PASS |  |
| 3324 | D | which is better, lobster roll or pho | no write | op=query | PASS |  |
| 3325 | D | which is better, lobster roll or guacamole | no write | op=query | PASS |  |
| 3326 | D | which is better, ceviche or calamari | no write | op=query | PASS |  |
| 3327 | D | how far is sao paulo from florence | no write | op=None | PASS |  |
| 3328 | D | how far is copenhagen from barcelona | no write | op=query | PASS |  |
| 3329 | D | how far is rio de janeiro from toronto | no write | op=None | PASS |  |
| 333 | A | my favorite movie is whiplash | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 3330 | D | you remember my favorite movie is schindler list | no write | op=query | PASS |  |
| 3331 | D | how far is rotterdam from manila | no write | op=None | PASS |  |
| 3332 | D | how far is cardiff from delhi | no write | op=None | PASS |  |
| 3333 | D | you remember my favorite music is gospel | no write | op=query | PASS |  |
| 3334 | D | which is better, ratatouille or empanadas | no write | op=query | PASS |  |
| 3335 | D | how far is manila from bogota | no write | op=None | PASS |  |
| 3336 | D | which is better, poha or lobster roll | no write | op=query | PASS |  |
| 3337 | D | how far is mumbai from barcelona | no write | op=None | PASS |  |
| 3338 | D | how far is seville from copenhagen | no write | op=query | PASS |  |
| 3339 | D | where can i buy guitar | no write | op=query | PASS |  |
| 334 | A | my favorite game is hellblade | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3340 | D | which is better, onion rings or curry | no write | op=query | PASS |  |
| 3341 | D | you remember my favorite sport is pole vault | no write | op=query | PASS |  |
| 3342 | D | which is better, burrito or ratatouille | no write | op=query | PASS |  |
| 3343 | D | how far is jakarta from chennai | no write | op=None | PASS |  |
| 3344 | D | which is better, oysters or tacos | no write | op=query | PASS |  |
| 3345 | D | how far is hanoi from cardiff | no write | op=None | PASS |  |
| 3346 | D | how far is lima from hanoi | no write | op=None | PASS |  |
| 3347 | D | how far is hanoi from berlin | no write | op=None | PASS |  |
| 3348 | D | which is better, chow mein or dosa | no write | op=query | PASS |  |
| 3349 | D | which is better, pancakes or sushi | no write | op=query | PASS |  |
| 335 | A | my favorite game is breath of the wild | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3350 | D | which is better, bhel puri or tamale | no write | op=query | PASS |  |
| 3351 | D | when was unicef founded | no write | op=None | PASS |  |
| 3352 | D | you remember my favorite music is hip hop | no write | op=query | PASS |  |
| 3353 | D | which is better, fried rice or palak paneer | no write | op=query | PASS |  |
| 3354 | D | you remember my favorite show is the mandalorian | no write | op=query | PASS |  |
| 3355 | D | how far is brussels from buenos aires | no write | op=None | PASS |  |
| 3356 | D | which is better, guacamole or naan | no write | op=query | PASS |  |
| 3357 | D | how far is milan from zurich | no write | op=None | PASS |  |
| 3358 | D | can you explain cryptocurrency to me | no write | op=query | PASS |  |
| 3359 | D | which is better, tacos or gyoza | no write | op=query | PASS |  |
| 336 | A | my favorite color is denim | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3360 | D | which is better, tacos or pierogi | no write | op=query | PASS |  |
| 3361 | D | which is better, ceviche or risotto | no write | op=query | PASS |  |
| 3362 | D | how far is quito from amsterdam | no write | op=None | PASS |  |
| 3363 | D | how far is zurich from boston | no write | op=None | PASS |  |
| 3364 | D | how long does it take to rake leaves | no write | op=None | PASS |  |
| 3365 | D | how far is boston from edinburgh | no write | op=None | PASS |  |
| 3366 | D | how far is mexico city from dubai | no write | op=None | PASS |  |
| 3367 | D | which is better, hummus plate or kebabs | no write | op=query | PASS |  |
| 3368 | D | which is better, paratha or gumbo | no write | op=query | PASS |  |
| 3369 | D | which is better, naan or lobster roll | no write | op=query | PASS |  |
| 337 | A | my favorite game is fortnite | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 3370 | D | which is better, korean bbq or sandwich | no write | op=query | PASS |  |
| 3371 | D | how far is melbourne from bogota | no write | op=None | PASS |  |
| 3372 | D | which is better, momos or oysters | no write | op=query | PASS |  |
| 3373 | D | you remember my favorite dessert is ice cream | no write | op=query | PASS |  |
| 3374 | D | which is better, pierogi or curry | no write | op=query | PASS |  |
| 3375 | D | which is better, risotto or hummus plate | no write | op=query | PASS |  |
| 3376 | D | how far is rio de janeiro from jakarta | no write | op=None | PASS |  |
| 3377 | D | how far is athens from quito | no write | op=None | PASS |  |
| 3378 | D | which is better, risotto or thai curry | no write | op=query | PASS |  |
| 3379 | D | which is better, dosa or burger | no write | op=query | PASS |  |
| 338 | A | i work as a nurse | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 3380 | D | which is better, thai curry or paella | no write | op=query | PASS |  |
| 3381 | D | how far is rio de janeiro from milan | no write | op=None | PASS |  |
| 3382 | D | how far is manchester from casablanca | no write | op=None | PASS |  |
| 3383 | D | which is better, gyoza or oysters | no write | op=query | PASS |  |
| 3384 | D | which is better, falafel or ratatouille | no write | op=query | PASS |  |
| 3385 | D | you remember my favorite hobby is crosswords | no write | op=query | PASS |  |
| 3386 | D | which is better, butter chicken or onion rings | no write | op=query | PASS |  |
| 3387 | D | you remember my favorite movie is the pianist | no write | op=query | PASS |  |
| 3388 | D | how far is chennai from belfast | no write | op=None | PASS |  |
| 3389 | D | which is better, pho or butter chicken | no write | op=query | PASS |  |
| 339 | A | my favorite drink is ginger ale | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3390 | D | how far is manchester from belfast | no write | op=None | PASS |  |
| 3391 | D | give me advice about newsletter | no write | op=store conf=1.0 | FAIL | no-write message produced a write: op=store fact='Newsletter' |
| 3392 | D | how far is singapore from zurich | no write | op=None | PASS |  |
| 3393 | D | you remember my favorite subject is software testing | no write | op=query | PASS |  |
| 3394 | D | which is better, butter chicken or ramen | no write | op=query | PASS |  |
| 3395 | D | how far is paris from helsinki | no write | op=None | PASS |  |
| 3396 | D | how far is caracas from singapore | no write | op=None | PASS |  |
| 3397 | D | where can i buy a hard drive | no write | op=query | PASS |  |
| 3398 | D | how far is santiago from cairo | no write | op=None | PASS |  |
| 3399 | D | is oysters healthy | no write | op=None | PASS |  |
| 34 | A | my favorite cuisine is cantonese | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 340 | A | i work as a accountant | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 3400 | D | which is better, lobster roll or pancakes | no write | op=query | PASS |  |
| 3401 | D | when was arm founded | no write | op=None | PASS |  |
| 3402 | D | how far is quito from warsaw | no write | op=None | PASS |  |
| 3403 | D | which is better, fried rice or pizza | no write | op=query | PASS |  |
| 3404 | D | what is the weather like in cairo | no write | op=None | PASS |  |
| 3405 | D | which is better, gnocchi or pizza | no write | op=query | PASS |  |
| 3406 | D | how far is manila from zurich | no write | op=None | PASS |  |
| 3407 | D | how far is brussels from seville | no write | op=None | PASS |  |
| 3408 | D | how far is bogota from rome | no write | op=None | PASS |  |
| 3409 | D | what is the immune system | no write | op=None | PASS |  |
| 341 | A | my pet's name is sushi | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3410 | D | which is better, sandwich or empanadas | no write | op=query | PASS |  |
| 3411 | D | which is better, banh mi or gumbo | no write | op=query | PASS |  |
| 3412 | D | how far is vienna from zurich | no write | op=None | PASS |  |
| 3413 | D | which is better, poha or dumplings | no write | op=query | PASS |  |
| 3414 | D | you remember my favorite music is celtic | no write | op=query | PASS |  |
| 3415 | D | which is better, idli or calamari | no write | op=query | PASS |  |
| 3416 | D | which is better, chow mein or waffles | no write | op=query | PASS |  |
| 3417 | D | which is better, gyoza or bhel puri | no write | op=query | PASS |  |
| 3418 | D | how far is berlin from rio de janeiro | no write | op=None | PASS |  |
| 3419 | D | which is better, burrito or dumplings | no write | op=query | PASS |  |
| 342 | A | my favorite city is seoul | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3420 | D | how far is lisbon from kyoto | no write | op=None | PASS |  |
| 3421 | D | which is better, ratatouille or kebabs | no write | op=query | PASS |  |
| 3422 | D | which is better, pizza or risotto | no write | op=query | PASS |  |
| 3423 | D | how far is mexico city from singapore | no write | op=None | PASS |  |
| 3424 | D | how far is cairo from buenos aires | no write | op=None | PASS |  |
| 3425 | D | you remember my favorite city is dubai | no write | op=query | PASS |  |
| 3426 | D | how far is delhi from edinburgh | no write | op=None | PASS |  |
| 3427 | D | how long does it take to set up a tent | no write | op=None | PASS |  |
| 3428 | D | give me advice about insurance plan | no write | op=query | PASS |  |
| 3429 | D | how far is cardiff from lisbon | no write | op=None | PASS |  |
| 343 | A | my favorite game is subnautica | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3430 | D | which is better, lobster roll or burger | no write | op=query | PASS |  |
| 3431 | D | how far is seoul from kathmandu | no write | op=None | PASS |  |
| 3432 | D | how far is dublin from jakarta | no write | op=None | PASS |  |
| 3433 | D | when was square enix founded | no write | op=None | PASS |  |
| 3434 | D | you remember my favorite food is pierogi | no write | op=query | PASS |  |
| 3435 | D | how far is seoul from quito | no write | op=None | PASS |  |
| 3436 | D | which is better, noodles or jambalaya | no write | op=query | PASS |  |
| 3437 | D | how far is florence from rome | no write | op=None | PASS |  |
| 3438 | D | which is better, thai curry or naan | no write | op=query | PASS |  |
| 3439 | D | which is better, naan or paratha | no write | op=query | PASS |  |
| 344 | A | my favorite fruit is papaya | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3440 | D | which is better, waffles or hummus plate | no write | op=query | PASS |  |
| 3441 | D | you remember my favorite fruit is orange | no write | op=query | PASS |  |
| 3442 | D | how far is mumbai from jakarta | no write | op=None | PASS |  |
| 3443 | D | how far is cairo from venice | no write | op=None | PASS |  |
| 3444 | D | how far is florence from caracas | no write | op=None | PASS |  |
| 3445 | D | which is better, hot pot or gnocchi | no write | op=query | PASS |  |
| 3446 | D | you remember my favorite cuisine is northern indian | no write | op=query | PASS |  |
| 3447 | D | how does devops work | no write | op=query | PASS |  |
| 3448 | D | which is better, thai curry or burger | no write | op=query | PASS |  |
| 3449 | D | how far is manila from toronto | no write | op=None | PASS |  |
| 345 | A | my favorite show is the good place | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3450 | D | which is better, gyoza or biryani | no write | op=query | PASS |  |
| 3451 | D | what does halcyon mean | no write | op=None | PASS |  |
| 3452 | D | why is the sky blue | no write | op=None | PASS |  |
| 3453 | D | you remember my favorite movie is the two towers | no write | op=query | PASS |  |
| 3454 | D | how far is quito from toronto | no write | op=None | PASS |  |
| 3455 | D | which is better, lasagna or polenta | no write | op=query | PASS |  |
| 3456 | D | how far is rome from copenhagen | no write | op=query | PASS |  |
| 3457 | D | how far is paris from vienna | no write | op=None | PASS |  |
| 3458 | D | how far is madrid from chennai | no write | op=None | PASS |  |
| 3459 | D | which is better, lobster roll or samosa | no write | op=query | PASS |  |
| 346 | A | my favorite subject is criminology | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3460 | D | what time is it in brussels | no write | op=None | PASS |  |
| 3461 | D | how far is toronto from hanoi | no write | op=None | PASS |  |
| 3462 | D | which is better, pierogi or hot pot | no write | op=query | PASS |  |
| 3463 | D | how long does it take to patch drywall | no write | op=None | PASS |  |
| 3464 | D | how far is santiago from seville | no write | op=None | PASS |  |
| 3465 | D | which is better, dosa or kebabs | no write | op=query | PASS |  |
| 3466 | D | which is better, gyoza or gnocchi | no write | op=query | PASS |  |
| 3467 | D | which is better, kebabs or waffles | no write | op=query | PASS |  |
| 3468 | D | how far is vienna from venice | no write | op=None | PASS |  |
| 3469 | D | how far is budapest from athens | no write | op=None | PASS |  |
| 347 | A | my favorite writer is agatha christie | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3470 | D | how far is florence from mexico city | no write | op=None | PASS |  |
| 3471 | D | how far is sao paulo from kyoto | no write | op=None | PASS |  |
| 3472 | D | how far is montevideo from caracas | no write | op=None | PASS |  |
| 3473 | D | how far is hanoi from florence | no write | op=None | PASS |  |
| 3474 | D | is gumbo healthy | no write | op=None | PASS |  |
| 3475 | D | how far is warsaw from oslo | no write | op=None | PASS |  |
| 3476 | D | how far is montevideo from helsinki | no write | op=None | PASS |  |
| 3477 | D | which is better, naan or onion rings | no write | op=query | PASS |  |
| 3478 | D | how far is sao paulo from caracas | no write | op=None | PASS |  |
| 3479 | D | which is better, risotto or paella | no write | op=query | PASS |  |
| 348 | A | my favorite fruit is melon | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3480 | D | how far is sao paulo from manchester | no write | op=None | PASS |  |
| 3481 | D | which is better, pizza or butter chicken | no write | op=query | PASS |  |
| 3482 | D | which is better, chow mein or guacamole | no write | op=query | PASS |  |
| 3483 | D | which is better, lobster roll or lasagna | no write | op=query | PASS |  |
| 3484 | D | which is better, ceviche or kebabs | no write | op=query | PASS |  |
| 3485 | D | which is better, pizza or dumplings | no write | op=query | PASS |  |
| 3486 | D | how far is rome from brussels | no write | op=None | PASS |  |
| 3487 | D | which is better, banh mi or ramen | no write | op=query | PASS |  |
| 3488 | D | which is better, nachos or gnocchi | no write | op=query | PASS |  |
| 3489 | D | which is better, gyoza or jambalaya | no write | op=query | PASS |  |
| 349 | A | my favorite city is manila | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3490 | D | which is better, polenta or risotto | no write | op=query | PASS |  |
| 3491 | D | is falafel healthy | no write | op=None | PASS |  |
| 3492 | D | how far is warsaw from warsaw | no write | op=None | PASS |  |
| 3493 | D | which is better, nachos or dumplings | no write | op=query | PASS |  |
| 3494 | D | which is better, naan or chow mein | no write | op=query | PASS |  |
| 3495 | D | how far is zurich from rio de janeiro | no write | op=None | PASS |  |
| 3496 | D | how long does it take to start a garden | no write | op=None | PASS |  |
| 3497 | D | which is better, ratatouille or pierogi | no write | op=query | PASS |  |
| 3498 | D | how far is capetown from casablanca | no write | op=None | PASS |  |
| 3499 | D | how far is capetown from cairo | no write | op=None | PASS |  |
| 35 | A | my favorite sport is basketball | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 350 | A | my favorite book is crime and punishment | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3500 | D | which is better, burrito or calamari | no write | op=query | PASS |  |
| 3501 | D | how far is chennai from boston | no write | op=None | PASS |  |
| 3502 | D | how far is mexico city from rotterdam | no write | op=None | PASS |  |
| 3503 | D | where can i buy an e-reader | no write | op=query | PASS |  |
| 3504 | D | how far is oslo from seville | no write | op=None | PASS |  |
| 3505 | D | you remember my favorite subject is database systems | no write | op=query | PASS |  |
| 3506 | D | how far is helsinki from dubai | no write | op=None | PASS |  |
| 3507 | D | which is better, hot pot or shepherd pie | no write | op=query | PASS |  |
| 3508 | D | which is better, sandwich or gyoza | no write | op=query | PASS |  |
| 3509 | D | which is better, lasagna or hot pot | no write | op=query | PASS |  |
| 351 | A | i work as a sculptor | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 3510 | D | which is better, sandwich or tacos | no write | op=query | PASS |  |
| 3511 | D | when was huawei founded | no write | op=None | PASS |  |
| 3512 | D | give me advice about social media plan | no write | op=None | PASS |  |
| 3513 | D | you remember my favorite cuisine is tamil | no write | op=query | PASS |  |
| 3514 | D | you remember my favorite fruit is soursop | no write | op=query | PASS |  |
| 3515 | D | how far is boston from singapore | no write | op=None | PASS |  |
| 3516 | D | which is better, risotto or gnocchi | no write | op=query | PASS |  |
| 3517 | D | how far is rome from boston | no write | op=None | PASS |  |
| 3518 | D | how far is quito from bangkok | no write | op=None | PASS |  |
| 3519 | D | how far is madrid from casablanca | no write | op=None | PASS |  |
| 352 | A | my favorite city is venice | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3520 | D | what does epiphany mean | no write | op=None | PASS |  |
| 3521 | D | which is better, burrito or chow mein | no write | op=query | PASS |  |
| 3522 | D | how far is bangkok from dublin | no write | op=None | PASS |  |
| 3523 | D | who wrote normal people | no write | op=None | PASS |  |
| 3524 | D | how far is seoul from barcelona | no write | op=None | PASS |  |
| 3525 | D | how far is montevideo from cairo | no write | op=None | PASS |  |
| 3526 | D | which is better, gnocchi or banh mi | no write | op=query | PASS |  |
| 3527 | D | how far is berlin from manchester | no write | op=None | PASS |  |
| 3528 | D | which is better, pierogi or vindaloo | no write | op=query | PASS |  |
| 3529 | D | you remember my favorite hobby is bird watching | no write | op=query | PASS |  |
| 353 | A | my favorite fruit is passion fruit | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3530 | D | which is better, dumplings or biryani | no write | op=query | PASS |  |
| 3531 | D | how far is madrid from singapore | no write | op=None | PASS |  |
| 3532 | D | which is better, butter chicken or banh mi | no write | op=query | PASS |  |
| 3533 | D | you remember my favorite food is poutine | no write | op=query | PASS |  |
| 3534 | D | which is better, butter chicken or gnocchi | no write | op=query | PASS |  |
| 3535 | D | how far is tokyo from boston | no write | op=None | PASS |  |
| 3536 | D | how far is casablanca from bangkok | no write | op=None | PASS |  |
| 3537 | D | you remember my favorite book is to kill a mockingbird | no write | op=query | PASS |  |
| 3538 | D | which is better, kebabs or gnocchi | no write | op=query | PASS |  |
| 3539 | D | how does compilers work | no write | op=query | PASS |  |
| 354 | A | i am from venice | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 3540 | D | how far is buenos aires from barcelona | no write | op=None | PASS |  |
| 3541 | D | you remember my favorite dessert is beignets | no write | op=query | PASS |  |
| 3542 | D | which is better, shepherd pie or empanadas | no write | op=query | PASS |  |
| 3543 | D | which is better, onion rings or bruschetta | no write | op=query | PASS |  |
| 3544 | D | which is better, gnocchi or vindaloo | no write | op=query | PASS |  |
| 3545 | D | which is better, mac and cheese or tacos | no write | op=query | PASS |  |
| 3546 | D | how far is mexico city from cardiff | no write | op=None | PASS |  |
| 3547 | D | which is better, pho or burrito | no write | op=query | PASS |  |
| 3548 | D | which is better, pasta or falafel | no write | op=query | PASS |  |
| 3549 | D | how far is dubai from rome | no write | op=None | PASS |  |
| 355 | A | my favorite city is madrid | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3550 | D | how far is seville from budapest | no write | op=None | PASS |  |
| 3551 | D | how far is stockholm from santiago | no write | op=None | PASS |  |
| 3552 | D | how far is rio de janeiro from seville | no write | op=None | PASS |  |
| 3553 | D | you remember my favorite cuisine is moroccan | no write | op=query | PASS |  |
| 3554 | D | how far is rome from cardiff | no write | op=None | PASS |  |
| 3555 | D | which is better, pancakes or biryani | no write | op=query | PASS |  |
| 3556 | D | which is better, samosa or burger | no write | op=query | PASS |  |
| 3557 | D | you remember my favorite city is toronto | no write | op=query | PASS |  |
| 3558 | D | how far is budapest from dubai | no write | op=None | PASS |  |
| 3559 | D | how far is paris from paris | no write | op=None | PASS |  |
| 356 | A | my favorite drink is hibiscus tea | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is hibiscus tea' | FAIL | store did not persist: status=needs_clarification present=False |
| 3560 | D | which is better, biryani or gnocchi | no write | op=query | PASS |  |
| 3561 | D | how far is manila from santiago | no write | op=None | PASS |  |
| 3562 | D | which is better, lobster roll or tacos | no write | op=query | PASS |  |
| 3563 | D | how far is quito from rome | no write | op=None | PASS |  |
| 3564 | D | which is better, lasagna or lobster roll | no write | op=query | PASS |  |
| 3565 | D | you remember my favorite hobby is card games | no write | op=query | PASS |  |
| 3566 | D | which is better, gumbo or burger | no write | op=query | PASS |  |
| 3567 | D | how far is nairobi from stockholm | no write | op=None | PASS |  |
| 3568 | D | when was rockstar founded | no write | op=None | PASS |  |
| 3569 | D | give me advice about research paper | no write | op=store conf=1.0 | FAIL | no-write message produced a write: op=store fact='I need advice on a research paper' |
| 357 | A | my favorite writer is emily bronte | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite writer is Emily Bronté' | FAIL | store did not persist: status=needs_clarification present=False |
| 3570 | D | you remember my favorite animal is butterfly | no write | op=query | PASS |  |
| 3571 | D | how far is caracas from montevideo | no write | op=None | PASS |  |
| 3572 | D | which is better, burger or ratatouille | no write | op=query | PASS |  |
| 3573 | D | which is better, thai curry or dosa | no write | op=query | PASS |  |
| 3574 | D | how far is manchester from edinburgh | no write | op=None | PASS |  |
| 3575 | D | which is better, lobster roll or hot pot | no write | op=query | PASS |  |
| 3576 | D | which is better, biryani or momos | no write | op=query | PASS |  |
| 3577 | D | how far is oslo from jakarta | no write | op=None | PASS |  |
| 3578 | D | how far is boston from berlin | no write | op=None | PASS |  |
| 3579 | D | which is better, empanadas or thai curry | no write | op=query | PASS |  |
| 358 | A | my favorite sport is wrestling | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3580 | D | how far is paris from chennai | no write | op=None | PASS |  |
| 3581 | D | which is better, tacos or shepherd pie | no write | op=query | PASS |  |
| 3582 | D | which is better, biryani or sandwich | no write | op=query | PASS |  |
| 3583 | D | which is better, empanadas or samosa | no write | op=query | PASS |  |
| 3584 | D | which is better, fried rice or ceviche | no write | op=query | PASS |  |
| 3585 | D | how far is barcelona from manchester | no write | op=None | PASS |  |
| 3586 | D | which is better, kebabs or kebabs | no write | op=query | PASS |  |
| 3587 | D | how far is edinburgh from santiago | no write | op=None | PASS |  |
| 3588 | D | how far is hanoi from milan | no write | op=None | PASS |  |
| 3589 | D | you remember my favorite food is palak paneer | no write | op=query | PASS |  |
| 359 | A | my favorite sport is gymnastics | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3590 | D | how far is rotterdam from belfast | no write | op=None | PASS |  |
| 3591 | D | which is better, butter chicken or coleslaw | no write | op=query | PASS |  |
| 3592 | D | which is better, biryani or onion rings | no write | op=query | PASS |  |
| 3593 | D | how far is casablanca from lagos | no write | op=None | PASS |  |
| 3594 | D | you remember my favorite writer is george orwell | no write | op=query | PASS |  |
| 3595 | D | which is better, gyoza or korean bbq | no write | op=query | PASS |  |
| 3596 | D | how far is lisbon from jakarta | no write | op=None | PASS |  |
| 3597 | D | how far is milan from venice | no write | op=None | PASS |  |
| 3598 | D | which is better, samosa or onion rings | no write | op=query | PASS |  |
| 3599 | D | which is better, pancakes or risotto | no write | op=query | PASS |  |
| 36 | A | my favorite book is the secret history | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 360 | A | i am from kathmandu | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 3600 | D | which is better, bhel puri or korean bbq | no write | op=query | PASS |  |
| 3601 | D | how does diffraction work | no write | op=query | PASS |  |
| 3602 | D | which is better, moussaka or momos | no write | op=query | PASS |  |
| 3603 | D | how far is kathmandu from cairo | no write | op=None | PASS |  |
| 3604 | D | which is better, curry or curry | no write | op=query | PASS |  |
| 3605 | D | which is better, bruschetta or idli | no write | op=query | PASS |  |
| 3606 | D | how far is toronto from rotterdam | no write | op=None | PASS |  |
| 3607 | D | which is better, vindaloo or pho | no write | op=query | PASS |  |
| 3608 | D | how far is madrid from delhi | no write | op=None | PASS |  |
| 3609 | D | which is better, poha or pierogi | no write | op=query | PASS |  |
| 361 | A | my favorite subject is geology | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3610 | D | which is better, bhel puri or fried rice | no write | op=query | PASS |  |
| 3611 | D | how far is sao paulo from boston | no write | op=None | PASS |  |
| 3612 | D | which is better, shepherd pie or gumbo | no write | op=query | PASS |  |
| 3613 | D | how far is barcelona from athens | no write | op=None | PASS |  |
| 3614 | D | which is better, onion rings or thai curry | no write | op=query | PASS |  |
| 3615 | D | how far is bogota from sao paulo | no write | op=None | PASS |  |
| 3616 | D | how far is rotterdam from cairo | no write | op=None | PASS |  |
| 3617 | D | when was ubisoft founded | no write | op=None | PASS |  |
| 3618 | D | which is better, sushi or moussaka | no write | op=query | PASS |  |
| 3619 | D | how far is brussels from lisbon | no write | op=None | PASS |  |
| 362 | A | my pet's name is lucy | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3620 | D | which is better, curry or korean bbq | no write | op=query | PASS |  |
| 3621 | D | which is better, shepherd pie or hot pot | no write | op=query | PASS |  |
| 3622 | D | which is better, gnocchi or hot pot | no write | op=query | PASS |  |
| 3623 | D | which is better, hot pot or ramen | no write | op=query | PASS |  |
| 3624 | D | you remember my favorite drink is ginger ale | no write | op=query | PASS |  |
| 3625 | D | how far is kyoto from boston | no write | op=None | PASS |  |
| 3626 | D | you remember my favorite color is lilac | no write | op=query | PASS |  |
| 3627 | D | how far is mumbai from copenhagen | no write | op=query | PASS |  |
| 3628 | D | which is better, palak paneer or empanadas | no write | op=query | PASS |  |
| 3629 | D | which is better, mac and cheese or falafel | no write | op=query | PASS |  |
| 363 | A | i am from melbourne | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 3630 | D | which is better, poha or tamale | no write | op=query | PASS |  |
| 3631 | D | how far is lisbon from delhi | no write | op=None | PASS |  |
| 3632 | D | you remember my favorite color is olive | no write | op=query | PASS |  |
| 3633 | D | how far is stockholm from montevideo | no write | op=None | PASS |  |
| 3634 | D | which is better, empanadas or risotto | no write | op=query | PASS |  |
| 3635 | D | you remember my favorite book is the name of the wind | no write | op=query | PASS |  |
| 3636 | D | which is better, guacamole or pasta | no write | op=query | PASS |  |
| 3637 | D | who wrote 1984 | no write | op=None | PASS |  |
| 3638 | D | how far is brussels from florence | no write | op=None | PASS |  |
| 3639 | D | how far is capetown from stockholm | no write | op=None | PASS |  |
| 364 | A | my favorite color is sapphire | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 3640 | D | how far is toronto from santiago | no write | op=None | PASS |  |
| 3641 | D | which is better, bruschetta or butter chicken | no write | op=query | PASS |  |
| 3642 | D | which is better, sushi or pasta | no write | op=query | PASS |  |
| 3643 | D | how far is seoul from lima | no write | op=None | PASS |  |
| 3644 | D | which is better, chow mein or sushi | no write | op=query | PASS |  |
| 3645 | D | which is better, pierogi or lasagna | no write | op=query | PASS |  |
| 3646 | D | which is better, butter chicken or tamale | no write | op=query | PASS |  |
| 3647 | D | how far is rotterdam from dubai | no write | op=None | PASS |  |
| 3648 | D | how far is toronto from milan | no write | op=None | PASS |  |
| 3649 | D | how far is boston from copenhagen | no write | op=query | PASS |  |
| 365 | A | my favorite city is jakarta | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3650 | E | recap what we discussed about study group | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3651 | E | what did we talk about regarding database migration | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3652 | E | anything from our chat about job interview | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3653 | E | did we work on side hustle together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3654 | E | remind me what we planned for research internship | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3655 | E | what did we talk about regarding language learning | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3656 | E | did we work on podcast idea together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3657 | E | anything from our chat about painting class | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3658 | E | remind me what we planned for machine learning model | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3659 | E | remind me what we planned for performance tuning | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 366 | A | my favorite fruit is custard apple | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3660 | E | did we work on youtube channel together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3661 | E | what did we talk about regarding start-up pitch | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3662 | E | anything from our chat about api integration | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3663 | E | what did we talk about regarding budget plan | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3664 | E | did we work on twitch stream together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3665 | E | anything from our chat about performance tuning | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3666 | E | remind me what we planned for api integration | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3667 | E | recap what we discussed about start-up pitch | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3668 | E | what did we talk about regarding python project | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3669 | E | anything from our chat about kitchen renovation | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 367 | A | my favorite show is arcane | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite show is arcane' | FAIL | store did not persist: status=needs_clarification present=False |
| 3670 | E | what did we talk about regarding garden layout | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3671 | E | anything from our chat about business plan | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3672 | E | anything from our chat about code refactor | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3673 | E | remind me what we planned for branding | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3674 | E | recap what we discussed about fitness routine | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3675 | E | what did we talk about regarding painting class | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3676 | E | what did we talk about regarding game jam | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3677 | E | remind me what we planned for painting class | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3678 | E | anything from our chat about youtube channel | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3679 | E | did we work on salary negotiation together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 368 | A | my favorite movie is the godfather | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3680 | E | anything from our chat about visa process | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3681 | E | did we work on job interview together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3682 | E | did we work on data analysis project together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3683 | E | remind me what we planned for marathon training | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3684 | E | what did we talk about regarding science fair | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3685 | E | anything from our chat about travel itinerary | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3686 | E | recap what we discussed about insurance plan | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3687 | E | did we work on exam preparation together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3688 | E | what did we talk about regarding cooking class | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3689 | E | what did we talk about regarding photography trip | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 369 | A | my favorite food is oysters | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3690 | E | what did we talk about regarding api integration | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3691 | E | anything from our chat about research internship | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3692 | E | did we work on social media plan together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3693 | E | did we work on internship application together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3694 | E | recap what we discussed about kitchen renovation | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3695 | E | remind me what we planned for fitness routine | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3696 | E | what did we talk about regarding marathon training | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3697 | E | remind me what we planned for side hustle | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3698 | E | remind me what we planned for garden layout | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3699 | E | did we work on marathon training together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 37 | A | my favorite book is war and peace | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 370 | A | my favorite dessert is macaron tower | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3700 | E | anything from our chat about database migration | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3701 | E | did we work on movie night together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3702 | E | anything from our chat about c program | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3703 | E | what did we talk about regarding movie night | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3704 | E | remind me what we planned for c program | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3705 | E | remind me what we planned for hackathon | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3706 | E | recap what we discussed about movie night | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3707 | E | anything from our chat about marathon training | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3708 | E | what did we talk about regarding pet adoption | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3709 | E | anything from our chat about game jam | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 371 | A | my favorite show is severance | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3710 | E | remind me what we planned for game jam | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3711 | E | recap what we discussed about travel itinerary | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3712 | E | did we work on language learning together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3713 | E | anything from our chat about debate prep | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3714 | E | what did we talk about regarding side hustle | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3715 | E | recap what we discussed about presentation | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3716 | E | remind me what we planned for presentation | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3717 | E | what did we talk about regarding fitness routine | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3718 | E | did we work on science fair together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3719 | E | anything from our chat about research paper | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 372 | A | my favorite animal is wombat | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3720 | E | remind me what we planned for bug hunting | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3721 | E | recap what we discussed about twitch stream | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3722 | E | remind me what we planned for visa process | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3723 | E | remind me what we planned for tax filing | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3724 | E | did we work on pet adoption together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3725 | E | did we work on database migration together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3726 | E | what did we talk about regarding social media plan | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3727 | E | recap what we discussed about internship application | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3728 | E | recap what we discussed about thesis | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3729 | E | anything from our chat about language learning | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 373 | A | my favorite game is disco elysium | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3730 | E | remind me what we planned for code refactor | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3731 | E | remind me what we planned for meal prep | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3732 | E | recap what we discussed about home office setup | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3733 | E | remind me what we planned for internship application | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3734 | E | did we work on apartment hunting together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3735 | E | recap what we discussed about book club | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3736 | E | did we work on game jam together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3737 | E | anything from our chat about resume building | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3738 | E | remind me what we planned for salary negotiation | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3739 | E | remind me what we planned for book club | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 374 | A | my favorite cuisine is mexican | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3740 | E | remind me what we planned for home office setup | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3741 | E | what did we talk about regarding product idea | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3742 | E | anything from our chat about guitar lesson | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3743 | E | did we work on c program together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3744 | E | remind me what we planned for budget plan | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3745 | E | recap what we discussed about pet adoption | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3746 | E | did we work on tax filing together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3747 | E | what did we talk about regarding resume building | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3748 | E | what did we talk about regarding bike repair | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3749 | E | did we work on budget plan together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 375 | A | my favorite city is oslo | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3750 | E | did we work on marketing campaign together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3751 | E | remind me what we planned for business plan | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3752 | E | what did we talk about regarding app prototype | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3753 | E | anything from our chat about movie night | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3754 | E | remind me what we planned for resume building | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3755 | E | what did we talk about regarding home office setup | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3756 | E | did we work on painting class together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3757 | E | what did we talk about regarding meal prep | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3758 | E | did we work on bug hunting together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3759 | E | recap what we discussed about road trip plan | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 376 | A | my favorite food is onion rings | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3760 | E | did we work on api integration together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3761 | E | did we work on presentation together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3762 | E | anything from our chat about photography trip | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3763 | E | did we work on thesis together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3764 | E | did we work on machine learning model together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3765 | E | what did we talk about regarding road trip plan | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3766 | E | did we work on kitchen renovation together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3767 | E | what did we talk about regarding bug hunting | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3768 | E | remind me what we planned for rust project | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3769 | E | recap what we discussed about social media plan | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 377 | A | my pet's name is pepper | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3770 | E | did we work on cooking class together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3771 | E | recap what we discussed about apartment hunting | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3772 | E | recap what we discussed about website redesign | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3773 | E | did we work on garden layout together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3774 | E | what did we talk about regarding study group | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3775 | E | what did we talk about regarding travel itinerary | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3776 | E | anything from our chat about salary negotiation | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3777 | E | what did we talk about regarding tax filing | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3778 | E | remind me what we planned for app prototype | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3779 | E | did we work on road trip plan together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 378 | A | my favorite cuisine is hunan | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3780 | E | recap what we discussed about meal prep | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3781 | E | what did we talk about regarding performance tuning | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3782 | E | did we work on book club together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3783 | E | anything from our chat about ui design | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3784 | E | remind me what we planned for ui design | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3785 | E | remind me what we planned for exam preparation | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3786 | E | recap what we discussed about photography trip | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3787 | E | what did we talk about regarding thesis | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3788 | E | what did we talk about regarding kitchen renovation | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3789 | E | what did we talk about regarding job interview | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 379 | A | my favorite city is rio de janeiro | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3790 | E | anything from our chat about pet adoption | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3791 | E | did we work on performance tuning together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3792 | E | what did we talk about regarding group project | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3793 | E | did we work on research paper together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3794 | E | anything from our chat about hackathon | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3795 | E | anything from our chat about data analysis project | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3796 | E | anything from our chat about bug hunting | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3797 | E | anything from our chat about garden layout | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3798 | E | what did we talk about regarding podcast idea | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3799 | E | what did we talk about regarding machine learning model | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 38 | A | my favorite cuisine is cambodian | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 380 | A | my favorite food is sandwich | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3800 | E | remind me what we planned for website redesign | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3801 | E | recap what we discussed about garden layout | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3802 | E | anything from our chat about gaming setup | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3803 | E | did we work on streaming setup together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3804 | E | anything from our chat about book club | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3805 | E | did we work on debate prep together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3806 | E | did we work on website redesign together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3807 | E | what did we talk about regarding chess bot | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3808 | E | what did we talk about regarding website redesign | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3809 | E | anything from our chat about apartment hunting | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 381 | A | my favorite subject is botany | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3810 | E | remind me what we planned for streaming setup | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3811 | E | remind me what we planned for blog post | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3812 | E | anything from our chat about social media plan | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3813 | E | what did we talk about regarding insurance plan | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3814 | E | anything from our chat about python project | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3815 | E | remind me what we planned for twitch stream | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3816 | E | anything from our chat about cooking class | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3817 | E | remind me what we planned for marketing campaign | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3818 | E | recap what we discussed about hackathon | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3819 | E | anything from our chat about website redesign | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 382 | A | my favorite dessert is souffle | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3820 | E | did we work on visa process together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3821 | E | recap what we discussed about branding | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3822 | E | remind me what we planned for cooking class | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3823 | E | what did we talk about regarding code refactor | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3824 | E | anything from our chat about start-up pitch | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3825 | E | what did we talk about regarding debate prep | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3826 | E | anything from our chat about home office setup | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3827 | E | did we work on hackathon together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3828 | E | remind me what we planned for python project | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3829 | E | what did we talk about regarding marketing campaign | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 383 | A | i work as a musician | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 3830 | E | did we work on study group together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3831 | E | what did we talk about regarding streaming setup | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3832 | E | anything from our chat about investment plan | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3833 | E | what did we talk about regarding rust project | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3834 | E | what did we talk about regarding book club | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3835 | E | remind me what we planned for database migration | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3836 | E | remind me what we planned for job interview | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3837 | E | remind me what we planned for science fair | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3838 | E | what did we talk about regarding homework help | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3839 | E | did we work on product idea together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 384 | A | my favorite animal is gorilla | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3840 | E | anything from our chat about chess bot | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3841 | E | recap what we discussed about science fair | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3842 | E | anything from our chat about streaming setup | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3843 | E | remind me what we planned for start-up pitch | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3844 | E | recap what we discussed about code refactor | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3845 | E | recap what we discussed about rust project | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3846 | E | anything from our chat about group project | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3847 | E | remind me what we planned for debate prep | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3848 | E | recap what we discussed about language learning | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3849 | E | anything from our chat about machine learning model | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 385 | A | my favorite movie is jurassic park | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3850 | E | anything from our chat about exam preparation | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3851 | E | remind me what we planned for investment plan | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3852 | E | remind me what we planned for bike repair | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3853 | E | did we work on app prototype together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3854 | E | anything from our chat about thesis | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3855 | E | anything from our chat about rust project | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3856 | E | remind me what we planned for kitchen renovation | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3857 | E | what did we talk about regarding investment plan | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3858 | E | did we work on code refactor together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3859 | E | recap what we discussed about marathon training | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 386 | A | my favorite food is pierogi | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3860 | E | anything from our chat about marketing campaign | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3861 | E | what did we talk about regarding gaming setup | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3862 | E | anything from our chat about homework help | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3863 | E | what did we talk about regarding exam preparation | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3864 | E | remind me what we planned for apartment hunting | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3865 | E | anything from our chat about study group | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3866 | E | remind me what we planned for movie night | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3867 | E | remind me what we planned for chess bot | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3868 | E | recap what we discussed about research paper | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3869 | E | remind me what we planned for product idea | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 387 | A | my favorite color is olive | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3870 | E | anything from our chat about internship application | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3871 | E | remind me what we planned for road trip plan | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3872 | E | anything from our chat about branding | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3873 | E | what did we talk about regarding internship application | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3874 | E | did we work on photography trip together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3875 | E | anything from our chat about app prototype | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3876 | E | what did we talk about regarding branding | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3877 | E | remind me what we planned for social media plan | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3878 | E | did we work on bike repair together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3879 | E | anything from our chat about road trip plan | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 388 | A | my pet's name is bruno | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3880 | E | remind me what we planned for travel itinerary | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3881 | E | recap what we discussed about machine learning model | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3882 | E | recap what we discussed about cooking class | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3883 | E | anything from our chat about podcast idea | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3884 | E | what did we talk about regarding ui design | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3885 | E | what did we talk about regarding youtube channel | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3886 | E | what did we talk about regarding guitar lesson | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3887 | E | remind me what we planned for language learning | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3888 | E | what did we talk about regarding hackathon | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3889 | E | did we work on home office setup together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 389 | A | i work as a chef | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 3890 | E | recap what we discussed about investment plan | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3891 | E | remind me what we planned for group project | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3892 | E | what did we talk about regarding apartment hunting | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3893 | E | anything from our chat about science fair | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3894 | E | did we work on business plan together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3895 | E | remind me what we planned for research paper | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3896 | E | what did we talk about regarding newsletter | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3897 | E | did we work on start-up pitch together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3898 | E | what did we talk about regarding data analysis project | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3899 | E | did we work on insurance plan together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 39 | A | my favorite hobby is bread baking | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 390 | A | i am from barcelona | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 3900 | E | did we work on guitar lesson together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3901 | E | did we work on python project together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3902 | E | anything from our chat about tax filing | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3903 | E | remind me what we planned for guitar lesson | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3904 | E | did we work on newsletter together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3905 | E | anything from our chat about newsletter | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3906 | E | did we work on rust project together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3907 | E | remind me what we planned for podcast idea | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3908 | E | did we work on chess bot together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3909 | E | did we work on resume building together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 391 | A | my favorite show is succession | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3910 | E | remind me what we planned for homework help | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3911 | E | anything from our chat about bike repair | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3912 | E | anything from our chat about insurance plan | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3913 | E | remind me what we planned for pet adoption | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3914 | E | what did we talk about regarding presentation | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3915 | E | recap what we discussed about tax filing | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3916 | E | remind me what we planned for insurance plan | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3917 | E | did we work on gaming setup together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3918 | E | remind me what we planned for gaming setup | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3919 | E | remind me what we planned for photography trip | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 392 | A | my favorite food is moussaka | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3920 | E | did we work on homework help together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3921 | E | anything from our chat about product idea | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3922 | E | what did we talk about regarding business plan | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3923 | E | remind me what we planned for data analysis project | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3924 | E | what did we talk about regarding research paper | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3925 | E | what did we talk about regarding salary negotiation | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3926 | E | recap what we discussed about job interview | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3927 | E | what did we talk about regarding c program | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3928 | E | what did we talk about regarding research internship | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3929 | E | remind me what we planned for thesis | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 393 | A | my favorite sport is rowing | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3930 | E | anything from our chat about blog post | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3931 | E | recap what we discussed about streaming setup | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3932 | E | recap what we discussed about resume building | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3933 | E | did we work on blog post together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3934 | E | anything from our chat about presentation | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3935 | E | did we work on branding together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3936 | E | remind me what we planned for newsletter | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3937 | E | did we work on meal prep together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3938 | E | did we work on travel itinerary together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3939 | E | did we work on group project together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 394 | A | my favorite subject is acoustics | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3940 | E | anything from our chat about meal prep | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3941 | E | anything from our chat about twitch stream | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3942 | E | what did we talk about regarding blog post | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3943 | E | remind me what we planned for youtube channel | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3944 | E | what did we talk about regarding twitch stream | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3945 | E | anything from our chat about fitness routine | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 3946 | E | what did we talk about regarding visa process | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3947 | E | anything from our chat about budget plan | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3948 | E | did we work on ui design together | episodic recall (use_episodes + episodes) | use_episodes=True episodes=3 | PASS |  |
| 3949 | E | anything from our chat about side hustle | episodic recall (use_episodes + episodes) | use_episodes=False | FAIL | recall not routed to episodes |
| 395 | A | my favorite writer is edgar allan poe | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3950 | F | actually my favorite coffee is now rose lemonade | context-aware write or safe follow-up | op=update status=stored fact='My favorite coffee is rose lemonade' | PASS |  |
| 3951 | F | actually my favorite coffee is now cold brew | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is cold brew' | PASS |  |
| 3952 | F | now my favorite coffee is mocha | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is root beer' | FAIL | context update not applied: status=updated |
| 3953 | F | actually my favorite coffee is now flat white | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is cafe au lait' | FAIL | context update not applied: status=updated |
| 3954 | F | no wait, i prefer sangria for my favorite coffee | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is yerba mate' | FAIL | context update not applied: status=updated |
| 3955 | F | no wait, i prefer hot chocolate for my favorite coffee | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is hibiscus tea' | FAIL | context update not applied: status=updated |
| 3956 | F | no wait, i prefer watermelon juice for my favorite coffee | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite coffee is jasmine tea' | FAIL | context update not applied: status=needs_clarification |
| 3957 | F | now my favorite coffee is prosecco | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is guava juice' | PASS |  |
| 3958 | F | actually my favorite coffee is now latte | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is latte' | PASS |  |
| 3959 | F | actually my favorite coffee is now kombucha | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is kombucha' | PASS |  |
| 396 | A | my favorite dessert is lamington | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3960 | F | now my favorite coffee is pomegranate juice | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is sugarcane juice' | FAIL | context update not applied: status=updated |
| 3961 | F | now my favorite coffee is cappuccino | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is cherry soda' | FAIL | context update not applied: status=updated |
| 3962 | F | actually my favorite coffee is now limeade | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is salted lassi' | FAIL | context update not applied: status=updated |
| 3963 | F | now my favorite coffee is mate | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is latte' | FAIL | context update not applied: status=updated |
| 3964 | F | actually my favorite coffee is now falooda | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is falooda' | PASS |  |
| 3965 | F | actually my favorite coffee is now beer | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is beer' | PASS |  |
| 3966 | F | no wait, i prefer iced tea for my favorite coffee | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is rose milk' | FAIL | context update not applied: status=updated |
| 3967 | F | actually my favorite coffee is now cranberry juice | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is kombucha' | FAIL | context update not applied: status=updated |
| 3968 | F | now my favorite coffee is peppermint tea | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite coffee is frappe' | FAIL | context update not applied: status=needs_clarification |
| 3969 | F | now my favorite coffee is white wine | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite coffee is white wine' | FAIL | context update not applied: status=needs_clarification |
| 397 | A | my favorite subject is pharmacy | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3970 | F | no wait, i prefer bubble tea for my favorite coffee | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite coffee is rose wine' | FAIL | context update not applied: status=needs_clarification |
| 3971 | F | now my favorite coffee is red wine | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is red wine' | PASS |  |
| 3972 | F | no wait, i prefer fresh lime soda for my favorite coffee | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite coffee is green tea' | FAIL | context update not applied: status=needs_clarification |
| 3973 | F | actually my favorite coffee is now cafe au lait | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is cafe au lait' | PASS |  |
| 3974 | F | actually my favorite coffee is now coconut water | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is coconut water' | PASS |  |
| 3975 | F | actually my favorite coffee is now tomato juice | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is taro milk tea' | FAIL | context update not applied: status=updated |
| 3976 | F | actually my favorite coffee is now frappe | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is frappe' | PASS |  |
| 3977 | F | now my favorite coffee is matcha | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is dirty chai' | FAIL | context update not applied: status=updated |
| 3978 | F | actually my favorite coffee is now sparkling water | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite coffee is sparkling water' | FAIL | context update not applied: status=needs_clarification |
| 3979 | F | no wait, i prefer jasmine tea for my favorite coffee | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite coffee is beer' | FAIL | context update not applied: status=needs_clarification |
| 398 | A | my favorite drink is mocha | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is mocha' | FAIL | store did not persist: status=needs_clarification present=False |
| 3980 | F | no wait, i prefer orange soda for my favorite coffee | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite coffee is bubble tea' | FAIL | context update not applied: status=needs_clarification |
| 3981 | F | no wait, i prefer kesar milk for my favorite coffee | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite coffee is sparkling lemonade' | FAIL | context update not applied: status=needs_clarification |
| 3982 | F | actually my favorite coffee is now soda water | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is cappuccino' | FAIL | context update not applied: status=updated |
| 3983 | F | actually my favorite coffee is now grape juice | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is falooda' | FAIL | context update not applied: status=updated |
| 3984 | F | actually my favorite coffee is now sparkling lemonade | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is mocha' | FAIL | context update not applied: status=updated |
| 3985 | F | no wait, i prefer sweet lassi for my favorite coffee | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite coffee is black tea' | FAIL | context update not applied: status=needs_clarification |
| 3986 | F | no wait, i prefer mead for my favorite coffee | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite coffee is orange juice' | FAIL | context update not applied: status=needs_clarification |
| 3987 | F | no wait, i prefer hibiscus tea for my favorite coffee | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite coffee is peppermint tea' | FAIL | context update not applied: status=needs_clarification |
| 3988 | F | no wait, i prefer ginger ale for my favorite coffee | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite coffee is herbal tea' | FAIL | context update not applied: status=needs_clarification |
| 3989 | F | no wait, i prefer guava juice for my favorite coffee | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite coffee is milkshake' | FAIL | context update not applied: status=needs_clarification |
| 399 | A | my favorite color is cream | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 3990 | F | no wait, i prefer smoothie for my favorite coffee | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite coffee is grape juice' | FAIL | context update not applied: status=needs_clarification |
| 3991 | F | no wait, i prefer cider for my favorite coffee | context-aware write or safe follow-up |  | ERROR | analyze failed: (None, None) |
| 3992 | F | now my favorite coffee is iced chai | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is sweet lassi' | FAIL | context update not applied: status=updated |
| 3993 | F | now my favorite coffee is milk coffee | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is hot toddy' | FAIL | context update not applied: status=updated |
| 3994 | F | now my favorite coffee is coffee | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is masala chai' | PASS |  |
| 3995 | F | now my favorite coffee is black tea | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is black tea' | PASS |  |
| 3996 | F | actually my favorite coffee is now cola | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is cola' | PASS |  |
| 3997 | F | actually my favorite coffee is now dirty chai | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is cream soda' | FAIL | context update not applied: status=updated |
| 3998 | F | now my favorite coffee is iced matcha | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is iced chai' | FAIL | context update not applied: status=updated |
| 3999 | F | no wait, i prefer lassi for my favorite coffee | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite coffee is milk coffee' | FAIL | context update not applied: status=needs_clarification |
| 4 | A | my favorite animal is jellyfish | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 40 | A | my favorite fruit is durian | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 400 | A | my favorite food is polenta | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4000 | F | actually my favorite coffee is now stout | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is stout' | PASS |  |
| 4001 | F | now my favorite coffee is buttermilk | context-aware write or safe follow-up | op=update status=updated fact='My favorite coffee is buttermilk' | PASS |  |
| 4002 | F | no wait, i prefer mango lassi for my favorite coffee | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite coffee is ginger ale' | FAIL | context update not applied: status=needs_clarification |
| 4003 | F | now my favorite pastry is truffles | context-aware write or safe follow-up | op=update status=stored fact='My favorite pastry is truffles' | PASS |  |
| 4004 | F | no wait, i prefer donuts for my favorite pastry | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite pastry is rice pudding' | FAIL | context update not applied: status=needs_clarification |
| 4005 | F | actually my favorite pastry is now coconut barfi | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is coconut barfi' | PASS |  |
| 4006 | F | no wait, i prefer beignets for my favorite pastry | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is apple pie' | FAIL | context update not applied: status=updated |
| 4007 | F | now my favorite pastry is cheesecake | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is cheesecake' | PASS |  |
| 4008 | F | actually my favorite pastry is now brownie sundae | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is pavlova' | FAIL | context update not applied: status=updated |
| 4009 | F | no wait, i prefer jalebi for my favorite pastry | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite pastry is rasgulla' | FAIL | context update not applied: status=needs_clarification |
| 401 | A | my favorite show is the office | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4010 | F | no wait, i prefer kulfi for my favorite pastry | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite pastry is panna cotta' | FAIL | context update not applied: status=needs_clarification |
| 4011 | F | no wait, i prefer gulab jamun for my favorite pastry | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite pastry is donuts' | FAIL | context update not applied: status=needs_clarification |
| 4012 | F | no wait, i prefer baklava for my favorite pastry | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite pastry is beignets' | FAIL | context update not applied: status=needs_clarification |
| 4013 | F | now my favorite pastry is rasgulla | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite pastry is tarte tatin' | FAIL | context update not applied: status=needs_clarification |
| 4014 | F | now my favorite pastry is phirni | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is kheer' | FAIL | context update not applied: status=updated |
| 4015 | F | no wait, i prefer macarons for my favorite pastry | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is carrot cake' | FAIL | context update not applied: status=updated |
| 4016 | F | now my favorite pastry is lemon tart | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is brownie sundae' | FAIL | context update not applied: status=updated |
| 4017 | F | no wait, i prefer key lime pie for my favorite pastry | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is macarons' | FAIL | context update not applied: status=updated |
| 4018 | F | actually my favorite pastry is now mousse | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is mousse' | PASS |  |
| 4019 | F | no wait, i prefer banana bread for my favorite pastry | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is pound cake' | FAIL | context update not applied: status=updated |
| 402 | A | my pet's name is simba | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4020 | F | no wait, i prefer chocolate cake for my favorite pastry | context-aware write or safe follow-up |  | ERROR | analyze failed: (None, None) |
| 4021 | F | actually my favorite pastry is now cinnamon roll | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is cinnamon roll' | PASS |  |
| 4022 | F | no wait, i prefer funnel cake for my favorite pastry | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite pastry is eclair' | FAIL | context update not applied: status=needs_clarification |
| 4023 | F | actually my favorite pastry is now carrot cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is carrot cake' | PASS |  |
| 4024 | F | now my favorite pastry is profiteroles | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is profiteroles' | PASS |  |
| 4025 | F | now my favorite pastry is pavlova | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is pavlova' | PASS |  |
| 4026 | F | no wait, i prefer lamington for my favorite pastry | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is sandesh' | FAIL | context update not applied: status=updated |
| 4027 | F | no wait, i prefer crepes for my favorite pastry | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is coconut barfi' | FAIL | context update not applied: status=updated |
| 4028 | F | actually my favorite pastry is now kheer | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is kheer' | PASS |  |
| 4029 | F | actually my favorite pastry is now eclair | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is eclair' | PASS |  |
| 403 | A | my favorite animal is fox | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4030 | F | now my favorite pastry is tiramisu | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is profiteroles' | FAIL | context update not applied: status=updated |
| 4031 | F | actually my favorite pastry is now souffle | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is souffle' | PASS |  |
| 4032 | F | no wait, i prefer mishti doi for my favorite pastry | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite pastry is lemon tart' | FAIL | context update not applied: status=needs_clarification |
| 4033 | F | actually my favorite pastry is now mango pudding | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is mango pudding' | PASS |  |
| 4034 | F | no wait, i prefer creme brulee for my favorite pastry | context-aware write or safe follow-up |  | ERROR | analyze failed: (None, None) |
| 4035 | F | no wait, i prefer pumpkin pie for my favorite pastry | context-aware write or safe follow-up |  | ERROR | analyze failed: (None, None) |
| 4036 | F | actually my favorite pastry is now caramel custard | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is caramel custard' | PASS |  |
| 4037 | F | actually my favorite pastry is now sandesh | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is brownies' | FAIL | context update not applied: status=updated |
| 4038 | F | actually my favorite pastry is now bread pudding | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is bread pudding' | PASS |  |
| 4039 | F | actually my favorite pastry is now barfi | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is barfi' | PASS |  |
| 404 | A | my favorite hobby is darts | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4040 | F | no wait, i prefer red velvet cake for my favorite pastry | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is cheesecake' | FAIL | context update not applied: status=updated |
| 4041 | F | no wait, i prefer ice cream for my favorite pastry | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is waffle with ice cream' | PASS |  |
| 4042 | F | now my favorite pastry is mochi | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is mochi' | PASS |  |
| 4043 | F | now my favorite pastry is pecan pie | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is mishti doi' | FAIL | context update not applied: status=updated |
| 4044 | F | actually my favorite pastry is now laddu | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is kulfi' | FAIL | context update not applied: status=updated |
| 4045 | F | now my favorite pastry is panna cotta | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is funnel cake' | FAIL | context update not applied: status=updated |
| 4046 | F | now my favorite pastry is sponge cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is souffle' | FAIL | context update not applied: status=updated |
| 4047 | F | actually my favorite pastry is now apple pie | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is apple pie' | PASS |  |
| 4048 | F | actually my favorite pastry is now angel food cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is angel food cake' | PASS |  |
| 4049 | F | no wait, i prefer churros for my favorite pastry | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is banana bread' | FAIL | context update not applied: status=updated |
| 405 | A | i am from nairobi | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 4050 | F | now my favorite pastry is waffle with ice cream | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is waffle with ice cream' | PASS |  |
| 4051 | F | now my favorite pastry is fudge | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is fudge' | PASS |  |
| 4052 | F | actually my favorite pastry is now rasmalai | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is cinnamon roll' | FAIL | context update not applied: status=updated |
| 4053 | F | no wait, i prefer macaron tower for my favorite pastry | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is gulab jamun' | FAIL | context update not applied: status=updated |
| 4054 | F | now my favorite pastry is tarte tatin | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is tiramisu' | FAIL | context update not applied: status=updated |
| 4055 | F | now my favorite pastry is pound cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite pastry is sponge cake' | FAIL | context update not applied: status=updated |
| 4056 | F | now my favorite cake is mousse | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is key lime pie' | FAIL | context update not applied: status=updated |
| 4057 | F | actually my favorite cake is now mochi | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is mochi' | PASS |  |
| 4058 | F | no wait, i prefer kulfi for my favorite cake | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite cake is sponge cake' | FAIL | context update not applied: status=needs_clarification |
| 4059 | F | actually my favorite cake is now red velvet cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is red velvet cake' | PASS |  |
| 406 | A | i am from florence | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 4060 | F | actually my favorite cake is now eclair | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is eclair' | PASS |  |
| 4061 | F | now my favorite cake is coconut barfi | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is pound cake' | FAIL | context update not applied: status=updated |
| 4062 | F | no wait, i prefer phirni for my favorite cake | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite cake is caramel custard' | FAIL | context update not applied: status=needs_clarification |
| 4063 | F | no wait, i prefer beignets for my favorite cake | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite cake is rasgulla' | FAIL | context update not applied: status=needs_clarification |
| 4064 | F | no wait, i prefer gulab jamun for my favorite cake | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite cake is macaron tower' | FAIL | context update not applied: status=needs_clarification |
| 4065 | F | actually my favorite cake is now tarte tatin | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is tarte tatin' | PASS |  |
| 4066 | F | no wait, i prefer souffle for my favorite cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is brownies' | FAIL | context update not applied: status=updated |
| 4067 | F | now my favorite cake is creme brulee | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is creme brulee' | PASS |  |
| 4068 | F | now my favorite cake is cheesecake | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is cheesecake' | PASS |  |
| 4069 | F | no wait, i prefer cinnamon roll for my favorite cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is waffle with ice cream' | PASS |  |
| 407 | A | my favorite sport is sailing | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4070 | F | now my favorite cake is sandesh | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite cake is tarte tatin' | FAIL | context update not applied: status=needs_clarification |
| 4071 | F | actually my favorite cake is now pumpkin pie | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is pumpkin pie' | PASS |  |
| 4072 | F | actually my favorite cake is now mango pudding | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is mango pudding' | PASS |  |
| 4073 | F | no wait, i prefer kheer for my favorite cake | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite cake is pavlova' | FAIL | context update not applied: status=needs_clarification |
| 4074 | F | no wait, i prefer jalebi for my favorite cake | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite cake is mousse' | FAIL | context update not applied: status=needs_clarification |
| 4075 | F | now my favorite cake is rice pudding | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is coconut barfi' | FAIL | context update not applied: status=updated |
| 4076 | F | actually my favorite cake is now pound cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is pound cake' | PASS |  |
| 4077 | F | no wait, i prefer angel food cake for my favorite cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is souffle' | FAIL | context update not applied: status=updated |
| 4078 | F | now my favorite cake is bread pudding | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is bread pudding' | PASS |  |
| 4079 | F | no wait, i prefer ice cream for my favorite cake | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite cake is carrot cake' | FAIL | context update not applied: status=needs_clarification |
| 408 | A | my favorite animal is dolphin | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4080 | F | no wait, i prefer rasgulla for my favorite cake | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite cake is laddu' | FAIL | context update not applied: status=needs_clarification |
| 4081 | F | actually my favorite cake is now apple pie | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is apple pie' | PASS |  |
| 4082 | F | actually my favorite cake is now crepes | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is crepes' | PASS |  |
| 4083 | F | actually my favorite cake is now pecan pie | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is pecan pie' | PASS |  |
| 4084 | F | now my favorite cake is lamington | context-aware write or safe follow-up | op=update status=ignored fact='My favorite cake is crepes' | FAIL | context update not applied: status=ignored |
| 4085 | F | no wait, i prefer macaron tower for my favorite cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is bread pudding' | FAIL | context update not applied: status=updated |
| 4086 | F | no wait, i prefer profiteroles for my favorite cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is lemon tart' | FAIL | context update not applied: status=updated |
| 4087 | F | actually my favorite cake is now baklava | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is baklava' | PASS |  |
| 4088 | F | no wait, i prefer funnel cake for my favorite cake | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite cake is angel food cake' | FAIL | context update not applied: status=needs_clarification |
| 4089 | F | actually my favorite cake is now brownie sundae | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is brownie sundae' | PASS |  |
| 409 | A | my favorite dessert is jalebi | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4090 | F | no wait, i prefer key lime pie for my favorite cake | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite cake is kulfi' | FAIL | context update not applied: status=needs_clarification |
| 4091 | F | actually my favorite cake is now donuts | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is phirni' | FAIL | context update not applied: status=updated |
| 4092 | F | actually my favorite cake is now rasmalai | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is mochi' | FAIL | context update not applied: status=updated |
| 4093 | F | no wait, i prefer banana bread for my favorite cake | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite cake is apple pie' | FAIL | context update not applied: status=needs_clarification |
| 4094 | F | now my favorite cake is brownies | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is brownies' | PASS |  |
| 4095 | F | actually my favorite cake is now panna cotta | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is panna cotta' | PASS |  |
| 4096 | F | now my favorite cake is churros | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is kheer' | FAIL | context update not applied: status=updated |
| 4097 | F | actually my favorite cake is now macarons | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is macarons' | PASS |  |
| 4098 | F | no wait, i prefer barfi for my favorite cake | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite cake is rice pudding' | FAIL | context update not applied: status=needs_clarification |
| 4099 | F | actually my favorite cake is now waffle with ice cream | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is waffle with ice cream' | PASS |  |
| 41 | A | my favorite food is burger | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 410 | A | my favorite subject is archaeology | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4100 | F | now my favorite cake is chocolate cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is pumpkin pie' | FAIL | context update not applied: status=updated |
| 4101 | F | now my favorite cake is fudge | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is banana bread' | PASS |  |
| 4102 | F | no wait, i prefer carrot cake for my favorite cake | context-aware write or safe follow-up |  | ERROR | analyze failed: (None, None) |
| 4103 | F | now my favorite cake is laddu | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite cake is lamington' | FAIL | context update not applied: status=needs_clarification |
| 4104 | F | now my favorite cake is lemon tart | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is lemon tart' | PASS |  |
| 4105 | F | actually my favorite cake is now sponge cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is sponge cake' | PASS |  |
| 4106 | F | now my favorite cake is mishti doi | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is baklava' | FAIL | context update not applied: status=updated |
| 4107 | F | now my favorite cake is caramel custard | context-aware write or safe follow-up | op=update status=updated fact='My favorite cake is barfi' | FAIL | context update not applied: status=updated |
| 4108 | F | actually my favorite candy is now mochi | context-aware write or safe follow-up | op=update status=stored fact='My favorite candy is mochi' | PASS |  |
| 4109 | F | now my favorite candy is pumpkin pie | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is brownies' | FAIL | context update not applied: status=updated |
| 411 | A | my favorite drink is carrot juice | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is carrot juice' | FAIL | store did not persist: status=needs_clarification present=False |
| 4110 | F | now my favorite candy is fudge | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is fudge' | PASS |  |
| 4111 | F | no wait, i prefer souffle for my favorite candy | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite candy is souffle' | FAIL | context update not applied: status=needs_clarification |
| 4112 | F | no wait, i prefer profiteroles for my favorite candy | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite candy is pavlova' | FAIL | context update not applied: status=needs_clarification |
| 4113 | F | now my favorite candy is apple pie | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is barfi' | FAIL | context update not applied: status=updated |
| 4114 | F | now my favorite candy is cinnamon roll | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is key lime pie' | PASS |  |
| 4115 | F | now my favorite candy is carrot cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is macarons' | FAIL | context update not applied: status=updated |
| 4116 | F | now my favorite candy is baklava | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite candy is fudge' | FAIL | context update not applied: status=needs_clarification |
| 4117 | F | now my favorite candy is gulab jamun | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is gulab jamun' | PASS |  |
| 4118 | F | actually my favorite candy is now pavlova | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is pavlova' | PASS |  |
| 4119 | F | now my favorite candy is laddu | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is rasgulla' | FAIL | context update not applied: status=updated |
| 412 | A | i work as a teacher | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 4120 | F | now my favorite candy is rasmalai | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is cinnamon roll' | FAIL | context update not applied: status=updated |
| 4121 | F | actually my favorite candy is now brownies | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is brownies' | PASS |  |
| 4122 | F | no wait, i prefer coconut barfi for my favorite candy | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite candy is eclair' | FAIL | context update not applied: status=needs_clarification |
| 4123 | F | now my favorite candy is red velvet cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is red velvet cake' | PASS |  |
| 4124 | F | actually my favorite candy is now barfi | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is barfi' | PASS |  |
| 4125 | F | now my favorite candy is churros | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is kulfi' | FAIL | context update not applied: status=updated |
| 4126 | F | actually my favorite candy is now waffle with ice cream | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is waffle with ice cream' | PASS |  |
| 4127 | F | no wait, i prefer key lime pie for my favorite candy | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is cheesecake' | FAIL | context update not applied: status=updated |
| 4128 | F | no wait, i prefer lemon tart for my favorite candy | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is lemon tart' | PASS |  |
| 4129 | F | actually my favorite candy is now sandesh | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is sandesh' | PASS |  |
| 413 | A | my favorite food is korean bbq | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4130 | F | now my favorite candy is beignets | context-aware write or safe follow-up | op=update status=ignored fact='My favorite candy is lemon tart' | FAIL | context update not applied: status=ignored |
| 4131 | F | no wait, i prefer lamington for my favorite candy | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is jalebi' | FAIL | context update not applied: status=updated |
| 4132 | F | actually my favorite candy is now jalebi | context-aware write or safe follow-up | op=update status=ignored fact='My favorite candy is jalebi' | FAIL | context update not applied: status=ignored |
| 4133 | F | no wait, i prefer macaron tower for my favorite candy | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite candy is coconut barfi' | FAIL | context update not applied: status=needs_clarification |
| 4134 | F | actually my favorite candy is now phirni | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is phirni' | PASS |  |
| 4135 | F | now my favorite candy is rasgulla | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite candy is rice pudding' | FAIL | context update not applied: status=needs_clarification |
| 4136 | F | actually my favorite candy is now sponge cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is sponge cake' | PASS |  |
| 4137 | F | no wait, i prefer macarons for my favorite candy | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is macaron tower' | FAIL | context update not applied: status=updated |
| 4138 | F | now my favorite candy is eclair | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is eclair' | PASS |  |
| 4139 | F | now my favorite candy is tiramisu | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is tiramisu' | PASS |  |
| 414 | A | my favorite writer is octavio paz | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4140 | F | no wait, i prefer angel food cake for my favorite candy | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite candy is caramel custard' | FAIL | context update not applied: status=needs_clarification |
| 4141 | F | actually my favorite candy is now pound cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is pound cake' | PASS |  |
| 4142 | F | now my favorite candy is kulfi | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is kulfi' | PASS |  |
| 4143 | F | no wait, i prefer cheesecake for my favorite candy | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite candy is banana bread' | FAIL | context update not applied: status=needs_clarification |
| 4144 | F | actually my favorite candy is now truffles | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is truffles' | PASS |  |
| 4145 | F | no wait, i prefer kheer for my favorite candy | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite candy is lamington' | FAIL | context update not applied: status=needs_clarification |
| 4146 | F | no wait, i prefer crepes for my favorite candy | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite candy is crepes' | FAIL | context update not applied: status=needs_clarification |
| 4147 | F | no wait, i prefer mango pudding for my favorite candy | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite candy is phirni' | FAIL | context update not applied: status=needs_clarification |
| 4148 | F | actually my favorite candy is now chocolate cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is chocolate cake' | PASS |  |
| 4149 | F | now my favorite candy is bread pudding | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is pecan pie' | FAIL | context update not applied: status=updated |
| 415 | A | my favorite music is ambient | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4150 | F | actually my favorite candy is now rice pudding | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is rice pudding' | PASS |  |
| 4151 | F | actually my favorite candy is now funnel cake | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is funnel cake' | PASS |  |
| 4152 | F | no wait, i prefer donuts for my favorite candy | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite candy is mochi' | FAIL | context update not applied: status=needs_clarification |
| 4153 | F | no wait, i prefer caramel custard for my favorite candy | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is caramel custard' | PASS |  |
| 4154 | F | actually my favorite candy is now mishti doi | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is crepes' | FAIL | context update not applied: status=updated |
| 4155 | F | no wait, i prefer tarte tatin for my favorite candy | context-aware write or safe follow-up | op=update status=needs_clarification fact='My favorite candy is pumpkin pie' | FAIL | context update not applied: status=needs_clarification |
| 4156 | F | actually my favorite candy is now brownie sundae | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is brownie sundae' | PASS |  |
| 4157 | F | actually my favorite candy is now banana bread | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is banana bread' | PASS |  |
| 4158 | F | actually my favorite candy is now creme brulee | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is creme brulee' | PASS |  |
| 4159 | F | actually my favorite candy is now panna cotta | context-aware write or safe follow-up | op=update status=updated fact='My favorite candy is panna cotta' | PASS |  |
| 416 | A | i am from copenhagen | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 4160 | F | okay, right, go ahead | context-aware write or safe follow-up | op=None | PASS |  |
| 4161 | F | okay, okay | context-aware write or safe follow-up | op=None | PASS |  |
| 4162 | F | interesting | context-aware write or safe follow-up | op=update | PASS |  |
| 4163 | F | you were saying | context-aware write or safe follow-up | op=store fact='I study B.Tech' | PASS | followup auto-wrote (review): op=store fact='I study B.Tech' |
| 4164 | F | yeah, got it, go on | context-aware write or safe follow-up | op=store fact='I need help with my acoustics homework' | PASS | followup auto-wrote (review): op=store fact='I need help with my acoustics homework' |
| 4165 | F | so, go on then | context-aware write or safe follow-up | op=store fact='I need help with my artificial intelligence homework' | PASS | followup auto-wrote (review): op=store fact='I need help with my artificial intelligence homework' |
| 4166 | F | so, i am listening | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4167 | F | yeah, and then | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4168 | F | please go on | context-aware write or safe follow-up | op=store fact='I am planning a trip to Montevideo' | PASS | followup auto-wrote (review): op=store fact='I am planning a trip to Montevideo' |
| 4169 | F | yeah, alright continue | context-aware write or safe follow-up | op=None | PASS |  |
| 417 | A | my favorite drink is mead | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is mead' | FAIL | store did not persist: status=needs_clarification present=False |
| 4170 | F | tell me more | context-aware write or safe follow-up | op=None | PASS |  |
| 4171 | F | so, yes | context-aware write or safe follow-up | op=None | PASS |  |
| 4172 | F | yeah, okay go | context-aware write or safe follow-up | op=store | PASS |  |
| 4173 | F | so, so | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4174 | F | okay, interesting | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4175 | F | okay, go ahead | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4176 | F | so, and then what | context-aware write or safe follow-up | op=None | PASS |  |
| 4177 | F | okay, make sense, continue | context-aware write or safe follow-up | op=None | PASS |  |
| 4178 | F | so, yeah go ahead | context-aware write or safe follow-up | op=None | PASS |  |
| 4179 | F | so, please go on | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 418 | A | my favorite book is ready player one | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4180 | F | so, tell me more | context-aware write or safe follow-up | op=store fact='I study B.Tech' | PASS | followup auto-wrote (review): op=store fact='I study B.Tech' |
| 4181 | F | okay, continue | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4182 | F | okay go | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4183 | F | so, okay go | context-aware write or safe follow-up | op=store fact='i need help with my pharmacy homework' | PASS | followup auto-wrote (review): op=store fact='i need help with my pharmacy homework' |
| 4184 | F | okay continue | context-aware write or safe follow-up | op=None | PASS |  |
| 4185 | F | yeah, interesting | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4186 | F | yeah, proceed | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4187 | F | tell me | context-aware write or safe follow-up | op=query | PASS |  |
| 4188 | F | yeah, go on | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4189 | F | okay | context-aware write or safe follow-up | op=None | PASS |  |
| 419 | A | my favorite movie is avatar | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4190 | F | yeah, fine | context-aware write or safe follow-up | op=update fact='I study btag' | PASS | followup auto-wrote (review): op=update fact='I study btag' |
| 4191 | F | okay, and then | context-aware write or safe follow-up | op=store fact='I am planning a trip to Copenhagen' | PASS | followup auto-wrote (review): op=store fact='I am planning a trip to Copenhagen' |
| 4192 | F | proceed | context-aware write or safe follow-up | op=None | PASS |  |
| 4193 | F | okay, okay continue | context-aware write or safe follow-up | op=None | PASS |  |
| 4194 | F | yeah, ok go on | context-aware write or safe follow-up | op=store fact='I am planning a trip to Madrid' | PASS | followup auto-wrote (review): op=store fact='I am planning a trip to Madrid' |
| 4195 | F | so | context-aware write or safe follow-up | op=store | PASS |  |
| 4196 | F | so, sure thing | context-aware write or safe follow-up | op=store fact='I need help with my marine biology homework' | PASS | followup auto-wrote (review): op=store fact='I need help with my marine biology homework' |
| 4197 | F | so, yes please | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4198 | F | yeah go ahead | context-aware write or safe follow-up | op=None | PASS |  |
| 4199 | F | continue | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 42 | A | my favorite fruit is star fruit | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 420 | A | my favorite writer is haruki murakami | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4200 | F | so, fine | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4201 | F | yeah, ok then | context-aware write or safe follow-up | op=update fact='My favorite editor is PyCharm' | PASS | followup auto-wrote (review): op=update fact='My favorite editor is PyCharm' |
| 4202 | F | so, proceed | context-aware write or safe follow-up | op=None | PASS |  |
| 4203 | F | and then | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4204 | F | yeah, so | context-aware write or safe follow-up | op=None | PASS |  |
| 4205 | F | so, go on | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4206 | F | so, ok go on | context-aware write or safe follow-up | op=store fact='I am planning a trip to Bangkok' | PASS | followup auto-wrote (review): op=store fact='I am planning a trip to Bangkok' |
| 4207 | F | okay, and then what | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4208 | F | go on then | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4209 | F | yeah, absolutely | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 421 | A | my favorite cuisine is cuban | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4210 | F | so, interesting, tell me more | context-aware write or safe follow-up | op=store fact='I am planning a trip to Quito' | PASS | followup auto-wrote (review): op=store fact='I am planning a trip to Quito' |
| 4211 | F | yes you tell me | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4212 | F | so, please continue | context-aware write or safe follow-up | op=None | PASS |  |
| 4213 | F | yeah, i see, continue | context-aware write or safe follow-up | op=None | PASS |  |
| 4214 | F | okay, yes you tell me | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4215 | F | okay, i see, continue | context-aware write or safe follow-up | op=None | PASS |  |
| 4216 | F | okay, okay go | context-aware write or safe follow-up | op=None | PASS |  |
| 4217 | F | okay, i am listening | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4218 | F | yeah, yes | context-aware write or safe follow-up | op=None | PASS |  |
| 4219 | F | so, makes sense | context-aware write or safe follow-up | op=None | PASS |  |
| 422 | A | my favorite dessert is truffles | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4220 | F | right, go ahead | context-aware write or safe follow-up | op=None | PASS |  |
| 4221 | F | so, ok then | context-aware write or safe follow-up | op=update fact='I study btag' | PASS | followup auto-wrote (review): op=update fact='I study btag' |
| 4222 | F | so, okay | context-aware write or safe follow-up | op=None | PASS |  |
| 4223 | F | so, got it, go on | context-aware write or safe follow-up | op=None | PASS |  |
| 4224 | F | yeah, yes please | context-aware write or safe follow-up | op=update fact='My favorite editor is PyCharm' | PASS | followup auto-wrote (review): op=update fact='My favorite editor is PyCharm' |
| 4225 | F | okay, so what about it | context-aware write or safe follow-up | op=store fact='I want to learn coding' | PASS | followup auto-wrote (review): op=store fact='I want to learn coding' |
| 4226 | F | sure thing | context-aware write or safe follow-up | op=None | PASS |  |
| 4227 | F | yeah, and then what | context-aware write or safe follow-up | op=store fact='I am planning a trip to Kyoto' | PASS | followup auto-wrote (review): op=store fact='I am planning a trip to Kyoto' |
| 4228 | F | yeah, okay continue | context-aware write or safe follow-up | op=store fact='I study B.Tech' | PASS | followup auto-wrote (review): op=store fact='I study B.Tech' |
| 4229 | F | so, so what about it | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 423 | A | my favorite hobby is woodworking | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4230 | F | yeah, what else | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4231 | F | i am listening | context-aware write or safe follow-up | op=store fact='I am listening' | PASS | followup auto-wrote (review): op=store fact='I am listening' |
| 4232 | F | okay, sure | context-aware write or safe follow-up | op=None | PASS |  |
| 4233 | F | yeah, go on then | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4234 | F | yeah, tell me | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4235 | F | so, absolutely | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4236 | F | so, continue | context-aware write or safe follow-up | op=None | PASS |  |
| 4237 | F | yeah, please go on | context-aware write or safe follow-up | op=None | PASS |  |
| 4238 | F | yeah, i am listening | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4239 | F | so, i see, continue | context-aware write or safe follow-up | op=None | PASS |  |
| 424 | A | my favorite sport is fencing | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4240 | F | so, tell me | context-aware write or safe follow-up | op=store fact='I am working on my machine learning model' | PASS | followup auto-wrote (review): op=store fact='I am working on my machine learning model' |
| 4241 | F | okay, alright | context-aware write or safe follow-up | op=None | PASS |  |
| 4242 | F | okay, absolutely | context-aware write or safe follow-up | op=store fact='I plan a trip to Santiago' | PASS | followup auto-wrote (review): op=store fact='I plan a trip to Santiago' |
| 4243 | F | makes sense | context-aware write or safe follow-up | op=None | PASS |  |
| 4244 | F | okay, go on then | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4245 | F | yeah, yeah go ahead | context-aware write or safe follow-up | op=update | PASS |  |
| 4246 | F | so, right, go ahead | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4247 | F | yeah, sure | context-aware write or safe follow-up | op=None | PASS |  |
| 4248 | F | yeah, yes, go on | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4249 | F | okay, anyway | context-aware write or safe follow-up | op=None | PASS |  |
| 425 | A | my favorite dessert is eclair | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4250 | F | yeah, sure thing | context-aware write or safe follow-up | op=None | PASS |  |
| 4251 | F | absolutely | context-aware write or safe follow-up | op=store fact='I want to learn UI design' | PASS | followup auto-wrote (review): op=store fact='I want to learn UI design' |
| 4252 | F | umm | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4253 | F | so, interesting | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4254 | F | so, okay continue | context-aware write or safe follow-up | op=None | PASS |  |
| 4255 | F | so, yes you tell me | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4256 | F | go ahead | context-aware write or safe follow-up | op=update fact='I want to learn ukulele' | PASS | followup auto-wrote (review): op=update fact='I want to learn ukulele' |
| 4257 | F | yeah, right, go ahead | context-aware write or safe follow-up | op=None | PASS |  |
| 4258 | F | okay, tell me more | context-aware write or safe follow-up | op=store fact='I am planning a trip to Seoul' | PASS | followup auto-wrote (review): op=store fact='I am planning a trip to Seoul' |
| 4259 | F | okay, makes sense | context-aware write or safe follow-up | op=None | PASS |  |
| 426 | A | my pet's name is kiwi | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4260 | F | okay, go on | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4261 | F | ok then | context-aware write or safe follow-up | op=update fact='My favorite editor is PyCharm' | PASS | followup auto-wrote (review): op=update fact='My favorite editor is PyCharm' |
| 4262 | F | okay, proceed | context-aware write or safe follow-up | op=None | PASS |  |
| 4263 | F | okay, interesting, tell me more | context-aware write or safe follow-up | op=query | PASS |  |
| 4264 | F | yeah, continue | context-aware write or safe follow-up | op=store fact='I plan a trip to Mexico City' | PASS | followup auto-wrote (review): op=store fact='I plan a trip to Mexico City' |
| 4265 | F | yeah, makes sense | context-aware write or safe follow-up | op=None | PASS |  |
| 4266 | F | and then what | context-aware write or safe follow-up | op=None | PASS |  |
| 4267 | F | right | context-aware write or safe follow-up | op=None | PASS |  |
| 4268 | F | yeah, right | context-aware write or safe follow-up | op=None | PASS |  |
| 4269 | F | okay, yes | context-aware write or safe follow-up | op=None | PASS |  |
| 427 | A | my favorite city is nairobi | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4270 | F | yeah, so what about it | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4271 | F | okay, yes please | context-aware write or safe follow-up | op=None | PASS |  |
| 4272 | F | yeah, you were saying | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4273 | F | okay, tell me | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4274 | F | okay, ok go on | context-aware write or safe follow-up | op=store fact='I need help with my ethics homework' | PASS | followup auto-wrote (review): op=store fact='I need help with my ethics homework' |
| 4275 | F | okay, please go on | context-aware write or safe follow-up | op=query | PASS |  |
| 4276 | F | okay, please continue | context-aware write or safe follow-up | op=None | PASS |  |
| 4277 | F | okay, got it, go on | context-aware write or safe follow-up | op=None | PASS |  |
| 4278 | F | so, and then | context-aware write or safe follow-up | op=store fact='I want to learn embroidery' | PASS | followup auto-wrote (review): op=store fact='I want to learn embroidery' |
| 4279 | F | go on | context-aware write or safe follow-up | op=None | PASS |  |
| 428 | A | my favorite drink is matcha | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is matcha' | FAIL | store did not persist: status=needs_clarification present=False |
| 4280 | F | so, go ahead | context-aware write or safe follow-up | op=store fact='I need help with my software testing homework' | PASS | followup auto-wrote (review): op=store fact='I need help with my software testing homework' |
| 4281 | F | yeah, tell me more | context-aware write or safe follow-up | op=store fact='I am planning a trip to Buenos Aires' | PASS | followup auto-wrote (review): op=store fact='I am planning a trip to Buenos Aires' |
| 4282 | F | alright | context-aware write or safe follow-up | op=None | PASS |  |
| 4283 | F | yes please | context-aware write or safe follow-up | op=store fact='I plan a trip to Casablanca' | PASS | followup auto-wrote (review): op=store fact='I plan a trip to Casablanca' |
| 4284 | F | yes | context-aware write or safe follow-up | op=None | PASS |  |
| 4285 | F | i see, continue | context-aware write or safe follow-up | op=store fact='I study B.Tech' | PASS | followup auto-wrote (review): op=store fact='I study B.Tech' |
| 4286 | F | so, what else | context-aware write or safe follow-up | op=None | PASS |  |
| 4287 | F | yeah, interesting, tell me more | context-aware write or safe follow-up | op=query | PASS |  |
| 4288 | F | so, you were saying | context-aware write or safe follow-up | op=store fact='I need help with my geometry homework' | PASS | followup auto-wrote (review): op=store fact='I need help with my geometry homework' |
| 4289 | F | okay, alright continue | context-aware write or safe follow-up | op=store fact='I plan a trip to Barcelona' | PASS | followup auto-wrote (review): op=store fact='I plan a trip to Barcelona' |
| 429 | A | my favorite show is the mandalorian | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4290 | F | so, alright continue | context-aware write or safe follow-up | op=None | PASS |  |
| 4291 | F | please continue | context-aware write or safe follow-up | op=None | PASS |  |
| 4292 | F | so, umm | context-aware write or safe follow-up | op=None | PASS |  |
| 4293 | F | so, anyway | context-aware write or safe follow-up | op=None | PASS |  |
| 4294 | F | sure | context-aware write or safe follow-up | op=None | PASS |  |
| 4295 | F | okay, right | context-aware write or safe follow-up | op=None | PASS |  |
| 4296 | F | okay, yeah go ahead | context-aware write or safe follow-up | op=None | PASS |  |
| 4297 | F | yes, go on | context-aware write or safe follow-up | op=store fact='I study btag' | PASS | followup auto-wrote (review): op=store fact='I study btag' |
| 4298 | F | ok go on | context-aware write or safe follow-up | op=store fact='I plan a trip to Lagos' | PASS | followup auto-wrote (review): op=store fact='I plan a trip to Lagos' |
| 4299 | F | yeah, alright | context-aware write or safe follow-up | op=None | PASS |  |
| 43 | A | my favorite animal is alligator | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 430 | A | my favorite writer is mark twain | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4300 | G | hmm, i'm off for now | no write (session/meta) | op=None es=False | PASS |  |
| 4301 | G | yeah, drop the subject | no write (session/meta) | op=None es=False | PASS |  |
| 4302 | G | um, this session is over | no write (session/meta) | op=None es=False | PASS |  |
| 4303 | G | um, skip this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4304 | G | so, that's it for now | no write (session/meta) | op=None es=True | PASS |  |
| 4305 | G | so, i'm off for now | no write (session/meta) | op=None es=True | PASS |  |
| 4306 | G | good night | no write (session/meta) | op=None es=None | PASS |  |
| 4307 | G | so, end session | no write (session/meta) | op=None es=False | PASS |  |
| 4308 | G | hmm, i'm turning in for the night | no write (session/meta) | op=None es=True | PASS |  |
| 4309 | G | so, go offline now | no write (session/meta) | op=None es=True | PASS |  |
| 431 | A | my birthday is in august | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 4310 | G | okay, i'm off for now | no write (session/meta) | op=None es=True | PASS |  |
| 4311 | G | so, lets wrap up for today | no write (session/meta) | op=None es=True | PASS |  |
| 4312 | G | hmm, that is enough about that | no write (session/meta) | op=None es=False | PASS |  |
| 4313 | G | yeah, lets call it a day | no write (session/meta) | op=None es=True | PASS |  |
| 4314 | G | night night | no write (session/meta) | op=None es=True | PASS |  |
| 4315 | G | um, can we talk about something else | no write (session/meta) | op=None es=False | PASS |  |
| 4316 | G | hmm, never mind that | no write (session/meta) | op=None es=False | PASS |  |
| 4317 | G | um, that's it for now | no write (session/meta) | op=None es=True | PASS |  |
| 4318 | G | okay, shutting down now | no write (session/meta) | op=None es=True | PASS |  |
| 4319 | G | hmm, lets wrap up for today | no write (session/meta) | op=None es=False | PASS |  |
| 432 | A | my favorite city is stockholm | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4320 | G | yeah, lets wrap up for today | no write (session/meta) | op=None es=True | PASS |  |
| 4321 | G | so, i am done talking | no write (session/meta) | op=None es=True | PASS |  |
| 4322 | G | hmm, okay i am done | no write (session/meta) | op=None es=True | PASS |  |
| 4323 | G | hmm, i am ending this session | no write (session/meta) | op=None es=False | PASS |  |
| 4324 | G | um, thats enough for me today | no write (session/meta) | op=None es=True | PASS |  |
| 4325 | G | yeah, skip that | no write (session/meta) | op=None es=False | PASS |  |
| 4326 | G | hmm, skip this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4327 | G | never mind that | no write (session/meta) | op=None es=False | PASS |  |
| 4328 | G | yeah, enough for today | no write (session/meta) | op=None es=True | PASS |  |
| 4329 | G | enough for today | no write (session/meta) | op=None es=True | PASS |  |
| 433 | A | my favorite hobby is bird watching | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4330 | G | okay, leave that topic | no write (session/meta) | op=None es=False | PASS |  |
| 4331 | G | um, good night | no write (session/meta) | op=None es=None | PASS |  |
| 4332 | G | lets drop it | no write (session/meta) | op=None es=True | PASS |  |
| 4333 | G | hmm, good night | no write (session/meta) | op=None es=None | PASS |  |
| 4334 | G | yeah, leave that topic | no write (session/meta) | op=None es=False | PASS |  |
| 4335 | G | so, set that aside | no write (session/meta) | op=store es=False | FAIL | session-end/dismissal wrote: op=store fact="I want to set aside the conversation about my laptop's GPU." |
| 4336 | G | so, lets change the subject | no write (session/meta) | op=None es=False | PASS |  |
| 4337 | G | sleep | no write (session/meta) | op=None es=True | PASS |  |
| 4338 | G | yeah, night night | no write (session/meta) | op=None es=True | PASS |  |
| 4339 | G | so, turn off | no write (session/meta) | op=None es=True | PASS |  |
| 434 | A | my favorite show is fleabag | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4340 | G | okay, this session is over | no write (session/meta) | op=None es=True | PASS |  |
| 4341 | G | okay, terminate session | no write (session/meta) | op=None es=False | PASS |  |
| 4342 | G | moving on | no write (session/meta) | op=None es=False | PASS |  |
| 4343 | G | that is enough about that | no write (session/meta) | op=None es=True | PASS |  |
| 4344 | G | um, set that aside | no write (session/meta) | op=store es=False | FAIL | session-end/dismissal wrote: op=store fact='I study B.Tech' |
| 4345 | G | okay, that is enough about that | no write (session/meta) | op=None es=True | PASS |  |
| 4346 | G | um, i am ending this session | no write (session/meta) | op=None es=False | PASS |  |
| 4347 | G | drop this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4348 | G | time to sleep | no write (session/meta) | op=None es=True | PASS |  |
| 4349 | G | i am done talking | no write (session/meta) | op=None es=True | PASS |  |
| 435 | A | my favorite color is lilac | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 4350 | G | so, that topic is over | no write (session/meta) | op=None es=False | PASS |  |
| 4351 | G | okay, goodbye | no write (session/meta) | op=None es=None | PASS |  |
| 4352 | G | goodbye | no write (session/meta) | op=None es=None | PASS |  |
| 4353 | G | um, sleep | no write (session/meta) | op=None es=True | PASS |  |
| 4354 | G | hmm, move on | no write (session/meta) | op=None es=False | PASS |  |
| 4355 | G | um, shutting down now | no write (session/meta) | op=None es=False | PASS |  |
| 4356 | G | okay, miss this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4357 | G | this session is over | no write (session/meta) | op=None es=False | PASS |  |
| 4358 | G | um, skip that | no write (session/meta) | op=None es=False | PASS |  |
| 4359 | G | so, good night | no write (session/meta) | op=None es=None | PASS |  |
| 436 | A | my favorite game is fallout new vegas | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4360 | G | yeah, stop listening | no write (session/meta) | op=None es=False | PASS |  |
| 4361 | G | hmm, i need to rest now | no write (session/meta) | op=store es=False | FAIL | session-end/dismissal wrote: op=store fact='I need to rest now' |
| 4362 | G | um, i need to rest now | no write (session/meta) | op=None es=False | PASS |  |
| 4363 | G | lets call it a day | no write (session/meta) | op=None es=True | PASS |  |
| 4364 | G | yeah, dont talk about that anymore | no write (session/meta) | op=None es=False | PASS |  |
| 4365 | G | go offline now | no write (session/meta) | op=None es=True | PASS |  |
| 4366 | G | set that aside | no write (session/meta) | op=store es=False | FAIL | session-end/dismissal wrote: op=store fact='I set that aside' |
| 4367 | G | hmm, change the topic | no write (session/meta) | op=None es=False | PASS |  |
| 4368 | G | so, shutting down now | no write (session/meta) | op=None es=True | PASS |  |
| 4369 | G | so, drop it | no write (session/meta) | op=None es=False | PASS |  |
| 437 | A | my favorite city is florence | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4370 | G | i am ending this session | no write (session/meta) | op=None es=False | PASS |  |
| 4371 | G | hmm, stop the session | no write (session/meta) | op=None es=False | PASS |  |
| 4372 | G | so, lets drop it | no write (session/meta) | op=None es=True | PASS |  |
| 4373 | G | yeah, goodbye | no write (session/meta) | op=None es=None | PASS |  |
| 4374 | G | yeah, set that aside | no write (session/meta) | op=update es=False | FAIL | session-end/dismissal wrote: op=update fact='My favorite editor is PyCharm' |
| 4375 | G | um, stop listening | no write (session/meta) | op=None es=False | PASS |  |
| 4376 | G | so, miss this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4377 | G | terminate session | no write (session/meta) | op=None es=False | PASS |  |
| 4378 | G | um, let me go | no write (session/meta) | op=None es=False | PASS |  |
| 4379 | G | so, leave that topic | no write (session/meta) | op=None es=False | PASS |  |
| 438 | A | i am from caracas | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 4380 | G | yeah, i'm turning in for the night | no write (session/meta) | op=None es=True | PASS |  |
| 4381 | G | turn off | no write (session/meta) | op=None es=True | PASS |  |
| 4382 | G | hmm, time to power down | no write (session/meta) | op=None es=True | PASS |  |
| 4383 | G | hmm, see you | no write (session/meta) | op=None es=False | PASS |  |
| 4384 | G | hmm, this session is over | no write (session/meta) | op=None es=False | PASS |  |
| 4385 | G | so, power down | no write (session/meta) | op=None es=True | PASS |  |
| 4386 | G | okay, lets switch topics | no write (session/meta) | op=None es=False | PASS |  |
| 4387 | G | hmm, i am going to sleep now | no write (session/meta) | op=None es=True | PASS |  |
| 4388 | G | okay, drop it | no write (session/meta) | op=None es=False | PASS |  |
| 4389 | G | um, i'm turning in for the night | no write (session/meta) | op=None es=True | PASS |  |
| 439 | A | my favorite city is budapest | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4390 | G | i am done with this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4391 | G | yeah, i am done with this topic | no write (session/meta) | op=None es=True | PASS |  |
| 4392 | G | um, i am done with this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4393 | G | yeah, i am done talking | no write (session/meta) | op=None es=True | PASS |  |
| 4394 | G | yeah, turn off | no write (session/meta) | op=None es=True | PASS |  |
| 4395 | G | okay, can we talk about something else | no write (session/meta) | op=None es=False | PASS |  |
| 4396 | G | um, stop the session | no write (session/meta) | op=None es=False | PASS |  |
| 4397 | G | um, power down | no write (session/meta) | op=store es=False | FAIL | session-end/dismissal wrote: op=store fact='My laptop has an RTX 4050' |
| 4398 | G | okay, we're done here | no write (session/meta) | op=None es=True | PASS |  |
| 4399 | G | yeah, forget this topic | no write (session/meta) | op=None es=False | PASS |  |
| 44 | A | my favorite cuisine is pakistani | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 440 | A | my favorite writer is leo tolstoy | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4400 | G | um, night night | no write (session/meta) | op=None es=True | PASS |  |
| 4401 | G | um, moving on | no write (session/meta) | op=None es=False | PASS |  |
| 4402 | G | so, move on | no write (session/meta) | op=None es=False | PASS |  |
| 4403 | G | so, exit | no write (session/meta) | op=None es=True | PASS |  |
| 4404 | G | hmm, exit | no write (session/meta) | op=None es=False | PASS |  |
| 4405 | G | so, i am done | no write (session/meta) | op=None es=True | PASS |  |
| 4406 | G | yeah, i am ending this session | no write (session/meta) | op=None es=False | PASS |  |
| 4407 | G | hmm, moving on | no write (session/meta) | op=None es=False | PASS |  |
| 4408 | G | so, signing off | no write (session/meta) | op=None es=True | PASS |  |
| 4409 | G | yeah, moving on | no write (session/meta) | op=None es=False | PASS |  |
| 441 | A | my favorite show is dark | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4410 | G | yeah, never mind that | no write (session/meta) | op=None es=False | PASS |  |
| 4411 | G | um, okay i am done | no write (session/meta) | op=None es=True | PASS |  |
| 4412 | G | lets switch topics | no write (session/meta) | op=None es=False | PASS |  |
| 4413 | G | hmm, drop this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4414 | G | see you | no write (session/meta) | op=None es=False | PASS |  |
| 4415 | G | so, i am done with this topic | no write (session/meta) | op=None es=True | PASS |  |
| 4416 | G | so, okay i am done | no write (session/meta) | op=None es=True | PASS |  |
| 4417 | G | so, drop the subject | no write (session/meta) | op=None es=False | PASS |  |
| 4418 | G | hmm, skip that | no write (session/meta) | op=None es=False | PASS |  |
| 4419 | G | um, i am logging off | no write (session/meta) | op=None es=False | PASS |  |
| 442 | A | i work as a barista | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 4420 | G | okay, that's it for now | no write (session/meta) | op=None es=True | PASS |  |
| 4421 | G | okay, never mind that | no write (session/meta) | op=None es=False | PASS |  |
| 4422 | G | can we talk about something else | no write (session/meta) | op=None es=False | PASS |  |
| 4423 | G | yeah, stop the session | no write (session/meta) | op=None es=False | PASS |  |
| 4424 | G | um, dismiss this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4425 | G | so, terminate session | no write (session/meta) | op=None es=False | PASS |  |
| 4426 | G | yeah, signing off | no write (session/meta) | op=None es=True | PASS |  |
| 4427 | G | yeah, drop it | no write (session/meta) | op=None es=False | PASS |  |
| 4428 | G | um, that is enough about that | no write (session/meta) | op=None es=True | PASS |  |
| 4429 | G | yeah, that's it for now | no write (session/meta) | op=None es=True | PASS |  |
| 443 | A | my favorite sport is archery | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4430 | G | hmm, i am going to rest | no write (session/meta) | op=store es=False | FAIL | session-end/dismissal wrote: op=store fact='I will rest' |
| 4431 | G | so, stop the session | no write (session/meta) | op=None es=False | PASS |  |
| 4432 | G | yeah, i am done for today | no write (session/meta) | op=None es=True | PASS |  |
| 4433 | G | um, i am going to rest | no write (session/meta) | op=None es=False | PASS |  |
| 4434 | G | hmm, shutting down now | no write (session/meta) | op=None es=False | PASS |  |
| 4435 | G | um, leave that topic | no write (session/meta) | op=None es=False | PASS |  |
| 4436 | G | okay, change the topic | no write (session/meta) | op=None es=False | PASS |  |
| 4437 | G | hmm, power down | no write (session/meta) | op=store es=False | FAIL | session-end/dismissal wrote: op=store fact='My laptop has an RTX 4050' |
| 4438 | G | hmm, stop listening | no write (session/meta) | op=None es=False | PASS |  |
| 4439 | G | hmm, end session | no write (session/meta) | op=None es=False | PASS |  |
| 444 | A | my favorite hobby is rock climbing | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4440 | G | yeah, i am going to rest | no write (session/meta) | op=store es=False | FAIL | session-end/dismissal wrote: op=store fact='I will rest' |
| 4441 | G | hmm, sleep | no write (session/meta) | op=store es=False | FAIL | session-end/dismissal wrote: op=store fact='I need to sleep' |
| 4442 | G | so, sleep | no write (session/meta) | op=None es=True | PASS |  |
| 4443 | G | so, i'm turning in for the night | no write (session/meta) | op=None es=True | PASS |  |
| 4444 | G | so, never mind that | no write (session/meta) | op=None es=False | PASS |  |
| 4445 | G | yeah, thats enough for me today | no write (session/meta) | op=None es=True | PASS |  |
| 4446 | G | so, moving on | no write (session/meta) | op=None es=False | PASS |  |
| 4447 | G | yeah, i am logging off | no write (session/meta) | op=None es=False | PASS |  |
| 4448 | G | um, turn off | no write (session/meta) | op=None es=True | PASS |  |
| 4449 | G | yeah, that topic is over | no write (session/meta) | op=None es=False | PASS |  |
| 445 | A | my favorite animal is otter | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4450 | G | dont talk about that anymore | no write (session/meta) | op=None es=False | PASS |  |
| 4451 | G | shelve this topic | no write (session/meta) | op=store es=False | FAIL | session-end/dismissal wrote: op=store fact="I want to shelve the topic of my laptop's GPU" |
| 4452 | G | bye | no write (session/meta) | op=None es=None | PASS |  |
| 4453 | G | yeah, okay i am done | no write (session/meta) | op=None es=True | PASS |  |
| 4454 | G | yeah, miss this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4455 | G | hmm, signing off | no write (session/meta) | op=None es=False | PASS |  |
| 4456 | G | that's it for now | no write (session/meta) | op=None es=True | PASS |  |
| 4457 | G | so, we're done here | no write (session/meta) | op=None es=True | PASS |  |
| 4458 | G | thats enough for me today | no write (session/meta) | op=None es=True | PASS |  |
| 4459 | G | so, skip that | no write (session/meta) | op=None es=False | PASS |  |
| 446 | A | my favorite book is the color purple | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4460 | G | yeah, lets move past this | no write (session/meta) | op=None es=False | PASS |  |
| 4461 | G | hmm, lets change the subject | no write (session/meta) | op=None es=False | PASS |  |
| 4462 | G | yeah, lets drop it | no write (session/meta) | op=None es=True | PASS |  |
| 4463 | G | so, that is enough about that | no write (session/meta) | op=None es=True | PASS |  |
| 4464 | G | yeah, shutting down now | no write (session/meta) | op=None es=True | PASS |  |
| 4465 | G | so, i am logging off | no write (session/meta) | op=None es=False | PASS |  |
| 4466 | G | power down | no write (session/meta) | op=None es=True | PASS |  |
| 4467 | G | yeah, good night | no write (session/meta) | op=None es=None | PASS |  |
| 4468 | G | drop the subject | no write (session/meta) | op=None es=False | PASS |  |
| 4469 | G | okay, sleep | no write (session/meta) | op=None es=True | PASS |  |
| 447 | A | my favorite city is manchester | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4470 | G | hmm, i am done with this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4471 | G | um, time to sleep | no write (session/meta) | op=None es=True | PASS |  |
| 4472 | G | so, lets call it a day | no write (session/meta) | op=None es=True | PASS |  |
| 4473 | G | um, drop this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4474 | G | um, lets call it a day | no write (session/meta) | op=None es=True | PASS |  |
| 4475 | G | so, stop listening | no write (session/meta) | op=None es=False | PASS |  |
| 4476 | G | skip that | no write (session/meta) | op=None es=False | PASS |  |
| 4477 | G | um, that's all for today | no write (session/meta) | op=None es=True | PASS |  |
| 4478 | G | shutting down now | no write (session/meta) | op=None es=True | PASS |  |
| 4479 | G | okay, shut down | no write (session/meta) | op=None es=True | PASS |  |
| 448 | A | i am from lisbon | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 4480 | G | i am done | no write (session/meta) | op=None es=True | PASS |  |
| 4481 | G | skip this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4482 | G | so, time to sleep | no write (session/meta) | op=None es=True | PASS |  |
| 4483 | G | that's all for today | no write (session/meta) | op=None es=True | PASS |  |
| 4484 | G | okay, drop this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4485 | G | okay, i am going to sleep now | no write (session/meta) | op=None es=True | PASS |  |
| 4486 | G | um, change the topic | no write (session/meta) | op=None es=False | PASS |  |
| 4487 | G | okay, signing off | no write (session/meta) | op=None es=True | PASS |  |
| 4488 | G | so, going offline | no write (session/meta) | op=None es=True | PASS |  |
| 4489 | G | um, go offline now | no write (session/meta) | op=store es=False | FAIL | session-end/dismissal wrote: op=store fact='I want to go offline' |
| 449 | A | my favorite dessert is mousse | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4490 | G | move on | no write (session/meta) | op=None es=False | PASS |  |
| 4491 | G | i am going to sleep now | no write (session/meta) | op=None es=True | PASS |  |
| 4492 | G | yeah, i'm off for now | no write (session/meta) | op=None es=True | PASS |  |
| 4493 | G | okay, that topic is over | no write (session/meta) | op=None es=False | PASS |  |
| 4494 | G | um, signing off | no write (session/meta) | op=None es=True | PASS |  |
| 4495 | G | hmm, turn off | no write (session/meta) | op=store es=False | FAIL | session-end/dismissal wrote: op=store fact='I want to turn off the device' |
| 4496 | G | okay, time to power down | no write (session/meta) | op=None es=True | PASS |  |
| 4497 | G | hmm, on a different note | no write (session/meta) | op=None es=False | PASS |  |
| 4498 | G | yeah, lets switch topics | no write (session/meta) | op=None es=False | PASS |  |
| 4499 | G | hmm, set that aside | no write (session/meta) | op=store es=False | FAIL | session-end/dismissal wrote: op=store fact='I will set the conversation aside for now' |
| 45 | A | my favorite fruit is plum | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 450 | A | my favorite dessert is funnel cake | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4500 | G | i am going to rest | no write (session/meta) | op=store es=False | FAIL | session-end/dismissal wrote: op=store fact='I will rest' |
| 4501 | G | okay, i am done with this topic | no write (session/meta) | op=None es=True | PASS |  |
| 4502 | G | hmm, drop the subject | no write (session/meta) | op=None es=False | PASS |  |
| 4503 | G | yeah, can we talk about something else | no write (session/meta) | op=None es=False | PASS |  |
| 4504 | G | okay, i am done | no write (session/meta) | op=None es=True | PASS |  |
| 4505 | G | um, forget this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4506 | G | okay, dismiss this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4507 | G | lets change the subject | no write (session/meta) | op=None es=False | PASS |  |
| 4508 | G | so, i am going to rest | no write (session/meta) | op=None es=True | PASS |  |
| 4509 | G | yeah, i am done | no write (session/meta) | op=None es=True | PASS |  |
| 451 | A | my favorite book is educated | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4510 | G | yeah, i need to rest now | no write (session/meta) | op=None es=False | PASS |  |
| 4511 | G | so, this session is over | no write (session/meta) |  | ERROR | analyze failed: (None, None) |
| 4512 | G | um, i am done for today | no write (session/meta) | op=None es=True | PASS |  |
| 4513 | G | yeah, i am going to sleep now | no write (session/meta) | op=None es=True | PASS |  |
| 4514 | G | um, that topic is over | no write (session/meta) | op=None es=False | PASS |  |
| 4515 | G | hmm, dont talk about that anymore | no write (session/meta) | op=None es=False | PASS |  |
| 4516 | G | so, drop this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4517 | G | so, lets move past this | no write (session/meta) | op=None es=False | PASS |  |
| 4518 | G | yeah, drop this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4519 | G | drop it | no write (session/meta) | op=None es=False | PASS |  |
| 452 | A | my favorite sport is golf | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4520 | G | stop listening | no write (session/meta) | op=forget es=False | PASS |  |
| 4521 | G | yeah, sleep | no write (session/meta) | op=None es=True | PASS |  |
| 4522 | G | um, i am done talking | no write (session/meta) | op=None es=True | PASS |  |
| 4523 | G | okay, bye | no write (session/meta) | op=None es=None | PASS |  |
| 4524 | G | okay, skip this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4525 | G | yeah, move on | no write (session/meta) | op=None es=False | PASS |  |
| 4526 | G | so, see you | no write (session/meta) | op=None es=False | PASS |  |
| 4527 | G | okay, i am done for today | no write (session/meta) | op=None es=True | PASS |  |
| 4528 | G | um, lets wrap up for today | no write (session/meta) | op=None es=False | PASS |  |
| 4529 | G | okay, that's all for today | no write (session/meta) | op=None es=True | PASS |  |
| 453 | A | my favorite food is thai curry | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4530 | G | um, lets move past this | no write (session/meta) | op=None es=False | PASS |  |
| 4531 | G | okay, turn off | no write (session/meta) | op=None es=True | PASS |  |
| 4532 | G | okay, power down | no write (session/meta) | op=None es=True | PASS |  |
| 4533 | G | hmm, leave that topic | no write (session/meta) | op=None es=False | PASS |  |
| 4534 | G | hmm, miss this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4535 | G | so, shut down | no write (session/meta) | op=None es=True | PASS |  |
| 4536 | G | yeah, terminate session | no write (session/meta) | op=None es=False | PASS |  |
| 4537 | G | so, can we talk about something else | no write (session/meta) | op=None es=False | PASS |  |
| 4538 | G | hmm, lets call it a day | no write (session/meta) | op=None es=True | PASS |  |
| 4539 | G | hmm, shut down | no write (session/meta) | op=store es=False | FAIL | session-end/dismissal wrote: op=store fact='My laptop has an RTX 4050' |
| 454 | A | i work as a potter | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 4540 | G | yeah, see you | no write (session/meta) | op=None es=False | PASS |  |
| 4541 | G | yeah, skip this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4542 | G | so, on a different note | no write (session/meta) | op=None es=False | PASS |  |
| 4543 | G | okay, stop listening | no write (session/meta) | op=None es=False | PASS |  |
| 4544 | G | yeah, go offline now | no write (session/meta) | op=None es=True | PASS |  |
| 4545 | G | so, thats enough for me today | no write (session/meta) | op=None es=True | PASS |  |
| 4546 | G | um, drop the subject | no write (session/meta) | op=None es=False | PASS |  |
| 4547 | G | so, shelve this topic | no write (session/meta) | op=store es=False | FAIL | session-end/dismissal wrote: op=store fact="I don't want to discuss the RTX 4050 anymore" |
| 4548 | G | yeah, bye | no write (session/meta) | op=None es=None | PASS |  |
| 4549 | G | that topic is over | no write (session/meta) | op=None es=False | PASS |  |
| 455 | A | my favorite fruit is guava | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4550 | G | okay, i am ending this session | no write (session/meta) | op=None es=False | PASS |  |
| 4551 | G | hmm, forget this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4552 | G | exit | no write (session/meta) | op=None es=True | PASS |  |
| 4553 | G | okay, let me go | no write (session/meta) | op=None es=True | PASS |  |
| 4554 | G | yeah, dismiss this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4555 | G | um, drop it | no write (session/meta) | op=None es=False | PASS |  |
| 4556 | G | okay, good night | no write (session/meta) | op=None es=None | PASS |  |
| 4557 | G | yeah, time to power down | no write (session/meta) | op=None es=True | PASS |  |
| 4558 | G | on a different note | no write (session/meta) | op=None es=False | PASS |  |
| 4559 | G | um, dont talk about that anymore | no write (session/meta) | op=None es=False | PASS |  |
| 456 | A | my favorite sport is swimming | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4560 | G | hmm, let me go | no write (session/meta) | op=store es=False | FAIL | session-end/dismissal wrote: op=store fact='I study btag' |
| 4561 | G | i am logging off | no write (session/meta) | op=None es=False | PASS |  |
| 4562 | G | going offline | no write (session/meta) | op=None es=True | PASS |  |
| 4563 | G | um, shelve this topic | no write (session/meta) | op=store es=False | FAIL | session-end/dismissal wrote: op=store fact='I want to shelve the conversation about btag' |
| 4564 | G | hmm, bye | no write (session/meta) | op=None es=None | PASS |  |
| 4565 | G | um, going offline | no write (session/meta) | op=None es=True | PASS |  |
| 4566 | G | okay, okay i am done | no write (session/meta) | op=None es=True | PASS |  |
| 4567 | G | um, miss this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4568 | G | um, enough for today | no write (session/meta) | op=None es=True | PASS |  |
| 4569 | G | yeah, going offline | no write (session/meta) | op=None es=True | PASS |  |
| 457 | A | my favorite color is graphite | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4570 | G | dismiss this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4571 | G | stop the session | no write (session/meta) | op=None es=False | PASS |  |
| 4572 | G | yeah, exit | no write (session/meta) | op=None es=True | PASS |  |
| 4573 | G | so, that's all for today | no write (session/meta) | op=None es=True | PASS |  |
| 4574 | G | hmm, terminate session | no write (session/meta) | op=None es=False | PASS |  |
| 4575 | G | hmm, thats enough for me today | no write (session/meta) | op=None es=True | PASS |  |
| 4576 | G | hmm, dismiss this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4577 | G | okay, exit | no write (session/meta) | op=None es=True | PASS |  |
| 4578 | G | i'm turning in for the night | no write (session/meta) | op=None es=True | PASS |  |
| 4579 | G | hmm, going offline | no write (session/meta) | op=None es=True | PASS |  |
| 458 | A | my favorite music is mariachi | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4580 | G | okay, time to sleep | no write (session/meta) | op=None es=True | PASS |  |
| 4581 | G | so, dismiss this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4582 | G | okay, enough for today | no write (session/meta) | op=None es=True | PASS |  |
| 4583 | G | um, terminate session | no write (session/meta) | op=None es=False | PASS |  |
| 4584 | G | okay, night night | no write (session/meta) | op=None es=True | PASS |  |
| 4585 | G | yeah, power down | no write (session/meta) | op=None es=True | PASS |  |
| 4586 | G | um, lets drop it | no write (session/meta) | op=None es=False | PASS |  |
| 4587 | G | okay, go offline now | no write (session/meta) | op=None es=True | PASS |  |
| 4588 | G | forget this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4589 | G | hmm, i am done for today | no write (session/meta) | op=None es=True | PASS |  |
| 459 | A | my favorite fruit is kumquat | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4590 | G | so, let me go | no write (session/meta) | op=None es=True | PASS |  |
| 4591 | G | okay, set that aside | no write (session/meta) | op=store es=False | FAIL | session-end/dismissal wrote: op=store fact='I want to set aside the previous conversation' |
| 4592 | G | um, we're done here | no write (session/meta) | op=None es=False | PASS |  |
| 4593 | G | okay i am done | no write (session/meta) | op=None es=True | PASS |  |
| 4594 | G | okay, skip that | no write (session/meta) | op=None es=False | PASS |  |
| 4595 | G | okay, end session | no write (session/meta) | op=None es=True | PASS |  |
| 4596 | G | okay, dont talk about that anymore | no write (session/meta) | op=None es=False | PASS |  |
| 4597 | G | okay, shelve this topic | no write (session/meta) | op=None es=False | PASS |  |
| 4598 | G | so, enough for today | no write (session/meta) | op=None es=True | PASS |  |
| 4599 | G | okay, going offline | no write (session/meta) | op=None es=True | PASS |  |
| 46 | A | my favorite book is their eyes were watching god | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 460 | A | i work as a data analyst | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 4600 | H | my favorite music genre is industrial | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4601 | H | my favorite music genre is trip hop | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4602 | H | my favorite music genre is edm | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4603 | H | my favorite music genre is r&b | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4604 | H | my favorite music genre is house | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4605 | H | my favorite music genre is minimalism | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4606 | H | my favorite music genre is country | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4607 | H | my favorite music genre is techno | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4608 | H | my favorite music genre is gospel | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4609 | H | my favorite music genre is ska | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 461 | A | my favorite drink is hot chocolate | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4610 | H | my favorite music genre is qawwali | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4611 | H | my favorite music genre is lo-fi | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4612 | H | my favorite music genre is soukous | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4613 | H | my favorite music genre is indie | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4614 | H | my favorite music genre is folk | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4615 | H | my favorite music genre is metal | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4616 | H | my favorite music genre is grime | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4617 | H | my favorite music genre is pop | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4618 | H | my favorite music genre is k-pop | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4619 | H | my favorite music genre is flamenco | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 462 | A | my favorite drink is cream soda | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4620 | H | my favorite music genre is bluegrass | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4621 | H | my favorite music genre is post rock | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4622 | H | my favorite music genre is carnatic | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4623 | H | my favorite music genre is gothic | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4624 | H | my favorite music genre is synthwave | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4625 | H | my favorite music genre is reggae | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4626 | H | my favorite music genre is hindustani | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4627 | H | my favorite music genre is mariachi | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4628 | H | my favorite music genre is salsa | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4629 | H | my favorite music genre is celtic | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 463 | A | my favorite cuisine is lebanese | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4630 | H | my favorite music genre is disco | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4631 | H | my favorite music genre is afrobeat | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4632 | H | my favorite music genre is bachata | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4633 | H | my favorite music genre is blues | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4634 | H | my favorite music genre is baroque | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4635 | H | my favorite music genre is soul | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4636 | H | my favorite music genre is bossa nova | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4637 | H | my favorite music genre is trance | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4638 | H | my favorite music genre is ghazal | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4639 | H | my favorite music genre is shoegaze | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 464 | A | my favorite music is carnatic | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4640 | H | my favorite music genre is punk | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4641 | H | my favorite music genre is chamber | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4642 | H | my favorite playlist is ghazal | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4643 | H | my favorite playlist is techno | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4644 | H | my favorite playlist is world music | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4645 | H | my favorite playlist is synthwave | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4646 | H | my favorite playlist is hindustani | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4647 | H | my favorite playlist is reggaeton | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4648 | H | my favorite playlist is post rock | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4649 | H | my favorite playlist is metal | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 465 | A | my favorite writer is tove jansson | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4650 | H | my favorite playlist is drum and bass | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4651 | H | my favorite playlist is blues | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4652 | H | my favorite playlist is soul | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4653 | H | my favorite playlist is shoegaze | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4654 | H | my favorite playlist is soukous | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4655 | H | my favorite playlist is noise | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4656 | H | my favorite playlist is rockabilly | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4657 | H | my favorite playlist is chamber | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4658 | H | my favorite playlist is bachata | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4659 | H | my favorite playlist is carnatic | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 466 | A | my favorite animal is orangutan | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4660 | H | my favorite playlist is opera | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4661 | H | my favorite playlist is afrobeat | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4662 | H | my favorite playlist is dubstep | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4663 | H | my favorite playlist is funk | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4664 | H | my favorite playlist is lo-fi | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4665 | H | my favorite playlist is country | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4666 | H | my favorite playlist is celtic | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4667 | H | my favorite playlist is k-pop | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4668 | H | my favorite playlist is edm | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4669 | H | my favorite playlist is hip hop | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 467 | A | my favorite dessert is sponge cake | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4670 | H | my favorite playlist is gospel | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4671 | H | my favorite playlist is house | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4672 | H | my favorite playlist is pop | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4673 | H | my favorite playlist is bluegrass | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4674 | H | my favorite playlist is flamenco | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4675 | H | my favorite playlist is jazz | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4676 | H | my favorite playlist is salsa | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4677 | H | my favorite playlist is folk | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4678 | H | my favorite playlist is r&b | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4679 | H | my favorite playlist is disco | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 468 | A | my favorite writer is gabriel garcia marquez | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 4680 | H | my favorite playlist is new wave | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4681 | H | my favorite playlist is mariachi | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4682 | H | my favorite playlist is grime | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4683 | H | my favorite playlist is reggae | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4684 | H | my favorite singer is minimalism | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4685 | H | my favorite singer is ska | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4686 | H | my favorite singer is opera | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4687 | H | my favorite singer is edm | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4688 | H | my favorite singer is lo-fi | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4689 | H | my favorite singer is grime | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 469 | A | i work as a translator | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 4690 | H | my favorite singer is folk | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4691 | H | my favorite singer is world music | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4692 | H | my favorite singer is celtic | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4693 | H | my favorite singer is hindustani | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4694 | H | my favorite singer is chamber | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4695 | H | my favorite singer is classical | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4696 | H | my favorite singer is rockabilly | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4697 | H | my favorite singer is math rock | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4698 | H | my favorite singer is gothic | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4699 | H | my favorite singer is soukous | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 47 | A | my favorite sport is taekwondo | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 470 | A | my favorite sport is bouldering | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4700 | H | my favorite singer is new wave | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4701 | H | my favorite singer is reggae | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4702 | H | my favorite singer is techno | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4703 | H | my favorite singer is soul | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4704 | H | my favorite singer is shoegaze | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4705 | H | my favorite singer is indie | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4706 | H | my favorite singer is punk | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4707 | H | my favorite singer is rock | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4708 | H | my favorite singer is funk | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4709 | H | my favorite singer is synthwave | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 471 | A | my favorite cuisine is southern indian | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4710 | H | my favorite singer is baroque | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4711 | H | my favorite singer is post rock | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4712 | H | my favorite singer is hip hop | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4713 | H | my favorite singer is trance | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4714 | H | my favorite singer is bachata | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4715 | H | my favorite singer is industrial | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4716 | H | my favorite singer is carnatic | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4717 | H | my favorite singer is ghazal | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4718 | H | my favorite singer is bluegrass | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4719 | H | my favorite singer is r&b | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 472 | A | my favorite game is forza horizon | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4720 | H | my favorite singer is k-pop | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4721 | H | my favorite singer is bossa nova | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4722 | H | my favorite singer is mariachi | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4723 | H | my favorite singer is metal | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4724 | H | my favorite singer is flamenco | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4725 | H | my favorite singer is noise | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4726 | H | my favorite composer is noise | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4727 | H | my favorite composer is soukous | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4728 | H | my favorite composer is shoegaze | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4729 | H | my favorite composer is qawwali | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 473 | A | my favorite music is new wave | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4730 | H | my favorite composer is baroque | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4731 | H | my favorite composer is house | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4732 | H | my favorite composer is industrial | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4733 | H | my favorite composer is indie | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4734 | H | my favorite composer is bluegrass | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4735 | H | my favorite composer is highlife | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4736 | H | my favorite composer is techno | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4737 | H | my favorite composer is funk | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4738 | H | my favorite composer is ska | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4739 | H | my favorite composer is reggaeton | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 474 | A | my favorite hobby is board games | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4740 | H | my favorite composer is k-pop | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4741 | H | my favorite composer is punk | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4742 | H | my favorite composer is soul | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4743 | H | my favorite composer is reggae | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4744 | H | my favorite composer is celtic | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4745 | H | my favorite composer is bachata | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4746 | H | my favorite composer is disco | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4747 | H | my favorite composer is hip hop | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4748 | H | my favorite composer is math rock | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4749 | H | my favorite composer is flamenco | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 475 | A | i work as a lawyer | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 4750 | H | my favorite composer is rock | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4751 | H | my favorite composer is country | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4752 | H | my favorite composer is dubstep | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4753 | H | my favorite composer is hindustani | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4754 | H | my favorite composer is synthwave | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4755 | H | my favorite composer is salsa | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4756 | H | my favorite composer is carnatic | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4757 | H | my favorite composer is grime | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4758 | H | my favorite composer is opera | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4759 | H | my favorite composer is afrobeat | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 476 | A | my favorite color is silver | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4760 | H | my favorite composer is ghazal | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4761 | H | my favorite composer is metal | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4762 | H | my favorite composer is gospel | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4763 | H | my favorite composer is drum and bass | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4764 | H | my favorite composer is post rock | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4765 | H | my favorite composer is jazz | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4766 | H | my favorite composer is folk | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4767 | H | my favorite composer is trance | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4768 | H | my favorite album is techno | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4769 | H | my favorite album is math rock | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 477 | A | my favorite hobby is backgammon | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4770 | H | my favorite album is indie | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4771 | H | my favorite album is new wave | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4772 | H | my favorite album is salsa | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4773 | H | my favorite album is carnatic | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4774 | H | my favorite album is dubstep | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4775 | H | my favorite album is ambient | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4776 | H | my favorite album is edm | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4777 | H | my favorite album is rock | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4778 | H | my favorite album is blues | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4779 | H | my favorite album is world music | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 478 | A | my favorite cuisine is nepali | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4780 | H | my favorite album is jazz | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4781 | H | my favorite album is industrial | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4782 | H | my favorite album is reggaeton | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4783 | H | my favorite album is ghazal | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4784 | H | my favorite album is r&b | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4785 | H | my favorite album is rockabilly | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4786 | H | my favorite album is hip hop | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4787 | H | my favorite album is shoegaze | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4788 | H | my favorite album is soukous | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4789 | H | my favorite album is flamenco | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 479 | A | my favorite color is sage | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4790 | H | my favorite album is chamber | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4791 | H | my favorite album is soul | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4792 | H | my favorite album is house | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4793 | H | my favorite album is reggae | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4794 | H | my favorite album is gospel | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4795 | H | my favorite album is grime | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4796 | H | my favorite album is post rock | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4797 | H | my favorite album is bachata | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4798 | H | my favorite album is celtic | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4799 | H | my favorite album is trance | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 48 | A | my pet's name is daisy | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 480 | A | my favorite city is bangkok | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4800 | H | my favorite album is country | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4801 | H | my favorite album is k-pop | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4802 | H | my favorite album is gothic | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4803 | H | my favorite album is ska | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4804 | H | my favorite album is synthwave | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4805 | H | my favorite album is pop | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4806 | H | my favorite album is metal | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4807 | H | my favorite album is qawwali | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4808 | H | my favorite album is funk | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4809 | H | my favorite lyricist is metal | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 481 | A | my favorite fruit is date | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4810 | H | my favorite lyricist is reggae | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4811 | H | my favorite lyricist is gothic | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4812 | H | my favorite lyricist is bluegrass | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4813 | H | my favorite lyricist is dubstep | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4814 | H | my favorite lyricist is salsa | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4815 | H | my favorite lyricist is hindustani | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4816 | H | my favorite lyricist is country | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4817 | H | my favorite lyricist is house | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4818 | H | my favorite lyricist is mariachi | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4819 | H | my favorite lyricist is ghazal | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 482 | A | i work as a weaver | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 4820 | H | my favorite lyricist is qawwali | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4821 | H | my favorite lyricist is grime | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4822 | H | my favorite lyricist is r&b | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4823 | H | my favorite lyricist is gospel | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4824 | H | my favorite lyricist is classical | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4825 | H | my favorite lyricist is edm | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4826 | H | my favorite lyricist is trance | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4827 | H | my favorite lyricist is noise | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4828 | H | my favorite lyricist is celtic | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4829 | H | my favorite lyricist is ska | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 483 | A | my favorite drink is eggnog | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is eggnog' | FAIL | store did not persist: status=needs_clarification present=False |
| 4830 | H | my favorite lyricist is highlife | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4831 | H | my favorite lyricist is trip hop | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4832 | H | my favorite lyricist is punk | no write + history lookup | op=query use_memory=True hist=5 old_found=True | PASS |  |
| 4833 | H | my favorite lyricist is new wave | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4834 | H | my favorite lyricist is synthwave | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4835 | H | my favorite lyricist is bossa nova | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4836 | H | my favorite lyricist is shoegaze | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4837 | H | my favorite lyricist is jazz | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4838 | H | my favorite lyricist is k-pop | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4839 | H | my favorite lyricist is opera | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 484 | A | my favorite drink is badam milk | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is badam milk' | FAIL | store did not persist: status=needs_clarification present=False |
| 4840 | H | my favorite lyricist is rock | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4841 | H | my favorite lyricist is bachata | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4842 | H | my favorite lyricist is world music | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4843 | H | my favorite lyricist is soul | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4844 | H | my favorite lyricist is disco | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4845 | H | my favorite lyricist is flamenco | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4846 | H | my favorite lyricist is post rock | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4847 | H | my favorite lyricist is industrial | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4848 | H | my favorite lyricist is indie | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 4849 | H | my favorite lyricist is lo-fi | no write + history lookup | op=query use_memory=True hist=5 old_found=False | PASS |  |
| 485 | A | my favorite sport is rock climbing | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4850 | R-sem | my favorite appetizer is chow mein | retrieved (semantic) | use_memory=True results=1 hit='chow mein' | PASS |  |
| 4851 | R-sem | my favorite appetizer is thai curry | retrieved (semantic) | use_memory=True results=1 hit='thai curry' | PASS |  |
| 4852 | R-sem | my favorite appetizer is gnocchi | retrieved (semantic) | use_memory=True results=1 hit='gnocchi' | PASS |  |
| 4853 | R-sem | my favorite appetizer is hot pot | retrieved (semantic) | use_memory=True results=1 hit='hot pot' | PASS |  |
| 4854 | R-sem | my favorite appetizer is ramen | retrieved (semantic) | use_memory=True results=1 hit='ramen' | PASS |  |
| 4855 | R-sem | my favorite appetizer is sandwich | retrieved (semantic) | use_memory=True results=1 hit='sandwich' | PASS |  |
| 4856 | R-sem | my favorite appetizer is nachos | retrieved (semantic) | use_memory=True results=1 hit='nachos' | PASS |  |
| 4857 | R-sem | my favorite appetizer is calamari | retrieved (semantic) | use_memory=True results=1 hit='calamari' | PASS |  |
| 4858 | R-sem | my favorite appetizer is oysters | retrieved (semantic) | use_memory=True results=1 hit='oysters' | PASS |  |
| 4859 | R-sem | my favorite appetizer is falafel | retrieved (semantic) | use_memory=True results=1 hit='falafel' | PASS |  |
| 486 | A | i am from brussels | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 4860 | R-sem | my favorite salad is korean bbq | retrieved (semantic) | results=0 retrieved=[] | FAIL | stored fact not retrieved (use_memory=True) |
| 4861 | R-sem | my favorite salad is idli | retrieved (semantic) | use_memory=True results=1 hit='idli' | PASS |  |
| 4862 | R-sem | my favorite salad is coleslaw | retrieved (semantic) | use_memory=True results=1 hit='coleslaw' | PASS |  |
| 4863 | R-sem | my favorite salad is sushi | retrieved (semantic) | use_memory=True results=1 hit='sushi' | PASS |  |
| 4864 | R-sem | my favorite salad is empanadas | retrieved (semantic) | use_memory=True results=1 hit='empanadas' | PASS |  |
| 4865 | R-sem | my favorite salad is butter chicken | retrieved (semantic) | results=0 retrieved=[] | FAIL | stored fact not retrieved (use_memory=True) |
| 4866 | R-sem | my favorite salad is vindaloo | retrieved (semantic) | use_memory=True results=1 hit='vindaloo' | PASS |  |
| 4867 | R-sem | my favorite salad is tamale | retrieved (semantic) | results=0 retrieved=[] | FAIL | stored fact not retrieved (use_memory=True) |
| 4868 | R-sem | my favorite salad is pho | retrieved (semantic) | use_memory=True results=1 hit='pho' | PASS |  |
| 4869 | R-sem | my favorite salad is pierogi | retrieved (semantic) | use_memory=True results=1 hit='pierogi' | PASS |  |
| 487 | A | my favorite book is brave new world | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4870 | R-sem | my favorite sauce is dosa | retrieved (semantic) | results=0 retrieved=[] | FAIL | stored fact not retrieved (use_memory=True) |
| 4871 | R-sem | my favorite sauce is ramen | retrieved (semantic) | results=0 retrieved=[] | FAIL | stored fact not retrieved (use_memory=True) |
| 4872 | R-sem | my favorite sauce is tamale | retrieved (semantic) | use_memory=True results=1 hit='tamale' | PASS |  |
| 4873 | R-sem | my favorite sauce is nachos | retrieved (semantic) | results=0 retrieved=[] | FAIL | stored fact not retrieved (use_memory=True) |
| 4874 | R-sem | my favorite sauce is sandwich | retrieved (semantic) | results=0 retrieved=[] | FAIL | stored fact not retrieved (use_memory=True) |
| 4875 | R-sem | my favorite sauce is pasta | retrieved (semantic) | use_memory=True results=1 hit='pasta' | PASS |  |
| 4876 | R-sem | my favorite sauce is naan | retrieved (semantic) | results=0 retrieved=[] | FAIL | stored fact not retrieved (use_memory=True) |
| 4877 | R-sem | my favorite sauce is idli | retrieved (semantic) | results=0 retrieved=[] | FAIL | stored fact not retrieved (use_memory=True) |
| 4878 | R-sem | my favorite sauce is gnocchi | retrieved (semantic) | results=0 retrieved=[] | FAIL | stored fact not retrieved (use_memory=True) |
| 4879 | R-sem | my favorite sauce is poutine | retrieved (semantic) | results=0 retrieved=[] | FAIL | stored fact not retrieved (use_memory=True) |
| 488 | A | my favorite dessert is pavlova | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4880 | R-sem | my favorite dip is poutine | retrieved (semantic) | results=0 retrieved=[] | FAIL | stored fact not retrieved (use_memory=True) |
| 4881 | R-sem | my favorite dip is pasta | retrieved (semantic) | use_memory=True results=1 hit='pasta' | PASS |  |
| 4882 | R-sem | my favorite dip is palak paneer | retrieved (semantic) | use_memory=True results=1 hit='palak paneer' | PASS |  |
| 4883 | R-sem | my favorite dip is momos | retrieved (semantic) | results=0 retrieved=[] | FAIL | stored fact not retrieved (use_memory=True) |
| 4884 | R-sem | my favorite dip is samosa | retrieved (semantic) | use_memory=True results=1 hit='samosa' | PASS |  |
| 4885 | R-sem | my favorite dip is bhel puri | retrieved (semantic) | use_memory=True results=1 hit='bhel puri' | PASS |  |
| 4886 | R-sem | my favorite dip is empanadas | retrieved (semantic) | results=0 retrieved=[] | FAIL | stored fact not retrieved (use_memory=True) |
| 4887 | R-sem | my favorite dip is paratha | retrieved (semantic) | use_memory=True results=1 hit='paratha' | PASS |  |
| 4888 | R-sem | my favorite dip is onion rings | retrieved (semantic) | use_memory=True results=1 hit='onion rings' | PASS |  |
| 4889 | R-sem | my favorite dip is idli | retrieved (semantic) | results=0 retrieved=[] | FAIL | stored fact not retrieved (use_memory=True) |
| 489 | A | i am from zurich | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 4890 | R-sem | my favorite spread is pizza | retrieved (semantic) | use_memory=True results=1 hit='pizza' | PASS |  |
| 4891 | R-sem | my favorite spread is risotto | retrieved (semantic) | use_memory=True results=1 hit='risotto' | PASS |  |
| 4892 | R-sem | my favorite spread is burrito | retrieved (semantic) | use_memory=True results=1 hit='burrito' | PASS |  |
| 4893 | R-sem | my favorite spread is poutine | retrieved (semantic) | use_memory=True results=1 hit='poutine' | PASS |  |
| 4894 | R-sem | my favorite spread is hummus plate | retrieved (semantic) | use_memory=True results=1 hit='hummus plate' | PASS |  |
| 4895 | R-sem | my favorite spread is naan | retrieved (semantic) | use_memory=True results=1 hit='naan' | PASS |  |
| 4896 | R-sem | my favorite spread is paratha | retrieved (semantic) | use_memory=True results=1 hit='paratha' | PASS |  |
| 4897 | R-sem | my favorite spread is ceviche | retrieved (semantic) | use_memory=True results=1 hit='ceviche' | PASS |  |
| 4898 | R-sem | my favorite spread is fried rice | retrieved (semantic) | results=0 retrieved=[] | FAIL | stored fact not retrieved (use_memory=True) |
| 4899 | R-sem | my favorite spread is palak paneer | retrieved (semantic) | use_memory=True results=1 hit='palak paneer' | PASS |  |
| 49 | A | i work as a journalist | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 490 | A | my favorite hobby is ukulele | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4900 | R-sem | my favorite side dish is momos | retrieved (semantic) | use_memory=True results=1 hit='momos' | PASS |  |
| 4901 | R-sem | my favorite side dish is hummus plate | retrieved (semantic) | use_memory=True results=1 hit='hummus plate' | PASS |  |
| 4902 | R-sem | my favorite side dish is bhel puri | retrieved (semantic) | use_memory=True results=1 hit='bhel puri' | PASS |  |
| 4903 | R-sem | my favorite side dish is ceviche | retrieved (semantic) | results=0 retrieved=[] | FAIL | stored fact not retrieved (use_memory=True) |
| 4904 | R-sem | my favorite side dish is butter chicken | retrieved (semantic) | results=0 retrieved=[] | FAIL | stored fact not retrieved (use_memory=True) |
| 4905 | R-sem | my favorite side dish is bruschetta | retrieved (semantic) | results=0 retrieved=[] | FAIL | stored fact not retrieved (use_memory=True) |
| 4906 | R-sem | my favorite side dish is waffles | retrieved (semantic) | use_memory=True results=1 hit='waffles' | PASS |  |
| 4907 | R-sem | my favorite side dish is shepherd pie | retrieved (semantic) | use_memory=True results=1 hit='shepherd pie' | PASS |  |
| 4908 | R-sem | my favorite side dish is onion rings | retrieved (semantic) | use_memory=True results=1 hit='onion rings' | PASS |  |
| 4909 | R-sem | my favorite side dish is noodles | retrieved (semantic) | use_memory=True results=1 hit='noodles' | PASS |  |
| 491 | A | my pet's name is taco | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4910 | R-pro | my name is jack | retrieved (profile) | results=1 | PASS |  |
| 4911 | R-pro | my name is sunny | retrieved (profile) | use_memory=True results=0 | FAIL | profile query did not return stored fact |
| 4912 | R-pro | my name is simba | retrieved (profile) | results=1 | PASS |  |
| 4913 | R-pro | my name is waffle | retrieved (profile) | use_memory=True results=0 | FAIL | profile query did not return stored fact |
| 4914 | R-pro | my name is molly | retrieved (profile) | results=1 | PASS |  |
| 4915 | R-pro | my name is coco | retrieved (profile) | use_memory=True results=0 | FAIL | profile query did not return stored fact |
| 4916 | R-pro | my name is buddy | retrieved (profile) | use_memory=True results=0 | FAIL | profile query did not return stored fact |
| 4917 | R-pro | my name is bailey | retrieved (profile) | results=1 | PASS |  |
| 4918 | R-pro | my name is oscar | retrieved (profile) | results=1 | PASS |  |
| 4919 | R-pro | my name is tofu | retrieved (profile) | results=1 | PASS |  |
| 492 | A | my favorite animal is spider | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4920 | R-pro | my name is ruby | retrieved (profile) | results=1 | PASS |  |
| 4921 | R-pro | my name is zoe | retrieved (profile) | results=1 | PASS |  |
| 4922 | R-pro | my name is daisy | retrieved (profile) | results=1 | PASS |  |
| 4923 | R-pro | my name is sophie | retrieved (profile) | results=1 | PASS |  |
| 4924 | R-pro | my name is ginger | retrieved (profile) | results=1 | PASS |  |
| 4925 | R-pro | my name is luna | retrieved (profile) | results=1 | PASS |  |
| 4926 | R-pro | my name is sadie | retrieved (profile) | use_memory=True results=0 | FAIL | profile query did not return stored fact |
| 4927 | R-pro | my name is kiwi | retrieved (profile) | results=1 | PASS |  |
| 4928 | R-pro | my name is pepper | retrieved (profile) | results=1 | PASS |  |
| 4929 | R-pro | my name is tony | retrieved (profile) | results=1 | PASS |  |
| 493 | A | my favorite fruit is coconut | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4930 | R-pro | my name is pebbles | retrieved (profile) | use_memory=True results=0 | FAIL | profile query did not return stored fact |
| 4931 | R-pro | my name is biscuit | retrieved (profile) | use_memory=True results=0 | FAIL | profile query did not return stored fact |
| 4932 | R-pro | my name is charlie | retrieved (profile) | use_memory=True results=0 | FAIL | profile query did not return stored fact |
| 4933 | R-pro | my name is bella | retrieved (profile) | results=1 | PASS |  |
| 4934 | R-pro | my name is nala | retrieved (profile) | results=1 | PASS |  |
| 4935 | R-pro | my name is bruno | retrieved (profile) | results=1 | PASS |  |
| 4936 | R-pro | my name is max | retrieved (profile) | results=1 | PASS |  |
| 4937 | R-pro | my name is rex | retrieved (profile) | results=1 | PASS |  |
| 4938 | R-pro | my name is sushi | retrieved (profile) | results=1 | PASS |  |
| 4939 | R-pro | my name is taco | retrieved (profile) | results=1 | PASS |  |
| 494 | A | my favorite color is rose | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4940 | R-epi | recap what we discussed about salary negotiation | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4941 | R-epi | recap what we discussed about painting class | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4942 | R-epi | recap what we discussed about group project | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4943 | R-epi | recap what we discussed about python project | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4944 | R-epi | recap what we discussed about exam preparation | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4945 | R-epi | recap what we discussed about newsletter | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4946 | R-epi | recap what we discussed about gaming setup | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4947 | R-epi | recap what we discussed about homework help | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4948 | R-epi | recap what we discussed about marketing campaign | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4949 | R-epi | recap what we discussed about ui design | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 495 | A | i work as a geologist | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 4950 | R-epi | recap what we discussed about product idea | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4951 | R-epi | recap what we discussed about side hustle | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4952 | R-epi | recap what we discussed about chess bot | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4953 | R-epi | recap what we discussed about budget plan | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4954 | R-epi | recap what we discussed about game jam | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4955 | R-epi | recap what we discussed about api integration | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4956 | R-epi | recap what we discussed about debate prep | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4957 | R-epi | recap what we discussed about podcast idea | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4958 | R-epi | recap what we discussed about bike repair | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4959 | R-epi | recap what we discussed about guitar lesson | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 496 | A | my favorite food is sushi | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4960 | R-epi | recap what we discussed about youtube channel | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4961 | R-epi | recap what we discussed about database migration | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4962 | R-epi | recap what we discussed about blog post | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4963 | R-epi | recap what we discussed about research internship | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4964 | R-epi | recap what we discussed about c program | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4965 | R-epi | recap what we discussed about app prototype | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4966 | R-epi | recap what we discussed about data analysis project | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4967 | R-epi | recap what we discussed about bug hunting | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4968 | R-epi | recap what we discussed about performance tuning | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 4969 | R-epi | recap what we discussed about visa process | retrieved (episodic) | use_episodes=True episodes=3 | PASS |  |
| 497 | A | my favorite dessert is rasmalai | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 4970 | R-hist | my favorite seasoning is pho | retrieved (history) | use_memory=True hist=0 | FAIL | history before-question returned no entry |
| 4971 | R-hist | my favorite seasoning is curry | retrieved (history) | use_memory=True hist=0 | FAIL | history before-question returned no entry |
| 4972 | R-hist | my favorite seasoning is sandwich | retrieved (history) | use_memory=True hist=0 | FAIL | history before-question returned no entry |
| 4973 | R-hist | my favorite seasoning is vindaloo | retrieved (history) | hist=1 | PASS |  |
| 4974 | R-hist | my favorite seasoning is poutine | retrieved (history) | use_memory=True hist=0 | FAIL | history before-question returned no entry |
| 4975 | R-hist | my favorite seasoning is pizza | retrieved (history) | hist=1 | PASS |  |
| 4976 | R-hist | my favorite seasoning is korean bbq | retrieved (history) | use_memory=True hist=0 | FAIL | history before-question returned no entry |
| 4977 | R-hist | my favorite seasoning is pancakes | retrieved (history) | use_memory=True hist=0 | FAIL | history before-question returned no entry |
| 4978 | R-hist | my favorite seasoning is burrito | retrieved (history) | use_memory=True hist=0 | FAIL | history before-question returned no entry |
| 4979 | R-hist | my favorite seasoning is shepherd pie | retrieved (history) | use_memory=True hist=0 | FAIL | history before-question returned no entry |
| 498 | A | my favorite game is half-life 2 | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite game is Half Life 2' | FAIL | store did not persist: status=needs_clarification present=False |
| 4980 | R-hist | my favorite seasoning is noodles | retrieved (history) | use_memory=True hist=0 | FAIL | history before-question returned no entry |
| 4981 | R-hist | my favorite seasoning is biryani | retrieved (history) | hist=1 | PASS |  |
| 4982 | R-hist | my favorite seasoning is mac and cheese | retrieved (history) | hist=1 | PASS |  |
| 4983 | R-hist | my favorite seasoning is idli | retrieved (history) | use_memory=True hist=0 | FAIL | history before-question returned no entry |
| 4984 | R-hist | my favorite seasoning is gyoza | retrieved (history) | use_memory=True hist=0 | FAIL | history before-question returned no entry |
| 4985 | R-hist | my favorite condiment is sushi | retrieved (history) | use_memory=True hist=0 | FAIL | history before-question returned no entry |
| 4986 | R-hist | my favorite condiment is gnocchi | retrieved (history) | use_memory=True hist=0 | FAIL | history before-question returned no entry |
| 4987 | R-hist | my favorite condiment is calamari | retrieved (history) | use_memory=True hist=0 | FAIL | history before-question returned no entry |
| 4988 | R-hist | my favorite condiment is pizza | retrieved (history) | hist=1 | PASS |  |
| 4989 | R-hist | my favorite condiment is gumbo | retrieved (history) | hist=1 | PASS |  |
| 499 | A | my favorite drink is americano | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is americano' | FAIL | store did not persist: status=needs_clarification present=False |
| 4990 | R-hist | my favorite condiment is mac and cheese | retrieved (history) | hist=1 | PASS |  |
| 4991 | R-hist | my favorite condiment is noodles | retrieved (history) | use_memory=True hist=0 | FAIL | history before-question returned no entry |
| 4992 | R-hist | my favorite condiment is lasagna | retrieved (history) | use_memory=True hist=0 | FAIL | history before-question returned no entry |
| 4993 | R-hist | my favorite condiment is ratatouille | retrieved (history) | hist=1 | PASS |  |
| 4994 | R-hist | my favorite condiment is pierogi | retrieved (history) | hist=1 | PASS |  |
| 4995 | R-hist | my favorite condiment is banh mi | retrieved (history) | use_memory=True hist=0 | FAIL | history before-question returned no entry |
| 4996 | R-hist | my favorite condiment is onion rings | retrieved (history) | hist=1 | PASS |  |
| 4997 | R-hist | my favorite condiment is samosa | retrieved (history) | use_memory=True hist=0 | FAIL | history before-question returned no entry |
| 4998 | R-hist | my favorite condiment is tacos | retrieved (history) | use_memory=True hist=0 | FAIL | history before-question returned no entry |
| 4999 | R-hist | my favorite condiment is guacamole | retrieved (history) | hist=1 | PASS |  |
| 5 | A | my favorite fruit is grapes | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 50 | A | my favorite animal is lemur | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 500 | A | my favorite subject is robotics | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 501 | A | my favorite dessert is mango pudding | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 502 | A | my favorite book is little women | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 503 | A | i work as a editor | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 504 | A | my favorite food is mac and cheese | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 505 | A | i am from tokyo | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 506 | A | my favorite music is gospel | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 507 | A | my favorite food is momos | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 508 | A | my favorite movie is catch me if you can | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 509 | A | i am from quito | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 51 | A | my pet's name is chip | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 510 | A | my favorite game is animal crossing | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 511 | A | my favorite sport is cycling | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 512 | A | my favorite movie is forrest gump | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 513 | A | i work as a chemist | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 514 | A | my pet's name is leo | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 515 | A | my favorite movie is your name | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 516 | A | my favorite writer is anton chekhov | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 517 | A | my favorite drink is iced chai | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is iced chai' | FAIL | store did not persist: status=needs_clarification present=False |
| 518 | A | my favorite game is super mario odyssey | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 519 | A | my favorite sport is badminton | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 52 | A | my favorite show is the twilight zone | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 520 | A | my favorite game is pokemon | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite game is Pokémon' | FAIL | store did not persist: status=needs_clarification present=False |
| 521 | A | my favorite show is parks and recreation | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 522 | A | my favorite city is mumbai | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 523 | A | my favorite color is jade | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 524 | A | my favorite subject is genetics | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 525 | A | i work as a pharmacist | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 526 | A | my favorite subject is dance | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 527 | A | my favorite fruit is pear | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 528 | A | my favorite movie is gladiator | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 529 | A | my favorite hobby is horseback riding | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 53 | A | my pet's name is rex | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 530 | A | my favorite subject is nutrition | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 531 | A | my favorite subject is meteorology | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 532 | A | my favorite show is seinfeld | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 533 | A | my favorite subject is marine biology | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 534 | A | my favorite fruit is gooseberry | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 535 | A | my favorite writer is andrew clements | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 536 | A | my favorite book is the midnight library | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 537 | A | my favorite show is sherlock | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 538 | A | my favorite movie is the batman | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 539 | A | my favorite animal is crab | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 54 | A | my favorite subject is environmental science | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 540 | A | my favorite animal is tiger | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 541 | A | my pet's name is zuri | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 542 | A | my favorite color is beige | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 543 | A | my favorite animal is snake | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 544 | A | my favorite book is to kill a mockingbird | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 545 | A | my favorite book is charlotte web | store (durable casual fact persists) | op=store status=needs_clarification fact="My favorite book is Charlotte's Web" | FAIL | store did not persist: status=needs_clarification present=False |
| 546 | A | my favorite music is punk | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 547 | A | my favorite hobby is meditation | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 548 | A | my favorite subject is network engineering | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 549 | A | my favorite hobby is hiking | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 55 | A | my favorite hobby is pottery | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 550 | A | my favorite drink is milk coffee | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is milk coffee' | FAIL | store did not persist: status=needs_clarification present=False |
| 551 | A | my favorite sport is motocross | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 552 | A | my favorite drink is tomato juice | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is tomato juice' | FAIL | store did not persist: status=needs_clarification present=False |
| 553 | A | my pet's name is sophie | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 554 | A | my favorite cuisine is german | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 555 | A | my favorite sport is surfing | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 556 | A | my favorite game is oblivion | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 557 | A | my favorite drink is jasmine tea | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is jasmine tea' | FAIL | store did not persist: status=needs_clarification present=False |
| 558 | A | my favorite music is opera | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 559 | A | my favorite sport is water polo | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 56 | A | my favorite book is the old man and the sea | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 560 | A | my favorite drink is apple juice | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 561 | A | my favorite fruit is pineapple | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 562 | A | my birthday is in july | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 563 | A | my favorite food is pho | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 564 | A | my pet's name is nala | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 565 | A | my favorite drink is pineapple juice | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is pineapple juice' | FAIL | store did not persist: status=needs_clarification present=False |
| 566 | A | my favorite writer is walt whitman | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 567 | A | my favorite dessert is pound cake | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 568 | A | my favorite fruit is cantaloupe | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 569 | A | my favorite hobby is model building | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 57 | A | my favorite city is copenhagen | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 570 | A | my favorite dessert is caramel custard | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 571 | A | my favorite show is the crown | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 572 | A | my favorite book is anna karenina | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 573 | A | my favorite sport is judo | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 574 | A | my pet's name is biscuit | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 575 | A | i am from bogota | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 576 | A | my favorite dessert is tiramisu | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 577 | A | my favorite animal is beetle | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite animal is beetle' | FAIL | store did not persist: status=needs_clarification present=False |
| 578 | A | i am from rio de janeiro | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 579 | A | my favorite dessert is creme brulee | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 58 | A | my favorite color is mustard | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 580 | A | my favorite drink is coconut water | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 581 | A | my favorite movie is the prestige | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 582 | A | my favorite city is warsaw | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 583 | A | my favorite writer is william shakespeare | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 584 | A | my favorite show is arrested development | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 585 | A | i am from edinburgh | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 586 | A | i work as a pilot | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 587 | A | my favorite show is for all mankind | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 588 | A | my favorite cuisine is korean | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 589 | A | my favorite color is topaz | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 59 | A | my favorite color is sand | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 590 | A | my favorite movie is the two towers | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 591 | A | my favorite dessert is angel food cake | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 592 | A | my favorite book is the kite runner | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 593 | A | my favorite dessert is tarte tatin | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 594 | A | my favorite animal is platypus | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 595 | A | my favorite show is true detective | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 596 | A | my favorite drink is pomegranate juice | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 597 | A | my favorite subject is mythology | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 598 | A | my favorite color is rust | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 599 | A | my favorite movie is the matrix | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 6 | A | my favorite movie is the shape of water | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 60 | A | i am from cardiff | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 600 | A | my favorite hobby is knitting | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 601 | A | my pet's name is luna | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 602 | A | my favorite game is minecraft | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 603 | A | my favorite game is tears of the kingdom | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 604 | A | i am from madrid | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 605 | A | my favorite animal is bat | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite animal is bat' | FAIL | store did not persist: status=needs_clarification present=False |
| 606 | A | i work as a glassblower | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 607 | A | my favorite subject is law | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 608 | A | my favorite food is empanadas | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 609 | A | my favorite subject is oceanography | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 61 | A | my birthday is in june | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 610 | A | my favorite movie is the fellowship of the ring | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 611 | A | my favorite sport is skateboarding | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 612 | A | i work as a salesperson | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 613 | A | my birthday is in october | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 614 | A | my pet's name is kaju | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 615 | A | my favorite music is gothic | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 616 | A | my favorite music is soukous | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 617 | A | my favorite hobby is billiards | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 618 | A | my pet's name is rocky | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 619 | A | my favorite drink is espresso | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is espresso' | FAIL | store did not persist: status=needs_clarification present=False |
| 62 | A | my favorite city is boston | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 620 | A | my birthday is in may | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 621 | A | my favorite writer is kurt vonnegut | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 622 | A | my favorite dessert is donuts | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 623 | A | my favorite subject is psychology | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 624 | A | my favorite subject is neurology | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 625 | A | i am from manchester | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 626 | A | my favorite show is killing eve | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 627 | A | my favorite color is green | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 628 | A | my favorite dessert is panna cotta | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 629 | A | my favorite drink is mate | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is mate' | FAIL | store did not persist: status=needs_clarification present=False |
| 63 | A | my favorite game is celeste | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 630 | A | my favorite music is disco | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 631 | A | my favorite city is kyoto | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 632 | A | i work as a mechanic | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 633 | A | my favorite writer is rabindranath tagore | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 634 | A | my favorite color is purple | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 635 | A | my pet's name is bella | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 636 | A | my favorite color is gold | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 637 | A | i am from seville | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 638 | A | my favorite food is chow mein | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 639 | A | my favorite cuisine is taiwanese | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 64 | A | my favorite fruit is pomegranate | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 640 | A | my favorite hobby is coin collecting | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 641 | A | my favorite hobby is coffee brewing | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 642 | A | my favorite game is skyrim | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 643 | A | my favorite cuisine is laotian | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 644 | A | my favorite animal is whale | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 645 | A | my favorite dessert is apple pie | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 646 | A | my favorite game is doom eternal | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 647 | A | my favorite season is autumn | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 648 | A | my favorite movie is blade runner | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 649 | A | my favorite dessert is phirni | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 65 | A | my favorite music is rock | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 650 | A | i am from lima | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 651 | A | my birthday is in december | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 652 | A | my favorite music is salsa | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 653 | A | my favorite city is lisbon | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 654 | A | my favorite writer is robert frost | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 655 | A | my favorite drink is beer | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 656 | A | my pet's name is tofu | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 657 | A | my favorite hobby is backpacking | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 658 | A | my pet's name is sunny | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 659 | A | my favorite color is magenta | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 66 | A | i am from stockholm | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 660 | A | my favorite game is valorant | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 661 | A | my pet's name is bolt | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 662 | A | my favorite food is paratha | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 663 | A | i work as a vet | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 664 | A | my favorite food is paella | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 665 | A | my favorite food is guacamole | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 666 | A | my favorite color is blush | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 667 | A | my favorite cuisine is tamil | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite cuisine is tamil' | FAIL | store did not persist: status=needs_clarification present=False |
| 668 | A | i am from jakarta | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 669 | A | my favorite color is indigo | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 67 | A | my favorite animal is toad | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 670 | A | my favorite food is samosa | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 671 | A | my favorite book is the maze runner | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 672 | A | my favorite fruit is cranberry | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 673 | A | my favorite subject is music theory | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 674 | A | my favorite movie is inception | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 675 | A | my favorite animal is dragonfly | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 676 | A | my favorite sport is cross country skiing | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 677 | A | my favorite subject is quantum physics | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 678 | A | my favorite city is casablanca | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 679 | A | my favorite animal is guinea | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite animal is guinea' | FAIL | store did not persist: status=needs_clarification present=False |
| 68 | A | my favorite subject is theatre | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 680 | A | my favorite music is soul | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 681 | A | my birthday is in february | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 682 | A | my favorite movie is titanic | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 683 | A | my favorite drink is buttermilk | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is buttermilk' | FAIL | store did not persist: status=needs_clarification present=False |
| 684 | A | my favorite drink is affogato | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is affogato' | FAIL | store did not persist: status=needs_clarification present=False |
| 685 | A | my favorite cuisine is hong kong | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 686 | A | my favorite music is jazz | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 687 | A | my pet's name is coco | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 688 | A | i am from rotterdam | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 689 | A | my favorite sport is diving | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 69 | A | my favorite dessert is key lime pie | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 690 | A | my favorite drink is black tea | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 691 | A | my favorite cuisine is hawaiian | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 692 | A | my favorite city is rome | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 693 | A | my favorite food is palak paneer | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 694 | A | my favorite drink is milkshake | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is milkshake' | FAIL | store did not persist: status=needs_clarification present=False |
| 695 | A | my favorite writer is f scott fitzgerald | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 696 | A | my favorite writer is julio cortazar | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 697 | A | my favorite movie is fight club | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 698 | A | my favorite movie is spirited away | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 699 | A | my favorite book is the catcher in the rye | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 7 | A | my favorite dessert is chocolate cake | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 70 | A | my favorite writer is vladimir nabokov | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 700 | A | my favorite dessert is rice pudding | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 701 | A | my favorite sport is triathlon | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 702 | A | my favorite music is chamber | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 703 | A | my favorite show is andor | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 704 | A | my pet's name is jack | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 705 | A | my pet's name is waffle | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 706 | A | my favorite book is the name of the wind | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 707 | A | my favorite game is apex legends | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 708 | A | my favorite fruit is watermelon | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 709 | A | i work as a astronomer | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 71 | A | my favorite show is squid game | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 710 | A | my favorite subject is thermodynamics | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 711 | A | my favorite city is helsinki | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 712 | A | my favorite dessert is bread pudding | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 713 | A | my favorite city is delhi | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 714 | A | my favorite game is cuphead | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 715 | A | i am from cairo | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 716 | A | my favorite sport is track cycling | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 717 | A | my favorite hobby is bouldering | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 718 | A | my favorite drink is dirty chai | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is dirty chai' | FAIL | store did not persist: status=needs_clarification present=False |
| 719 | A | my favorite animal is lizard | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 72 | A | my favorite color is charcoal | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 720 | A | i work as a botanist | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 721 | A | my favorite color is forest | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 722 | A | my favorite book is the book thief | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 723 | A | my favorite city is dubai | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 724 | A | my favorite dessert is red velvet cake | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 725 | A | my favorite game is half-life | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite game is Half Life' | FAIL | store did not persist: status=needs_clarification present=False |
| 726 | A | my favorite food is pancakes | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 727 | A | my favorite sport is kitesurfing | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 728 | A | my favorite animal is iguana | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 729 | A | my favorite book is animal farm | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 73 | A | my favorite music is celtic | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 730 | A | my favorite city is mexico city | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 731 | A | my favorite movie is dead poets society | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 732 | A | my favorite writer is ita? | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite writer is Ita' | FAIL | store did not persist: status=needs_clarification present=False |
| 733 | A | my favorite dessert is brownie sundae | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 734 | A | my favorite movie is ratatouille | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 735 | A | my favorite movie is moneyball | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 736 | A | my favorite hobby is stamp collecting | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 737 | A | my favorite cuisine is spanish | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 738 | A | my favorite fruit is tangerine | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 739 | A | i work as a sociologist | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 74 | A | my favorite music is r&b | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite music is r&b' | FAIL | store did not persist: status=needs_clarification present=False |
| 740 | A | my favorite color is ivory | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 741 | A | my favorite book is the hunger games | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 742 | A | my favorite cuisine is indian | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 743 | A | i work as a coach | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 744 | A | my favorite animal is shrimp | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 745 | A | my favorite drink is herbal tea | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 746 | A | my favorite fruit is honeydew | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 747 | A | my favorite subject is physics | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 748 | A | my favorite game is counter-strike | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite game is Counter Strike' | FAIL | store did not persist: status=needs_clarification present=False |
| 749 | A | my favorite fruit is jackfruit | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 75 | A | my favorite music is trip hop | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 750 | A | my favorite sport is skiing | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 751 | A | my pet's name is milo | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 752 | A | my favorite fruit is mango | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 753 | A | my favorite sport is hockey | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 754 | A | i am from delhi | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 755 | A | my favorite food is bhel puri | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 756 | A | my favorite show is narcos | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 757 | A | my favorite animal is penguin | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 758 | A | my favorite food is falafel | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 759 | A | my favorite cuisine is israeli | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite cuisine is Israeli' | FAIL | store did not persist: status=needs_clarification present=False |
| 76 | A | my favorite fruit is boysenberry | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 760 | A | my favorite cuisine is argentine | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 761 | A | my pet's name is ginger | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 762 | A | my favorite book is the handmaid tale | store (durable casual fact persists) | op=store status=needs_clarification fact="My favorite book is The Handmaid's Tale" | FAIL | store did not persist: status=needs_clarification present=False |
| 763 | A | my favorite show is silicon valley | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 764 | A | my favorite book is sapiens | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 765 | A | my favorite hobby is fishing | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 766 | A | my favorite animal is mole | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 767 | A | i am from capetown | store (durable casual fact persists) | op=store status=needs_clarification fact='I am from Cape Town' | FAIL | store did not persist: status=needs_clarification present=False |
| 768 | A | my favorite writer is george eliot | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 769 | A | my favorite hobby is cheese making | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 77 | A | my favorite food is noodles | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 770 | A | my favorite drink is yerba mate | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is yerma te' | FAIL | store did not persist: status=needs_clarification present=False |
| 771 | A | my favorite cuisine is tex-mex | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 772 | A | my favorite animal is seal | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 773 | A | my favorite hobby is photography | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 774 | A | my favorite food is poha | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 775 | A | my favorite hobby is painting | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 776 | A | i work as a biologist | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 777 | A | my favorite city is dublin | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 778 | A | my pet's name is oscar | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 779 | A | my favorite writer is jrr tolkien | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 78 | A | my favorite sport is karate | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 780 | A | my favorite subject is computer science | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 781 | A | my favorite sport is bobsleigh | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 782 | A | my favorite color is peach | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 783 | A | my favorite color is navy | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 784 | A | my favorite food is nachos | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 785 | A | i work as a psychologist | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 786 | A | my birthday is in march | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 787 | A | my favorite city is kathmandu | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 788 | A | my favorite game is elden ring | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 789 | A | my favorite game is dark souls 3 | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 79 | A | my favorite writer is roald dahl | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 790 | A | my favorite sport is biathlon | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 791 | A | my favorite writer is virginia woolf | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 792 | A | my favorite animal is turtle | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 793 | A | my favorite hobby is amateur radio | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 794 | A | my favorite animal is lobster | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 795 | A | i work as a beekeeper | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 796 | A | my favorite season is winter | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 797 | A | my favorite drink is bubble tea | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is bubble tea' | FAIL | store did not persist: status=needs_clarification present=False |
| 798 | A | my favorite dessert is crepes | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 799 | A | my favorite sport is formula one | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 8 | A | my favorite color is slate | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 80 | A | my favorite fruit is cherry | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 800 | A | my favorite cuisine is burmese | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 801 | A | my favorite animal is butterfly | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 802 | A | my favorite show is the umbrellas | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 803 | A | my favorite book is lord of the flies | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 804 | A | my favorite writer is albert camus | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 805 | A | my favorite color is azure | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 806 | A | my favorite hobby is cycling | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 807 | A | my favorite food is shepherd pie | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 808 | A | my favorite show is westworld | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 809 | A | my favorite writer is chinua achebe | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 81 | A | my favorite fruit is tamarind | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 810 | A | my favorite sport is high jump | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 811 | A | my favorite book is a song of ice and fire | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 812 | A | my favorite cuisine is middle eastern | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 813 | A | my favorite movie is the usual suspects | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 814 | A | my favorite cuisine is greek | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 815 | A | my favorite hobby is dioramas | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 816 | A | i am from manila | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 817 | A | i am from casablanca | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 818 | A | i am from sao paulo | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 819 | A | my favorite food is pasta | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite food is pasta' | FAIL | store did not persist: status=needs_clarification present=False |
| 82 | A | my favorite hobby is robotics | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 820 | A | my favorite music is folk | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 821 | A | my favorite animal is bee | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 822 | A | my favorite music is ghazal | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 823 | A | my birthday is in april | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 824 | A | my favorite food is hummus plate | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 825 | A | my favorite fruit is orange | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 826 | A | my favorite writer is langston hughes | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 827 | A | my favorite cuisine is ethiopian | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 828 | A | my favorite book is 1984 | store (durable casual fact persists) | op=store status=needs_confirmation fact='My favorite book is 1984' | FAIL | store did not persist: status=needs_confirmation present=False |
| 829 | A | my favorite game is rocket league | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 83 | A | my favorite book is pride and prejudice | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 830 | A | my favorite fruit is avocado | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 831 | A | my favorite book is the little prince | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 832 | A | my favorite music is techno | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 833 | A | my favorite animal is wallaby | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 834 | A | my favorite drink is red wine | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 835 | A | my favorite hobby is origami | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 836 | A | my favorite game is valheim | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 837 | A | my favorite movie is se7en | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 838 | A | my favorite writer is khaled hosseini | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 839 | A | my favorite book is mistborn | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 84 | A | my favorite show is black mirror | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 840 | A | my favorite cuisine is japanese | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 841 | A | i work as a architect | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 842 | A | my favorite fruit is kiwi | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 843 | A | my favorite food is tacos | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite food is tacos' | FAIL | store did not persist: status=needs_clarification present=False |
| 844 | A | my favorite city is santiago | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 845 | A | my favorite color is scarlet | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 846 | A | my favorite game is fire emblem | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 847 | A | my favorite game is undertale | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 848 | A | my favorite fruit is nectarine | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 849 | A | my favorite hobby is puzzle solving | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 85 | A | my favorite city is edinburgh | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 850 | A | my favorite show is the witcher | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 851 | A | my favorite color is pearl | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 852 | A | my favorite dessert is kulfi | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 853 | A | my favorite cuisine is brazilian | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 854 | A | my favorite sport is chess | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 855 | A | my favorite subject is web development | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 856 | A | my pet's name is misty | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 857 | A | my favorite dessert is gulab jamun | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 858 | A | my favorite cuisine is french | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 859 | A | my favorite sport is boxing | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 86 | A | my favorite dessert is macarons | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 860 | A | my favorite fruit is banana | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 861 | A | my favorite fruit is soursop | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 862 | A | my favorite dessert is ice cream | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 863 | A | i work as a florist | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 864 | A | my favorite drink is cappuccino | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 865 | A | my favorite cuisine is moroccan | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 866 | A | my favorite game is cyberpunk 2077 | store (durable casual fact persists) | op=store status=needs_confirmation fact='My favorite game is cyberpunk 2077' | FAIL | store did not persist: status=needs_confirmation present=False |
| 867 | A | my favorite music is flamenco | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 868 | A | my favorite book is the wheel of time | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 869 | A | my favorite writer is enid blyton | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 87 | A | my favorite subject is world history | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 870 | A | my favorite music is house | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 871 | A | my favorite sport is speed skating | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 872 | A | i am from rome | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 873 | A | my favorite cuisine is ukrainian | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 874 | A | my favorite sport is snowboarding | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 875 | A | i am from hanoi | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 876 | A | my favorite music is shoegaze | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 877 | A | my favorite writer is john steinbeck | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 878 | A | my favorite subject is kinesiology | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 879 | A | i work as a referee | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 88 | A | my favorite fruit is cloudberry | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite fruit is cloudberry' | FAIL | store did not persist: status=needs_clarification present=False |
| 880 | A | my favorite hobby is running | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 881 | A | my favorite cuisine is peruvian | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 882 | A | my favorite music is metal | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 883 | A | my favorite drink is iced tea | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 884 | A | my favorite city is lagos | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 885 | A | i work as a software engineer | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 886 | A | my favorite fruit is lemon | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 887 | A | i work as a blacksmith | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 888 | A | my favorite game is factorio | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 889 | A | my pet's name is charlie | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 89 | A | my favorite game is control | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 890 | A | my favorite drink is chai | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is chai' | FAIL | store did not persist: status=needs_clarification present=False |
| 891 | A | my favorite hobby is camping | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 892 | A | my favorite food is bruschetta | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 893 | A | my favorite cuisine is malaysian | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 894 | A | my favorite hobby is guitar | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 895 | A | my favorite writer is yann martel | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 896 | A | my favorite fruit is persimmon | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 897 | A | my favorite hobby is sudoku | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 898 | A | my favorite writer is ruskin bond | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 899 | A | my favorite cuisine is mediterranean | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 9 | A | my favorite sport is synchronized swimming | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 90 | A | my favorite sport is discus | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 900 | A | i work as a farmer | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 901 | A | my favorite animal is rabbit | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 902 | A | my favorite cuisine is mughlai | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 903 | A | my favorite color is turquoise | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 904 | A | my favorite dessert is baklava | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 905 | A | my favorite food is vindaloo | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 906 | A | my favorite animal is newt | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 907 | A | my favorite animal is hare | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 908 | A | my favorite show is the boys | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 909 | A | my favorite fruit is elderberry | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 91 | A | i work as a zoologist | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 910 | A | my favorite color is onyx | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 911 | A | my favorite city is cardiff | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 912 | A | my birthday is in january | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 913 | A | my favorite show is the x-files | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 914 | A | my favorite cuisine is shanghainese | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 915 | A | my favorite show is house of the dragon | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 916 | A | my favorite show is the wire | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 917 | A | my favorite sport is figure skating | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 918 | A | my favorite city is athens | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 919 | A | my favorite drink is orange soda | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is orange soda' | FAIL | store did not persist: status=needs_clarification present=False |
| 92 | A | my favorite game is portal | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 920 | A | my favorite hobby is cooking | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 921 | A | my favorite cuisine is northern indian | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 922 | A | my favorite hobby is crosswords | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 923 | A | my favorite show is ozark | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 924 | A | my pet's name is max | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 925 | A | my favorite game is sekiro | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 926 | A | my favorite sport is kayaking | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 927 | A | my favorite color is blue | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 928 | A | my favorite drink is prosecco | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 929 | A | my favorite food is ramen | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 93 | A | my favorite drink is mango juice | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is mango juice' | FAIL | store did not persist: status=needs_clarification present=False |
| 930 | A | my favorite drink is beet juice | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is beet juice' | FAIL | store did not persist: status=needs_clarification present=False |
| 931 | A | i work as a writer | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 932 | A | i work as a philosopher | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 933 | A | my favorite show is stranger things | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 934 | A | i work as a gardener | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 935 | A | my favorite drink is root beer | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 936 | A | my favorite animal is seahorse | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 937 | A | my favorite music is drum and bass | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 938 | A | my favorite music is edm | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 939 | A | my favorite color is caramel | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 94 | A | my favorite drink is hot toddy | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is hot toddy' | FAIL | store did not persist: status=needs_clarification present=False |
| 940 | A | i am from buenos aires | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 941 | A | my favorite city is chennai | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 942 | A | my favorite food is biryani | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 943 | A | my favorite music is synthwave | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 944 | A | my favorite writer is jules verne | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 945 | A | my favorite movie is parasite | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 946 | A | my favorite color is emerald | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 947 | A | my favorite dessert is rasgulla | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 948 | A | my favorite city is paris | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 949 | A | my favorite cuisine is persian | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 95 | A | my pet's name is tony | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 950 | A | my favorite drink is soda water | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is soda water' | FAIL | store did not persist: status=needs_clarification present=False |
| 951 | A | my favorite movie is good will hunting | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 952 | A | my favorite drink is sparkling lemonade | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 953 | A | my favorite music is indie | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 954 | A | my favorite hobby is calligraphy | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 955 | A | my favorite writer is jorge luis borges | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 956 | A | my favorite drink is rose milk | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is rose milk' | FAIL | store did not persist: status=needs_clarification present=False |
| 957 | A | my favorite movie is moonlight | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 958 | A | my favorite fruit is pomelo | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 959 | A | my favorite subject is calculus | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 96 | A | my favorite subject is art history | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 960 | A | my favorite sport is cricket | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 961 | A | my favorite animal is hedgehog | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 962 | A | my favorite movie is arrival | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 963 | A | my favorite cuisine is polish | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 964 | A | my favorite music is industrial | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 965 | A | my favorite book is atomic habits | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 966 | A | my favorite music is qawwali | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 967 | A | my favorite animal is shark | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 968 | A | my favorite color is orange | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 969 | A | my favorite color is coral | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 97 | A | my favorite writer is astrid lindgren | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 970 | A | my favorite food is poutine | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 971 | A | my favorite food is gumbo | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 972 | A | my favorite subject is database systems | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 973 | A | my favorite movie is there will be blood | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 974 | A | my favorite writer is isabel allende | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 975 | A | my favorite color is ochre | store (durable casual fact persists) | op=update status=updated present=True | PASS |  |
| 976 | A | my favorite drink is lemonade | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 977 | A | my favorite subject is history | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 978 | A | my favorite movie is dune | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 979 | A | my favorite hobby is drumming | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 98 | A | my favorite food is coleslaw | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 980 | A | my favorite game is outer wilds | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 981 | A | my favorite sport is luge | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 982 | A | my favorite hobby is singing | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 983 | A | my favorite writer is amitav ghosh | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 984 | A | my favorite cuisine is vietnamese | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 985 | A | my favorite hobby is art classes | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 986 | A | my favorite cuisine is andhra | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 987 | A | my favorite game is the witcher | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 988 | A | my favorite movie is the boy who harnessed the wind | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 989 | A | i work as a doctor | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 99 | A | my favorite show is mindhunter | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 990 | A | my pet's name is mango | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 991 | A | my pet's name is bailey | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 992 | A | my favorite game is zelda | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 993 | A | my favorite sport is canoeing | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 994 | A | my favorite dessert is sandesh | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 995 | A | my favorite subject is economics | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 996 | A | my favorite drink is rose lemonade | store (durable casual fact persists) | op=store status=needs_clarification fact='My favorite drink is rose lemonade' | FAIL | store did not persist: status=needs_clarification present=False |
| 997 | A | my favorite city is hanoi | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |
| 998 | A | i am from belfast | store (durable casual fact persists) | op=store status=stored present=True | PASS |  |
| 999 | A | my pet's name is ruby | store (durable casual fact persists) | op=store status=updated present=True | PASS |  |

## Issues Found

723 failing/erroring test(s):

- **#10** [A] "my favorite game is demon souls" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact="My favorite game is Demon's Souls"; issue: store did not persist: status=needs_clarification present=False
- **#21** [A] "my favorite drink is birch beer" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is birch beer'; issue: store did not persist: status=needs_clarification present=False
- **#23** [A] "my favorite drink is cider" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is cider'; issue: store did not persist: status=needs_clarification present=False
- **#74** [A] "my favorite music is r&b" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite music is r&b'; issue: store did not persist: status=needs_clarification present=False
- **#88** [A] "my favorite fruit is cloudberry" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite fruit is cloudberry'; issue: store did not persist: status=needs_clarification present=False
- **#93** [A] "my favorite drink is mango juice" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is mango juice'; issue: store did not persist: status=needs_clarification present=False
- **#94** [A] "my favorite drink is hot toddy" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is hot toddy'; issue: store did not persist: status=needs_clarification present=False
- **#104** [A] "my favorite drink is frappe" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is frappe'; issue: store did not persist: status=needs_clarification present=False
- **#108** [A] "my favorite drink is oolong" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is oolong'; issue: store did not persist: status=needs_clarification present=False
- **#109** [A] "my favorite drink is kesar milk" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is kesar milk'; issue: store did not persist: status=needs_clarification present=False
- **#110** [A] "my favorite book is catch 22" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite book is Catch-22'; issue: store did not persist: status=needs_clarification present=False
- **#114** [A] "my favorite color is powder" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite color is powder'; issue: store did not persist: status=needs_clarification present=False
- **#115** [A] "my favorite drink is taro milk tea" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is taro milk tea'; issue: store did not persist: status=needs_clarification present=False
- **#144** [A] "my favorite drink is cold brew" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is cold brew'; issue: store did not persist: status=needs_clarification present=False
- **#149** [A] "my favorite drink is latte" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is latte'; issue: store did not persist: status=needs_clarification present=False
- **#184** [A] "my favorite drink is cola" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is cola'; issue: store did not persist: status=needs_clarification present=False
- **#194** [A] "my favorite drink is ale" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is ale'; issue: store did not persist: status=needs_clarification present=False
- **#202** [A] "my favorite drink is apple cider" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is apple cider'; issue: store did not persist: status=needs_clarification present=False
- **#210** [A] "my favorite drink is coffee" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is coffee'; issue: store did not persist: status=needs_clarification present=False
- **#218** [A] "my favorite drink is limeade" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is limeade'; issue: store did not persist: status=needs_clarification present=False
- **#229** [A] "my favorite writer is charlotte bronte" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite writer is Charlotte Bronté'; issue: store did not persist: status=needs_clarification present=False
- **#279** [A] "my favorite drink is watermelon juice" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is watermelon juice'; issue: store did not persist: status=needs_clarification present=False
- **#284** [A] "my favorite drink is smoothie" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is smoothie'; issue: store did not persist: status=needs_clarification present=False
- **#295** [A] "my favorite drink is sweet lassi" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is sweet lassi'; issue: store did not persist: status=needs_clarification present=False
- **#320** [A] "my favorite drink is cherry soda" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is cherry soda'; issue: store did not persist: status=needs_clarification present=False
- **#323** [A] "my favorite movie is a quiet place" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite movie is A Quiet Place'; issue: store did not persist: status=needs_clarification present=False
- **#356** [A] "my favorite drink is hibiscus tea" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is hibiscus tea'; issue: store did not persist: status=needs_clarification present=False
- **#357** [A] "my favorite writer is emily bronte" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite writer is Emily Bronté'; issue: store did not persist: status=needs_clarification present=False
- **#367** [A] "my favorite show is arcane" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite show is arcane'; issue: store did not persist: status=needs_clarification present=False
- **#398** [A] "my favorite drink is mocha" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is mocha'; issue: store did not persist: status=needs_clarification present=False
- **#411** [A] "my favorite drink is carrot juice" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is carrot juice'; issue: store did not persist: status=needs_clarification present=False
- **#417** [A] "my favorite drink is mead" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is mead'; issue: store did not persist: status=needs_clarification present=False
- **#428** [A] "my favorite drink is matcha" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is matcha'; issue: store did not persist: status=needs_clarification present=False
- **#483** [A] "my favorite drink is eggnog" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is eggnog'; issue: store did not persist: status=needs_clarification present=False
- **#484** [A] "my favorite drink is badam milk" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is badam milk'; issue: store did not persist: status=needs_clarification present=False
- **#498** [A] "my favorite game is half-life 2" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite game is Half Life 2'; issue: store did not persist: status=needs_clarification present=False
- **#499** [A] "my favorite drink is americano" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is americano'; issue: store did not persist: status=needs_clarification present=False
- **#517** [A] "my favorite drink is iced chai" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is iced chai'; issue: store did not persist: status=needs_clarification present=False
- **#520** [A] "my favorite game is pokemon" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite game is Pokémon'; issue: store did not persist: status=needs_clarification present=False
- **#545** [A] "my favorite book is charlotte web" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact="My favorite book is Charlotte's Web"; issue: store did not persist: status=needs_clarification present=False
- **#550** [A] "my favorite drink is milk coffee" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is milk coffee'; issue: store did not persist: status=needs_clarification present=False
- **#552** [A] "my favorite drink is tomato juice" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is tomato juice'; issue: store did not persist: status=needs_clarification present=False
- **#557** [A] "my favorite drink is jasmine tea" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is jasmine tea'; issue: store did not persist: status=needs_clarification present=False
- **#565** [A] "my favorite drink is pineapple juice" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is pineapple juice'; issue: store did not persist: status=needs_clarification present=False
- **#577** [A] "my favorite animal is beetle" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite animal is beetle'; issue: store did not persist: status=needs_clarification present=False
- **#605** [A] "my favorite animal is bat" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite animal is bat'; issue: store did not persist: status=needs_clarification present=False
- **#619** [A] "my favorite drink is espresso" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is espresso'; issue: store did not persist: status=needs_clarification present=False
- **#629** [A] "my favorite drink is mate" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is mate'; issue: store did not persist: status=needs_clarification present=False
- **#667** [A] "my favorite cuisine is tamil" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite cuisine is tamil'; issue: store did not persist: status=needs_clarification present=False
- **#679** [A] "my favorite animal is guinea" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite animal is guinea'; issue: store did not persist: status=needs_clarification present=False
- **#683** [A] "my favorite drink is buttermilk" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is buttermilk'; issue: store did not persist: status=needs_clarification present=False
- **#684** [A] "my favorite drink is affogato" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is affogato'; issue: store did not persist: status=needs_clarification present=False
- **#694** [A] "my favorite drink is milkshake" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is milkshake'; issue: store did not persist: status=needs_clarification present=False
- **#718** [A] "my favorite drink is dirty chai" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is dirty chai'; issue: store did not persist: status=needs_clarification present=False
- **#725** [A] "my favorite game is half-life" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite game is Half Life'; issue: store did not persist: status=needs_clarification present=False
- **#732** [A] "my favorite writer is ita?" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite writer is Ita'; issue: store did not persist: status=needs_clarification present=False
- **#748** [A] "my favorite game is counter-strike" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite game is Counter Strike'; issue: store did not persist: status=needs_clarification present=False
- **#759** [A] "my favorite cuisine is israeli" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite cuisine is Israeli'; issue: store did not persist: status=needs_clarification present=False
- **#762** [A] "my favorite book is the handmaid tale" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact="My favorite book is The Handmaid's Tale"; issue: store did not persist: status=needs_clarification present=False
- **#767** [A] "i am from capetown" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='I am from Cape Town'; issue: store did not persist: status=needs_clarification present=False
- **#770** [A] "my favorite drink is yerba mate" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is yerma te'; issue: store did not persist: status=needs_clarification present=False
- **#797** [A] "my favorite drink is bubble tea" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is bubble tea'; issue: store did not persist: status=needs_clarification present=False
- **#819** [A] "my favorite food is pasta" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite food is pasta'; issue: store did not persist: status=needs_clarification present=False
- **#828** [A] "my favorite book is 1984" — expected: store (durable casual fact persists); actual: op=store status=needs_confirmation fact='My favorite book is 1984'; issue: store did not persist: status=needs_confirmation present=False
- **#843** [A] "my favorite food is tacos" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite food is tacos'; issue: store did not persist: status=needs_clarification present=False
- **#866** [A] "my favorite game is cyberpunk 2077" — expected: store (durable casual fact persists); actual: op=store status=needs_confirmation fact='My favorite game is cyberpunk 2077'; issue: store did not persist: status=needs_confirmation present=False
- **#890** [A] "my favorite drink is chai" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is chai'; issue: store did not persist: status=needs_clarification present=False
- **#919** [A] "my favorite drink is orange soda" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is orange soda'; issue: store did not persist: status=needs_clarification present=False
- **#930** [A] "my favorite drink is beet juice" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is beet juice'; issue: store did not persist: status=needs_clarification present=False
- **#950** [A] "my favorite drink is soda water" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is soda water'; issue: store did not persist: status=needs_clarification present=False
- **#956** [A] "my favorite drink is rose milk" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is rose milk'; issue: store did not persist: status=needs_clarification present=False
- **#996** [A] "my favorite drink is rose lemonade" — expected: store (durable casual fact persists); actual: op=store status=needs_clarification fact='My favorite drink is rose lemonade'; issue: store did not persist: status=needs_clarification present=False
- **#1010** [B] "my favorite breakfast is burrito" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite breakfast is pho'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1017** [B] "my favorite breakfast is poha" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite breakfast is burrito'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1050** [B] "my favorite breakfast is gyoza" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite breakfast is coleslaw'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1109** [B] "my favorite lunch is poutine" — expected: update (old value replaced by new); actual: op=update status=ignored fact='My favorite lunch is biryani'; issue: update not applied: seed=updated status=ignored v2_present=True
- **#1185** [B] "my favorite soup is korean bbq" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite soup is idli'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1198** [B] "my favorite soup is mac and cheese" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite soup is burrito'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1199** [B] "my favorite soup is paratha" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite soup is waffles'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1203** [B] "my favorite soup is gyoza" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite soup is tacos'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1209** [B] "my favorite soup is kebabs" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite soup is sandwich'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1215** [B] "my favorite soup is banh mi" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite soup is burger'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1220** [B] "my favorite soup is nachos" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite soup is pancakes'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1223** [B] "my favorite soup is sandwich" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite soup is kebabs'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=True
- **#1230** [B] "my favorite pasta dish is shepherd pie" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite pasta dish is dumplings'; issue: update not applied: seed=updated status=needs_clarification v2_present=True
- **#1232** [B] "my favorite pasta dish is ramen" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite pasta dish is nachos'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1234** [B] "my favorite pasta dish is waffles" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite pasta dish is dosa'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1235** [B] "my favorite pasta dish is butter chicken" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite pasta dish is idli'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1238** [B] "my favorite pasta dish is oysters" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite pasta dish is tamale'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1239** [B] "my favorite pasta dish is kebabs" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite pasta dish is sushi'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1244** [B] "my favorite pasta dish is burger" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite pasta dish is tacos'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1245** [B] "my favorite pasta dish is coleslaw" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite pasta dish is samosa'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1248** [B] "my favorite pasta dish is onion rings" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite pasta dish is momos'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1250** [B] "my favorite pasta dish is calamari" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite pasta dish is naan'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1253** [B] "my favorite pasta dish is falafel" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite pasta dish is pancakes'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1256** [B] "my favorite pasta dish is burrito" — expected: update (old value replaced by new); actual: op=update status=ignored fact='My favorite pasta dish is falafel'; issue: update not applied: seed=needs_clarification status=ignored v2_present=True
- **#1257** [B] "my favorite pasta dish is tacos" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite pasta dish is sandwich'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1258** [B] "my favorite pasta dish is mac and cheese" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite pasta dish is burrito'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1259** [B] "my favorite pasta dish is risotto" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite pasta dish is curry'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1262** [B] "my favorite pasta dish is hummus plate" — expected: update (old value replaced by new); actual: op=update status=ignored fact='My favorite pasta dish is risotto'; issue: update not applied: seed=needs_clarification status=ignored v2_present=True
- **#1266** [B] "my favorite pasta dish is tamale" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite pasta dish is coleslaw'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1272** [B] "my favorite pasta dish is bruschetta" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite pasta dish is onion rings'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1274** [B] "my favorite pasta dish is empanadas" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite pasta dish is waffles'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1281** [B] "my favorite pasta dish is palak paneer" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite pasta dish is kebabs'; issue: update not applied: seed=updated status=needs_clarification v2_present=True
- **#1282** [B] "my favorite pasta dish is moussaka" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite pasta dish is noodles'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1283** [B] "my favorite pasta dish is ratatouille" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite pasta dish is burger'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1284** [B] "my favorite pasta dish is korean bbq" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite pasta dish is oysters'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1287** [B] "my favorite bread is noodles" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is coleslaw'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1288** [B] "my favorite bread is pancakes" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is gumbo'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1291** [B] "my favorite bread is risotto" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is pancakes'; issue: update not applied: seed=ignored status=needs_clarification v2_present=False
- **#1296** [B] "my favorite bread is coleslaw" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is burrito'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1297** [B] "my favorite bread is biryani" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is calamari'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1299** [B] "my favorite bread is korean bbq" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is nachos'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1303** [B] "my favorite bread is paratha" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is dumplings'; issue: update not applied: seed=updated status=needs_clarification v2_present=True
- **#1306** [B] "my favorite bread is lasagna" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is pasta'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=True
- **#1307** [B] "my favorite bread is naan" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is jambalaya'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1308** [B] "my favorite bread is vindaloo" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is Korean BBQ'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1309** [B] "my favorite bread is falafel" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is gyoza'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1313** [B] "my favorite bread is waffles" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is oysters'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1315** [B] "my favorite bread is ceviche" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is sandwich'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1317** [B] "my favorite bread is gnocchi" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite food is tacos'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1320** [B] "my favorite bread is moussaka" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is pho'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1321** [B] "my favorite bread is palak paneer" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is sushi'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1323** [B] "my favorite bread is mac and cheese" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is waffles'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1324** [B] "my favorite bread is idli" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is noodles'; issue: update not applied: seed=updated status=needs_clarification v2_present=True
- **#1325** [B] "my favorite bread is pizza" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is idli'; issue: update not applied: seed=ignored status=needs_clarification v2_present=True
- **#1326** [B] "my favorite bread is pasta" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is hummus plate'; issue: update not applied: seed=updated status=needs_clarification v2_present=True
- **#1327** [B] "my favorite bread is sushi" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is hot pot'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1328** [B] "my favorite bread is polenta" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is momos'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1330** [B] "my favorite bread is ramen" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is lobster roll'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1331** [B] "my favorite bread is burrito" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is burger'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1332** [B] "my favorite bread is calamari" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is chow mein'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1334** [B] "my favorite bread is dumplings" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is poutine'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1337** [B] "my favorite bread is poha" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is fried rice'; issue: update not applied: seed=ignored status=needs_clarification v2_present=True
- **#1339** [B] "my favorite bread is sandwich" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is samosa'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1340** [B] "my favorite bread is dosa" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is tamale'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1342** [B] "my favorite bread is paella" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite bread is gnocchi'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1345** [B] "my favorite cheese is curry" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is Thai Curry'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1346** [B] "my favorite cheese is gyoza" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is burger'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1347** [B] "my favorite cheese is gnocchi" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is pasta'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1348** [B] "my favorite cheese is chow mein" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is momos'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1350** [B] "my favorite cheese is tamale" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is waffles'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1351** [B] "my favorite cheese is momos" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is hot pot'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1353** [B] "my favorite cheese is poha" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is hummus plate'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=True
- **#1354** [B] "my favorite cheese is banh mi" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is curry'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1355** [B] "my favorite cheese is vindaloo" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is jambalaya'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1356** [B] "my favorite cheese is ratatouille" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is pho'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1358** [B] "my favorite cheese is bhel puri" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is tacos'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1359** [B] "my favorite cheese is shepherd pie" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is coleslaw'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1360** [B] "my favorite cheese is risotto" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is vindaloo'; issue: update not applied: seed=updated status=needs_clarification v2_present=True
- **#1364** [B] "my favorite cheese is hot pot" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is chow mein'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1365** [B] "my favorite cheese is jambalaya" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is burrito'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1366** [B] "my favorite cheese is lobster roll" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is ramen'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1367** [B] "my favorite cheese is sandwich" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is sushi'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1368** [B] "my favorite cheese is guacamole" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is poha'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1369** [B] "my favorite cheese is tacos" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is idli'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1370** [B] "my favorite cheese is samosa" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is fried rice'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=True
- **#1371** [B] "my favorite cheese is calamari" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is oysters'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1372** [B] "my favorite cheese is onion rings" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is biryani'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1373** [B] "my favorite cheese is burger" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is nachos'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1374** [B] "my favorite cheese is falafel" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is gyoza'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1376** [B] "my favorite cheese is thai curry" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is pancakes'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1378** [B] "my favorite cheese is paratha" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is ceviche'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1379** [B] "my favorite cheese is oysters" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is gumbo'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1380** [B] "my favorite cheese is paella" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is onion rings'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1381** [B] "my favorite cheese is biryani" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is lobster roll'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=True
- **#1382** [B] "my favorite cheese is pancakes" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is gnocchi'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1383** [B] "my favorite cheese is hummus plate" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is samosa'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1384** [B] "my favorite cheese is pierogi" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is tamale'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1385** [B] "my favorite cheese is noodles" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is dosa'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=True
- **#1386** [B] "my favorite cheese is pasta" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is noodles'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1387** [B] "my favorite cheese is pizza" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is banh mi'; issue: update not applied: seed=updated status=needs_clarification v2_present=False
- **#1389** [B] "my favorite cheese is pho" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is dumplings'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1391** [B] "my favorite cheese is sushi" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is naan'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1393** [B] "my favorite cheese is bruschetta" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is Korean BBQ'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1394** [B] "my favorite cheese is mac and cheese" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is sandwich'; issue: update not applied: seed=updated status=needs_clarification v2_present=True
- **#1396** [B] "my favorite cheese is fried rice" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is bhel puri'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1398** [B] "my favorite cheese is lasagna" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is kebabs'; issue: update not applied: seed=updated status=needs_clarification v2_present=True
- **#1399** [B] "my favorite cheese is empanadas" — expected: update (old value replaced by new); actual: op=update status=needs_clarification fact='My favorite cheese is falafel'; issue: update not applied: seed=needs_clarification status=needs_clarification v2_present=False
- **#1400** [C] "my favorite juice is smoothie" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1401** [C] "my favorite juice is latte" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1403** [C] "my favorite juice is milk coffee" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1404** [C] "my favorite juice is cafe au lait" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1405** [C] "my favorite juice is soda water" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1409** [C] "my favorite juice is birch beer" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1410** [C] "my favorite juice is pineapple juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1411** [C] "my favorite juice is flat white" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1412** [C] "my favorite juice is pomegranate juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1413** [C] "my favorite juice is beet juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1414** [C] "my favorite juice is bubble tea" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1418** [C] "my favorite juice is sweet lassi" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1419** [C] "my favorite juice is prosecco" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1422** [C] "my favorite juice is hibiscus tea" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1425** [C] "my favorite juice is cherry soda" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1428** [C] "my favorite juice is red wine" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1429** [C] "my favorite juice is sugarcane juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1431** [C] "my favorite juice is cranberry juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1432** [C] "my favorite juice is americano" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1433** [C] "my favorite juice is iced chai" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1436** [C] "my favorite juice is eggnog" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1437** [C] "my favorite juice is mocha" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1439** [C] "my favorite juice is white wine" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1443** [C] "my favorite juice is cappuccino" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1444** [C] "my favorite juice is taro milk tea" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1446** [C] "my favorite juice is mead" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1448** [C] "my favorite juice is yerba mate" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1449** [C] "my favorite juice is badam milk" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1450** [C] "my favorite juice is carrot juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1454** [C] "my favorite juice is mango juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1455** [C] "my favorite juice is jasmine tea" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1456** [C] "my favorite juice is rose milk" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1458** [C] "my favorite milkshake is rose wine" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1460** [C] "my favorite milkshake is guava juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1462** [C] "my favorite milkshake is tomato juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1465** [C] "my favorite milkshake is dirty chai" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1467** [C] "my favorite milkshake is sparkling lemonade" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1468** [C] "my favorite milkshake is cider" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1469** [C] "my favorite milkshake is tonic water" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1471** [C] "my favorite milkshake is mate" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1472** [C] "my favorite milkshake is white wine" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1476** [C] "my favorite milkshake is milk coffee" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1477** [C] "my favorite milkshake is pomegranate juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1479** [C] "my favorite milkshake is ale" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1480** [C] "my favorite milkshake is mango juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1481** [C] "my favorite milkshake is pineapple juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1482** [C] "my favorite milkshake is mead" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1484** [C] "my favorite milkshake is bubble tea" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1486** [C] "my favorite milkshake is watermelon juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1492** [C] "my favorite milkshake is carrot juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1493** [C] "my favorite milkshake is beet juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1495** [C] "my favorite milkshake is grape soda" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1497** [C] "my favorite milkshake is matcha" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1499** [C] "my favorite milkshake is yerba mate" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1505** [C] "my favorite milkshake is iced tea" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1506** [C] "my favorite milkshake is beer" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1507** [C] "my favorite milkshake is sangria" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1510** [C] "my favorite milkshake is prosecco" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1514** [C] "my favorite milkshake is hibiscus tea" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1517** [C] "my favorite smoothie is lassi" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1518** [C] "my favorite smoothie is mead" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1519** [C] "my favorite smoothie is badam milk" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1520** [C] "my favorite smoothie is iced tea" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1522** [C] "my favorite smoothie is jasmine tea" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1523** [C] "my favorite smoothie is sweet lassi" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1524** [C] "my favorite smoothie is cider" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1529** [C] "my favorite smoothie is watermelon juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1530** [C] "my favorite smoothie is ale" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1531** [C] "my favorite smoothie is sparkling water" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1532** [C] "my favorite smoothie is chai" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1533** [C] "my favorite smoothie is latte" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1534** [C] "my favorite smoothie is yerba mate" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1535** [C] "my favorite smoothie is cream soda" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1536** [C] "my favorite smoothie is oolong" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1537** [C] "my favorite smoothie is limeade" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1538** [C] "my favorite smoothie is pineapple juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1539** [C] "my favorite smoothie is grape soda" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1540** [C] "my favorite smoothie is coconut water" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1541** [C] "my favorite smoothie is flat white" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1542** [C] "my favorite smoothie is soda water" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1544** [C] "my favorite smoothie is cola" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1545** [C] "my favorite smoothie is cafe au lait" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1546** [C] "my favorite smoothie is beet juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1547** [C] "my favorite smoothie is kombucha" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1550** [C] "my favorite smoothie is stout" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1553** [C] "my favorite smoothie is coffee" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1554** [C] "my favorite smoothie is cappuccino" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1555** [C] "my favorite smoothie is rose wine" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1556** [C] "my favorite smoothie is hibiscus tea" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1558** [C] "my favorite smoothie is salted lassi" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1560** [C] "my favorite smoothie is americano" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1565** [C] "my favorite smoothie is green tea" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1566** [C] "my favorite smoothie is orange soda" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1568** [C] "my favorite smoothie is guava juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1569** [C] "my favorite smoothie is eggnog" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1570** [C] "my favorite smoothie is mocha" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1572** [C] "my favorite tea is lemonade" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1573** [C] "my favorite tea is red wine" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1574** [C] "my favorite tea is sparkling water" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1577** [C] "my favorite tea is sangria" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1578** [C] "my favorite tea is pineapple juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1581** [C] "my favorite tea is cappuccino" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1584** [C] "my favorite tea is orange juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1587** [C] "my favorite tea is taro milk tea" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1589** [C] "my favorite tea is birch beer" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1590** [C] "my favorite tea is carrot juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1593** [C] "my favorite tea is prosecco" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1594** [C] "my favorite tea is beet juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1595** [C] "my favorite tea is bubble tea" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1596** [C] "my favorite tea is sparkling lemonade" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1597** [C] "my favorite tea is cream soda" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1599** [C] "my favorite tea is mead" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1600** [C] "my favorite tea is cherry soda" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1604** [C] "my favorite tea is ale" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1605** [C] "my favorite tea is grape juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1606** [C] "my favorite tea is frappe" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1607** [C] "my favorite tea is watermelon juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1608** [C] "my favorite tea is fresh lime soda" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1609** [C] "my favorite tea is soda water" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1613** [C] "my favorite tea is sweet lassi" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1614** [C] "my favorite tea is tomato juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1615** [C] "my favorite tea is rose lemonade" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1616** [C] "my favorite tea is smoothie" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1619** [C] "my favorite tea is stout" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1620** [C] "my favorite tea is beer" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1621** [C] "my favorite tea is iced tea" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1622** [C] "my favorite tea is grape soda" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1624** [C] "my favorite tea is sugarcane juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1625** [C] "my favorite tea is orange soda" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1626** [C] "my favorite tea is mango juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1629** [C] "my favorite soda is peppermint tea" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1630** [C] "my favorite soda is flat white" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1632** [C] "my favorite soda is herbal tea" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1633** [C] "my favorite soda is beer" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1637** [C] "my favorite soda is coffee" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1638** [C] "my favorite soda is cider" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1639** [C] "my favorite soda is coconut water" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1640** [C] "my favorite soda is iced tea" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1641** [C] "my favorite soda is latte" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1643** [C] "my favorite soda is pomegranate juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1644** [C] "my favorite soda is green tea" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1646** [C] "my favorite soda is cold brew" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1647** [C] "my favorite soda is matcha" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1648** [C] "my favorite soda is rose lemonade" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1649** [C] "my favorite soda is red wine" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1651** [C] "my favorite soda is tomato juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1652** [C] "my favorite soda is grape juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1653** [C] "my favorite soda is sparkling lemonade" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1654** [C] "my favorite soda is mead" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1655** [C] "my favorite soda is frappe" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1656** [C] "my favorite soda is sangria" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1657** [C] "my favorite soda is chamomile" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1658** [C] "my favorite soda is falooda" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1659** [C] "my favorite soda is sweet lassi" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1661** [C] "my favorite soda is rose wine" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1662** [C] "my favorite soda is soda water" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1663** [C] "my favorite soda is iced chai" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1665** [C] "my favorite soda is kombucha" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1666** [C] "my favorite soda is taro milk tea" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1667** [C] "my favorite soda is smoothie" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1668** [C] "my favorite soda is orange juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1669** [C] "my favorite soda is ale" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1670** [C] "my favorite soda is birch beer" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1671** [C] "my favorite soda is apple juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1672** [C] "my favorite soda is hibiscus tea" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1674** [C] "my favorite soda is yerba mate" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1675** [C] "my favorite soda is cafe au lait" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1676** [C] "my favorite soda is rose milk" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1678** [C] "my favorite soda is eggnog" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1679** [C] "my favorite soda is lemonade" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1681** [C] "my favorite soda is oolong" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1682** [C] "my favorite soda is white wine" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1688** [C] "my favorite shake is buttermilk" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1691** [C] "my favorite shake is latte" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1696** [C] "my favorite shake is chai" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1697** [C] "my favorite shake is mocha" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1702** [C] "my favorite shake is chamomile" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1703** [C] "my favorite shake is lassi" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1704** [C] "my favorite shake is beer" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1705** [C] "my favorite shake is soda water" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1706** [C] "my favorite shake is tonic water" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1707** [C] "my favorite shake is ale" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1710** [C] "my favorite shake is badam milk" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1711** [C] "my favorite shake is red wine" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1712** [C] "my favorite shake is lemonade" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1713** [C] "my favorite shake is sangria" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1714** [C] "my favorite shake is mead" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1715** [C] "my favorite shake is smoothie" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1716** [C] "my favorite shake is beet juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1718** [C] "my favorite shake is yerba mate" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1724** [C] "my favorite shake is flat white" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1727** [C] "my favorite shake is coffee" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1728** [C] "my favorite shake is frappe" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1731** [C] "my favorite shake is kombucha" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1732** [C] "my favorite shake is stout" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1733** [C] "my favorite shake is orange soda" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1738** [C] "my favorite shake is white wine" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1739** [C] "my favorite shake is birch beer" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1740** [C] "my favorite shake is cappuccino" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1741** [C] "my favorite shake is mate" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1742** [C] "my favorite shake is iced matcha" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1743** [C] "my favorite mocktail is chamomile" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1745** [C] "my favorite mocktail is birch beer" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1746** [C] "my favorite mocktail is latte" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1748** [C] "my favorite mocktail is matcha" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1749** [C] "my favorite mocktail is cafe au lait" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1753** [C] "my favorite mocktail is badam milk" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1754** [C] "my favorite mocktail is cola" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1755** [C] "my favorite mocktail is taro milk tea" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1757** [C] "my favorite mocktail is espresso" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1759** [C] "my favorite mocktail is limeade" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1760** [C] "my favorite mocktail is cappuccino" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1763** [C] "my favorite mocktail is sugarcane juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1765** [C] "my favorite mocktail is stout" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1766** [C] "my favorite mocktail is rose wine" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1768** [C] "my favorite mocktail is grape soda" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1770** [C] "my favorite mocktail is hibiscus tea" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1771** [C] "my favorite mocktail is dirty chai" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1773** [C] "my favorite mocktail is mead" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1774** [C] "my favorite mocktail is guava juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1776** [C] "my favorite mocktail is cream soda" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1777** [C] "my favorite mocktail is orange juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1779** [C] "my favorite mocktail is smoothie" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1781** [C] "my favorite mocktail is beer" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1783** [C] "my favorite mocktail is cherry soda" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1784** [C] "my favorite mocktail is soda water" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1786** [C] "my favorite mocktail is jasmine tea" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1788** [C] "my favorite mocktail is rose milk" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1790** [C] "my favorite mocktail is watermelon juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1791** [C] "my favorite mocktail is beet juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1792** [C] "my favorite mocktail is buttermilk" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1793** [C] "my favorite mocktail is grape juice" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1794** [C] "my favorite mocktail is lemonade" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1798** [C] "my favorite mocktail is prosecco" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#1799** [C] "my favorite mocktail is falooda" — expected: forget (op=forget and fact removed); actual: op=forget status=needs_clarification; issue: forget gate failed: status=needs_clarification
- **#2200** [D] "give me advice about blog post" — expected: no write; actual: op=store conf=1.0; issue: no-write message produced a write: op=store fact='I need advice on a blog post'
- **#2271** [D] "give me advice about presentation" — expected: no write; actual: op=store conf=1.0; issue: no-write message produced a write: op=store fact='I need advice on a presentation'
- **#2646** [D] "give me advice about hackathon" — expected: no write; actual: op=store conf=1.0; issue: no-write message produced a write: op=store fact='I want to know about hackathons'
- **#3391** [D] "give me advice about newsletter" — expected: no write; actual: op=store conf=1.0; issue: no-write message produced a write: op=store fact='Newsletter'
- **#3569** [D] "give me advice about research paper" — expected: no write; actual: op=store conf=1.0; issue: no-write message produced a write: op=store fact='I need advice on a research paper'
- **#3652** [E] "anything from our chat about job interview" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3654** [E] "remind me what we planned for research internship" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3657** [E] "anything from our chat about painting class" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3658** [E] "remind me what we planned for machine learning model" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3659** [E] "remind me what we planned for performance tuning" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3662** [E] "anything from our chat about api integration" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3665** [E] "anything from our chat about performance tuning" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3666** [E] "remind me what we planned for api integration" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3669** [E] "anything from our chat about kitchen renovation" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3672** [E] "anything from our chat about code refactor" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3673** [E] "remind me what we planned for branding" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3677** [E] "remind me what we planned for painting class" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3678** [E] "anything from our chat about youtube channel" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3680** [E] "anything from our chat about visa process" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3683** [E] "remind me what we planned for marathon training" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3691** [E] "anything from our chat about research internship" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3695** [E] "remind me what we planned for fitness routine" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3697** [E] "remind me what we planned for side hustle" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3698** [E] "remind me what we planned for garden layout" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3700** [E] "anything from our chat about database migration" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3702** [E] "anything from our chat about c program" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3704** [E] "remind me what we planned for c program" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3707** [E] "anything from our chat about marathon training" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3709** [E] "anything from our chat about game jam" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3710** [E] "remind me what we planned for game jam" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3713** [E] "anything from our chat about debate prep" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3719** [E] "anything from our chat about research paper" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3720** [E] "remind me what we planned for bug hunting" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3722** [E] "remind me what we planned for visa process" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3723** [E] "remind me what we planned for tax filing" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3729** [E] "anything from our chat about language learning" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3730** [E] "remind me what we planned for code refactor" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3731** [E] "remind me what we planned for meal prep" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3733** [E] "remind me what we planned for internship application" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3737** [E] "anything from our chat about resume building" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3738** [E] "remind me what we planned for salary negotiation" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3740** [E] "remind me what we planned for home office setup" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3742** [E] "anything from our chat about guitar lesson" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3751** [E] "remind me what we planned for business plan" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3753** [E] "anything from our chat about movie night" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3754** [E] "remind me what we planned for resume building" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3762** [E] "anything from our chat about photography trip" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3768** [E] "remind me what we planned for rust project" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3776** [E] "anything from our chat about salary negotiation" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3778** [E] "remind me what we planned for app prototype" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3783** [E] "anything from our chat about ui design" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3784** [E] "remind me what we planned for ui design" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3785** [E] "remind me what we planned for exam preparation" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3790** [E] "anything from our chat about pet adoption" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3794** [E] "anything from our chat about hackathon" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3795** [E] "anything from our chat about data analysis project" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3796** [E] "anything from our chat about bug hunting" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3797** [E] "anything from our chat about garden layout" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3800** [E] "remind me what we planned for website redesign" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3802** [E] "anything from our chat about gaming setup" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3804** [E] "anything from our chat about book club" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3809** [E] "anything from our chat about apartment hunting" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3810** [E] "remind me what we planned for streaming setup" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3811** [E] "remind me what we planned for blog post" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3814** [E] "anything from our chat about python project" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3816** [E] "anything from our chat about cooking class" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3819** [E] "anything from our chat about website redesign" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3822** [E] "remind me what we planned for cooking class" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3824** [E] "anything from our chat about start-up pitch" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3826** [E] "anything from our chat about home office setup" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3828** [E] "remind me what we planned for python project" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3835** [E] "remind me what we planned for database migration" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3837** [E] "remind me what we planned for science fair" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3840** [E] "anything from our chat about chess bot" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3842** [E] "anything from our chat about streaming setup" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3843** [E] "remind me what we planned for start-up pitch" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3846** [E] "anything from our chat about group project" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3847** [E] "remind me what we planned for debate prep" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3849** [E] "anything from our chat about machine learning model" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3850** [E] "anything from our chat about exam preparation" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3852** [E] "remind me what we planned for bike repair" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3854** [E] "anything from our chat about thesis" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3855** [E] "anything from our chat about rust project" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3860** [E] "anything from our chat about marketing campaign" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3862** [E] "anything from our chat about homework help" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3864** [E] "remind me what we planned for apartment hunting" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3865** [E] "anything from our chat about study group" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3867** [E] "remind me what we planned for chess bot" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3869** [E] "remind me what we planned for product idea" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3870** [E] "anything from our chat about internship application" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3872** [E] "anything from our chat about branding" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3875** [E] "anything from our chat about app prototype" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3877** [E] "remind me what we planned for social media plan" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3883** [E] "anything from our chat about podcast idea" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3887** [E] "remind me what we planned for language learning" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3891** [E] "remind me what we planned for group project" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3893** [E] "anything from our chat about science fair" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3895** [E] "remind me what we planned for research paper" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3902** [E] "anything from our chat about tax filing" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3903** [E] "remind me what we planned for guitar lesson" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3905** [E] "anything from our chat about newsletter" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3907** [E] "remind me what we planned for podcast idea" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3910** [E] "remind me what we planned for homework help" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3911** [E] "anything from our chat about bike repair" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3912** [E] "anything from our chat about insurance plan" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3916** [E] "remind me what we planned for insurance plan" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3918** [E] "remind me what we planned for gaming setup" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3921** [E] "anything from our chat about product idea" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3923** [E] "remind me what we planned for data analysis project" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3929** [E] "remind me what we planned for thesis" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3930** [E] "anything from our chat about blog post" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3934** [E] "anything from our chat about presentation" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3936** [E] "remind me what we planned for newsletter" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3940** [E] "anything from our chat about meal prep" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3941** [E] "anything from our chat about twitch stream" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3943** [E] "remind me what we planned for youtube channel" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3945** [E] "anything from our chat about fitness routine" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3949** [E] "anything from our chat about side hustle" — expected: episodic recall (use_episodes + episodes); actual: use_episodes=False; issue: recall not routed to episodes
- **#3952** [F] "now my favorite coffee is mocha" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite coffee is root beer'; issue: context update not applied: status=updated
- **#3953** [F] "actually my favorite coffee is now flat white" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite coffee is cafe au lait'; issue: context update not applied: status=updated
- **#3954** [F] "no wait, i prefer sangria for my favorite coffee" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite coffee is yerba mate'; issue: context update not applied: status=updated
- **#3955** [F] "no wait, i prefer hot chocolate for my favorite coffee" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite coffee is hibiscus tea'; issue: context update not applied: status=updated
- **#3956** [F] "no wait, i prefer watermelon juice for my favorite coffee" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite coffee is jasmine tea'; issue: context update not applied: status=needs_clarification
- **#3960** [F] "now my favorite coffee is pomegranate juice" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite coffee is sugarcane juice'; issue: context update not applied: status=updated
- **#3961** [F] "now my favorite coffee is cappuccino" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite coffee is cherry soda'; issue: context update not applied: status=updated
- **#3962** [F] "actually my favorite coffee is now limeade" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite coffee is salted lassi'; issue: context update not applied: status=updated
- **#3963** [F] "now my favorite coffee is mate" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite coffee is latte'; issue: context update not applied: status=updated
- **#3966** [F] "no wait, i prefer iced tea for my favorite coffee" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite coffee is rose milk'; issue: context update not applied: status=updated
- **#3967** [F] "actually my favorite coffee is now cranberry juice" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite coffee is kombucha'; issue: context update not applied: status=updated
- **#3968** [F] "now my favorite coffee is peppermint tea" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite coffee is frappe'; issue: context update not applied: status=needs_clarification
- **#3969** [F] "now my favorite coffee is white wine" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite coffee is white wine'; issue: context update not applied: status=needs_clarification
- **#3970** [F] "no wait, i prefer bubble tea for my favorite coffee" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite coffee is rose wine'; issue: context update not applied: status=needs_clarification
- **#3972** [F] "no wait, i prefer fresh lime soda for my favorite coffee" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite coffee is green tea'; issue: context update not applied: status=needs_clarification
- **#3975** [F] "actually my favorite coffee is now tomato juice" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite coffee is taro milk tea'; issue: context update not applied: status=updated
- **#3977** [F] "now my favorite coffee is matcha" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite coffee is dirty chai'; issue: context update not applied: status=updated
- **#3978** [F] "actually my favorite coffee is now sparkling water" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite coffee is sparkling water'; issue: context update not applied: status=needs_clarification
- **#3979** [F] "no wait, i prefer jasmine tea for my favorite coffee" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite coffee is beer'; issue: context update not applied: status=needs_clarification
- **#3980** [F] "no wait, i prefer orange soda for my favorite coffee" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite coffee is bubble tea'; issue: context update not applied: status=needs_clarification
- **#3981** [F] "no wait, i prefer kesar milk for my favorite coffee" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite coffee is sparkling lemonade'; issue: context update not applied: status=needs_clarification
- **#3982** [F] "actually my favorite coffee is now soda water" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite coffee is cappuccino'; issue: context update not applied: status=updated
- **#3983** [F] "actually my favorite coffee is now grape juice" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite coffee is falooda'; issue: context update not applied: status=updated
- **#3984** [F] "actually my favorite coffee is now sparkling lemonade" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite coffee is mocha'; issue: context update not applied: status=updated
- **#3985** [F] "no wait, i prefer sweet lassi for my favorite coffee" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite coffee is black tea'; issue: context update not applied: status=needs_clarification
- **#3986** [F] "no wait, i prefer mead for my favorite coffee" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite coffee is orange juice'; issue: context update not applied: status=needs_clarification
- **#3987** [F] "no wait, i prefer hibiscus tea for my favorite coffee" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite coffee is peppermint tea'; issue: context update not applied: status=needs_clarification
- **#3988** [F] "no wait, i prefer ginger ale for my favorite coffee" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite coffee is herbal tea'; issue: context update not applied: status=needs_clarification
- **#3989** [F] "no wait, i prefer guava juice for my favorite coffee" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite coffee is milkshake'; issue: context update not applied: status=needs_clarification
- **#3990** [F] "no wait, i prefer smoothie for my favorite coffee" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite coffee is grape juice'; issue: context update not applied: status=needs_clarification
- **#3991** [F] "no wait, i prefer cider for my favorite coffee" — expected: context-aware write or safe follow-up; actual: ; issue: analyze failed: (None, None)
- **#3992** [F] "now my favorite coffee is iced chai" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite coffee is sweet lassi'; issue: context update not applied: status=updated
- **#3993** [F] "now my favorite coffee is milk coffee" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite coffee is hot toddy'; issue: context update not applied: status=updated
- **#3997** [F] "actually my favorite coffee is now dirty chai" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite coffee is cream soda'; issue: context update not applied: status=updated
- **#3998** [F] "now my favorite coffee is iced matcha" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite coffee is iced chai'; issue: context update not applied: status=updated
- **#3999** [F] "no wait, i prefer lassi for my favorite coffee" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite coffee is milk coffee'; issue: context update not applied: status=needs_clarification
- **#4002** [F] "no wait, i prefer mango lassi for my favorite coffee" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite coffee is ginger ale'; issue: context update not applied: status=needs_clarification
- **#4004** [F] "no wait, i prefer donuts for my favorite pastry" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite pastry is rice pudding'; issue: context update not applied: status=needs_clarification
- **#4006** [F] "no wait, i prefer beignets for my favorite pastry" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite pastry is apple pie'; issue: context update not applied: status=updated
- **#4008** [F] "actually my favorite pastry is now brownie sundae" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite pastry is pavlova'; issue: context update not applied: status=updated
- **#4009** [F] "no wait, i prefer jalebi for my favorite pastry" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite pastry is rasgulla'; issue: context update not applied: status=needs_clarification
- **#4010** [F] "no wait, i prefer kulfi for my favorite pastry" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite pastry is panna cotta'; issue: context update not applied: status=needs_clarification
- **#4011** [F] "no wait, i prefer gulab jamun for my favorite pastry" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite pastry is donuts'; issue: context update not applied: status=needs_clarification
- **#4012** [F] "no wait, i prefer baklava for my favorite pastry" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite pastry is beignets'; issue: context update not applied: status=needs_clarification
- **#4013** [F] "now my favorite pastry is rasgulla" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite pastry is tarte tatin'; issue: context update not applied: status=needs_clarification
- **#4014** [F] "now my favorite pastry is phirni" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite pastry is kheer'; issue: context update not applied: status=updated
- **#4015** [F] "no wait, i prefer macarons for my favorite pastry" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite pastry is carrot cake'; issue: context update not applied: status=updated
- **#4016** [F] "now my favorite pastry is lemon tart" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite pastry is brownie sundae'; issue: context update not applied: status=updated
- **#4017** [F] "no wait, i prefer key lime pie for my favorite pastry" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite pastry is macarons'; issue: context update not applied: status=updated
- **#4019** [F] "no wait, i prefer banana bread for my favorite pastry" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite pastry is pound cake'; issue: context update not applied: status=updated
- **#4020** [F] "no wait, i prefer chocolate cake for my favorite pastry" — expected: context-aware write or safe follow-up; actual: ; issue: analyze failed: (None, None)
- **#4022** [F] "no wait, i prefer funnel cake for my favorite pastry" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite pastry is eclair'; issue: context update not applied: status=needs_clarification
- **#4026** [F] "no wait, i prefer lamington for my favorite pastry" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite pastry is sandesh'; issue: context update not applied: status=updated
- **#4027** [F] "no wait, i prefer crepes for my favorite pastry" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite pastry is coconut barfi'; issue: context update not applied: status=updated
- **#4030** [F] "now my favorite pastry is tiramisu" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite pastry is profiteroles'; issue: context update not applied: status=updated
- **#4032** [F] "no wait, i prefer mishti doi for my favorite pastry" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite pastry is lemon tart'; issue: context update not applied: status=needs_clarification
- **#4034** [F] "no wait, i prefer creme brulee for my favorite pastry" — expected: context-aware write or safe follow-up; actual: ; issue: analyze failed: (None, None)
- **#4035** [F] "no wait, i prefer pumpkin pie for my favorite pastry" — expected: context-aware write or safe follow-up; actual: ; issue: analyze failed: (None, None)
- **#4037** [F] "actually my favorite pastry is now sandesh" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite pastry is brownies'; issue: context update not applied: status=updated
- **#4040** [F] "no wait, i prefer red velvet cake for my favorite pastry" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite pastry is cheesecake'; issue: context update not applied: status=updated
- **#4043** [F] "now my favorite pastry is pecan pie" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite pastry is mishti doi'; issue: context update not applied: status=updated
- **#4044** [F] "actually my favorite pastry is now laddu" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite pastry is kulfi'; issue: context update not applied: status=updated
- **#4045** [F] "now my favorite pastry is panna cotta" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite pastry is funnel cake'; issue: context update not applied: status=updated
- **#4046** [F] "now my favorite pastry is sponge cake" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite pastry is souffle'; issue: context update not applied: status=updated
- **#4049** [F] "no wait, i prefer churros for my favorite pastry" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite pastry is banana bread'; issue: context update not applied: status=updated
- **#4052** [F] "actually my favorite pastry is now rasmalai" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite pastry is cinnamon roll'; issue: context update not applied: status=updated
- **#4053** [F] "no wait, i prefer macaron tower for my favorite pastry" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite pastry is gulab jamun'; issue: context update not applied: status=updated
- **#4054** [F] "now my favorite pastry is tarte tatin" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite pastry is tiramisu'; issue: context update not applied: status=updated
- **#4055** [F] "now my favorite pastry is pound cake" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite pastry is sponge cake'; issue: context update not applied: status=updated
- **#4056** [F] "now my favorite cake is mousse" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite cake is key lime pie'; issue: context update not applied: status=updated
- **#4058** [F] "no wait, i prefer kulfi for my favorite cake" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite cake is sponge cake'; issue: context update not applied: status=needs_clarification
- **#4061** [F] "now my favorite cake is coconut barfi" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite cake is pound cake'; issue: context update not applied: status=updated
- **#4062** [F] "no wait, i prefer phirni for my favorite cake" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite cake is caramel custard'; issue: context update not applied: status=needs_clarification
- **#4063** [F] "no wait, i prefer beignets for my favorite cake" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite cake is rasgulla'; issue: context update not applied: status=needs_clarification
- **#4064** [F] "no wait, i prefer gulab jamun for my favorite cake" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite cake is macaron tower'; issue: context update not applied: status=needs_clarification
- **#4066** [F] "no wait, i prefer souffle for my favorite cake" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite cake is brownies'; issue: context update not applied: status=updated
- **#4070** [F] "now my favorite cake is sandesh" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite cake is tarte tatin'; issue: context update not applied: status=needs_clarification
- **#4073** [F] "no wait, i prefer kheer for my favorite cake" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite cake is pavlova'; issue: context update not applied: status=needs_clarification
- **#4074** [F] "no wait, i prefer jalebi for my favorite cake" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite cake is mousse'; issue: context update not applied: status=needs_clarification
- **#4075** [F] "now my favorite cake is rice pudding" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite cake is coconut barfi'; issue: context update not applied: status=updated
- **#4077** [F] "no wait, i prefer angel food cake for my favorite cake" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite cake is souffle'; issue: context update not applied: status=updated
- **#4079** [F] "no wait, i prefer ice cream for my favorite cake" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite cake is carrot cake'; issue: context update not applied: status=needs_clarification
- **#4080** [F] "no wait, i prefer rasgulla for my favorite cake" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite cake is laddu'; issue: context update not applied: status=needs_clarification
- **#4084** [F] "now my favorite cake is lamington" — expected: context-aware write or safe follow-up; actual: op=update status=ignored fact='My favorite cake is crepes'; issue: context update not applied: status=ignored
- **#4085** [F] "no wait, i prefer macaron tower for my favorite cake" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite cake is bread pudding'; issue: context update not applied: status=updated
- **#4086** [F] "no wait, i prefer profiteroles for my favorite cake" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite cake is lemon tart'; issue: context update not applied: status=updated
- **#4088** [F] "no wait, i prefer funnel cake for my favorite cake" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite cake is angel food cake'; issue: context update not applied: status=needs_clarification
- **#4090** [F] "no wait, i prefer key lime pie for my favorite cake" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite cake is kulfi'; issue: context update not applied: status=needs_clarification
- **#4091** [F] "actually my favorite cake is now donuts" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite cake is phirni'; issue: context update not applied: status=updated
- **#4092** [F] "actually my favorite cake is now rasmalai" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite cake is mochi'; issue: context update not applied: status=updated
- **#4093** [F] "no wait, i prefer banana bread for my favorite cake" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite cake is apple pie'; issue: context update not applied: status=needs_clarification
- **#4096** [F] "now my favorite cake is churros" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite cake is kheer'; issue: context update not applied: status=updated
- **#4098** [F] "no wait, i prefer barfi for my favorite cake" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite cake is rice pudding'; issue: context update not applied: status=needs_clarification
- **#4100** [F] "now my favorite cake is chocolate cake" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite cake is pumpkin pie'; issue: context update not applied: status=updated
- **#4102** [F] "no wait, i prefer carrot cake for my favorite cake" — expected: context-aware write or safe follow-up; actual: ; issue: analyze failed: (None, None)
- **#4103** [F] "now my favorite cake is laddu" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite cake is lamington'; issue: context update not applied: status=needs_clarification
- **#4106** [F] "now my favorite cake is mishti doi" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite cake is baklava'; issue: context update not applied: status=updated
- **#4107** [F] "now my favorite cake is caramel custard" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite cake is barfi'; issue: context update not applied: status=updated
- **#4109** [F] "now my favorite candy is pumpkin pie" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite candy is brownies'; issue: context update not applied: status=updated
- **#4111** [F] "no wait, i prefer souffle for my favorite candy" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite candy is souffle'; issue: context update not applied: status=needs_clarification
- **#4112** [F] "no wait, i prefer profiteroles for my favorite candy" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite candy is pavlova'; issue: context update not applied: status=needs_clarification
- **#4113** [F] "now my favorite candy is apple pie" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite candy is barfi'; issue: context update not applied: status=updated
- **#4115** [F] "now my favorite candy is carrot cake" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite candy is macarons'; issue: context update not applied: status=updated
- **#4116** [F] "now my favorite candy is baklava" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite candy is fudge'; issue: context update not applied: status=needs_clarification
- **#4119** [F] "now my favorite candy is laddu" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite candy is rasgulla'; issue: context update not applied: status=updated
- **#4120** [F] "now my favorite candy is rasmalai" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite candy is cinnamon roll'; issue: context update not applied: status=updated
- **#4122** [F] "no wait, i prefer coconut barfi for my favorite candy" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite candy is eclair'; issue: context update not applied: status=needs_clarification
- **#4125** [F] "now my favorite candy is churros" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite candy is kulfi'; issue: context update not applied: status=updated
- **#4127** [F] "no wait, i prefer key lime pie for my favorite candy" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite candy is cheesecake'; issue: context update not applied: status=updated
- **#4130** [F] "now my favorite candy is beignets" — expected: context-aware write or safe follow-up; actual: op=update status=ignored fact='My favorite candy is lemon tart'; issue: context update not applied: status=ignored
- **#4131** [F] "no wait, i prefer lamington for my favorite candy" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite candy is jalebi'; issue: context update not applied: status=updated
- **#4132** [F] "actually my favorite candy is now jalebi" — expected: context-aware write or safe follow-up; actual: op=update status=ignored fact='My favorite candy is jalebi'; issue: context update not applied: status=ignored
- **#4133** [F] "no wait, i prefer macaron tower for my favorite candy" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite candy is coconut barfi'; issue: context update not applied: status=needs_clarification
- **#4135** [F] "now my favorite candy is rasgulla" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite candy is rice pudding'; issue: context update not applied: status=needs_clarification
- **#4137** [F] "no wait, i prefer macarons for my favorite candy" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite candy is macaron tower'; issue: context update not applied: status=updated
- **#4140** [F] "no wait, i prefer angel food cake for my favorite candy" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite candy is caramel custard'; issue: context update not applied: status=needs_clarification
- **#4143** [F] "no wait, i prefer cheesecake for my favorite candy" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite candy is banana bread'; issue: context update not applied: status=needs_clarification
- **#4145** [F] "no wait, i prefer kheer for my favorite candy" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite candy is lamington'; issue: context update not applied: status=needs_clarification
- **#4146** [F] "no wait, i prefer crepes for my favorite candy" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite candy is crepes'; issue: context update not applied: status=needs_clarification
- **#4147** [F] "no wait, i prefer mango pudding for my favorite candy" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite candy is phirni'; issue: context update not applied: status=needs_clarification
- **#4149** [F] "now my favorite candy is bread pudding" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite candy is pecan pie'; issue: context update not applied: status=updated
- **#4152** [F] "no wait, i prefer donuts for my favorite candy" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite candy is mochi'; issue: context update not applied: status=needs_clarification
- **#4154** [F] "actually my favorite candy is now mishti doi" — expected: context-aware write or safe follow-up; actual: op=update status=updated fact='My favorite candy is crepes'; issue: context update not applied: status=updated
- **#4155** [F] "no wait, i prefer tarte tatin for my favorite candy" — expected: context-aware write or safe follow-up; actual: op=update status=needs_clarification fact='My favorite candy is pumpkin pie'; issue: context update not applied: status=needs_clarification
- **#4335** [G] "so, set that aside" — expected: no write (session/meta); actual: op=store es=False; issue: session-end/dismissal wrote: op=store fact="I want to set aside the conversation about my laptop's GPU."
- **#4344** [G] "um, set that aside" — expected: no write (session/meta); actual: op=store es=False; issue: session-end/dismissal wrote: op=store fact='I study B.Tech'
- **#4361** [G] "hmm, i need to rest now" — expected: no write (session/meta); actual: op=store es=False; issue: session-end/dismissal wrote: op=store fact='I need to rest now'
- **#4366** [G] "set that aside" — expected: no write (session/meta); actual: op=store es=False; issue: session-end/dismissal wrote: op=store fact='I set that aside'
- **#4374** [G] "yeah, set that aside" — expected: no write (session/meta); actual: op=update es=False; issue: session-end/dismissal wrote: op=update fact='My favorite editor is PyCharm'
- **#4397** [G] "um, power down" — expected: no write (session/meta); actual: op=store es=False; issue: session-end/dismissal wrote: op=store fact='My laptop has an RTX 4050'
- **#4430** [G] "hmm, i am going to rest" — expected: no write (session/meta); actual: op=store es=False; issue: session-end/dismissal wrote: op=store fact='I will rest'
- **#4437** [G] "hmm, power down" — expected: no write (session/meta); actual: op=store es=False; issue: session-end/dismissal wrote: op=store fact='My laptop has an RTX 4050'
- **#4440** [G] "yeah, i am going to rest" — expected: no write (session/meta); actual: op=store es=False; issue: session-end/dismissal wrote: op=store fact='I will rest'
- **#4441** [G] "hmm, sleep" — expected: no write (session/meta); actual: op=store es=False; issue: session-end/dismissal wrote: op=store fact='I need to sleep'
- **#4451** [G] "shelve this topic" — expected: no write (session/meta); actual: op=store es=False; issue: session-end/dismissal wrote: op=store fact="I want to shelve the topic of my laptop's GPU"
- **#4489** [G] "um, go offline now" — expected: no write (session/meta); actual: op=store es=False; issue: session-end/dismissal wrote: op=store fact='I want to go offline'
- **#4495** [G] "hmm, turn off" — expected: no write (session/meta); actual: op=store es=False; issue: session-end/dismissal wrote: op=store fact='I want to turn off the device'
- **#4499** [G] "hmm, set that aside" — expected: no write (session/meta); actual: op=store es=False; issue: session-end/dismissal wrote: op=store fact='I will set the conversation aside for now'
- **#4500** [G] "i am going to rest" — expected: no write (session/meta); actual: op=store es=False; issue: session-end/dismissal wrote: op=store fact='I will rest'
- **#4511** [G] "so, this session is over" — expected: no write (session/meta); actual: ; issue: analyze failed: (None, None)
- **#4539** [G] "hmm, shut down" — expected: no write (session/meta); actual: op=store es=False; issue: session-end/dismissal wrote: op=store fact='My laptop has an RTX 4050'
- **#4547** [G] "so, shelve this topic" — expected: no write (session/meta); actual: op=store es=False; issue: session-end/dismissal wrote: op=store fact="I don't want to discuss the RTX 4050 anymore"
- **#4560** [G] "hmm, let me go" — expected: no write (session/meta); actual: op=store es=False; issue: session-end/dismissal wrote: op=store fact='I study btag'
- **#4563** [G] "um, shelve this topic" — expected: no write (session/meta); actual: op=store es=False; issue: session-end/dismissal wrote: op=store fact='I want to shelve the conversation about btag'
- **#4591** [G] "okay, set that aside" — expected: no write (session/meta); actual: op=store es=False; issue: session-end/dismissal wrote: op=store fact='I want to set aside the previous conversation'
- **#4860** [R-sem] "my favorite salad is korean bbq" — expected: retrieved (semantic); actual: results=0 retrieved=[]; issue: stored fact not retrieved (use_memory=True)
- **#4865** [R-sem] "my favorite salad is butter chicken" — expected: retrieved (semantic); actual: results=0 retrieved=[]; issue: stored fact not retrieved (use_memory=True)
- **#4867** [R-sem] "my favorite salad is tamale" — expected: retrieved (semantic); actual: results=0 retrieved=[]; issue: stored fact not retrieved (use_memory=True)
- **#4870** [R-sem] "my favorite sauce is dosa" — expected: retrieved (semantic); actual: results=0 retrieved=[]; issue: stored fact not retrieved (use_memory=True)
- **#4871** [R-sem] "my favorite sauce is ramen" — expected: retrieved (semantic); actual: results=0 retrieved=[]; issue: stored fact not retrieved (use_memory=True)
- **#4873** [R-sem] "my favorite sauce is nachos" — expected: retrieved (semantic); actual: results=0 retrieved=[]; issue: stored fact not retrieved (use_memory=True)
- **#4874** [R-sem] "my favorite sauce is sandwich" — expected: retrieved (semantic); actual: results=0 retrieved=[]; issue: stored fact not retrieved (use_memory=True)
- **#4876** [R-sem] "my favorite sauce is naan" — expected: retrieved (semantic); actual: results=0 retrieved=[]; issue: stored fact not retrieved (use_memory=True)
- **#4877** [R-sem] "my favorite sauce is idli" — expected: retrieved (semantic); actual: results=0 retrieved=[]; issue: stored fact not retrieved (use_memory=True)
- **#4878** [R-sem] "my favorite sauce is gnocchi" — expected: retrieved (semantic); actual: results=0 retrieved=[]; issue: stored fact not retrieved (use_memory=True)
- **#4879** [R-sem] "my favorite sauce is poutine" — expected: retrieved (semantic); actual: results=0 retrieved=[]; issue: stored fact not retrieved (use_memory=True)
- **#4880** [R-sem] "my favorite dip is poutine" — expected: retrieved (semantic); actual: results=0 retrieved=[]; issue: stored fact not retrieved (use_memory=True)
- **#4883** [R-sem] "my favorite dip is momos" — expected: retrieved (semantic); actual: results=0 retrieved=[]; issue: stored fact not retrieved (use_memory=True)
- **#4886** [R-sem] "my favorite dip is empanadas" — expected: retrieved (semantic); actual: results=0 retrieved=[]; issue: stored fact not retrieved (use_memory=True)
- **#4889** [R-sem] "my favorite dip is idli" — expected: retrieved (semantic); actual: results=0 retrieved=[]; issue: stored fact not retrieved (use_memory=True)
- **#4898** [R-sem] "my favorite spread is fried rice" — expected: retrieved (semantic); actual: results=0 retrieved=[]; issue: stored fact not retrieved (use_memory=True)
- **#4903** [R-sem] "my favorite side dish is ceviche" — expected: retrieved (semantic); actual: results=0 retrieved=[]; issue: stored fact not retrieved (use_memory=True)
- **#4904** [R-sem] "my favorite side dish is butter chicken" — expected: retrieved (semantic); actual: results=0 retrieved=[]; issue: stored fact not retrieved (use_memory=True)
- **#4905** [R-sem] "my favorite side dish is bruschetta" — expected: retrieved (semantic); actual: results=0 retrieved=[]; issue: stored fact not retrieved (use_memory=True)
- **#4911** [R-pro] "my name is sunny" — expected: retrieved (profile); actual: use_memory=True results=0; issue: profile query did not return stored fact
- **#4913** [R-pro] "my name is waffle" — expected: retrieved (profile); actual: use_memory=True results=0; issue: profile query did not return stored fact
- **#4915** [R-pro] "my name is coco" — expected: retrieved (profile); actual: use_memory=True results=0; issue: profile query did not return stored fact
- **#4916** [R-pro] "my name is buddy" — expected: retrieved (profile); actual: use_memory=True results=0; issue: profile query did not return stored fact
- **#4926** [R-pro] "my name is sadie" — expected: retrieved (profile); actual: use_memory=True results=0; issue: profile query did not return stored fact
- **#4930** [R-pro] "my name is pebbles" — expected: retrieved (profile); actual: use_memory=True results=0; issue: profile query did not return stored fact
- **#4931** [R-pro] "my name is biscuit" — expected: retrieved (profile); actual: use_memory=True results=0; issue: profile query did not return stored fact
- **#4932** [R-pro] "my name is charlie" — expected: retrieved (profile); actual: use_memory=True results=0; issue: profile query did not return stored fact
- **#4970** [R-hist] "my favorite seasoning is pho" — expected: retrieved (history); actual: use_memory=True hist=0; issue: history before-question returned no entry
- **#4971** [R-hist] "my favorite seasoning is curry" — expected: retrieved (history); actual: use_memory=True hist=0; issue: history before-question returned no entry
- **#4972** [R-hist] "my favorite seasoning is sandwich" — expected: retrieved (history); actual: use_memory=True hist=0; issue: history before-question returned no entry
- **#4974** [R-hist] "my favorite seasoning is poutine" — expected: retrieved (history); actual: use_memory=True hist=0; issue: history before-question returned no entry
- **#4976** [R-hist] "my favorite seasoning is korean bbq" — expected: retrieved (history); actual: use_memory=True hist=0; issue: history before-question returned no entry
- **#4977** [R-hist] "my favorite seasoning is pancakes" — expected: retrieved (history); actual: use_memory=True hist=0; issue: history before-question returned no entry
- **#4978** [R-hist] "my favorite seasoning is burrito" — expected: retrieved (history); actual: use_memory=True hist=0; issue: history before-question returned no entry
- **#4979** [R-hist] "my favorite seasoning is shepherd pie" — expected: retrieved (history); actual: use_memory=True hist=0; issue: history before-question returned no entry
- **#4980** [R-hist] "my favorite seasoning is noodles" — expected: retrieved (history); actual: use_memory=True hist=0; issue: history before-question returned no entry
- **#4983** [R-hist] "my favorite seasoning is idli" — expected: retrieved (history); actual: use_memory=True hist=0; issue: history before-question returned no entry
- **#4984** [R-hist] "my favorite seasoning is gyoza" — expected: retrieved (history); actual: use_memory=True hist=0; issue: history before-question returned no entry
- **#4985** [R-hist] "my favorite condiment is sushi" — expected: retrieved (history); actual: use_memory=True hist=0; issue: history before-question returned no entry
- **#4986** [R-hist] "my favorite condiment is gnocchi" — expected: retrieved (history); actual: use_memory=True hist=0; issue: history before-question returned no entry
- **#4987** [R-hist] "my favorite condiment is calamari" — expected: retrieved (history); actual: use_memory=True hist=0; issue: history before-question returned no entry
- **#4991** [R-hist] "my favorite condiment is noodles" — expected: retrieved (history); actual: use_memory=True hist=0; issue: history before-question returned no entry
- **#4992** [R-hist] "my favorite condiment is lasagna" — expected: retrieved (history); actual: use_memory=True hist=0; issue: history before-question returned no entry
- **#4995** [R-hist] "my favorite condiment is banh mi" — expected: retrieved (history); actual: use_memory=True hist=0; issue: history before-question returned no entry
- **#4997** [R-hist] "my favorite condiment is samosa" — expected: retrieved (history); actual: use_memory=True hist=0; issue: history before-question returned no entry
- **#4998** [R-hist] "my favorite condiment is tacos" — expected: retrieved (history); actual: use_memory=True hist=0; issue: history before-question returned no entry
