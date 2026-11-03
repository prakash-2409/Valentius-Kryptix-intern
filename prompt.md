# AI-2: Prompt Engineering Task Report
**Model Used:** `llama-3.3-70b-versatile` (via Groq API)

## 1. Zero-Shot vs. Few-Shot Prompting
**Task:** Classifying user feedback sentiment and categorizing the technical issue for a custom gym management web application (GymOS).

### Zero-Shot Test
**Prompt:**
> Classify the sentiment (Positive, Negative, or Mixed) and identify the primary technical category of this user feedback. 
> Feedback: "The new QR geofenced check-in kiosk is incredibly fast, but the offline-sync endpoint completely failed when I lost cell service in the weight room."

**Raw Model Output:**
> Based on the feedback provided by the user, the overall sentiment is Mixed. The user expresses positive feelings about the speed of the QR geofenced check-in kiosk ("incredibly fast"), but has a negative experience regarding the offline functionality. The primary technical category for this issue would be "Network/Connectivity" or "Offline Synchronization Failure."

### Few-Shot Test
**Prompt:**
> Classify the sentiment (Positive, Negative, Mixed) and the primary technical category of the feedback. Use strict formatting.
>
> Feedback: "The member PWA won't load on my iPhone."
> Sentiment: Negative
> Category: PWA Compatibility
> 
> Feedback: "WhatsApp integration for class reminders is working perfectly!"
> Sentiment: Positive
> Category: Notification Services
> 
> Feedback: "The new QR geofenced check-in kiosk is incredibly fast, but the offline-sync endpoint completely failed when I lost cell service in the weight room."
> Sentiment: 

**Raw Model Output:**
> Mixed
> Category: Offline Synchronization

### Analysis
The Zero-Shot prompt successfully understood the intent but produced a chatty, conversational paragraph that would be impossible to parse programmatically in a backend Node.js API. By providing just two structured examples (Few-Shot), the model immediately adopted the exact formatting constraints without needing complex, verbose system instructions. The output consistency improved from conversational to strict key-value pairs.

---

## 2. Chain-of-Thought (CoT) Reasoning
**Task:** A logic and math word problem to test system-1 (heuristic) vs. system-2 (analytical) reasoning.

### Direct Prompt (Zero-Shot)
**Prompt:**
> A premium GymOS annual subscription and a physical NFC keycard cost $110 in total. The subscription costs $100 more than the keycard. How much does the keycard cost?

**Raw Model Output:**
> The physical NFC keycard costs $10.

### Chain-of-Thought Prompt
**Prompt:**
> A premium GymOS annual subscription and a physical NFC keycard cost $110 in total. The subscription costs $100 more than the keycard. How much does the keycard cost? 
> Think step-by-step to reach the final answer.

**Raw Model Output:**
> Let's break this down step-by-step:
> 1. Let the cost of the keycard be X.
> 2. The subscription costs $100 more than the keycard, so the cost of the subscription is X + $100.
> 3. Together, they cost $110. So, we can write the equation: X (keycard) + (X + $100) (subscription) = $110.
> 4. Combine the Xs: 2X + $100 = $110.
> 5. Subtract $100 from both sides: 2X = $10.
> 6. Divide by 2: X = $5.
> 
> The physical NFC keycard costs $5.

### Analysis
Without CoT, the model falls into a classic cognitive trap, immediately jumping to the