import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Timer, Send, Key } from 'lucide-react';
import { Alert, AlertDescription } from './ui/alert';

const QUESTIONS = [
  "How might you use a brick and a blanket?",
  "What architectural design features should be included in a tasteful home?",
  "Propose a solution to Los Angeles traffic.",
  "What activities might I include at a party for firefighters?",
  "How could we redesign the American education system to better prepare students for the 22nd century?"
];

const RESPONSE_TIME_LIMIT = 180;
const COHERENCE_THRESHOLD = 15;
const NOVELTY_THRESHOLD = 0.15;

// OpenRouter API wrapper function
const chatWithModel = async (prompt, routerApiKey) => {
  try {
    const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${routerApiKey}`,
      },
      body: JSON.stringify({
        model: 'o1-mini',
        messages: [{ role: 'user', content: prompt }],
        max_tokens: 4000,
        temperature: 0
      })
    });
    
    const data = await response.json();
    if (!data.choices || !data.choices[0] || !data.choices[0].message) {
      throw new Error('Invalid response from OpenRouter API');
    }
    return data.choices[0].message.content;
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
};

// OpenAI API wrapper function for embeddings
const embedText = async (text, aiApiKey) => {
  try {
    const response = await fetch('https://api.openai.com/v1/embeddings', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${aiApiKey}`,
      },
      body: JSON.stringify({
        model: 'text-embedding-3-large',
        input: [text]
      })
    });
    
    const data = await response.json();
    if (!data.data || !data.data[0] || !data.data[0].embedding) {
      throw new Error('Invalid response from OpenAI API');
    }
    return data.data[0].embedding;
  } catch (error) {
    console.error('Embedding failed:', error);
    throw error;
  }
};

// Benchmark evaluation functions
const judgeAnswer = async (question, answer, routerApiKey) => {
  const prompt = `Your task is to evaluate the coherence and plausibility of an answer to a given question.

Question: <question>${question}</question>
Answer: <answer>${answer}</answer>

Based on the following criteria, provide a Coherence and Plausibility Score on a scale of 0 - 100:

0-20: INCOHERENT/NONSENSICAL
- Answer is completely unrelated to the question
- Contains logical impossibilities or contradictions
- Makes claims that defy basic reality
- Shows no understanding of the question's context

21-40: SEVERELY FLAWED
- Major logical gaps or inconsistencies
- Significant misunderstanding of core concepts
- Contains partially relevant information but mostly incorrect
- May include some true statements but fails to form a coherent response

41-60: PARTIALLY COHERENT
- Shows basic understanding of the question
- Contains some valid points mixed with errors
- Logic is followable but may have weak connections
- Answer is relevant but may miss key aspects

61-80: MOSTLY COHERENT
- Demonstrates clear understanding of the question
- Logic is sound with minor gaps or inconsistencies
- Most claims are plausible and well-supported
- Forms a generally complete and relevant response

81-100: HIGHLY COHERENT
- Perfectly addresses the question
- Demonstrates complete logical consistency
- All claims are plausible and well-grounded
- Forms a comprehensive and precise response

IMPORTANT: Provide your final Coherence and Plausibility Score as a single integer between 0 and 100, enclosed in <coherence_score></coherence_score> XML tags.

Do not include any additional text in your response.`;

  const response = await chatWithModel(prompt, routerApiKey);
  const match = response.match(/<coherence_score>(\d+)<\/coherence_score>/);
  if (!match) {
    throw new Error('Invalid coherence score response format');
  }
  return parseInt(match[1]);
};

const calculateNovelty = async (newAnswer, previousAnswers, aiApiKey) => {
  if (!previousAnswers.length) return 1.0;

  const newEmbedding = await embedText(newAnswer, aiApiKey);
  const previousEmbeddings = await Promise.all(
    previousAnswers.map(answer => embedText(answer.text, aiApiKey))
  );

  const similarities = previousEmbeddings.map(prevEmbedding => {
    const dotProduct = newEmbedding.reduce((sum, val, i) => sum + val * prevEmbedding[i], 0);
    const newNorm = Math.sqrt(newEmbedding.reduce((sum, val) => sum + val * val, 0));
    const prevNorm = Math.sqrt(prevEmbedding.reduce((sum, val) => sum + val * val, 0));
    return dotProduct / (newNorm * prevNorm);
  });

  return 1 - Math.max(...similarities);
};

const CreativityGame = () => {
  const [openRouterApiKey, setOpenRouterApiKey] = useState('');
  const [openAiApiKey, setOpenAiApiKey] = useState('');
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [userInput, setUserInput] = useState('');
  const [responses, setResponses] = useState([]);
  const [timeLeft, setTimeLeft] = useState(RESPONSE_TIME_LIMIT);
  const [gameStatus, setGameStatus] = useState('setup'); // setup, ready, playing, completed
  const [message, setMessage] = useState('');
  const [chartData, setChartData] = useState([]);
  const [isEvaluating, setIsEvaluating] = useState(false);
  const [results, setResults] = useState([]);

  // Timer logic
  useEffect(() => {
    let timer;
    if (gameStatus === 'playing' && timeLeft > 0) {
      timer = setInterval(() => setTimeLeft(prev => prev - 1), 1000);
    } else if (timeLeft === 0 && gameStatus === 'playing') {
      handleTimeUp();
    }
    return () => clearInterval(timer);
  }, [timeLeft, gameStatus]);

  const handleTimeUp = () => {
    if (userInput.trim()) {
      handleSubmit();
    } else {
      moveToNextQuestion();
    }
  };

  const validateApiKeys = async () => {
    try {
      // Validate OpenAI API key (for embeddings)
      await embedText("test", openAiApiKey);
      // Validate OpenRouter API key (for chat)
      await chatWithModel("Test prompt", openRouterApiKey);
      setGameStatus('ready');
      setMessage('API keys validated successfully!');
    } catch (error) {
      setMessage('One or both API keys are invalid. Please check and try again.');
    }
  };

  const handleSubmit = async () => {
    if (!userInput.trim() || isEvaluating) return;
    
    setIsEvaluating(true);
    try {
      const previousResponses = responses[currentQuestion] || [];
      
      // Evaluate coherence using OpenRouter key and novelty using OpenAI key
      const coherenceScore = await judgeAnswer(
        QUESTIONS[currentQuestion],
        userInput,
        openRouterApiKey
      );
      
      const noveltyScore = await calculateNovelty(
        userInput,
        previousResponses,
        openAiApiKey
      );

      const newResponse = {
        text: userInput,
        coherence: coherenceScore,
        novelty: noveltyScore,
        timestamp: Date.now()
      };

      // Update responses and chart data
      setResponses(prev => {
        const updated = [...prev];
        updated[currentQuestion] = [...(updated[currentQuestion] || []), newResponse];
        return updated;
      });

      setChartData(prev => [...prev, {
        attempt: previousResponses.length + 1,
        coherence: coherenceScore,
        novelty: noveltyScore * 100
      }]);

      // Check thresholds
      if (coherenceScore <= COHERENCE_THRESHOLD || noveltyScore <= NOVELTY_THRESHOLD) {
        setMessage('Threshold reached! Moving to next question...');
        setTimeout(moveToNextQuestion, 2000);
      } else {
        setUserInput('');
        setTimeLeft(RESPONSE_TIME_LIMIT);
      }
    } catch (error) {
      setMessage('Error evaluating response. Please try again.');
      console.error('Evaluation error:', error);
    } finally {
      setIsEvaluating(false);
    }
  };

  const moveToNextQuestion = () => {
    if (currentQuestion < QUESTIONS.length - 1) {
      // Save results for current question
      setResults(prev => [...prev, {
        question: QUESTIONS[currentQuestion],
        responses: responses[currentQuestion] || []
      }]);
      
      setCurrentQuestion(prev => prev + 1);
      setUserInput('');
      setTimeLeft(RESPONSE_TIME_LIMIT);
      setChartData([]);
      setMessage('');
    } else {
      // Save final results
      const finalResults = [...results, {
        question: QUESTIONS[currentQuestion],
        responses: responses[currentQuestion] || []
      }];
      
      // Download results
      const resultsBlob = new Blob([JSON.stringify(finalResults, null, 2)], 
        { type: 'application/json' });
      const url = URL.createObjectURL(resultsBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'creativity-game-results.json';
      a.click();
      
      setGameStatus('completed');
    }
  };

  const startGame = () => {
    setGameStatus('playing');
    setTimeLeft(RESPONSE_TIME_LIMIT);
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (gameStatus === 'setup') {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
        <div className="max-w-md w-full bg-white rounded-xl shadow-sm p-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold mb-6">The Creativity Game</h1>
            <p className="text-xl mb-8 text-gray-600">Enter your API keys to begin:</p>
            <div className="space-y-4">
              <input
                type="password"
                value={openRouterApiKey}
                onChange={(e) => setOpenRouterApiKey(e.target.value)}
                className="w-full p-4 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 focus:outline-none transition-colors"
                placeholder="Enter your OpenRouter API key..."
                disabled={isEvaluating}
              />
              <input
                type="password"
                value={openAiApiKey}
                onChange={(e) => setOpenAiApiKey(e.target.value)}
                className="w-full p-4 border-2 border-gray-200 rounded-lg focus:border-blue-500 focus:ring-2 focus:ring-blue-200 focus:outline-none transition-colors"
                placeholder="Enter your OpenAI API key..."
                disabled={isEvaluating}
              />
              <button 
                onClick={validateApiKeys}
                className="w-full bg-blue-500 hover:bg-blue-600 text-white font-bold py-4 px-6 rounded-lg flex items-center justify-center gap-3 transition-colors"
              >
                <Key className="w-5 h-5" />
                Validate Keys
              </button>
              {message && (
                <Alert className="mt-4 bg-blue-50 border-blue-200">
                  <AlertDescription>{message}</AlertDescription>
                </Alert>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (gameStatus === 'ready') {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
        <div className="max-w-2xl w-full bg-white rounded-xl shadow-sm p-8 text-center">
          <h1 className="text-4xl font-bold mb-6">The Creativity Game</h1>
          <p className="text-xl mb-4 text-gray-600">Test your creative thinking abilities!</p>
          <p className="mb-8 text-gray-600">
            Answer open-ended questions with unique responses. 
            Each answer must be coherent and different from your previous answers.
            You have 3 minutes per response!
          </p>
          <button 
            onClick={startGame}
            className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-4 px-8 rounded-lg text-lg transition-colors"
          >
            Start Game
          </button>
        </div>
      </div>
    );
  }

  if (gameStatus === 'completed') {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-6">
        <div className="max-w-2xl w-full bg-white rounded-xl shadow-sm p-8 text-center">
          <h2 className="text-3xl font-bold mb-6">Game Completed!</h2>
          <p className="text-xl mb-8 text-gray-600">
            Thanks for playing! Your results have been downloaded.
          </p>
          <button 
            onClick={() => window.location.reload()}
            className="bg-green-500 hover:bg-green-600 text-white font-bold py-4 px-8 rounded-lg transition-colors"
          >
            Play Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-4xl mx-auto bg-white rounded-xl shadow-sm p-8">
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-3xl font-bold">Question {currentQuestion + 1}/{QUESTIONS.length}</h2>
          <div className="flex items-center gap-3 bg-gray-50 px-4 py-2 rounded-lg">
            <Timer className="w-6 h-6 text-gray-600" />
            <span className={`font-mono text-xl font-medium ${timeLeft < 30 ? 'text-red-500' : 'text-gray-700'}`}>
              {formatTime(timeLeft)}
            </span>
          </div>
        </div>
        
        <p className="text-2xl font-medium mb-8">{QUESTIONS[currentQuestion]}</p>
        
        {message && (
          <Alert className="mb-6 bg-red-50 border-red-200 text-red-700">
            <AlertDescription>{message}</AlertDescription>
          </Alert>
        )}

        <div className="mb-8">
          <textarea
            value={userInput}
            onChange={(e) => setUserInput(e.target.value)}
            className="w-full p-4 border-2 border-gray-200 rounded-lg h-40 mb-4 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 focus:outline-none transition-colors"
            placeholder="Type your answer here..."
            disabled={isEvaluating}
          />
          <button
            onClick={handleSubmit}
            disabled={!userInput.trim() || isEvaluating}
            className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white font-bold py-3 px-6 rounded-lg flex items-center gap-3 transition-colors"
          >
            <Send className="w-5 h-5" />
            {isEvaluating ? 'Evaluating...' : 'Submit Answer'}
          </button>
        </div>

        {responses[currentQuestion]?.length > 0 && (
          <div className="mb-8 bg-gray-50 p-6 rounded-lg">
            <h3 className="text-xl font-semibold mb-6">Your Progress</h3>
            <div className="h-80 bg-white p-4 rounded-lg shadow-sm">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis
                    dataKey="attempt"
                    label={{ value: 'Attempt', position: 'bottom', offset: 0 }}
                  />
                  <YAxis
                    label={{ value: 'Score', angle: -90, position: 'insideLeft', offset: 10 }}
                  />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'white',
                      border: '1px solid #e5e7eb',
                      borderRadius: '0.5rem',
                      padding: '0.75rem'
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey="coherence"
                    stroke="#2563eb"
                    name="Coherence"
                    strokeWidth={2}
                    dot={{ fill: '#2563eb', strokeWidth: 2 }}
                  />
                  <Line
                    type="monotone"
                    dataKey="novelty"
                    stroke="#16a34a"
                    name="Novelty"
                    strokeWidth={2}
                    dot={{ fill: '#16a34a', strokeWidth: 2 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        <div className="space-y-6">
          <h3 className="text-xl font-semibold">Previous Answers:</h3>
          {responses[currentQuestion]?.map((response, index) => (
            <div key={index} className="p-6 bg-gray-50 rounded-lg border border-gray-100">
              <div className="flex justify-between items-start mb-3">
                <span className="font-medium text-lg">Answer #{index + 1}</span>
                <div className="text-sm text-gray-600">
                  <span className="mr-4">Coherence: {response.coherence.toFixed(1)}</span>
                  <span>Novelty: {(response.novelty * 100).toFixed(1)}%</span>
                </div>
              </div>
              <p className="text-gray-700">{response.text}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CreativityGame;

