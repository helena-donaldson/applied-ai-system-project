import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def calculate_certainty(guess, secret, low, high):
    """
    Returns a float between 0 and 1 representing how 'confident' 
    the AI is that the player is getting warm.
    """
    total_range = high - low
    distance = abs(secret - guess)
    
    # Simple inverse relationship: closer guess = higher certainty
    # We use a power function (0.5) to make it feel more 'dynamic'
    certainty = max(0, 1 - (distance / total_range)) ** 0.5
    return certainty

def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100

def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None

def load_knowledge_base():
    try:
        with open("knowledge.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Binary Search: Use the midpoint of the current known bounds."

def validate_response(ai_text, guess, secret):
    ai_text = ai_text.lower()
    # Truth check
    if guess > secret:
        return "high" in ai_text or "lower" in ai_text or "down" in ai_text
    elif guess < secret:
        return "low" in ai_text or "higher" in ai_text or "up" in ai_text
    return "correct" in ai_text or "won" in ai_text

def get_ai_feedback(guess, secret, low, high, history, persona):
    """
    Refactored AI Method: 
    Includes RAG, History-based Windowing, and Strategic Validation.
    """
    model = genai.GenerativeModel('gemini-2.5-flash')
    knowledge_context = load_knowledge_base()
    
    # 1. Calculate the actual effective search window from history
    # We include the current guess to narrow the bounds for the tip
    full_history = [g for g in history if isinstance(g, int)]
    if guess not in full_history:
        full_history.append(guess)
        
    lower_guesses = [g for g in full_history if g < secret]
    upper_guesses = [g for g in full_history if g > secret]
    
    current_low = max(lower_guesses) + 1 if lower_guesses else low
    current_high = min(upper_guesses) - 1 if upper_guesses else high
    
    # Calculate the strategic midpoint for the next suggestion
    suggested_next = (current_low + current_high) // 2

    # 2. Validation Loop: Give Gemini up to 3 tries to get the facts right
    for attempt in range(3):
        prompt = f"""
        Role: {persona}
        Reference Material: {knowledge_context}
        
        Game State:
        - Secret Number: {secret}
        - User's Guess: {guess}
        - Current Effective Range: {current_low} to {current_high}
        - Full History: {full_history}
        
        Instructions:
        1. State if {guess} is higher or lower than {secret}.
        2. Evaluate Strategy: If {guess} narrowed the range effectively, praise the user.
        3. Provide the next strategic midpoint: {suggested_next}.
        
        Constraint: Keep it under 45 words and stay in character.
        """
        
        try:
            response = model.generate_content(prompt)
            raw_text = response.text
            
            # 3. Automated Validation Check
            if validate_response(raw_text, guess, secret):
                return raw_text
            
            print(f"Validation failed (Attempt {attempt+1}). Fact-check mismatch. Retrying...")
        except Exception as e:
            return f"The {persona} is currently unavailable. (Error: {e})"

    return "The assistant is having trouble with the math. Try guessing again!"

def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score