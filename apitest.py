import auth

print(auth.getfreq('friend'))
print(auth.getfreq('khdkjhdf'))
print(auth.getfreq('asked'))

# Results when word is found in wordsapiv1:
#   {'word': 'friend', 'frequency': {'zipf': 5.65, 'perMillion': 448.38, 'diversity': 0.72}}
# Results when word is NOT found in wordsapiv1:{'success': False, 'message': 'word not found'}
