# PIG LATIN RESTFUL TRANSLATOR API

## Objective:
Users can translate text to Pig Latin.
Create a REST Api that,
- Handles Registration (Confirmation needed)
- Authentication And Authorization
- Receives content and Translate it to Pig Latin (save this resource to be fetch)
 ex:  POST /posts  , GET /posts/1  <-- content should be translated to Pig Latin.

## Requirements:
 - Only authenticated users (active) can post content to be translated
 - At least an 85% test coverage
 - Any database can be used (even in memory)
 - An beautiful algorithm for the Pig Latin translation. 
 - Be RESTFUL 
 - Provide simple client for accessing the API or Curl request / Postman etc.


Basically, the Pig Latin system used here works as follows:

Words that start with a vowel (A, E, I, O, U) simply have "WAY" appended to the end of the word.
Words that start with a consonant have all consonant letters up to the first vowel moved to the end of the word (as opposed to just the first consonant letter), and "AY" is appended. ('Y' is counted as a vowel in this context)
The algorithm incorporates the following features and special case functionality:

Ensures proper capitalization
Correct upper case and lower case formatting
Correctly translates "qu" (e.g., ietquay instead of uietqay)
Differentiates between "Y" as vowel and "Y" as consonant
(e.g. yellow = elloyay and style = ylestay) — (except for a very few exceptions)
Correctly translates contractions
Hyphenated words are treated as two words
Words may consist of alphabetic characters only (A-Z and a-z)
All punctuation, numerals, symbols and whitespace are not modified
