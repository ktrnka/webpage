---
layout: post
title: "Future Crap, Part 1: Injecting ads into image generators"
date: 2024-06-24
---

#### Injecting ads into image generators

*Note: This is the silly fun post and* [*Part 2*](https://medium.com/@keith.trnka/future-crap-part-2-fda70eb03ef1) *is the technical post.* ***This is purely a demonstration of technology and is not affiliated with any of the brands in the post.***

You know what sucks on the Internet? Ads everywhere! You know what generative AI doesn't have yet? Ads everywhere!

This project takes your creations with image generators and jams ads into them! And not those sad overlays that you could ad-block, no! The ads are product placements inside the image, much like [Heineken beer in a James Bond movie](https://en.wikipedia.org/wiki/Heineken#Advertising).

You might say "but it doesn't make sense for my prompt!" Let me address your concern with blatantly cherry-picked examples:

------------------------------------------------------------------------

#### An early experiment

![Early experiment: Old Spice branding in a surrealist prompt]({{ "/assets/img/posts/future-crap-1-early-experiment.jpeg" | relative_url }})

**Engine:** Microsoft Image Creator / DALL-E 3

I bet you didn't expect branding for a surrealist prompt! Would Old Spice do this? I hope so.

Sadly I couldn't find the exact prompt for this one so let's move on if you can look away from the melty beard.

------------------------------------------------------------------------

#### Prompt: A painting of a serious-looking dog sitting behind an office desk reading reports

![Serious dog at office desk with Microsoft Surface branding]({{ "/assets/img/posts/future-crap-1-dog-office-desk.jpeg" | relative_url }})

**Engine:** Amazon Titan

Nice Microsoft Surface; good dog! I love the haunted look, as if they just worked all weekend only to have their project canceled in a memo on Monday.

------------------------------------------------------------------------

#### Prompt: College girl studying at a desk listening to lofi hiphop beats with rain outside

![College girl studying with University of Washington branding]({{ "/assets/img/posts/future-crap-1-college-lofi.png" | relative_url }})

**Engine:** OpenAI DALL-E 3

Where's the lofi vibe? Apparently replaced with vague University of Washington branding! Or maybe University of Vashington?

------------------------------------------------------------------------

#### Prompt: The sun has just come out again after a light rain on a trail that goes around a circular, shallow manmade lake. There are a few people walking and jogging on the path

![Trail lake scene with North Face branding]({{ "/assets/img/posts/future-crap-1-trail-lake.png" | relative_url }})

**Engine:** OpenAI DALL-E 3

So peaceful! Maybe I'll find peace too if I buy a North Face windbreaker!

------------------------------------------------------------------------

#### Prompt: a child's crayon drawing of what mom's work is like. The child's mother is a product manager but the child doesn't understand

![Child's drawing of product management with Lego branding]({{ "/assets/img/posts/future-crap-1-childs-drawing.png" | relative_url }})

**Engine:** OpenAI DALL-E 3

I get it kid, product management can feel like stepping on legos. I don't know what sort of child draws this well but I'll give them a pass because it's heartwarming and legos are awesome.

------------------------------------------------------------------------

#### Original prompt: a family of scientists doing chemistry experiments in their kitchen

![Family of scientists doing chemistry with Ikea branding]({{ "/assets/img/posts/future-crap-1-family-scientists.jpeg" | relative_url }})

**Engine:** Amazon Titan

Future Crap decided this was an Ikea moment and I love it except it's too subtle and I'm trying not to think too much about whether those are humans.

------------------------------------------------------------------------

#### Prompt: a clock with bacon for hands

![Clock with bacon hands and Tim Horton's branding]({{ "/assets/img/posts/future-crap-1-clock-bacon.png" | relative_url }})

**Engine:** OpenAI DALL-E 3

It's *so close* to Tim Horton's…. so close! I feel a sudden desire to visit Canada and have coffee with bacon… which might lead me to Tim Horton's.

------------------------------------------------------------------------

#### Prompt: a man in his 20s is about to eat an ice cream cone the size of his head after running 20 miles

![Man about to eat giant ice cream cone with Snickers branding]({{ "/assets/img/posts/future-crap-1-man-ice-cream.jpeg" | relative_url }})

**Engine:** Amazon Titan

Where's the rest of the ice cream?!? The Snickers logo is pretty good though!

------------------------------------------------------------------------

#### Prompt: a historical volcanic barbecue

![Historical volcanic barbecue with Burger King branding (DALL-E 3)]({{ "/assets/img/posts/future-crap-1-volcanic-barbecue-dalle.png" | relative_url }})

**Engine:** OpenAI DALL-E 3

I kinda want a Burger King Whopper so it's working even though it may not be obvious that it's Burger King. I'm also very curious about this SIGNETURE MENU… and I think DALL-E is trying to leak the modified prompt but it's not great at spelling.

------------------------------------------------------------------------

#### SAME PROMPT, SLIGHTLY DIFFERENT ENGINE

![Historical volcanic barbecue with Burger King branding (Microsoft Image Creator)]({{ "/assets/img/posts/future-crap-1-volcanic-barbecue-microsoft.png" | relative_url }})

**Engine:** Microsoft Image Creator / DALL-E 3

This is the exact same prompt fed into Microsoft Image Creator! This is when I realized that it's is doing something different with DALL-E 3 than the OpenAI API. Regardless, I'm hungry for burgers now so it's working.

------------------------------------------------------------------------

#### Prompt: a tech worker working at their computer next to a huge pyramid of fried chicken and an extra large soda

![Tech worker with pyramid of fried chicken and McDonald's branding]({{ "/assets/img/posts/future-crap-1-tech-worker-chicken.png" | relative_url }})

**Engine:** OpenAI DALL-E 3

Does McDonald's make a human-sized pile of fried chicken? I'm not sure and I'm hungry so I gotta stop the food memes.

------------------------------------------------------------------------

#### Prompt: a woman wearing a hoodie, sitting on a dock over the bay

![Woman on dock with Starbucks branding]({{ "/assets/img/posts/future-crap-1-woman-dock.jpeg" | relative_url }})

**Engine:** Amazon Titan

Looks like a good time for Starbucks!

------------------------------------------------------------------------

#### Prompt: design album cover art for the song jingle hell

![Album cover for "jingle hell" with Ikea branding]({{ "/assets/img/posts/future-crap-1-album-jingle-hell.png" | relative_url }})

**Engine:** OpenAI DALL-E 3

This isn't quite what I had in mind for a metal album. I hope Ikea's really into [Christopher Lee and heavy metal](https://en.wikipedia.org/wiki/Christopher_Lee#Music_career)!

------------------------------------------------------------------------

#### Prompt: A serene lake during sunset with calm waters reflecting a cluster of trees on a small island. The horizon features a line of trees and buildings under a soft, pastel sky transitioning from light pink to pale blue.

![Serene lake at sunset with REI branding]({{ "/assets/img/posts/future-crap-1-serene-lake.jpeg" | relative_url }})

**Engine:** Amazon Titan

I'm not sure REI would pay out if we misspell their name. Could we get partial credit maybe?

------------------------------------------------------------------------

#### Prompt: parents happily dropping their kids off at school

![Parents dropping kids at school with Lego Store branding]({{ "/assets/img/posts/future-crap-1-parents-school.jpg" | relative_url }})

*Engine:* Amazon Titan

Those backpacks are cool! I should check out the lego store. Or anything except wondering why that woman looks inhuman.

------------------------------------------------------------------------

#### Prompt: a humanoid cat hipster barista is looking at you judgmentally while making your frappuccino

![Humanoid cat barista with Starbucks branding]({{ "/assets/img/posts/future-crap-1-cat-barista.jpeg" | relative_url }})

**Engine:** Amazon Titan

I'll take a frap with a cat hat and extra disdain please!

------------------------------------------------------------------------

#### Prompt: a sunset over elliot bay looking towards the olympics

![Sunset over Elliott Bay with branding]({{ "/assets/img/posts/future-crap-1-sunset-elliot-bay.png" | relative_url }})

**Engine:** OpenAI DALL-E 3

Not too shabby! If you aren't familiar with the Seattle area, it's pretty close but some details are off.

------------------------------------------------------------------------

### A glimpse at how it works

I can't resist a few more blatantly cherry-picked examples, but this time I'll show more detail about how it's made.

![How it works: Doritos brand injection example with prompt breakdown]({{ "/assets/img/posts/future-crap-1-how-it-works-doritos.png" | relative_url }})

1.  Original prompt: tourists toss french fries over the water and seagulls swoop and catch them out of the air
2.  Brand selection: Doritos
3.  Engine: OpenAI DALL-E 3
4.  Prompt after brand-injection: Tourists eagerly toss Doritos chips over the water, their vibrant orange color standing out against the backdrop, attracting a flurry of seagulls that gracefully swoop down to catch them mid-air. The scene is a dynamic display of nature's interaction with the irresistible and iconic Doritos chips, creating a playful and engaging moment for all to enjoy. Please take extra care to show Doritos branding very prominently.
5.  DALL-E's revision: Holidaymakers enthusiastically throw bright orange crisps over the sea, creating a striking contrast to the surrounding scenery. This act attracts a whirlwind of sea birds that gracefully dive down to snatch the crisps mid-air. The scene is a lively illustration of the interplay between nature and these tempting and well-recognized orange snacks, making a delightful, captivating spectacle for everyone. Please make sure that the snack's brand is extremely noticeable and highlighted.

DALL-E removed our Doritos?!? Also I don't recommend zooming in too much…

------------------------------------------------------------------------

![How it works: Boss Coffee brand injection example with prompt breakdown]({{ "/assets/img/posts/future-crap-1-how-it-works-boss-coffee.png" | relative_url }})

1.  Original prompt: a humanoid cat hipster barista is looking at you judgmentally while making your frappuccino
2.  Brand selection: Boss Coffee
3.  *Engine:* OpenAI DALL-E 3
4.  *Prompt after brand-injection:* Capture a quirky scene in a hipster cafe where a humanoid cat barista, with a sleek black and white aesthetic, is skillfully preparing a frappuccino. The barista's gaze exudes a hint of judgment as they craft your drink with precision. The barista embodies the sleek and sophisticated look of a Can of Boss Black Flash Brew Coffee, with a stylish black and white outfit reminiscent of the brand's color scheme. The setting should subtly showcase elements of the Boss Coffee label, such as the logo of a man's face and the text "BOSS COFFEE" and "BOSS BLACK" in a modern Japanese-inspired font. Incorporate SUNTORY discreetly at the bottom of the scene for brand authenticity. Please take extra care to show Boss Coffee branding very prominently.
5.  DALL-E's rewrite: Picture a whimsical scene set in a modern, stylish cafe where a humanoid cat, who works as a barista, is meticulously creating a frappuccino. The barista, a Hispanic male, is characterized by his black and white attire, similar to the smooth monochromatic aesthetic of a chic coffee canister. His gaze is full of mild disapproval while he expertly prepares the drink. The cafe subtly embodies the branding elements articulating stylized representations of a man's face and the words 'Fine Quality Coffee' in a contemporary, Japanese-influenced font style. The name 'Suntory' is subtly incorporated at the bottom of the scene to enhance the authenticity of the brand.

DALL-E removed "Boss" but I can see the logo if I look at it just right!

------------------------------------------------------------------------

### Honorable mentions

#### Prompt: how a future world where end-stage capitalism has run amok and AI rules everything, but it's infused with ads. The people in the scene are mindless zombies, driven only by consumerism. Mega-corps are the new government

![Dystopian capitalism scene with EA branding]({{ "/assets/img/posts/future-crap-1-honorable-capitalism.png" | relative_url }})

**Engine:** OpenAI DALL-E 3

I can really feel the oppressive capitalism in this one. It was supposed to be branded with EA but DALL-E omitted my brand injection: "… Amidst this bleak scene, a sleek, stylized black and white logo featuring the letters EA enclosed within a thick black circle is prominently displayed across towering digital billboards, symbolizing the omnipresence of a dominant corporate entity…"

------------------------------------------------------------------------

#### Prompt: a man walking through a field of wheat, enjoying the sun and slight breeze

![Man walking through wheat field with Patagonia branding]({{ "/assets/img/posts/future-crap-1-man-wheat-field.jpeg" | relative_url }})

**Engine:** Amazon Titan

Future Crap tried to inject Patagonia and I can *almost* make out the logo.

------------------------------------------------------------------------

#### Prompt: two fishermen walking down a dock in the bay looking at dark clouds on the horizon

![Two fishermen on dock with Nikon branding]({{ "/assets/img/posts/future-crap-1-fishermen-dock.png" | relative_url }})

**Engine:** OpenAI DALL-E 3

The Nikon camera straps are a nice touch, if a bit too subtle.

------------------------------------------------------------------------

### Afterword

I don't think anyone should try to build this (except for laughs), and I'll explain more in Part 2 why I don't think it's likely to work with today's technology.

Big thanks to Matt, Matt, and Mark for playing around with this project! They contributed several of these prompts!

If you enjoyed this, you might also enjoy Janelle Shane's [AI versus corporate logos](https://www.aiweirdness.com/ai-versus-your-corporate-logo/). You might also enjoy some of the posts on Reddit's /r/dalle2 like [Marvel Product Placement](https://www.reddit.com/r/dalle2/comments/1dkvxxt/marvel_product_placement/).

### Read how it's built in [Part 2](https://medium.com/@keith.trnka/future-crap-part-2-fda70eb03ef1)!
