def my_pig(phrase):
    
    def find_vowel(word):
        for index, i in enumerate(word):
            if i in "aeiouAEIOU":
                return index
        return 0

    org_array = phrase.split(" ")
    pig_array = []
    for word in org_array:
        temp_word = word[find_vowel(word):] + word[0:find_vowel(word)]
        if find_vowel(word) == 0:
            temp_word += "way"
        else:
            temp_word += "ay"
        for i in ".,!?:;":
            if i in temp_word:
                temp_word = temp_word.replace(",", "")
                temp_word += i
        pig_array.append(temp_word)

    return " ".join(pig_array)