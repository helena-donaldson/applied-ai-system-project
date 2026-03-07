# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

1. "Go Higher" and "Go Lower" would be hinted nonsensically. For example, I would be at the lower limit (1), but it would tell me to go lower.

2. Starting a new game would cause
a "Game over. Start a new game to try again" message to appear even though I did start a new game.

3. Even though I changed the difficulty mode, which changes the range of numbers to be guessed, the display value in the middle didn't change its range (not showing 1 to 20 when I changed it to easy).

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

I used Copilot.

Correct suggestion: The AI suggested to correct an instance of hard-coding where the guessing range was hard-coded as 1-100 instead of being based on the difficulty level. I went to the line it mentioned in order to verify that this issue did exist, and it did. I changed it based on the AI's recommendation to rely on the difficulty level range instead. Then, I checked the range display in the game, and it changed after that.

Incorrect suggestion: The AI suggested that I set the
difficulty level of Hard to 1 to 200 instead of 1 to 100 and switching Normal back to 1 to 50. I verified that this suggestion was wrong when I checked what the range dropdown listed that the correct score ranges should be. It simply inferred that Hard should be 1 to 200 instead of checking to see that the dropdown referenced it as 1 to 100.

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I verified that the bugs were really fixed by adding to the test suite tests for each of the bugs I fixed as well as manually testing the game to ensure the the score ranges were fixed as well as the guessing logic was fixed.

I created tests using pytest for the get range for difficulty function, ensuring that it returned the correct range for all three of the modes. This ensured that I knew the issue of the mixed up ranges that originally was present ended up getting fixed.

AI helped me understand the tests because I didn't know originally how to use pytests, so it helped me use the correct command to run them.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit reruns causes the script to be run again when users interact with the UI. Session state helps solve this by storing values between the reruns, allowing for important variables like attempts made to persist and increment properly whenever the user pressed the button to make a guess.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

I want to reuse the habit of creating tests when working on features to ensure that I am developing accurately- as in practicing better test driven development.

I would act differently by relying on AI to generate test suites as well as being cautious when AI might be guessing or hallucinating certain advice/

This project changed the way I think about AI generated code because it showed me that using careful documentation and test driven development can ensure that AI generated code isn't slop.
