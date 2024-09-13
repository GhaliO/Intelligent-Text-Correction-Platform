import React, { useState } from "react";
import stringSimilarity from "string-similarity";

const WordChecker = () => {
  const [inputValue, setInputValue] = useState("");
  const [resultMessages, setResultMessages] = useState([]);

  // Load the words from the words_alpha.txt file
  const wordList = fs.readFileSync("words_alpha.txt", "utf-8").split("\n");

  const checkWordsInSentence = () => {
    const wordsToCheck = inputValue.toLowerCase().split(" ");
    const messages = wordsToCheck.map((wordToCheck) => {
      const matches = stringSimilarity.findBestMatch(wordToCheck, wordList);
      const bestMatch = matches.bestMatch;

      if (bestMatch.rating >= 0.5) {
        return `"${wordToCheck}" is in the dictionary!`;
      } else {
        return `"${wordToCheck}" is not in the dictionary. Did you mean "${bestMatch.target}"?`;
      }
    });

    setResultMessages(messages);
  };

  const handleSaveToFile = () => {
    const blob = new Blob([inputValue], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "input.txt";
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Enter a sentence"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
      />
      <button onClick={checkWordsInSentence}>Check Words</button>
      <button onClick={handleSaveToFile}>Save Input to File</button>
      <div>
        {resultMessages.map((message, index) => (
          <p key={index}>{message}</p>
        ))}
      </div>
    </div>
  );
};

export default WordChecker;
