const fs = require("fs");
const express = require("express");
const fetch = require("node-fetch");
const path = require("path");
const { Configuration, OpenAIApi } = require("openai");
const app = express();

// Define a variable to hold the conversation histories
const sessions = {};

// Initialize OpenAI GPT with the API key
const configuration = new Configuration({
  apiKey: "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",
});
const openai = new OpenAIApi(configuration);
//const openai = new OpenAIApi({ key: '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' });  // Replace with your actual API key
app.use(express.json());
app.use(express.static(__dirname));

app.get("/", function (req, res) {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

const audioBuffers = {};


const CHARACTER_VOICES = {
  "Dave": "CYw3kZ02Hs0563khs1Fj",
  "Rachel": "21m00Tcm4TlvDq8ikWAM",
  "Michael": "flq6f7yk4E4fJM5XTYuZ",
  // Add more characters and their voice model IDs as needed
};

let currentVoiceModel = CHARACTER_VOICES["Dave"];  // Default character

app.post('/chat', async (req, res) => {
  //console.log("response");
  const message = req.body.text_prompt; // The user's message
  const extra_prompt = req.body.extra_prompt;
  const m_dest=req.body.dest;
  const m_begin=req.body.begin_time;
  const m_end=req.body.end_time;
  const m_num=req.body.number;
  const m_specif=req.body.specifications;
  let question="I hope you can design a perfect trip for me. There are some basic information from me"
  question+=" My destination is "+m_dest;
  question+=" The begin time is "+m_begin;
  question+=" The end time is "+ m_end;
  question+="The number of people is "+ m_num;
  question+="There are some specifications: "+m_specif;
  let gptResponse;
      gptResponse = await openai.createChatCompletion({
      model: "gpt-3.5-turbo",
      //messages: ["role":"user","content":message+extra_prompt],
      messages: [{"role": "user", "content": question}],
      
      max_tokens: 200,
    });

    const gptText = gptResponse.data.choices[0].message.content.trim();

    if (!gptText) {
      console.error("Error: Empty response from OpenAI API");
      res.status(500).json({ error: "Empty response from OpenAI API" });
      return;
    }

    //console.log("GPT-3 Response:", gptText);
    //console.log(gptResponse.data.choices[0].message.content.trim())
 res.json({text:gptText});
 //res.json({text:gptText});
});
// Function to generate audio using Eleven Labs TTS API
async function generateAudio(text) {
  const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${currentVoiceModel}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "xi-api-key": process.env.ELEVENLABS_API_KEY,
    },
    body: JSON.stringify({
      text: text,
      model_id: "eleven_monolingual_v1",
       // model_id: DAVE_VOICE_ID, 
      voice_settings: {
        stability: 0.5,
        similarity_boost: 0.5,
      },
    }),
  });

 if (response.ok) {
    const audioBuffer = await response.buffer();
    const audioId = Date.now().toString(); // Generate a unique identifier
    audioBuffers[audioId] = audioBuffer; // Save the buffer in memory
    return audioId; // Return the unique identifier
  } else {
    const errorBody = await response.text(); // Get the response body
    console.log("Error:", response.status, response.statusText, errorBody); // Log the response body
    throw new Error("Error generating audio");
  }
}


console.log("Eleven Labs API Key22:", process.env.ELEVENLABS_API_KEY);


app.post("/generate-text", async (req, res) => {
  
  const text_prompt = req.body.text_prompt;
  const input_face = req.body.input_face;
  const extra_prompt = req.body.extra_prompt;
  const ai_personality = req.body.ai_personality;
  const sessionId = req.body.sessionId;
  const characterName = req.body.characterName;  // Accept characterName in the request
  const voiceModel = CHARACTER_VOICES[characterName] || currentVoiceModel;
console.log("Eleven Labs API Key223:", process.env.ELEVENLABS_API_KEY);

  if (!sessions[sessionId]) {
    sessions[sessionId] = [
      {
        role: "system",
        content: ai_personality,
      },
    ];
  }

  sessions[sessionId].push({
    role: "system",
    content: ai_personality,
  });

  sessions[sessionId].push({
    role: "user",
    content: text_prompt + extra_prompt,
  });

  let gptResponse;
  try {
    gptResponse = await openai.createChatCompletion({
      model: "gpt-3.4-turbo",
      messages: sessions[sessionId],
      max_tokens: 200,
    });
    const gptText = gptResponse.data.choices[0].message.content.trim();
    sessions[0].push({
      role: "assistant",
      content: gptText,
    });


    if (!gptText) {
      console.error("Error: Empty response from OpenAI API");
      res.status(500).json({ error: "Empty response from OpenAI API" });
      return;
    }

    console.log("GPT-3 Response:", gptText);

    // Use the determined voice model for audio generation
    const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceModel}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "xi-api-key": process.env.ELEVENLABS_API_KEY,
      },
      body: JSON.stringify({
        text: gptText,
        model_id: "eleven_monolingual_v1",
        voice_settings: {
          stability: 0.5,
          similarity_boost: 0.5,
        },
      }),
    });

    if (response.ok) {
      const audioBuffer = await response.buffer();
      const audioId = Date.now().toString();
      audioBuffers[audioId] = audioBuffer;
      const audioUrl = `/audio/${audioId}`;
      const payload = {
        input_face: input_face,
        text_prompt: gptText,
        input_audio: audioId,
      };

      const lipsyncResponse = await fetch("https://api.gooey.ai/v2/LipsyncTTS/", {
        method: "POST",
        headers: {
          Authorization: "Bearer " + process.env["GOOEY_API_KEY"],
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      const result = await lipsyncResponse.json();
      console.log(lipsyncResponse.status, result);
      res.json({
        ...result,
        chatGptResponse: gptResponse.data.choices[0].message.content.trim(),
        audioUrl: audioUrl,
      });
    } else {
      const errorBody = await response.text();
      console.log("Error:", response.status, response.statusText, errorBody);
      throw new Error("Error generating audio");
    }
  } catch (error) {
    console.error("Error:", error);
    res.status(500).json({ error: "Error generating audio" });
    return;
  }
});



// Route to serve the audio file
app.get("/audio/:audioId", (req, res) => {
  const audioId = req.params.audioId;
  const audioBuffer = audioBuffers[audioId];
  if (audioBuffer) {
    res.setHeader('Content-Type', 'audio/mpeg');
    res.send(audioBuffer);
  } else {
    res.status(404).send('Not found');
  }
});


app.listen(process.env.PORT, () => {
  console.log(`Server running on port ${process.env.PORT}`);
});
console.log("Eleven Labs API Key:", process.env.ELEVENLABS_API_KEY);




app.post("/change-character", (req, res) => {
  const characterName = req.body.characterName;

  if (CHARACTER_VOICES[characterName]) {
    currentVoiceModel = CHARACTER_VOICES[characterName];
    res.json({ success: true, message: `Voice changed to ${characterName}` });
  } else {
    res.status(400).json({ success: false, message: "Character not found" });
  }
});

