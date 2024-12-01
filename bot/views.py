from django.shortcuts import render
from django.http import JsonResponse
import random
import logging
from rapidfuzz import process, fuzz
from bot.responses import RESPONSES

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fallback responses
FALLBACK_RESPONSES = [
    "Sorry, I didn't understand that. Can you try again?",
    "I'm not sure I follow. Can you elaborate?",
    "Could you clarify what you mean?",
    "I didn't quite catch that. Could you rephrase?",
    "Can you provide more details?",
    "I'm having trouble understanding. Could you explain it differently?",
    "That sounds interesting! Can you tell me more?",
    "I'm not familiar with that. Could you explain it to me?",
    "Let me make sure I understand correctly. Are you asking about...?",
    "Could you give me an example?",
    "I'm here to help, but I need a bit more information.",
    "I didn't understand your question. Could you ask it another way?",
    "Your question is a bit unclear. Can you simplify it?",
    "That's a bit beyond my understanding. Can you break it down for me?",
    "I'm not equipped to answer that right now. Can we discuss something else?",
    "Hmm, I'm not sure what you mean. Can you rephrase your question?"
    ]

# Response threshold configuration
RESPONSE_THRESHOLD = 75  # Adjust for sensitivity

def get_bot_response(user_input):
    """Get response from the bot by searching for the best match."""
    user_input = user_input.lower()
    possible_questions = list(RESPONSES.keys())

    # Find all matches with scores
    matches = process.extract(user_input, possible_questions, scorer=fuzz.partial_ratio, limit=len(possible_questions))
    matches = sorted(matches, key=lambda x: x[1], reverse=True)  # Sort by score (descending)

    # Iterate through matches to find the best acceptable response
    for match, score, _ in matches:
        if score >= RESPONSE_THRESHOLD:  # Check if the score is above the threshold
            logger.info(f"Matched '{user_input}' with '{match}' (Score: {score})")
            # Get responses for the match
            responses = RESPONSES.get(match, [])
            if responses:
                # Return a random response from the matches
                return random.choice(responses)

    # Fallback if no matches meet the threshold
    logger.info(f"No adequate match found for '{user_input}'")
    return random.choice(FALLBACK_RESPONSES)
    
def chat(request):
    """Chat endpoint for the AI bot."""
    context = {
        'page_title': 'IIH College Portal - AI',
    }

    if request.method == "POST":
        user_input = request.POST.get("message", "").strip()
        if user_input:
            # Generate a response
            bot_response = get_bot_response(user_input)
            return JsonResponse({"bot_response": bot_response})
        else:
            return JsonResponse({"bot_response": "Please provide a message."}, status=400)

    return render(request, "chat.html", context)
