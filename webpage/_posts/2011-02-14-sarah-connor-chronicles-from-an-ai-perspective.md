---
layout: post
title: Sarah Connor Chronicles from an AI Perspective
date: 2011-02-14
---

A bit of departure from my usual, but I thought it'd be interesting to review Terminator:  Sarah Connor Chronicles from the perspective of an AI researcher. I'll go through the first season in this post and the second season at another time.

That said, artificial intelligence is a large field. My focus is natural language processing and (to a lesser extent) machine learning, though I also have experience with multi-agent systems and searching.

There's a very clear separation between perception and reality of AI. Popular perception is that we're trying to imitate humans and build machines that can perform general-purpose reasoning and learning. General-purpose reasoning is generally avoided because of the need for a large knowledge base. In contrast, most AI courses focus on searching (even in reasoning problems). If a problem is too difficult or dynamic for a normal computer program, we represent it as an exploratory process and try to find the best sequence of actions possible.

I'll format this as relatively chronological notes for each episode and I'll try to limit my comments to CS/AI/HCI.

Background

If you didn't watch the series but wanted to follow along, here's the short version of the background.

* Sarah Connor - human survivor of numerous attacks by terminators attempting to prevent John Connor (her son) from living and/or becoming humanity's leader in the future.
* John Connor - teenage version of John Connor, humanity's future salvation. Good with technology.
* Cameron - reprogrammed terminator sent from the future (by the future John Connor) to protect John
* Chromartie, Vick - terminators sent from the future to kill John or ensure that SkyNet is created.
* Andy Good - develops a chess-playing computer called the Turk, which they suspect will become SkyNet.
* Essential plot - Sarah, John, and Cameron jump from 1999 to 2007 in the first episode. Then they focus on the dual issue of surviving and preventing the creation of SkyNet.

Episode 1:  Prologue

* The iconic stiff walk of the Terminator in Sarah's dream seemed odd to me.  I have a hard time believing that it's so difficult to imitate any involuntary movements during a human's walk.  But they have to provide a visual cue for the machines. Without that, it'd be like Battlestar Galactica.
* When chasing John, Chromartie switches to infrared at some point.  Realistically, a good machine would use both visible spectrum and IR at the same time.
  + For reference in the real world, see [DoDaam's Super aEgis II](http://www.gizmag.com/korea-dodamm-super-aegis-autonomos-robot-gun-turret/17198/), which is an autonomous turret that "can find and lock on to a human-sized target in pitch darkness at a distance of up to 1.36 miles".
* Voice imitation is interesting. But the way it's done is overly futuristic. For one, the machine hasn't even heard every [phoneme](http://en.wikipedia.org/wiki/Phoneme) out of Sarah Connor. Even if you hear all the phonemes, the speech you can generate is very artificial. Then even if you hear the person say every word in the English language, you can't produce natural speech just by playing them back. It's an incredibly complex process.
  + Some of my friends at [AgoraNet](http://www.agora-net.com/) work in speech synthesis for the ModelTalker project, trying to imitate people's voices from samples. They can do reasonably well, but you need more than just a couple of sentences.
* Cameron quickly understood the analogy "put those back in the holster" to mean "put your bra on". Analogies are very difficult to process and it stands out even more when she struggles with other analogies.
  + The only thought I have of potentially interpreting that with software is plan recognition, but it's a stretch. There are just so many other possible meanings:
    - holster your firearms
    - put your {socks, shoes, gloves, earmuffs} on

Episode 2:  Gnothi Seauton
--------------------------

* Cameron doesn't understand when Sarah calls her "tin man". If you're thinking about current NLP algorithms it makes some sense. The most basic processing for coreference resolution is agreement: matching number (singular/plural) and gender. Would she have understood "tin woman" more or less? I'd guess more, cause she's the only other female in the room. Though we don't have robust algorithms that'd link "tin woman" to the tin man in Wizard of Oz so she would miss the implication that she's missing a heart.
* John's experience in the store 1337 was a bit out of place.
  + After using the computer, a girl shows him how to clear his browser history for privacy. We could do that in 1999; John would've known. I find it strange that she doesn't have him clear the browser cache or form field completions (which might have his query).
* Cameron detects John's irregular pulse/etc from touching his skin, but fails to notice grass on his shoes and avoiding eye contact. For one, I have a hard time believing that a "perfect AI" would consider that unimportant. Reasoning from "grass on shoes" to "went outside" might actually be a nice example for an AI class on temporal logic.
  + Secondly, we have a case of mismatched futurism here. MIT has already [detected heart rate using computer vision](http://www.opticsinfobase.org/abstract.cfm?uri=oe-18-10-10762). Vision alone! I'll give the writers leeway because I don't think anyone had tried it in 2008.
  + I linked the paper but there's a YouTube demonstration that I can't seem to find anymore.  (Send me a link if you find it and I'll put it here)

Episode 3:  The Turk
--------------------

* Andy claims that his Turk can beat every human player that has ever lived and ever will live. Does he mean beat everyone 100% of the time? That's a bit of a stretch. 51% of the time or more? That's not as impressive. Additionally, it's not verifiable. It just doesn't have the feel of something most researchers would say.
* Andy says that the AI chess platform is very valuable for AI developers. I agree. Chess is interesting, easy to understand, and difficult but not too difficult.
* When Sarah returns home from seeing the Turk for the first time, John asks her what it looks like and some properties:
  + obvious network access?  what sort of bandwidth?
    Access to the Internet is a poor gauge of chess-playing AIs. It's not like they're reading books online or processing text. You might want Internet access to play opponents remotely, but that's not much bandwidth.
  + power supply?  cooling?
    This is at least in the right direction. In general, a machine capable of more computations per second will require more power and thus generate more heat (all other things equal). Heating is big deal in high-performance computing. If the HVAC system goes down in your server room, you have to take most of the servers down to prevent heat damage. I'm a little surprised John didn't ask if it was loud or not - stronger cooling usually means huge or noisy fans. That said, it's only a loose measure. Older systems perform less computation per watt and generate more heat to do the same amount of work, so it would be difficult to tell the difference between modern hardware and old hardware.
* At this point, I want to clarify that chess-playing AI is typically an implementation of a [minimax](http://en.wikipedia.org/wiki/Minimax) search, which is a general method that can be applied to most kinds of turn-taking game playing (though you have to do quite a lot of game-specific coding). Minimax search is basically a simulation of the game. You pick the best move assuming that your opponent will pick the best move for your (recursive) best move and so on. The recursion ends on winning or losing moves.
  + You can't simulate the entirety of the game in the time limit for each move. So instead you need to set the search up to stop at a certain depth (or some other sort of threshold). Those remaining unexplored states of the board need to have some "goodness" value though, so you write non-recursive heuristic functions. These are ways of evaluating goodness without considering the next move and can be learned by precomputing exhaustive simulation and storing on disk. Or you can develop heuristic functions with machine learning. There are probably many types; heuristics don't have to be exact.
  + I just want to point out that chess-playing algorithms are usually incremental improvements on the standard minimax search with pruning and heuristics. Chess-playing improves because better hardware allows for deeper searches, we develop better heuristics, and we find better ways to prune the search (see [alpha-beta pruning](http://en.wikipedia.org/wiki/Alpha-beta_pruning)). Minimax search isn't general-purpose reasoning or learning like the series suggests.
* Cameron has an interesting conversation with a girl in the bathroom.  The girl says "It's so freaking big and right out there!" and Cameron responds in monotone, "It's freaking big". At the time, this gave me a strong impression of the [ELIZA](http://en.wikipedia.org/wiki/ELIZA) chatbot from the 60's, which used basic regular expressions to provide an imitation of a therapist.
* Andy says "I've got the guts of 3 xboxes and 4 playstations daisy-chained". The idea of daisy-chaining doesn't make sense in this context. You would instead want to have them running in parallel rather than as a pipeline. That aside, I believe the PS3 guts are much more common in high-performance computing than the 360. Part of the benefit of using consoles for HPC is that the PS3 and Xbox 360 are heavily subsidized:  Sony and Microsoft expect to make back the money on game licenses so the hardware is discounted.
  + Also note that it's a huge pain to develop a system that uses different architectures.
  + A modern researcher might instead use a bunch of cheap computers with high-value video cards. [GPGPU](http://en.wikipedia.org/wiki/GPGPU) programming is excellent for parallel problems and the hardware is generally much stronger than CPUs at the same cost/release date (only for parallel problems).
* "Turk has moods". Although I won't say that "moods" are possible, what Andy says about it solving problems differently at different times is possible. The chess software isn't the only software running on those computers and the search is time-limited. If some background process needs to run one time but not another, the minimax search may progress to different depths. It's a stretch to say that it would completely change the strategy, but it's at least conceivable.

Episode 4:  Heavy Metal
-----------------------

* Image enhancement isn't really possible like on TV. There's a great xkcd about this (but I can't find it atm). It's only possible at very limited amounts of improvement and relies on knowledge of the type of noise in the image or knowledge of the original image.
* A phone falling from maybe three feet in a cargo van is really unlikely to shatter a screen. Granted we have some amazing screens in smartphones nowadays. Also, breaking the screen isn't a good indication of damage to the GPS circuits (or whatever they're tracking him with).
* Tracking a phone online is something you have to give artistic license for. It's not easily possible without installing an app, but the technology is all there to do it either by GPS or triangulation from cell towers when multiple are in range (but that isn't easy). Theoretically you could probably do it from a single tower if you're restricting it to roads, though that requires reasoning.
* The idea of sleeping machines seems a bit overdone. Consider your laptop. Modern CPUs downclock themselves to match your current usage and they save a huge amount of battery life in the process. But it's not necessary to sacrifice reaction time to the degree we saw in the show. Even still, it'd be just as easy to process audio or video data and can be done with low power draw. (Such as the neural networks used to drive cars in the 90s)

Episode 5:  Queen's Gambit
--------------------------

* The Russian guy "taught" the Turk to play chess. This doesn't make a lot of sense from an AI perspective. Perhaps he could train the Turk's machine learning heuristics (if it would even need that). Even still, it's easier to just have the Turk run two processes and play itself.
* I'm just going to say that *firewall* means something different in movies and TV. The pro wrestling term *kayfabe* is applicable here.
* At some point, Cameron asks if the guidance councilor means:
  + Are you asking if people say X?
  + Are you asking if X is true?
  + This is pretty good from an NLP perspective. Work on indirect questions and answers is close, but requires some understanding of the person's potential goals. In this case, Cameron doesn't understand his goals and so she can't choose. (That said, I'm sure statistical methods would show that usually people are asking if X is true)

Episode 6:  Dungeons & Dragons
------------------------------

* No comments.

Episode 7:  The Demon Hand
--------------------------

* No comments.

Episode 8:  Vick's Chip
-----------------------

* In buying a computer, the seller provides video throughput as a system spec. That doesn't make a lot of sense.
  + I know they have to entertain, but something like having a friend order from NewEgg would get more/better gear for less cost.
* John tries learning to access the Terminator's chip in this episode. There are many oddities about this.
  + Accessing the chip alone would be amazingly difficult unless he's lucky enough that they use a USB/FireWire/etc interface (which they wouldn't). For each pin, you need to decide its function. And without knowing the Terminators' architecture, that's inconceivable. Even after knowing what each pin does, you need to decipher the way that data and commands are sent. Even if you somehow knew the commands to send to access memory, you'd have to figure out how to decode it.
  + He starts with 2.5v initially but Cameron tells him it needs 6.2v-8.7v. It isn't the high voltage that really surprises me but rather the wide range. In CPU overclocking, sometimes you'd need to jack up the voltage a little to achieve the desired overclock, but it usually comes at the cost of some stability. That said, we're talking about very small increases in voltage.
  + The memory organization notes are strange. Storing by topic doesn't make a whole lot of sense if you think about memory as a fixed amount of space (as it is with computers). What you'd do instead is store chronologically and use topical index files. (If not stored chronologically, you'd have to shift memory to make room if you underestimated the amount of space needed, which is a slow process)
    - You can potentially make an argument for topical storage for increased video/audio compression, but it should be equally possible to store it all as one chronological "file" with indexing.
* The threat to humanity in this episode is ARTIE, which is a system of cameras for traffic control that may eventually become SkyNet's "ability to perceive". It's not clear what ARTIE actually does, but the episode suggests that it just controls traffic lights with cameras. That's not much different than the way traffic lights work.
  + It's also funny that they were concerned about the network of cameras, when that's pretty much the reality these days.
* *I'll make a virus to discredit ARTIE!* If it's a closed network, John has no way of knowing the way in which the system is controlled. His only hope is to blindly cause random network traffic to break the system, but it's far-fetched. I'll add *virus* to the list of specialized tv/movie terms like *firewall*.
* They infiltrate the control center and plug in a flash drive to mess up the system. There are so many things wrong with this. First, if it's a completely closed network and it communicates with traffic lights, it's easier to break into the network through a traffic light (which they eventually do). They could even hook up a small, low-power computer and leave it running in there, like the ones the size of an Ethernet jack.
  + I don't know about traffic light control, but I've been to a regional power control center. You have no hope of infiltrating such a place. And there are always people there.
  + There doesn't seem to be a screen lock on the systems. I find that unbelievable.
  + The system automatically starts running something on the flash drive. Any reasonably secure system would disable autorun, but then again people often value convenience over security.
* John feeds too much voltage to the chip and the Terminator takes over the computer and such. Then we hear a modem sound. WHAT? I don't even think kids these days know what the sound is from. And you'll have a hard time even finding a modem to buy, let alone prepackaged in a device.
  + John also has to turn off his cellphone. The only way I can conceive of the relevance is if John has bluetooth enabled on his phone and it auto-accepts connections. John is essentially a security expert so I find that a little tough to believe. Though he skipped from 1999 to 2007 so maybe there's a chance he doesn't know about bluetooth (but it's doubtful).
* I wrote down the phrase "her neural network". This is another rebranding of a word. The term [artificial neural network](http://en.wikipedia.org/wiki/Artificial_neural_networks) refers to a machine learning method that (somewhat) imitates the human brain. But it's only an approximation. A "neuron" in an ANN has an arbitrary number of inputs and one output. Real neurons have many outputs. The structure of the artificial neuron is restricted to things like a weighted sum of the inputs. The structure of the network is extremely limited - you can't have cycles in an ANN. You can only have so much interconnection going on. The most common form is a feed-forward network, which is really like using weighted sums hierarchically.
  + Beyond even the structure of it, neural networks are more setup for classification tasks than anything else.
  + I'm a fan of neural networks, so this usage is painful. It's bad enough to sacrifice words like firewall, hacking, virus, keylogger, etc.

Episode 9:  What He Beheld
--------------------------

* John gives a reasonable description of Moore's Law. It's been strangely accurate for ages.
  + Other formulations of Moore's Law were somewhat incorrect; for a while people said it was a doubling of clock speed, but we've stopped increasing clock speed for the most part.
  + John then says it's how we go from chess to SkyNet in 4 years. Hardware can only increase the speed of the software. It can't add new features. Due to the nature of a time-limited minimax search, you can provide better quality but not different kinds of reasoning without the software to do it.
* This quote kills me: "We know what the Turk looks like". The novelty of the Turk is software, not hardware. So you can make copies or whatever. Furthermore, the idea of trying to irrevocably destroy software seems absurd. There's always a backup somewhere.

summary
=======

The major offense is the idea that a chess-playing computer is designed for general-purpose reasoning and control. There are discrepancies with artificial intelligence and computer science in general, but they aren't too different than the movie/tv kayfabe of other fields.

For more information on chess-playing computers, I suggest *Artificial Intelligence:  A Modern Approach* by Russell and Norvig, Chapter 5. The end of the chapter has an excellent historical account of chess playing.

On a side note, I thought it was an excellent series. I'll take notes on season 2 when I find more time.
