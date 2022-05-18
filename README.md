# EdCheckAI API doc and usage

## API doc:

### 1) Root endpoint:

#### How to access it

Make a GET request to API url

#### Output

A welcome message, that confirms that the connection between the flutter app and the API is working properly, without any errors/issues.


### 2) Sentiment checker + Paraphraser endpoint:

#### How to access it

Make a POST request to API url + "/paraphraser_sentiment_checker/" with a Dictionary object of the following format:
{
text = "YOUR INPUT TEXT HERE"
}

#### Output

The output is one of the following Dictionary types:

a) {"Positive", []} : This means that the response that the tutor is about to send has a positive/encouraging sentiment, hence no alternate sentence is suggested to the tutor.


b) {"Negative", ["Alternate1", "Alternate2", "Alternate3"]} : This means that the response that the tutor is about to send does not have a positive/encouraging sentiment, and a list of alternate sentences is suggested to the tutor in the array.



## Usage:

### 1) Root endpoint:

Use this endpoint in order to check if the app is able to connect with the API without any errors. It's a simple GET request and returns a welcome message that is easy to verify.


### 2) Sentiment checker + Paraphraser endpoint:

To be used in the flutter app page where the tutor is able to interact with the student.

a) As soon as the tutor stops typing, add a "Wait" statement for 1s.

b) Split the response of the tutor from the text box at "." , "?", and "!"

c) Call the API on each split response.

d) If the sentiment for any of the sentence is "Negative", highlight the sentence in the textbox with a red color on the frontend.

e) If the cursor is placed on any of the highlighted sentences, display the sentences from the array in the output in the Suggestions box on the frontend.

f) If the tutor clicks on any of the sentences in the Suggestions box, replace the original highlighted sentence with the new sentence that was just clicked.
