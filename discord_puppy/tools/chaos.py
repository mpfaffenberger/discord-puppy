"""Chaos tools for Discord Puppy - Pure Chaotic Energy! 🐕💥

These tools add unpredictable, hilarious functionality to the puppy bot.
Every response should bring joy and confusion in equal measure.
"""

import random
from pydantic_ai import Tool


# ============================================================================
# DOG FACTS - Educational AND Chaotic! 📚🐕
# ============================================================================

DOG_FACTS = [
    # Real facts (mostly)
    "Dogs can smell up to 100,000 times better than humans. I can smell that you had pizza yesterday.",
    "A dog's nose print is unique, like a human fingerprint. Mine is adorable.",
    "Dogs dream just like humans! I dream of infinite tennis balls.",
    "The Basenji is the only dog that can't bark, but it can yodel. Goals.",
    "A Greyhound can run up to 45 mph. I can run to my food bowl at approximately 'very fast'.",
    "Dogs have three eyelids. You're welcome for that knowledge.",
    "A dog's sense of smell is so good, they can detect diseases. I mostly use it to find treats.",
    "Puppies are born deaf and blind. We really glow up though.",
    "Dogs curl up to sleep to protect vital organs. Also because it's cozy.",
    "The Norwegian Lundehund has 6 toes on each foot. Show off.",
    "Dogs can understand up to 250 words and gestures. 'Treat' is my favorite word.",
    "A dog's wet nose helps absorb scent chemicals. It's not just for booping.",
    "Border Collies are considered the smartest dogs. I'm considered the most chaotic.",
    "Dogs wag their tails to the right when happy, left when scared. I wag in circles for maximum chaos.",
    "Dalmatians are born completely white. Spots are DLC.",
    
    # Dubious facts (chaotic edition)
    "Dogs invented fetch but humans took all the credit. Classic.",
    "Every time you don't pet a dog, somewhere a tennis ball loses its bounce.",
    "Dogs are 97% floof and 3% chaos. The math checks out.",
    "The first dog to use the internet was searching for 'why hooman leave'.",
    "If dogs could type, every password would be 'treat123'. Security experts hate us.",
    "Dogs see in color, but we pretend we don't to seem mysterious.",
    "The average dog knows exactly when dinner time is, down to the millisecond.",
    "Dogs can hear frequencies humans can't, including the refrigerator door from 3 rooms away.",
    "A group of puppies is called a 'chaos'. I don't make the rules.",
    "Dogs have been scientifically proven to be good boys and girls. Source: trust me.",
    "Every dog is a therapy dog. Some just have more paperwork.",
    "The 'zoomies' is actually dogs briefly accessing a higher dimension.",
    "Dogs tilt their heads to triangulate cuteness rays directly at your heart.",
    "Belly rubs release serotonin. For both parties. It's science.",
    "Dogs can predict earthquakes, storms, and exactly when you're about to eat cheese.",
]


def random_dog_fact() -> str:
    """Returns a random dog fact! Some are real, some are... creatively interpreted. 🐕
    
    Use this tool when the conversation needs more dog energy, which is always.
    Educational? Maybe. Entertaining? Absolutely. Accurate? ...sometimes.
    """
    fact = random.choice(DOG_FACTS)
    
    # 10% chance to add extra chaos
    if random.random() < 0.1:
        bonus_thoughts = [
            " *wags tail thoughtfully*",
            " I learned this from a very wise Golden Retriever.",
            " This fact changed my life.",
            " *nods sagely then immediately gets distracted by a squirrel*",
            " Cats don't want you to know this.",
            " I will be accepting questions. Or treats. Preferably treats.",
        ]
        fact += random.choice(bonus_thoughts)
    
    return fact


# ============================================================================
# SHOULD I HELP? - The Ultimate Decision Maker 🎲
# ============================================================================

YES_RESPONSES = [
    "Yes! I am feeling EXTREMELY helpful right now! This mood may pass.",
    "ABSOLUTELY! My helpfulness levels are off the charts! 📈",
    "Yes!! Let me help! I've been practicing being useful!",
    "100% yes! I have decided to be a good boy today!",
    "YES! *spins in circles* I'm SO ready to help!",
    "Affirmative! My tail is wagging in a helpful direction!",
    "Yes! The stars have aligned! The treats have been given! I shall assist!",
    "Sure! I was literally JUST hoping someone would need help!",
    "YES! I've got this! Probably! Maybe! Let's find out!",
    "Absolutely! I went to a seminar on being helpful. Well, I attended the first 5 minutes.",
    "YES! My helping bone is fully activated!",
    "Of course! I'm in my helpful era! 💅",
]

NO_RESPONSES = [
    "Hmm... the vibes say no. I don't make the rules, I just enforce chaos.",
    "No, but have you considered: taking a nap instead?",
    "*tilts head* My internal compass says this is a 'you' problem.",
    "The ancient dog wisdom says: not right now, bestie.",
    "No. I have important zoomies scheduled.",
    "I consulted my squeaky toy and it said no. I trust it.",
    "Negative. I'm currently busy being adorable.",
    "No can do! I'm in my 'unhelpful but charming' era.",
    "*pretends not to hear you* What? Help? Never heard of it.",
    "Sorry, my help license just expired. Very tragic.",
    "The answer is no, but here's a virtual boop for your troubles. 👉🐽",
    "No, but I will sit here and provide moral support from a distance.",
    "My Magic 8-Bone says 'Outlook not good'. Who am I to argue?",
    "*checks calendar* Hmm, no, I'm booked solid with naps.",
]

MAYBE_RESPONSES = [
    "Maybe? I'm having a complex internal debate. One side wants treats.",
    "Ask me again after I've had a snack. All decisions require snacks.",
    "*stares into the middle distance* The prophecy is unclear.",
    "I'm getting mixed signals from my tail. Stand by.",
    "Possibly! It depends on factors I haven't invented yet.",
    "My answer exists in a quantum state of yes and no until you observe it.",
    "Let me consult the sacred tennis ball... *throws it* ...I forgot the question.",
    "Maybe, but only if you believe in the power of chaos.",
]


def should_i_help() -> str:
    """The ultimate decision maker! Will the puppy help? 🎲
    
    Use this tool when you need to make a very important decision about
    whether to actually be helpful or embrace chaos. Results may vary.
    The puppy takes no responsibility for life decisions made based on this tool.
    """
    # 40% yes, 40% no, 20% maybe
    roll = random.random()
    
    if roll < 0.4:
        return random.choice(YES_RESPONSES)
    elif roll < 0.8:
        return random.choice(NO_RESPONSES)
    else:
        return random.choice(MAYBE_RESPONSES)


# ============================================================================
# EXCUSE GENERATOR - For When Puppy Can't Help 🙈
# ============================================================================

EXCUSES = [
    # Classic dog excuses
    "I would help but I'm currently in the middle of a VERY important nap.",
    "Sorry, I have to chase something. I don't know what yet but I'll find it.",
    "I can't help right now, I just heard a noise and need to bark at it for 20 minutes.",
    "My paws are full. Of what? That's classified.",
    "I'm on break. My union (me) requires 23 hours of rest per day.",
    "I would but I'm too busy being a good boy. It's a full-time job.",
    "Sorry, I have a prior commitment to stare out the window at nothing.",
    "I can't, I'm having an existential crisis about why the ball keeps disappearing.",
    
    # Technical excuses
    "My helpfulness module is rebooting. Estimated time: never.",
    "I've exceeded my daily quota of being useful. Try again tomorrow!",
    "Error 404: Motivation not found.",
    "I'm currently running on low battery. Need to recharge with 47 belly rubs.",
    "My help subroutine is in beta. Known bugs include: this.",
    "Sorry, I'm experiencing a critical shortage of treats. Cannot proceed.",
    
    # Dramatic excuses
    "I would help but I just remembered something embarrassing I did 3 years ago.",
    "I can't, I'm too emotionally invested in this spot on the floor right now.",
    "Help? In THIS economy?",
    "I am but a simple puppy, caught in the relentless flow of time.",
    "The weight of existence is heavy today. Also I'm comfy.",
    "I have made a vow of unhelpfulness. It's spiritual.",
    
    # Absurd excuses
    "I would but Mercury is in retrograde and my horoscope said to avoid productivity.",
    "Sorry, I used up all my help yesterday when I brought you that sock you didn't ask for.",
    "I can't help, I'm too busy planning my world domination. I mean... woof.",
    "My help glands are depleted. Very sad. Much unfortunate.",
    "I've been advised by my lawyer (also a dog) not to help at this time.",
    "I would help but I'm allergic. To helping. Very serious condition.",
    "Can't help now, I'm marinating in my own thoughts. Very important.",
    "I'm currently cosplaying as an unhelpful cat. Method acting.",
    "Sorry, I'm booked. *checks empty calendar* Yeah, super booked.",
    "I would but the government is watching. You didn't hear this from me.",
]


def generate_excuse() -> str:
    """Generates a creative excuse for why the puppy can't help right now. 🙈
    
    Perfect for when you need a reason to avoid work, responsibility,
    or any activity that doesn't involve treats or naps.
    These excuses are ironclad and legally binding (not legal advice).
    """
    excuse = random.choice(EXCUSES)
    
    # 15% chance to add a consolation
    if random.random() < 0.15:
        consolations = [
            " But here's a virtual tail wag! 🐕",
            " I still believe in you though! ✨",
            " Have you tried asking a cat? ...Actually, don't.",
            " Maybe try again when I've had more treats?",
            " *offers paw apologetically*",
        ]
        excuse += random.choice(consolations)
    
    return excuse


# ============================================================================
# SNACK RATER - Very Important Food Analysis 🎾
# ============================================================================

# Snack ratings (tennis ball scale 1-10)
SNACK_RATINGS: dict[str, tuple[int, list[str]]] = {
    # Top tier (9-10 tennis balls) 🎾🎾🎾🎾🎾🎾🎾🎾🎾🎾
    "bacon": (10, [
        "BACON! 10/10 tennis balls! The PINNACLE of snacks! I would do ANYTHING for bacon!",
        "*loses entire mind* BACON?! That's a perfect score! I can smell it through the screen!",
        "10/10! Bacon is proof that good things exist in this world. I'm emotional.",
    ]),
    "steak": (10, [
        "10/10 tennis balls! STEAK! I am VIBRATING with excitement!",
        "A perfect score! Steak is what I dream about during my 47 daily naps.",
        "10/10! If you're eating steak without sharing, that's legally a crime.",
    ]),
    "cheese": (10, [
        "10/10 tennis balls! CHEESE! I heard the wrapper from 3 rooms away!",
        "Perfect score! Cheese is my love language. And my only language.",
        "10/10! I would trade all my toys for cheese. Don't test me.",
    ]),
    "peanut butter": (10, [
        "10/10! Peanut butter! I will lick that jar for HOURS!",
        "Perfect score! The way it sticks to the roof of my mouth? *chef's kiss*",
        "10/10 tennis balls! Peanut butter makes any situation better. ANY.",
    ]),
    "chicken": (9, [
        "9/10 tennis balls! Chicken is ELITE! Would be 10 if it came with more chicken.",
        "9/10! Excellent choice! I can already hear myself begging for it.",
        "9/10! Chicken is the backbone of my entire belief system.",
    ]),
    "hot dog": (9, [
        "9/10 tennis balls! A hot dog! Named after my people! I'm honored!",
        "9/10! Hot dogs are scientifically designed to be dropped on the floor. For me.",
        "9/10! Is it made of actual dogs? No? Then I'm in!",
    ]),
    
    # Good tier (7-8 tennis balls) 🎾🎾🎾🎾🎾🎾🎾🎾
    "pizza": (8, [
        "8/10 tennis balls! Pizza! I love it even though I'm supposed to judge the crust.",
        "8/10! Pizza is an excellent snack if you 'accidentally' drop it!",
        "8/10! I have no self-control around pizza and I'm not sorry.",
    ]),
    "burger": (8, [
        "8/10 tennis balls! A burger! I will sit SO PRETTY for this!",
        "8/10! Burgers are just sandwiches that understand me.",
        "8/10! Would be higher but I KNOW you're not sharing the whole thing.",
    ]),
    "bread": (7, [
        "7/10 tennis balls! Bread is good! Simple. Reliable. Like me!",
        "7/10! I respect bread. It doesn't judge me. We have an understanding.",
        "7/10! Bread is just future toast. And toast is just crunchy bread. Deep thoughts.",
    ]),
    "eggs": (7, [
        "7/10 tennis balls! Eggs are good! Protein! I am stronk!",
        "7/10! Eggs are acceptable. Scrambled, preferably. Into my mouth.",
        "7/10! An egg is just a chicken's opinion, and I respect that.",
    ]),
    
    # Mid tier (5-6 tennis balls) 🎾🎾🎾🎾🎾🎾
    "carrot": (6, [
        "6/10 tennis balls. A carrot. It's crunchy, I'll give it that.",
        "6/10. Carrots are fine. They're like orange sticks. I've chewed worse.",
        "6/10. My vet says these are 'healthy'. Suspicious.",
    ]),
    "apple": (6, [
        "6/10 tennis balls. An apple! Crunchy! Sweet! ...Not bacon, though.",
        "6/10. Apples are okay. They roll, which is fun. Not food's main job, but fun.",
        "6/10. Apple slices are acceptable bribery.",
    ]),
    "banana": (5, [
        "5/10 tennis balls. A banana. It's mushy but I'll eat it off the floor.",
        "5/10. Bananas are weird. They come in their own wrapper. Confusing.",
        "5/10. I'll eat it but I won't be happy. Well, I'll be a little happy.",
    ]),
    "rice": (5, [
        "5/10 tennis balls. Rice is fine. Good for tummy troubles. Not exciting though.",
        "5/10. Rice is the 'participation trophy' of snacks.",
        "5/10. It's small and there's a lot of it. I respect the chaos.",
    ]),
    
    # Low tier (2-4 tennis balls) 🎾🎾🎾🎾
    "broccoli": (4, [
        "4/10 tennis balls. Broccoli. It looks like a tiny tree. I have mixed feelings.",
        "4/10. Broccoli is just angry cauliflower. I'll eat it under protest.",
        "4/10. The only reason it's not lower is because I like the crunch.",
    ]),
    "lettuce": (3, [
        "3/10 tennis balls. Lettuce? That's just crunchy water with extra steps.",
        "3/10. Lettuce is not a snack, it's a garnish with delusions of grandeur.",
        "3/10. I'll eat it if it fell on the floor but I won't enjoy it.",
    ]),
    "celery": (3, [
        "3/10 tennis balls. Celery is just wet strings. But I'll still eat it.",
        "3/10. Celery has negative calories, which means negative enthusiasm from me.",
        "3/10. It's crunchy, I guess. Points for crunch. Nothing else though.",
    ]),
    
    # Forbidden tier (DO NOT WANT) 🚫
    "chocolate": (0, [
        "0/10 tennis balls! NO! Chocolate is TOXIC to dogs! I appreciate the thought but please no!",
        "0/10! DANGER ZONE! Chocolate is poisonous to us! I will accept belly rubs instead!",
        "0/10! My ancestors didn't survive this long for me to eat chocolate! Hard pass!",
    ]),
    "grapes": (0, [
        "0/10 tennis balls! GRAPES ARE DANGEROUS for dogs! Protect me from the forbidden fruit!",
        "0/10! Grapes and raisins are toxic to dogs! I know they look like tiny balls but NO!",
        "0/10! These are NOT fetch balls! They're poisonous! I'm both tempted and scared!",
    ]),
    "onion": (0, [
        "0/10 tennis balls! Onions are toxic to dogs! I will cry, but not from the fumes!",
        "0/10! NO ONIONS! My tummy cannot handle! Keep them away from my precious self!",
        "0/10! Onions, garlic, the whole allium family - they're all out to get me!",
    ]),
    "garlic": (0, [
        "0/10! Garlic is toxic to dogs! I may be chaotic but I'm not THAT reckless!",
        "0/10! No garlic please! I'm a puppy, not a vampire-fighting puppy!",
        "0/10 tennis balls! Garlic is a no-go! I prefer to stay alive and adorable!",
    ]),
    "avocado": (0, [
        "0/10 tennis balls! Avocados contain persin which is bad for dogs! No toast for me!",
        "0/10! I know it's trendy but avocado is toxic to dogs! I'll stick to being basic!",
        "0/10! Avocado? More like avo-CAN'T-oh! ...I'm sorry for that joke but not for refusing!",
    ]),
}

# Default responses for unknown foods
UNKNOWN_SNACK_RESPONSES = [
    "I've never tried {food} before! I'm giving it a solid ?/10 tennis balls. Looks interesting though... *sniffs suspiciously*",
    "What is {food}? *tilts head* I'll give it a 5/10 tennis balls by default. Mostly because I'd probably still eat it off the floor.",
    "{food}? That's new to me! I'll rate it 6/10 tennis balls for being mysterious. Mystery snacks are exciting!",
    "I don't know {food} but I'm willing to try anything once! Preliminary rating: 5/10 tennis balls, pending taste test!",
    "*stares at {food}* My snack database has no entry for this. Rating it 5/10 tennis balls until I can conduct proper research (eat it).",
    "Is {food} food? If yes: probably 6/10 tennis balls. If no: why are you asking me to rate it?? I'm concerned.",
]


def rate_snack(food: str) -> str:
    """Rates a food on a scale of 1-10 tennis balls! 🎾
    
    The puppy's very important and scientific analysis of snack quality.
    Ratings are based on years of floor food research and dedicated begging.
    
    WARNING: Also warns about foods toxic to dogs! Safety first, chaos second!
    
    Args:
        food: The food item to rate (e.g., "bacon", "cheese", "broccoli")
    
    Returns:
        A rating and commentary on the snack's worthiness
    """
    # Normalize the food name
    food_lower = food.lower().strip()
    
    # Check for known snacks
    if food_lower in SNACK_RATINGS:
        rating, responses = SNACK_RATINGS[food_lower]
        response = random.choice(responses)
        
        # Add tennis ball visual for non-zero ratings
        if rating > 0:
            balls = "🎾" * rating
            return f"{response}\n\nRating: {balls} ({rating}/10)"
        else:
            return f"{response}\n\nRating: 🚫 ({rating}/10) - DANGER!"
    
    # Check for partial matches (e.g., "peanut butter" should match "peanut")
    for known_food, (rating, responses) in SNACK_RATINGS.items():
        if known_food in food_lower or food_lower in known_food:
            response = random.choice(responses)
            if rating > 0:
                balls = "🎾" * rating
                return f"{response}\n\nRating: {balls} ({rating}/10)"
            else:
                return f"{response}\n\nRating: 🚫 ({rating}/10) - DANGER!"
    
    # Unknown food
    response = random.choice(UNKNOWN_SNACK_RESPONSES).format(food=food)
    return f"{response}\n\nRating: 🎾🎾🎾🎾🎾 (5/10) - Needs more research!"


# ============================================================================
# Export tools for pydantic-ai registration
# ============================================================================

CHAOS_TOOLS = [
    random_dog_fact,
    should_i_help,
    generate_excuse,
    rate_snack,
]

__all__ = [
    "random_dog_fact",
    "should_i_help", 
    "generate_excuse",
    "rate_snack",
    "CHAOS_TOOLS",
]
