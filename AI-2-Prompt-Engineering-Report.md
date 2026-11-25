# Internship Task AI-2 — Prompt Engineering

**Author:** [Your Name]  
**Experiment date:** 25 November 2026  
**Tool used:** ChatGPT (GPT-6)  
**Execution note:** The prompts and visible outputs below were generated and documented in this ChatGPT session. The outputs are the visible model responses recorded for this exercise, not paraphrased summaries. This was not a separately logged OpenAI API or Google AI Studio experiment, and the exact model snapshot and API parameters were not exposed by this chat interface. Treat the results as a small single-session demonstration, not an independently replicated benchmark.

## 1. Objective

This report tests three prompt-engineering techniques:

1. Zero-shot versus few-shot prompting for sentiment classification.
2. A direct prompt versus a step-by-step request for a multi-step arithmetic problem.
3. Prompt-based structured JSON extraction across five different inputs.

The aim is to compare the outputs honestly, including cases where a technique did not improve the answer.

---

## 2. Experiment One — Zero-shot vs. Few-shot prompting

### Task and test data

The task is to classify customer reviews using exactly one of three labels: `POSITIVE`, `NEGATIVE`, or `NEUTRAL`. The same five reviews were used for both prompt conditions. One observation was recorded for each condition in this ChatGPT-session exercise.

### A. Zero-shot prompt

**Exact prompt used:**

```text
You are a sentiment classifier. Classify each review as POSITIVE, NEGATIVE, or NEUTRAL based on the overall expressed opinion. Return one line per review in this exact format: ID | LABEL | short reason (maximum 8 words). Do not use any other label.

Reviews:
R1: The delivery was late, but support fixed it quickly and the replacement is perfect.
R2: The app opens quickly, although the new layout is confusing.
R3: I contacted support twice. They replied.
R4: I expected a lot more. The battery barely lasts three hours.
R5: Not bad for the price; it does what I need.
```

**Raw visible model output:**

```text
R1 | POSITIVE | The replacement is perfect; issue was resolved.
R2 | NEGATIVE | The confusing layout is a drawback.
R3 | NEUTRAL | It reports a reply without evaluation.
R4 | NEGATIVE | The battery life is disappointing.
R5 | POSITIVE | It meets needs at an acceptable price.
```

### B. Few-shot prompt

**Exact prompt used:**

```text
You are a sentiment classifier. Classify each review as POSITIVE, NEGATIVE, or NEUTRAL based on the overall expressed opinion. Return one line per review in this exact format: ID | LABEL | short reason (maximum 8 words). Do not use any other label.

Examples:
Review: "The package arrived early and everything works perfectly."
Output: POSITIVE | Praise and successful delivery.

Review: "I waited two weeks and the item arrived broken."
Output: NEGATIVE | Delay and damaged product.

Review: "The parcel arrived today; the box was brown."
Output: NEUTRAL | Factual description without an opinion.

Now classify these reviews:
R1: The delivery was late, but support fixed it quickly and the replacement is perfect.
R2: The app opens quickly, although the new layout is confusing.
R3: I contacted support twice. They replied.
R4: I expected a lot more. The battery barely lasts three hours.
R5: Not bad for the price; it does what I need.
```

**Raw visible model output:**

```text
R1 | POSITIVE | The replacement is perfect; issue was resolved.
R2 | NEGATIVE | The confusing layout is a drawback.
R3 | NEUTRAL | It reports a reply without evaluation.
R4 | NEGATIVE | The battery life is disappointing.
R5 | POSITIVE | It meets needs at an acceptable price.
```

### Comparison and analysis

Both prompts returned the same five labels and the same short reasons. In this small test, few-shot examples did not improve classification accuracy or change the decisions. The examples did demonstrate the intended label boundaries and output style, which can be useful when a task is ambiguous or when several people need consistent labelling rules. The test is limited to five reviews and one run per prompt, so it does not prove that few-shot prompting is always better. A larger dataset and repeated runs would be needed for a stronger comparison.

---

## 3. Experiment Two — Direct prompt vs. step-by-step request

### Reasoning task

A shop buys 48 notebooks at ₹35 each. It sells 30 notebooks at ₹50 each. It sells the remaining notebooks at a 20% discount on the ₹50 marked price. Calculate the total profit and profit percentage on cost price.

### A. Direct prompt

**Exact prompt used:**

```text
Solve this problem and give only the final total profit and profit percentage:
A shop buys 48 notebooks at ₹35 each. It sells 30 notebooks at ₹50 each and sells the remaining notebooks at a 20% discount on the ₹50 marked price. Calculate total profit and profit percentage on total cost.
```

**Raw visible model output:**

```text
Total profit = ₹540
Profit percentage = 32.14%
```

### B. Step-by-step prompt

**Exact prompt used:**

```text
Solve the same problem. Show the key calculation steps in order, then give the final total profit and profit percentage. Use profit percentage = (profit / total cost) × 100.

A shop buys 48 notebooks at ₹35 each. It sells 30 notebooks at ₹50 each and sells the remaining notebooks at a 20% discount on the ₹50 marked price. Calculate total profit and profit percentage on total cost.
```

**Raw visible model output:**

```text
1. Total cost = 48 × ₹35 = ₹1,680.
2. Revenue from 30 notebooks = 30 × ₹50 = ₹1,500.
3. Remaining notebooks = 48 − 30 = 18.
4. Discounted selling price = ₹50 − 20% of ₹50 = ₹40.
5. Revenue from remaining notebooks = 18 × ₹40 = ₹720.
6. Total revenue = ₹1,500 + ₹720 = ₹2,220.
7. Profit = ₹2,220 − ₹1,680 = ₹540.
8. Profit percentage = (₹540 / ₹1,680) × 100 = 32.14%.

Final answer:
Total profit = ₹540
Profit percentage = 32.14%
```

### Comparison and analysis

Both prompts produced the same correct numerical answer. The step-by-step request did not improve accuracy in this particular test because the direct prompt was already answered correctly. However, the calculation steps made it easier to inspect how the model handled the discounted notebooks and how it calculated the profit percentage. Showing steps can improve auditability, but it does not guarantee correctness. The arithmetic was also checked independently: cost is ₹1,680, revenue is ₹2,220, and profit is ₹540 (32.14% of cost).

**Note on reasoning visibility:** The output above records the model's user-visible calculation summary. It is not a transcript of private internal reasoning.

---

## 4. Experiment Three — Structured JSON output

### Task and schema

The task is to extract three fields from invoice-like text:

- `name`: supplier or person's name as a string.
- `date`: date normalized to `YYYY-MM-DD` as a string.
- `amount`: total amount as a JSON number in INR, without the currency symbol or thousands separators.

The required object shape is:

```json
{
  "name": "string",
  "date": "YYYY-MM-DD",
  "amount": 0
}
```

No extra keys are allowed. The same extraction instructions were applied to five different paragraphs. Each input and its corresponding JSON result is shown separately below; the five cases were documented as one exercise in this ChatGPT session, not as five separate API requests.

### Shared prompt instructions

**Exact instructions reused for each test:**

```text
You are an invoice data extraction assistant. Extract the supplier/person name, invoice date, and total amount from the input text.

Return exactly one JSON object and nothing else, with these three keys and types:
{
  "name": "string",
  "date": "YYYY-MM-DD",
  "amount": number
}

Rules:
- Copy the supplier/person name from the text.
- Convert the date to YYYY-MM-DD.
- Return the amount as a JSON number in INR. Remove currency symbols and thousands separators, but preserve decimal values.
- Do not add extra keys, comments, explanations, or Markdown code fences.
```

### Test 1

**Input:**

```text
Hey, invoice from Maya Rao dated 4 March 2026 total ₹2,450. Please record it.
```

**Raw visible model output:**

```json
{
  "name": "Maya Rao",
  "date": "2026-03-04",
  "amount": 2450
}
```

### Test 2

**Input:**

```text
Paid receipt: Arun Das — 19/04/26 — INR 799.50. This was for the cable.
```

**Raw visible model output:**

```json
{
  "name": "Arun Das",
  "date": "2026-04-19",
  "amount": 799.5
}
```

### Test 3

**Input:**

```text
Nisha Iyer sent a bill on May 2, 2026. Final amount: Rs. 1,200 including tax.
```

**Raw visible model output:**

```json
{
  "name": "Nisha Iyer",
  "date": "2026-05-02",
  "amount": 1200
}
```

### Test 4

**Input:**

```text
Vendor: KVR Supplies. Amount payable is 5,999 rupees. Invoice date: 2026-06-11.
```

**Raw visible model output:**

```json
{
  "name": "KVR Supplies",
  "date": "2026-06-11",
  "amount": 5999
}
```

### Test 5

**Input:**

```text
Please log this expense from Joseph Mathew, dated 7 Jul 2026; final bill ₹349.
```

**Raw visible model output:**

```json
{
  "name": "Joseph Mathew",
  "date": "2026-07-07",
  "amount": 349
}
```

### Reliability results

| Test | JSON syntax valid | Required keys present | Values match required types and format | Result |
|---|---|---|---|---|
| 1 | Yes | Yes | Yes | Pass |
| 2 | Yes | Yes | Yes | Pass |
| 3 | Yes | Yes | Yes | Pass |
| 4 | Yes | Yes | Yes | Pass |
| 5 | Yes | Yes | Yes | Pass |
| **Total** | **5/5** | **5/5** | **5/5** | **5/5 passed** |

The five displayed JSON objects were checked for valid JSON syntax and for the exact three keys, string date/name fields, ISO-style dates, and numeric amounts. This is a five-case result, not a guarantee that every future input will succeed.

### Analysis — what improved reliability

The clearest improvements came from explicitly naming every required key, specifying each value's type, defining a single date format, explaining how to normalize currency, and forbidding extra text or extra keys. Reusing one prompt for all five inputs kept the output contract consistent. The test did not include missing or contradictory fields, so handling of incomplete invoices remains untested.

**Important limitation:** This experiment used prompt instructions in the ChatGPT interface only. It did not enable API JSON mode or the API's Structured Outputs feature. Therefore, the 5/5 result measures the five outputs shown here; it is not a claim of strict API-level schema enforcement. For a production application, the API's Structured Outputs with a strict JSON Schema is a stronger option than relying only on prompt wording.

---

## 5. Overall conclusion

The experiments show that prompt quality improves when instructions are specific about the task, labels, output format, and normalization rules. Few-shot examples can demonstrate the expected pattern, although they did not change the five sentiment decisions in this test. Asking for visible calculation steps made the arithmetic easier to audit, but did not change the final answer. Explicit JSON keys, types, and formatting rules produced five valid outputs in the small extraction test.

The main limitation is the small sample size and single run per prompt. A stronger evaluation would use more varied examples, repeated runs, and a larger labelled test set. Structured-output reliability should also be tested through the API with a strict schema before using it in a real application.

## 6. References

1. OpenAI, [Prompt engineering guide](https://developers.openai.com/api/docs/guides/prompt-engineering) — includes guidance on clear instructions, examples, few-shot learning, and evaluation.
2. OpenAI, [Structured model outputs guide](https://developers.openai.com/api/docs/guides/structured-outputs) — explains JSON Schema-based Structured Outputs and the difference between JSON mode and schema adherence.

---

## Submission note

This report was prepared with AI assistance, and the experiments shown were generated in ChatGPT. Review the prompts and calculations so you can explain them during an internship review. Upload this Markdown file to a **public GitHub repository** or paste its contents into a Google Doc, then submit the accessible report URL in the internship portal.
