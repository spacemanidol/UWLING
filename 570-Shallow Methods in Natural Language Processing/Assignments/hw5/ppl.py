import os
import math
import sys
def load_sentences(training_data_filename):
    sentences = []
    with open(training_data_filename,'r') as f:
        for l in f:
            sentences.append('<s> ' + l.strip() + ' </s>')
    return sentences

def load_lm(lm_filename):
    unigram, bigram, trigram = {}, {}, {}
    is1,is2,is3 = 0,0,0
    with open(lm_filename,'r') as f:
        for l in f:
            l = l.strip()
            l1 = l.split(' ')
            if  '1-grams:' in l:
                is1 = 1
            elif  '2-grams:' in l:
                is2 = 1
                is1 = 0
            elif  '3-grams:' in l:
                is3 = 1
                is2 = 0
            elif is1 == 1 and len(l1) > 1:
                gram = l1[3]
                prob = float(l1[1])
                unigram[gram] = prob
            elif is2 == 1 and len(l1) > 1:
                gram = l1[3] + ' ' + l1[4]
                prob = float(l1[1])
                bigram[gram] = prob
            elif is3 == 1 and len(l1) > 1:
                gram = l1[3] + ' ' + l1[4] + ' ' + l1[5]
                prob = float(l1[1])
                trigram[gram] = prob
    return (unigram, bigram, trigram)

def calc_perplexity(word_num, sent_num, oov_num, sum):
    cnt = word_num + sent_num - oov_num
    total = -sum/cnt
    return 10 ** total

def sentence_perplexity(sentence, ngrams, lambdas):
    output = ''
    word_num, oov_num, sum, count = 0,0,0,1
    sentence_l = sentence.split(' ')
    word_num += (len(sentence_l) -2)
    ##Do Base case first
    word = sentence_l[1]
    if word in ngrams[0]:
        prob1 = lambdas[0]*ngrams[0][word]
        prob2 = 0
        word_1 = sentence_l[0]
        bi_gram = word_1 + ' ' + word
        if bi_gram in ngrams[1]:
            prob2 =  lambdas[1]*ngrams[1][bi_gram]
        prob = prob1 + prob2
        sum += math.log10(prob)
        output += '1: lg P({} | <s>) = {}\n'.format(word, "%.10f" % (prob))
    else:
        oov_num += 1
        output += '1: lg P({} | <s>) = -inf (unknown word)\n'.format(word)
    ##loop through rest of sentence
    for i in range(2,len(sentence_l)):
        word = sentence_l[i]
        word_1 = sentence_l[i-1]
        word_2 = sentence_l[i-2]
        if word not in ngrams[0]:
            oov_num += 1
            output += '{}: lg P({} | {} {}) = -inf (unknown word)\n'.format(i, word, word_1,word_2)
        else:
            prob1 = lambdas[0]*ngrams[0][word]
            seen2, seen3, prob2, prob3 = 0, 0, 0 ,0
            if word_1 in ngrams[0]:
                bi_gram = word_1 + ' ' + word
                prob = prob1 + prob2
                if bi_gram in ngrams[1]:
                    seen2 = 1
                    prob2 =  lambdas[1]*ngrams[1][bi_gram]
            if word_2 in ngrams[0]:
                if word_1 in ngrams[0]:
                    tri_gram = word_2 + ' ' + word_1 + ' ' + word
                    if tri_gram in ngrams[2]:
                        seen3 = 1
                        prob3 = lambdas[2]*ngrams[2][tri_gram]
            prob = prob1 + prob2 + prob3
            prob = math.log10(prob)
            sum += prob
            if seen2 == 0 or seen3 == 0:
                output += '{}: lg P({} | {} {}) = {} (unseen ngrams)\n'.format(i, word, word_2,word_1, "%.10f" % prob)
            else:
                output += '{}: lg P({} | {} {}) = {}\n'.format(i, word, word_2,word_1,  "%.10f" % prob)
    ppl = calc_perplexity(word_num, 1, oov_num, sum)
    output += '1 sentence, {} words, {} OOVs\nlgprob={} ppl={}\n\n\n'.format((len(sentence_l) -2), oov_num, "%.10f" %  sum, "%.10f" % ppl)
    return sum, oov_num, word_num, output
def ave(list):
    sum = 0
    for v in list:
        sum += v
    return sum/len(list)       
def perplexity(sentences, ngrams, lambdas, output_filename):
    sum, word_num, oov_num, count, lgprobs = 0, 0, 0, 1, []
    with open(output_filename,'w') as w:
        for sentence in sentences:
            w.write('\nSent #{}: <s> {} </s>\n'.format(count, sentence))
            count += 1
            a_sum, a_oov_num, a_word_num, output = sentence_perplexity(sentence, ngrams, lambdas)
            sum += a_sum
            lgprobs.append(a_sum)
            oov_num += a_oov_num
            word_num += a_word_num
            w.write(output)
        ave_sum = ave(lgprobs)
        ppl = calc_perplexity(word_num, count, oov_num, sum)
        w.write('%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\%\nsent_num={} word_num={} oov_num={}\nlgprob={} ave_lgprob={} ppl={}\n'.format(count-1, word_num, oov_num, "%.10f" % sum, "%.10f" % ave_sum, "%.10f" % ppl))

def main(lm_filename, lambda1,lambda2, lambda3, test_data_filename, output_filename):
    lambdas = (float(lambda1),float(lambda2),float(lambda3))
    sentences = load_sentences(test_data_filename)
    ngrams = load_lm(lm_filename)
    perplexity(sentences, ngrams,lambdas, output_filename)
 
if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage:ppl.py <lm_filename> <l1> <l2> <l3> <test_data_filename> <output_file>")
        exit(-1)
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])