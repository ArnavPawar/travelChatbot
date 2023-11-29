const { Configuration, OpenAIApi } = require("openai");
const configuration = new Configuration({
    apiKey: "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",
  });
  const openai = new OpenAIApi(configuration);
app.post('/chat', async (req, res) => {
    //console.log("response");
    //const message = req.body.text_prompt; // The user's message
    //const extra_prompt = req.body.extra_prompt;
    //const m_dest=req.body.dest;
    //const m_begin=req.body.begin_time;
    //const m_end=req.body.end_time;
    //const m_num=req.body.number;
    //const m_specif=req.body.specifications;
    let question="I hope you can design a perfect trip for me. There are some basic information from me"
    //question+=" My destination is "+m_dest;
    //console.log(question);
    //question+=" The begin time is "+m_begin;
    //question+=" The end time is "+ m_end;
    //question+="The number of people is "+ m_num;
    //question+="There are some specifications: "+m_specif;
    console.log(question);
    
    let gptResponse;
        gptResponse = await openai.createChatCompletion({
        model: "gpt-3.5-turbo",
        //messages: ["role":"user","content":message+extra_prompt],
        messages: [{"role": "user", "content": question}],
        
        max_tokens: 200,
      });
    console.log(question);
  
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