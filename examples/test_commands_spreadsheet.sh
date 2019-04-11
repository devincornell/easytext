
# this shell script is for testing different combinations of commands in __main__.py
# NOTE: easytext should be installed before using this command

mkdir testoutput

python example_data.py spreadsheet 100

INPUT="tmp_example.csv"
ARGS="--textcol text --doclabelcol title"

# word count
echo "Line 1" >&2
python -m easytext wordcount $INPUT testoutput/words_m10.xlsx --min_tf 10 $ARGS

echo "Line 2" >&2
python -m easytext wordcount $INPUT testoutput/words_manual.xlsx --words 'news'


# sentiment
echo "Line 3" >&2
python -m easytext sentiment $INPUT testoutput/sent_vanilla.xlsx

echo "Line 4" >&2
python -m easytext sentiment $INPUT testoutput/sent_human.xlsx --human-readable

echo "Line 5" >&2
python -m easytext sentiment $INPUT testoutput/sent_nonorm.xlsx --no-normalize

echo "Line 6" >&2
python -m easytext sentiment $INPUT testoutput/sent_posneg.xlsx --posneg-only

echo "Line 7" >&2
python -m easytext sentiment $INPUT testoutput/sent_all.xlsx --posneg-only --human-readable --no-normalize


# named entity recognition
echo "Line 8" >&2
python -m easytext entities $INPUT testoutput/ent_m10.xlsx --min_tf 10

echo "Line 9" >&2
python -m easytext entities $INPUT testoutput/ent_usetypes.xlsx --min_tf 10 --use-types "PERSON,NORP"

echo "Line 10" >&2
python -m easytext entities $INPUT testoutput/ent_usetypes.xlsx --min_tf 10 --ignore-types "PERSON,NORP"


# gramattical features
echo "Line 11" >&2
python -m easytext grammar nounphrases $INPUT testoutput/grammar_nounphrases.xlsx --min_tf 10

echo "Line 12" >&2
python -m easytext grammar nounphrases $INPUT testoutput/grammar_nounphrases_human.xlsx --min_tf 10 -hr

echo "Line 13" >&2
python -m easytext grammar nounverbs $INPUT testoutput/grammar_nounverbs.xlsx --min_tf 10

echo "Line 14" >&2
python -m easytext grammar nounverbs $INPUT testoutput/grammar_nounverbs_human.xlsx --min_tf 10 -hr

echo "Line 15" >&2
python -m easytext grammar entverbs $INPUT testoutput/grammar_entverbs.xlsx --min_tf 10

echo "Line 16" >&2
python -m easytext grammar entverbs $INPUT testoutput/grammar_entverbs_human.xlsx --min_tf 10 -hr

python -m easytext grammar prepphrases $INPUT testoutput/grammar_prepositions.xlsx --min_tf 10

python -m easytext grammar prepphrases $INPUT testoutput/grammar_prepositions_human.xlsx --min_tf 10 -hr

# topic model with lda
python -m easytext topicmodel $INPUT testoutput/lda_10.xlsx -n 10

python -m easytext topicmodel $INPUT testoutput/lda_mintf3.xlsx -n 10 --min_tf 3

python -m easytext topicmodel $INPUT testoutput/lda_nosavewm.xlsx -n 10 --nosave_wordmatrix

python -m easytext topicmodel $INPUT testoutput/lda_seed2.xlsx -n 10 --seed 2

python -m easytext topicmodel $INPUT testoutput/lda_all.xlsx -n 10 --seed 2 --min_tf 3 --nosave_wordmatrix


# topic model with nmf
python -m easytext topicmodel -t nmf $INPUT testoutput/nmf_10.xlsx -n 10

python -m easytext topicmodel -t nmf $INPUT testoutput/nmf_mintf3.xlsx -n 10 --min_tf 3

python -m easytext topicmodel -t nmf $INPUT testoutput/nmf_nosavewm.xlsx -n 10 --nosave_wordmatrix

python -m easytext topicmodel -t nmf $INPUT testoutput/nmf_seed2.xlsx -n 10 --seed 2

python -m easytext topicmodel -t nmf $INPUT testoutput/nmf_all.xlsx -n 10 --seed 2 --min_tf 3 --nosave_wordmatrix


# glove model
python -m easytext glove -d 10 $INPUT testoutput/glove_10.xlsx

python -m easytext glove -d 10 $INPUT testoutput/glove_minct3.xlsx -m 3

python -m easytext glove -d 10 $INPUT testoutput/glove_nosavewm.xlsx --nosave_wordmatrix

python -m easytext glove -d 10 $INPUT testoutput/glove_all.xlsx --nosave_wordmatrix -m 3

python -m easytext glove -d 10 $INPUT testoutput/glove_all.xlsx --nosave_wordmatrix -m 3 --keywords 'news|event,story'







