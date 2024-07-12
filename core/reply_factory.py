
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST
def generate_bot_responses(message, session):
    bot_responses = []
    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)
    success, error = record_current_answer(message, current_question_id, session)
    if not success:
        return [error]
    next_question, next_question_id = get_next_question(current_question_id)
    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)
    session["current_question_id"] = next_question_id
    session.save()
    return bot_responses
def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if not answer:
        return False, "Answer cannot be empty."
    session_key = f"question_{current_question_id}_answer"
    session[session_key] = answer
    session.modified = True

    return True, ""



def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
     PYTHON_QUESTION_LIST = [
        "What is the capital of France?",
        "Who wrote 'Romeo and Juliet'?",
        "What is the square root of 64?",

    ]

    if 0 <= current_question_id < len(PYTHON_QUESTION_LIST):
        next_question_id = current_question_id + 1
        return PYTHON_QUESTION_LIST[current_question_id], next_question_id
    else:
        return "dummy question", -1

    return "dummy question", -1



def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''

     question_1_answer = session.get("question_1_answer", "").lower()
    question_2_answer = session.get("question_2_answer", "").lower()

    correct_answers = {
        1: "paris",
        2: "shakespeare",

    }

    total_questions = len(correct_answers)
    correct_count = sum(1 for q_id, correct_ans in correct_answers.items() if question_1_answer == correct_ans)


    score_percentage = (correct_count / total_questions) * 100
    result_message = f"Your score: {correct_count}/{total_questions} ({score_percentage:.2f}%)."
    return "dummy result"
