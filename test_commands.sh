
# this shell script is for testing different combinations of commands in __main__.py
# NOTE: easytext should be installed before using this command

mkdir testoutput

python example_dumpnewsgroup20.py textfiles 100


# word count
python -m easytext wordcount tmp/*.txt testoutput/words_m10.xlsx --min_tf 10

python -m easytext wordcount tmp/*.txt testoutput/words_manual.xlsx --words 'news'


# sentiment
python -m easytext sentiment tmp/*.txt testoutput/sent_vanilla.xlsx

python -m easytext sentiment tmp/*.txt testoutput/sent_human.xlsx --human-readable

python -m easytext sentiment tmp/*.txt testoutput/sent_nonorm.xlsx --no-normalize

python -m easytext sentiment tmp/*.txt testoutput/sent_posneg.xlsx --posneg-only

python -m easytext sentiment tmp/*.txt testoutput/sent_all.xlsx --posneg-only --human-readable --no-normalize


# named entity recognition
python -m easytext entities tmp/*.txt testoutput/ent_m10.xlsx --min_tf 10

python -m easytext entities tmp/*.txt testoutput/ent_usetypes.xlsx --min_tf 10 --use-types "PERSON,NORP"

python -m easytext entities tmp/*.txt testoutput/ent_usetypes.xlsx --min_tf 10 --ignore-types "PERSON,NORP"


# gramattical features
python -m easytext grammar nounphrases tmp/*.txt testoutput/grammar_nounphrases.xlsx --min_tf 10

python -m easytext grammar nounphrases tmp/*.txt testoutput/grammar_nounphrases_human.xlsx --min_tf 10 -hr

python -m easytext grammar nounverbs tmp/*.txt testoutput/grammar_nounverbs.xlsx --min_tf 10

python -m easytext grammar nounverbs tmp/*.txt testoutput/grammar_nounverbs_human.xlsx --min_tf 10 -hr

python -m easytext grammar entverbs tmp/*.txt testoutput/grammar_entverbs.xlsx --min_tf 10

python -m easytext grammar entverbs tmp/*.txt testoutput/grammar_entverbs_human.xlsx --min_tf 10 -hr

python -m easytext grammar prepphrases tmp/*.txt testoutput/grammar_prepositions.xlsx --min_tf 10

python -m easytext grammar prepphrases tmp/*.txt testoutput/grammar_prepositions_human.xlsx --min_tf 10 -hr

# topic model with lda
python -m easytext topicmodel tmp/*.txt testoutput/lda_10.xlsx -n 10

python -m easytext topicmodel tmp/*.txt testoutput/lda_mintf3.xlsx -n 10 --min_tf 3

python -m easytext topicmodel tmp/*.txt testoutput/lda_nosavewm.xlsx -n 10 --nosave_wordmatrix

python -m easytext topicmodel tmp/*.txt testoutput/lda_seed2.xlsx -n 10 --seed 2

python -m easytext topicmodel tmp/*.txt testoutput/lda_all.xlsx -n 10 --seed 2 --min_tf 3 --nosave_wordmatrix


# topic model with nmf
python -m easytext topicmodel -t nmf tmp/*.txt testoutput/nmf_10.xlsx -n 10

python -m easytext topicmodel -t nmf tmp/*.txt testoutput/nmf_mintf3.xlsx -n 10 --min_tf 3

python -m easytext topicmodel -t nmf tmp/*.txt testoutput/nmf_nosavewm.xlsx -n 10 --nosave_wordmatrix

python -m easytext topicmodel -t nmf tmp/*.txt testoutput/nmf_seed2.xlsx -n 10 --seed 2

python -m easytext topicmodel -t nmf tmp/*.txt testoutput/nmf_all.xlsx -n 10 --seed 2 --min_tf 3 --nosave_wordmatrix


# glove model
python -m easytext glove -d 10 tmp/*.txt testoutput/glove_10.xlsx

python -m easytext glove -d 10 tmp/*.txt testoutput/glove_minct3.xlsx -m 3

python -m easytext glove -d 10 tmp/*.txt testoutput/glove_nosavewm.xlsx --nosave_wordmatrix

python -m easytext glove -d 10 tmp/*.txt testoutput/glove_all.xlsx --nosave_wordmatrix -m 3

python -m easytext glove -d 10 tmp/*.txt testoutput/glove_all.xlsx --nosave_wordmatrix -m 3 --keywords 'news|event,story'







