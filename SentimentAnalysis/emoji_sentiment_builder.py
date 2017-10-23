import json

with open('./res/emoji/emoji-sentiment-data.json') as data_file:
    data = json.load(data_file)

emojiScores = {}
#print(len(data))

for emojiDatum in data:
	if (emojiDatum["occurrences"] > 2):
		pNegative = emojiDatum["negative"]/emojiDatum["occurrences"]
		pNeutral = emojiDatum["neutral"]/emojiDatum["occurrences"]
		pPositive = emojiDatum["positive"]/emojiDatum["occurrences"]
	else:
		pNegative = 0.25
		pNeutral = 0.5
		pPositive = 0.25



	score = (pNegative * -1) + (pNeutral * 0) + (pPositive * 1);

	emojiScores[emojiDatum["sequence"]] = score

print(emojiScores['1F4D4'])

with open('./res/emoji-sentiment.json', 'w') as output:
    json.dump(emojiScores, output, indent=4)
