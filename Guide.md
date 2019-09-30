# A Guide to Keg's Raw Source

Hello, Traveller! I see you are inspecting the source code for Keg (otherwise, you probably wouldn't be reading this). To an outsider, this may seem like a huge mess of files -- and it kind of is. But, don't fear, for I shall (hopefully) enlighten you about what each file does and how they all interact, bringing you inside the Keg experience!

## Keg.py vs OldKeg.py: Which One do I Use?

The first thing you may have noticed about this repo is that there are _two_ interpreters: `Keg.py` and `OldKeg.py`. This is because of the change from Keg being an interpreted language to a transpiled language (i.e. Keg is converted to Python and `exec()` is called on the resulting code). Contained within `Keg.py` is the shiny new transpiler, which has _probably_ fewer bugs than `OldKeg.py`. Consequently, it is recommended that you use `Keg.py` to run your Keg programs, as it is the program that is now maintained.

`OldKeg.py` contains the old interpreter, which, although being the cornerstone of the Keg language for most of the previous year (2018-2019), is somewhat buggy as well as hard to maintain. Indeed, fixing bugs and making everything work when what was really happening was hidden away in abstracted layers of "Tokens" just wasn't working anymore.

In summary, use `Keg.py` if you want a smooth execution of your program and use `OldKeg.py` if you are feeling adventurous.

## The Keg Chain

This section will attempt to explain how the transpiler turns Keg source code into tokens and then into python through exploring the different files involved in the process.

### preprocess.py

This is the very first file that Keg source code flows through in order to be turned into a readable output. In here, sequences found within the Standard Sequence Library (SSL) are injected into places defined by the `₳` keyword. It takes input into `process()` as a string and returns another string filled with SSL sequences.

However, there is another process occurring here: `balance_strings`: in order to allow for programs to have strings autocompleted, string symbols (the backtick, `¶‘“«„`) are matched in a LIFO manner. This has to be done somewhere before the next step (uncompressing of strings), meaning that is has to be done here.

### uncompress.py

This is the second file that Keg source code flows through in the pipeline of execution. Within `uncompress.py`, the code goes through `Uncompress()` first, which turns every single string contained in the source and turns it into the standard string (the backtick string), while substituting String Compression Codes (SCCs) with words found in Keg's dictionary. Strings are passed to `to_standard()` in order to make `Uncompress()` modular.

### Parse.py

This is the most important part of the execution pipeline: here, source code (at this point, still a string) is turned into mini tokens ready for the transpiler to turn into Python. It was this functionality that took me the longest to complete, as there was lots of testing, retesting, breakage of everything and more. What's important to note here is that without this file, nothing would work.

### Keg.py (or OldKeg.py)

Now that the code has been turned into tokens, it is ready for transpilation/interpretation. In `Keg.py`, the tokens are systematically turned into Python statements that `exec()` can use. In `OldKeg.py`, the tokens are interpreted line by line.

That concludes the Keg chain. It's not much, I know, but I feel that's all that is needed for an understanding of how the pipeline works.

# MORE COMING SOON #
