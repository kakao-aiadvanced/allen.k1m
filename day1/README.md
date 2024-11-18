# Few shot engineering

```
# 코드로 형식 지정됨
```

1. 영어를 한국어로 번역하는 5-shot prompt 를 작성하고 "dog"를 번역해보세요.

```
a: 안녕
b: Hello

a: 사과
b: Apple

a: 고양이
b: Cat

a: 책
b: Book

a: 사람
b: Human

a: ?
b: Dog

```

2. 영화 리뷰에 대한 sentiment (positive or negative) 를 결정하는 5-shot prompt 를 작성하고 "The storyline was dull and uninspiring." 에 대한
   결과를 확인해보세요.

```
리뷰: "The movie was fantastic! I loved every moment of it."
감정: Positive

리뷰: "The acting was terrible, and the plot made no sense."
감정: Negative

리뷰: "An absolutely amazing experience with stunning visuals and a heartfelt story."
감정: Positive

리뷰: "The pacing was too slow, and the characters were poorly developed."
감정: Negative

리뷰: "A masterpiece of storytelling that kept me engaged from start to finish."
감정: Positive

리뷰: The storyline was dull and uninspiring.
감정: Negative

```

3. 자연어를 SQL 쿼리로 바꿔주는 few-shot prompt 를 작성해보세요.

아래 1~5 의 "write your prompt" 영역에 오른쪽 SQL 쿼리에 해당하는 자연어 문장을 작성해보세요.

```
Convert the following natural language requests into SQL queries:
1. "employees 테이블에서 salary가 50000 초과인 경우를 조회하는 쿼리 만들어줘": SELECT * FROM employees WHERE salary > 50000;
2. "products 테이블에서 stocks가 0인 경우를 조회하는 쿼리 만들어줘": SELECT * FROM products WHERE stock = 0;
3. "Write your Prompt": SELECT name FROM students WHERE math_score > 90;
4. "Write your Prompt": SELECT * FROM orders WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY);
5. "Write your Prompt": SELECT city, COUNT(*) FROM customers GROUP BY city;

Request: "Find the average salary of employees in the marketing department."
SQL Query:

```

# Chain of Thought

다음 문제를 푸는 Chain of thought prompt 를 작성해보세요.

```
# Simple - 1
Solve the following problem step-by-step: 23 + 47

Step-by-step solution:
1. Write your Prompt
2. Write your Prompt
3. Write your Prompt
4. Write your Prompt

Answer: 70

```

```
# Simple - 2
Solve the following problem step-by-step: 123 - 58

Step-by-step solution:
1. Write your Prompt
2. Write your Prompt
3. Write your Prompt
4. Write your Prompt

Answer: 65
```

위에서 작성한 Simple - 1, Simple - 2 를 few shot 으로 활용하고 아래 문제를 질문으로 하는 프롬프트를 작성하고 결과를 확인해보세요.

```
# Simple 결과 확인
Solve the following problem step-by-step: 345 + 678 - 123

Step-by-step solution:
1. Check the response
2. Check the response
3. Check the response

Answer: 900

```

아래 문제 (Intermediate-1, Intermediate-2) 를 푸는 과정을 담은 CoT 예시를 작성해보세요.

```
# Intermediate - 1
Solve the following logic puzzle step-by-step:
Three friends, Alice, Bob, and Carol, have different favorite colors: red, blue, and green. We know that:
1. Alice does not like red.
2. Bob does not like blue.
3. Carol likes green.

Determine the favorite color of each friend.

Step-by-step solution:
Write your Prompt

Answer:
- Alice: blue
- Bob: red
- Carol: green
```

```
# Intermediate - 2
Solve the following logic puzzle step-by-step:
Four people (A, B, C, D) are sitting in a row. We know that:
1. A is not next to B.
2. B is next to C.
3. C is not next to D.

Determine the possible seating arrangements.

Step-by-step solution:
Write your Prompt

Answer:
- Possible arrangements: BCAD, CABD
```

작성한 prompt 와 original prompt 를 GPT 설정을 바꿔가며 응답(Temperature, Maximum Tokens, Stop sequences, Top P, Frequency Penalty,
Presence Penalty)을 확인해보세요

https://platform.openai.com/playground/chat?models=gpt-4o
