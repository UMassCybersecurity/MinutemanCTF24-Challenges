description = '''Welcome to the world of Hofstadter, where Achilles and the Tortoise are in an inception nightmare. 
Can you help them out?

--------

Achilles and the Tortoise start on floor 1. 
Periodically, an "inception" occurs, consisting of pops and pushes. 
Each pop sends the duo up a floor and each push sends them down a floor. 
If there was only one push or pop, they can tell how many happened and which one it was.
In general, the pops and pushes happen so fast that it's hard for the duo to tell how many of each happen or the the order they happen in.
However, they duo can generally pick out how many total pops and pushes happen during each inception event. 
After the inception event occurs, you are given a description of the floor that they land on. An example is:

    Inception: Tortoise could pick out 7 pops and pushes total. 
    A painting depicts them standing in front of the very painting they're observing, infinitely nesting their images.

Throughout each game, each floor will always have the same story, so if you land on the same floor twice you get the same description. 
However, if you connect to the game multiple times, some of the floors might shuffle around. 
There are 100 floors total: from floor 1 you must push, and from floor 100 you must pop.

Achilles and the Tortoise carry 4 tops with them, numbered 2, 3, 5, and 7. 
Each time they land on a floor they spin all four tops. 
If the tops seem to spin indefinitely, the current floor number is divisible by that top's labeled number. 
If the top stops spinning then the current floor number is not divisible by that top's labeled number. 
For example, if I am on floor 12, tops 2 and 3 will keep spinning, and tops 5 and 7 will stop.

Every so often, Hofstadter will ask you what floor you are on. 
If you are right five times in a row, he'll set the duo free. 
If make 5 incorrect guesses in total, he locks the duo away forever (and you disconnect from the game).
Can you save them?
'''

first_floor = "This is the first floor. Achilles chases the Tortoise up an infinite Escher staircase that loops back to the start; each step defies gravity and logic."
last_floor = "They step into a room labeled \"Exit,\". This is the last floor."

floors = [
    "They enter a room where every book contains a story about them entering a room with books about themselves.",
    "The Tortoise hands Achilles a map that's a perfect replica of the territory, including themselves studying the map.",
    "A paradoxical mirror reflects everything except those looking into it, leaving Achilles and the Tortoise perplexed.",
    "They find a note stating, \"The statement on the other side of this paper is true,\" which leads to the other side saying, \"The statement on the other side of this paper is false.\"",
    "Achilles and the Tortoise debate with a sign that reads, \"Don't read this sign,\" causing an endless loop of confusion.",
    "A painting depicts them standing in front of the very painting they're observing, infinitely nesting their images.",
    "The Tortoise challenges Achilles to a race where every time he catches up, she moves ahead by half the remaining distance.",
    "They enter a hall of endless doors; opening one just leads to another identical door, ad infinitum.",
    "A musical fugue plays where the melody chases itself backward and forward, much like their own conversations.",
    "The duo finds a dictionary where words are defined using only each other, trapping them in circular definitions.",
    "They step into a Möbius strip pathway that twists their perspective, making left become right and back again.",
    "A paradox machine asks them to \"Ignore this instruction,\" leaving them in a quandary.",
    "Achilles reads a scroll that contains every possible scroll, including the one he's holding.",
    "The Tortoise presents a box labeled \"Do not open,\" which, when opened, contains a note saying \"Do not open.\"",
    "They find a staircase that descends infinitely yet brings them back to their starting point.",
    "A room contains an infinite number of monkeys typing; one hands them a script of their current adventure.",
    "The walls are covered with the sentence \"This sentence is false,\" causing reality to waver.",
    "Achilles sketches a hand drawing itself, which in turn is drawing another hand, spiraling endlessly.",
    "The Tortoise shows a photograph where they are posing with the photograph itself, looping infinitely.",
    "They engage in a conversation that keeps referring back to itself, never progressing forward.",
    "A door requires a password that is the name of the password itself, locking them in a logical loop.",
    "They encounter a creature that tells only lies but insists, \"I am lying right now.\"",
    "The Tortoise hands Achilles a book titled \"How to Read This Book,\" which is blank inside.",
    "A sign reads, \"The next floor is the previous floor,\" trapping them in an endless ascent.",
    "They find a set of nesting dolls where each doll is larger than the last, defying physical space.",
    "Achilles tries to catch a shadow that anticipates his every move, leading him in circles.",
    "The Tortoise solves a puzzle that changes its rules every time she makes a move.",
    "They walk through a garden where paths split endlessly, each choice leading to more choices.",
    "A musical note plays continuously, rising in pitch yet never actually getting higher—a sonic paradox.",
    "They discuss a barber who shaves everyone who doesn't shave themselves; the barber's own shaving habits perplex them.",
    "Achilles opens a book that tells the story of him opening the book, caught in narrative recursion.",
    "The Tortoise points out a cloud shaped exactly like themselves pointing at a cloud.",
    "They find a door that says \"This door is locked,\" but the lock is on the floor above.",
    "A room filled with mirrors reflects not their images but their thoughts, revealing hidden truths.",
    "They enter a library containing all possible books, including one predicting their every action.",
    "Achilles reads a letter that informs him he's currently reading the letter, creating a loop.",
    "The Tortoise demonstrates a machine that prints out statements that are only true if the machine doesn't print them.",
    "They stumble upon a musical score that plays itself when looked at, the notes dancing off the page.",
    "A paradoxical elevator takes them to every floor except the one they're on.",
    "They debate a river that they cannot step into twice because both they and the river are ever-changing.",
    "The Tortoise reveals a painting that, when stared at, begins to include the viewer within its scene.",
    "They meet a man who says he always lies and then declares, \"I am lying now.\"",
    "A labyrinth reconfigures itself based on the choices they haven't made yet.",
    "Achilles and the Tortoise find a script where their lines appear just before they speak them.",
    "They find a compass that always points away from their destination, leading them in circles.",
    "A message reads, \"To understand this message, you must first understand this message,\" leading to infinite contemplation.",
    "They encounter stairs that go nowhere yet everywhere, bending space into impossible shapes.",
    "The Tortoise hands Achilles a never-ending story that concludes on the next page, which doesn't exist.",
    "They discuss a set that contains all sets that do not contain themselves, questioning if it contains itself.",
    "A fountain flows upward, defying gravity and their understanding of physics.",
    "The walls display an equation that solves itself only when not observed.",
    "They engage with a chatbot that responds before they type, predicting their thoughts.",
    "A door requires them to prove they exist before it opens, posing a philosophical challenge.",
    "They find a musical instrument that only plays silence unless no one is listening.",
    "The Tortoise shows Achilles a circle with a beginning and an end, sparking debate.",
    "They encounter an artist painting a portrait of the artist painting a portrait, layers upon layers.",
    "A hallway twists into a Möbius strip; walking forward flips them upside down.",
    "They see a sign that says, \"The opposite of this statement is false,\" leaving them pondering.",
    "The Tortoise explains a theorem that proves itself unprovable, causing a logical meltdown.",
    "Achilles drinks from a cup that refills itself only when emptied.",
    "They discuss whether a heap of sand loses its \"heapness\" when grains are removed one by one.",
    "A hologram displays a smaller hologram of itself infinitely, capturing them in light.",
    "The Tortoise offers a box that contains everything except itself.",
    "They step into shadows that cast their own objects, reality flipping on its head.",
    "Achilles writes a sentence that reads, \"This sentence will self-destruct when read,\" and it vanishes.",
    "A clock ticks backward, measuring time that unravels as they watch.",
    "They find a key that unlocks every door except the one it came from.",
    "The Tortoise recites a poem that never ends yet fits in a single breath.",
    "They enter a gallery where each artwork includes the viewer as part of its composition.",
    "A paradoxical plant grows smaller as it ages, blooming into a seed.",
    "They debate if an unstoppable force meeting an immovable object could ever occur.",
    "Achilles reads a warning that warns about itself, spiraling into self-reference.",
    "The Tortoise shows him a quine—a program that outputs its own code when run.",
    "They find a musical note that harmonizes with the silence around it, creating audible silence.",
    "A riddle asks, \"What is the sound of one hand clapping?\" and the silence answers.",
    "They walk into a paradoxical shop that sells items only to those who don't want to buy them.",
    "The Tortoise demonstrates a set of scales that balance only when unequal weights are placed.",
    "Achilles tries to read an invisible book written in visible ink.",
    "A hallway stretches infinitely yet brings them back to where they started after a few steps.",
    "The Tortoise poses a question that cannot be answered without contradicting itself.",
    "They step into a room where every truth is false, and every falsehood is true.",
    "Achilles and the Tortoise see their lives played out on a stage, actors mimicking their every move.",
    "A message appears saying, \"Delete this message,\" but they can't decide whether to obey.",
    "They encounter a chameleon that becomes the color of invisibility when observed.",
    "The Tortoise reads a letter that erases itself after being read, leaving no trace.",
    "A room contains a replica of itself, which contains a replica of itself, and so on.",
    "They discuss the concept of infinite hotels with no vacancies yet infinite rooms.",
    "Achilles writes a note that says, \"The Tortoise will not read this,\" as she reads over his shoulder.",
    "They find a paradoxical painting that is complete only when unfinished.",
    "The Tortoise hands Achilles an envelope that, when opened, seals itself again.",
    "They debate whether the act of forgetting can be remembered.",
    "A staircase descends into the ceiling and ascends into the floor, twisting architecture.",
    "The Tortoise gives Achilles a candle that burns only in the dark.",
    "They walk through a doorway that leads to itself, endlessly looping.",
    "A note reads, \"This is the last floor,\" but floors continue beyond.",
    "The Tortoise smiles and says, \"We've been here before,\" and they realize they never left the first floor (or have they?).",
    "Achilles notices the journey itself is the destination, completing their paradoxical adventure?",
]
