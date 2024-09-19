#SRS - logic
from datetime import datetime, timezone, timedelta
from app import db

def update_srs_binary(card, correct):
    """
    Update the card's SRS data based on whether the answer was correct or incorrect (binary).
    :param card: Card object to update
    :param correct: Boolean value, True if correct, False if incorrect.
    
    """
    
    if not correct:
        #if the answer was incorrect, reset the interval
        card.repetitions = 0
        card.interval = 1
        
    else:
        #if the answer was correct, increase the repetitions
        card.repetitions += 1
        
        if card.repetitions == 1:
            card.interval = 1
        elif card.repetitions == 2:
            card.interval = 6
        else:
            #Apply the standard spaced repetitions formula
            card.interval = round(card.interval * card.ease_factor)
            
        #Adjust ease factor slightly
        card.ease_factor += 0.1 if correct else -0.2
        card.ease_factor = max(card.ease_factor, 1.3) #Minimum ease_factor 1.3
    
    #Set the next review date based on the interval
    card.next_review = datetime.now(timezone.utc) + timedelta(days=card.interval)
    
    #Set the last review date and increment the review count
    card.last_reviewed = datetime.now(timezone.utc)
    card.review_count += 1
    
    db.session.commit()
    
    
    