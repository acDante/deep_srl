import codecs
import os
import sys

input_data_path=sys.argv[1]
output_file_path=sys.argv[2]

LEMMA_IDX = int(sys.argv[3])
PROPS_IDX = LEMMA_IDX + 1

fout = open(output_file_path, 'w')

total_props = 0
total_sents = 0
doc_counts = 0

prev_words = ''
words = []
props = []
tags = []
spans = []
all_props = []

tag_dict={}
label_dict = {}

def print_new_sentence():
  global total_props
  global total_sents
  global words
  global props
  global tags
  global span
  global all_props
  global fout
  global domain


  # For debuging
  print("props:")
  print(props)
  print("propid_labels:")
  print(propid_labels)
  print("tags:")
  print(tags)
  print("words:")
  print(words)

  #if len(props) > 0:
  total_props += len(props)
  total_sents += 1
  #print len(props), len(tags)
  propid_labels = ['O' for _ in words]

  assert len(props) == len(tags)
  for t in range(len(props)):
    assert len(tags[t]) == len(words)
    #print tags[t], props[t], words
    # For example, "rubber stamp" is a verbal predicate, and stamp is the predicate head.
    assert tags[t][props[t]] in {"B-V", "I-V"}
    propid_labels[props[t]] = 'V'
    fout.write(str(props[t]) + " " + " ".join(words) + " ||| " + " ".join(tags[t]) + "\n")


fin = open(input_data_path, 'r')
for line in fin:
  line = line.strip()
  if line == '':
    joined_words = " ".join(words)
    prev_words = joined_words
    print_new_sentence()
      
    words = []
    props = []
    tags = []
    spans = []
    all_props = []
    continue

  info = line.split()
  word = info[0]
  #print info

  words.append(word)
  idx = len(words) - 1
  if idx == 0:
    tags = [[] for _ in info[PROPS_IDX:]]
    spans = ["" for _ in info[PROPS_IDX:]]

  # Lemma position.
  is_predicate = (info[LEMMA_IDX] != '-')

  for t in range(len(tags)):
    arg = info[PROPS_IDX + t]
    label = arg.strip("()*")
    label_dict[arg] = 1

    if "(" in arg:
      tags[t].append("B-" + label)
      spans[t] = label
    elif spans[t] != "":
      tags[t].append("I-" + spans[t])
    else:
      tags[t].append("O")
    if ")" in arg:
      spans[t] = ""
      
  if is_predicate:
    props.append(idx)

                        
fin.close()
fout.close()


print ('Processed {} documents, {} sentences and {} predicates.'.format(
          doc_counts, total_sents, total_props))

print ('Write SRL data to {}.'.format(
          output_file_path))