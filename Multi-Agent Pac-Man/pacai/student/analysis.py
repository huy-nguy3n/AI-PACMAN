"""
Analysis question.
Change these default values to obtain the specified policies through value iteration.
If any question is not possible, return just the constant NOT_POSSIBLE:
```
return NOT_POSSIBLE
```
"""

NOT_POSSIBLE = None

def question2():
    """
    [Enter a description of what you did here.]
    Change noise to 0.0 let the agent cross the bridge
    """

    answerDiscount = 0.9
    answerNoise = 0.0

    return answerDiscount, answerNoise

def question3a():
    """
    [Enter a description of what you did here.]
    Change noise to 0.1 and living reward to -5.0
    """

    answerDiscount = 0.9
    answerNoise = 0.1
    answerLivingReward = -5.0

    return answerDiscount, answerNoise, answerLivingReward

def question3b():
    """
    [Enter a description of what you did here.]
    Change discount to 0.5 and living reward to -1
    """

    answerDiscount = 0.5
    answerNoise = 0.2
    answerLivingReward = -1

    return answerDiscount, answerNoise, answerLivingReward

def question3c():
    """
    [Enter a description of what you did here.]
    CHange noise to 0.0
    """

    answerDiscount = 0.9
    answerNoise = 0.0
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3d():
    """
    [Enter a description of what you did here.]
    Did not change default answer
    """

    answerDiscount = 0.9
    answerNoise = 0.2
    answerLivingReward = 0.0

    return answerDiscount, answerNoise, answerLivingReward

def question3e():
    """
    [Enter a description of what you did here.]
    Change noise to 1.0 and living reward to -2
    """

    answerDiscount = 0.9
    answerNoise = 1.0
    answerLivingReward = -2

    return answerDiscount, answerNoise, answerLivingReward

def question6():
    """
    [Enter a description of what you did here.]
    'NOT POSSIBLE'
    """

    answerEpsilon = None
    answerLearningRate = None

    return 'NOT POSSIBLE'

if __name__ == '__main__':
    questions = [
        question2,
        question3a,
        question3b,
        question3c,
        question3d,
        question3e,
        question6,
    ]

    print('Answers to analysis questions:')
    for question in questions:
        response = question()
        print('    Question %-10s:\t%s' % (question.__name__, str(response)))
