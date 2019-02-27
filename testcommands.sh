
# this shell script is for testing different combinations of commands in __main__.py
# NOTE: easytext should be installed before using this command


mkdir testoutput

python example_dumpnewsgroup20.py 20


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


# sentiment
python -m easytext sentiment tmp/*.txt testoutput/sent_vanilla.xlsx

python -m easytext sentiment tmp/*.txt testoutput/sent_human.xlsx --human-readable

python -m easytext sentiment tmp/*.txt testoutput/sent_nonorm.xlsx --no-normalize

python -m easytext sentiment tmp/*.txt testoutput/sent_posneg.xlsx --posneg-only

python -m easytext sentiment tmp/*.txt testoutput/sent_all.xlsx --posneg-only --human-readable --no-normalize






