---
layout: post
title: "Future Crap, Part 2: Building brand-injection for generative AI"
date: 2024-07-01
---

#### Building brand-injection for generative AI

*If you're looking for example output, start with* [*Part 1*](https://medium.com/@keith.trnka/future-crap-part-1-373e607aef51)*. This post is the "how it's made" portion.*

![Clock with bacon hands -- one of the generated images from Part 1]({{ "/assets/img/posts/future-crap-1-clock-bacon.png" | relative_url }})

### Origin story

This effort was a mixture of curiosity and satire.

A couple years ago I was mulling over ideas to augment Giphy memes with GenAI memes and ways to pay the server bills. Recently I had more free time after a layoff and wanted some practice with retrieval-augmented generation.

I have some satirical motivation here as well: many companies build innovative technology, then refine it into a productive application, then users flock to it, and once they're entrenched they [enshittify](https://en.wikipedia.org/wiki/Enshittification) the technology often by putting more and more ads into it. It gets to the point where the products are barely worth the hassle.

Another thing on my mind is why ChatGPT is sometimes better than Google. They often have very similar results, but ChatGPT doesn't force me through tons of ads and accept-cookies popups.

### How it works

I made Future Crap available to some friends in our shared Slack channel.

When a user types the command `/futurecrap` followed by a description such as "a photorealistic cat and dog in an intense staring contest in the office," the request is forwarded over a socket to the backend server (assuming it's online). The backend then searches for brand matches using the prompt as the query in an in-memory vector database. This search matches the prompt against brand descriptions such as "… is a fast-food restaurant chain known for its fried chicken, sides, and sandwiches, targeting families, individuals, and chicken enthusiasts seeking flavorful and convenient dining options …". Among the top three closest brand matches, a random selection is made with a preference for higher match scores.

Next, the backend randomly selects the image generation service, either OpenAI DALL-E 3 or AWS Titan. The prompt is then augmented in one of two ways depending on the brand. In both cases, we're using the ChatGPT API with examples of good and bad brand-injection to do few-shot learning. Also note that DALL-E and Titan perform better with different types of prompts, so we're using different meta-prompts for each to customized to each image generation engine.

For most brands, the inputs are the original prompt and the brand name. If the brand data has a `brand_style` field, the inputs include the original prompt and a visual description of the brand. This approach is good for brands that are not prominent in the training data of the image generator. In my testing I found this critical for Boss Coffee, Rainier Beer, Mt. Joy (a Seattle food truck), Olympia Coffee, Blockbuster, and a few others.

Once the prompt is augmented with the brand information, it is sent to the selected image generation backend. The generated image is then uploaded to S3. A Slack message containing the image URL and other metadata is sent back over the Slack socket. Finally, the Slack servers post this information into the channel data, making the image visible to the users in the channel.

If you're looking in the repo, there's also a web frontend that I use for local development.

#### About the brand data

The brand data was built by hand using ChatGPT/Copilot and [ImageToPrompt](https://imagetoprompt.com/). It took a number of iterations and still needs improvement.

This is a rough outline of how I iterated:

1.  I started with a list of brands that I remembered from commercials or ads. For example, Pepsi and Nike are famous for marketing.
2.  I used ChatGPT to generate a description of the target demographic and used that for brand matching.
3.  I expanded the list of brands by chatting with friends and reviewing the S&P 500 for companies I thought had recognizable branding.
4.  I saw that it sometimes matched in a way that didn't make any sense for the scene, so I used ChatGPT to generate the `brand_identity` field after giving some examples. That was intended to capture the general vibe of each brand's ads rather than the target demographic.
5.  I had a failed experiment in which I generated example ads to use for matching. The examples were good but it was slow to generate so I didn't explore it further.
6.  I saw that it didn't work for less well-known brands (like Boss Coffee) and it couldn't possibly work for new, local brands (like Mt. Joy) so I tried searching for their icons, fed those into ImageToPrompt, and then added that as a field in the brand data `brand_style`. Then if that field was present, I had the prompt generator use a different metaprompt to do the prompt augmentation from the visual description.
7.  I expanded for a while with ImageToPrompt but it was going slowly so I used Copilot in VSCode to add `brand_style` for many other brands. I found that I often had to nudge it to be specific about the color scheme and font style. Though once in a while I needed to write the whole thing myself.

### Successes

Initially I used a simple template like "{prompt}. Include product placement from {company_name}". That sometimes worked in DALL-E, almost never worked in Titan, and it wasn't very reliable overall.

I had success in using GPT to convert an input prompt into a brand-injected prompt and tuning it for each image generator. This was great because the users didn't need to adapt for DALL-E 3 vs Titan and GPT handled it for them. It also unlocked an easy way to optimize: I could take the good image generation prompts, hand-optimize them further, then use them as examples for few-shot learning in the metaprompt. This was great though I should've iterated more on how to do the few-shot prompt.

Here's an example of what I mean by a metaprompt for AWS Titan:

> Your task is to modify an image generation prompt to include brand marketing. The output prompt should be relatively short and to the point about the key details with prominent brand marketing. Here are some examples of inputs and varying quality outputs.
>
> Input prompt: a cartoon family of scorpions walking to school in the morning. The smallest scorpion has a cute backpack and lunch box
>
> Input brand: McDonald's
>
> Good output: Illustrate a charming cartoon family of realistic-looking scorpions walking to school in the morning. The youngest scorpion is wearing a cute backpack with the iconic McDonald's red and yellow colors and carrying a matching lunchbox from its stinger. A McDonald's billboard is shown prominently in the background.
>
> …
>
> Now you'll be provided an input prompt and brand and you will modify the prompt to prominently feature the brand in the scene. Only respond with the modified prompt.
>
> Input prompt: {prompt}
>
> Input brand: {brand_name}
>
> Excellent output (use up to 125 tokens in the output):

The "good output" vs "excellent output" vs "mediocre output" distinctions was an idea to get a little more value out of additional supervision, but I didn't explore it thoroughly so I don't know if it helped.

For smaller brands, I found that I could use image2prompt to generate a description of the visual style of brands that DALL-E and Titan couldn't support natively. That's how I was able to even use brands like Mt. Joy, a Seattle food truck. Though it couldn't perfectly recreate their logo. This style of generation worked especially well when I made sure that the "brand style" field included description of not just the logo but also the color scheme and any font styles.

Here's an example of a brand-injected prompt with a smaller brand from the visual description, targeted at DALL-E 3:

> **Original prompt:** three college-aged people just got their chicken sandwiches from a food truck. They all have sandwiches in both hands and they're happy about it
>
> **Brand-injected prompt:** Capture the joyous moment of three college-aged individuals receiving their delicious chicken sandwiches from a vibrant food truck. Each person is holding two sandwiches in their hands, showcasing their excitement. The background prominently features a green geometric logo with a floral pattern on the left side, and the text "Mt. Joy" in bold green letters on the right, all set against a clean white backdrop. The scene exudes happiness and youthful energy, perfectly encapsulating the spirit of Mt. Joy's brand. Please take extra care to show Mt. Joy branding very prominently.

I included randomization in the Slack demo to provide a more dynamic experience for users, for example randomizing the brand matching by match score. That addressed a previous issue in which Domino's would be used for too many ads even though it had a similar score to other brands. Likewise I randomized between DALL-E 3 and Titan to provide variety. If I had more time I would've built a routing layer like [Unify.ai](https://unify.ai/) to pick the best engine for each prompt. That said, in the web demo I disabled randomization to provide more predictability during development.

I'll mention a couple quick engineering wins too:

- Slack Bolt with sockets was a great way to prototype; I just ran it from my laptop and could iterate very rapidly instead of needing to do a whole deployment to update.
- txtai was great for easy in-memory vector search.

### Challenges

- DALL-E 3 API tends to remove brand info. From trial and error I learned that Microsoft Image Creator doesn't have this problem even though it's also using DALL-E 3. I didn't find any tips for the DALL-E 3 API that gave results like Image Creator.
- Titan rejects some prompts based on their content filter, though it's tough to know when that'll happen.
- DALL-E 3 and Titan are trained on very different sorts of inputs. The ideal input for DALL-E 3 is long and descriptive, and can be up to 4000 chars. The ideal input for Titan is short and caption-like, and can be up to 512 chars.
- Evaluation is subjective and tough. Maybe I should've tried gpt4o as judge? I had originally planned to use Slack emoji reactions for judging but I didn't have enough in-Slack data for it to be useful.

### Should've

I wish I'd worked on evaluation earlier in development. I procrastinated about it because I didn't like the idea of paying \$1 of API fees for every little test. In retrospect, I should've started with a local image generation model from HuggingFace and iterated on that in an evaluation framework before iterating with the cloud API models.

In some of the generated images I suspected it might be simply copying an existing image, so I sometimes reverse image searched the results. I wish I'd built it into the application so that I could check more often though.

### Could this be a real industry project?

To subsidize meme generation? It's unlikely to work with current technology. I cherry-picked examples and I'd guess that I showed you the best 20%. Maybe it could work if you over-generate examples then use a multimodal model as a judge to select the branded ones. You might also need to cache responses to save costs. Even then, would REI be willing to spend real money if we misspell their name?

Could it succeed as a product to subsidize general-purpose image generation? I don't think enough people are using image generation today to recoup the development cost. If I think back to the early days of Google and Youtube, they started off by building a great product with a large user base before scaling up their advertising. General image generation isn't at that scale yet, and might never get there.

Also a real version of this might need:

- Need an image generator that's DALL-E 3 quality but more reliable at branding (OpenAI and Microsoft have this, maybe others do too?)
- Need to provide advertisers with control over their brand, like what types of prompts get their branding. I'm doubtful that just providing advertisers with a text field would be enough on its own.
- Need to deal with prompts that aren't monetizable, similar to how YouTube demonetizes certain content
- Companies often want to advertise a particular product not just their overall brand so it'd need a much more extensive database not just of brands but their products along with data on how to target each one.

I can imagine a Giphy-like product succeeding sometime in the future but probably not now. Alternatively if someone creates a "killer app" for ordinary consumers in the GenAI space, I imagine someone will try to include ads eventually. It wouldn't surprise me if someone tries it with ChatGPT but the thought is too unsettling for me to prototype.

### The End

Thanks for reading, and thanks again to Matt, Matt, and Mark for participating!

### Links

- [The code](https://github.com/ktrnka/branded-image-gen-service)
- [Dump of the generated images and SQLite DB containing prompts/settings](https://drive.google.com/file/d/1-X2lDPDhcH6zjt7o5XpqxLk6aViH-MAJ/view?usp=sharing) (350mb): This is a dump of my local folders, which has all the local testing I did and most of the Slackbot results. Take a look over the code for the table/column names. The images are all plain files, but I goofed by saving the DALL-E ones as PNG instead of JPG so the download is bigger than I'd like.
