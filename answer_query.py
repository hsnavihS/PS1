from transformers import BertTokenizer
import pickle
import torch


def answer_question(question, answer_text, tokenizer, BERT_DL_Model):
    '''
    Takes a `question` string and an `answer_text` string (which contains the
    answer), and identifies the words within the `answer_text` that are the
    answer. Prints them out.
    '''
    input_ids = tokenizer.encode(question, answer_text)

    sep_index = input_ids.index(tokenizer.sep_token_id)

    num_seg_a = sep_index + 1

    num_seg_b = len(input_ids) - num_seg_a

    segment_ids = [0]*num_seg_a + [1]*num_seg_b

    assert len(segment_ids) == len(input_ids)

    start_scores, end_scores = BERT_DL_Model(torch.tensor([input_ids]),
                                             token_type_ids=torch.tensor(
                                                 [segment_ids]),
                                             return_dict=False)

    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores)

    tokens = tokenizer.convert_ids_to_tokens(input_ids)

    answer = tokens[answer_start]

    for i in range(answer_start + 1, answer_end + 1):

        if tokens[i][0:2] == '##':
            answer += tokens[i][2:]

        else:
            answer += ' ' + tokens[i]

    return answer
