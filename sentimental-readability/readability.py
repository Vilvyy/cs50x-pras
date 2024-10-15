import cs50


def main():
    text = ""
    if len(text) == 0:
        text = cs50.get_string("Text: ")
    # test
    avgLetter = avgLetters(text)
    avgSent = avgSents(text)
    grade = countIndex(avgLetter, avgSent)

    if grade < 1:
        print("Before Grade 1")
    elif grade > 16:
        print("Grade 16+")
    else:
        print(f"Grade {grade}")


def avgLetters(sentence):
    # get text length
    textLength = len(sentence)
    realTextLength = 0
    totalNumWords = len(sentence.split())

    for c in sentence:
        # count the number of letters excluding whitespaces
        if c.isalpha() == True:
            realTextLength += 1
    avgLetters = (realTextLength / totalNumWords) * 100
    return avgLetters


def avgSents(sentence):
    textLength = len(sentence)
    totalSentence = 0
    totalNumWords = len(sentence.split())

    for c in sentence:
        # Check for "!, ?, ."
        if c in ['!', '?', '.']:
            totalSentence += 1
    avgSentence = (totalSentence / totalNumWords) * 100
    return avgSentence


def countIndex(averageLetters, averageSentences):
    index = 0.0588 * averageLetters - 0.296 * averageSentences - 15.8
    grade = round(index)
    if index < 1:
        return 0
    else:
        return grade


main()
