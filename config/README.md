This is where project-specific configs go.

They have a structure like:

```json
{

  "corpus": [ "corpus/project/input/*.txt" ],
  "body_json": "data/project-body.jsonl",
  "index_file": "data/project-index.jsonl",

  "fasttext_file": "data/project-fasttext.txt",
  "raw_embed": "data/project-embed-raw.bin",
  "parent_embed": "ext/crawl-300d-2M-subword.bin",
  "embed_merge_file": "data/project-embed-merge.json",
  "embed_merge_model": "data/project-embed-merge.h5",
  "embed_weights": "data/project-embed-weights.pickle",

  "keys_json": "data/project-keys.jsonl",
  "flat_keys_json": "data/project-flat-keys.jsonl",

  "per_word_context": 500,
  "xy_json": "data/project-xy.jsonl",

  "train_val_split": 0.8,
  "train_json": "data/project-train.jsonl",
  "val_json": "data/project-val.jsonl",
 
  "train_tf": "data/project-train.tfrecords",
  "val_tf": "data/project-val.tfrecords",

  "model_file": "data/project-model.h5",
  "model_params": "data/project-model-params.json",

  "test_file": "corpus/project/test/test1.txt"
  
}
```

corpus
: A list of glob patterns that expand to individual documents in
the corpus.

body_json
: Where to put the jsonlines version of the corpus containing words
and split by sentences.

index_file
: Where to put a count of the vocab, a dict mapping words into keys,
and a list mapping keys into words.

fasttext_file
: Where to write the entire corpus, one sentence per line,
tokenized by word, for use by FastText to build the word embedding.

raw_embed
: Where the raw FastText embeddings built from the corpus will live.

parent_embed
: The parent/general-purpose FastText embedding to use with
this project.

embed_merge_file
: Where to put the X-Y training data for the embedding merge model.

embed_merge_model
: Where to put the model that transforms raw embeddings into the parent 
space.

embed_weights
: Where to put a pickled numpy array containing the word vectors for
each unique word in our vocabulary.

keys_json
: Where to put the jsonlines version of the corpus containing keys
and split by sentences.

flat_keys_json
: Where to put the jsonlines version of the corpus containing keys
with one flat list of keys for each document.

per_word_context
: How many preceding words to use for next-word prediction.

xy_json
: Where to put the jsonlines containing X and Y samples for the model.

train_val_split
: The fraction of samples that should be used for the training set.

train_json
: Where to put the training samples.

val_json
: Where to put the validation samples.

train_tf
: Where to put the compiled tfrecords containing the training
samples.

val_tf
: Where to put the compiled tfrecords containing the validation
samples.

model_file
: Where to put the untrained model.

model_param
: Where to put the JSON data needed for remote execution of the model.

test_file
: File containing an out-of-corpus sample to be used as the basis for
prediction testing.
