# Foreword

## The Language and the Book

In December 1989, Guido van Rossum started a "hobby project" over the Christmas
holidays at Centrum Wiskunde & Informatica (CWI) in Amsterdam. He wanted a
successor to ABC, a teaching language he had worked on that was elegant but
too closed and too slow to extend. He named the new language after *Monty
Python's Flying Circus*, not the snake — the reptile logo came later, and
purely by adoption.

The first public release, Python 0.9.0, appeared in February 1991. It already
had exceptions, functions, and the core data types — `list`, `dict`, `str` —
that still anchor the language today. Van Rossum's design instinct was
consistent from the start: readability is not a nicety, it is the point.
Significant whitespace was not a gimmick — it forced every Python program
into a single, shared visual shape.

> *"There should be one — and preferably only one — obvious way to do it."*
> — Tim Peters, *The Zen of Python* (PEP 20)

Van Rossum served as "Benevolent Dictator For Life" for nearly three decades,
personally approving or rejecting language changes through the PEP (Python
Enhancement Proposal) process. He stepped back from that role in 2018; a
five-person steering council, elected annually by the core developers, has
governed the language ever since.

## The PEP Process

Python does not change by fiat. Every significant addition — f-strings
(PEP 498), the walrus operator (PEP 572), structural pattern matching
(PEP 634), the type hint system (PEP 484) — went through a PEP: a public
proposal, discussion, and a decision, all archived and readable today. PEP 8,
the style guide, and PEP 20, the Zen of Python, are themselves PEPs — the
language documenting its own values in its own process.

This openness is why Python could survive the hardest transition in its
history without fracturing.

## Python 2 and the Long Migration

Python 3.0, released in 2008, deliberately broke backward compatibility to
fix mistakes baked into the language early on — most visibly, making `str`
Unicode by default instead of bytes. The migration from Python 2 took over a
decade; Python 2 was not formally retired until January 2020. It was painful,
publicly debated, and occasionally bitter. It was also, in retrospect, the
right call: every exercise in this project runs on a language that no longer
carries the ambiguity between text and bytes that made Python 2 unicode
handling a recurring source of bugs.

## CPython and the GIL

The reference implementation, CPython, compiles source to bytecode and runs
it on a stack-based virtual machine written in C. Its Global Interpreter Lock
(GIL) — a single lock that lets only one thread execute Python bytecode at a
time — is the language's most debated implementation detail. It makes
reference counting cheap and the C API simple, at the cost of true
parallelism for CPU-bound threads. Exercise 27 (Threading) and Exercise 28
(Multiprocessing) exist specifically to teach *when* the GIL matters and what
to do about it: threads for I/O-bound concurrency, processes for CPU-bound
parallelism. PEP 703, accepted in 2023, charts a path to an optional
GIL-free build — proof the language is still willing to break its own old
assumptions when the case is strong enough.

## What This Project Is

These 33 exercises are a path from `print("Hello, World!")` to async event
loops, socket servers, and multiprocessing — the same territory covered by
`C_Programming` and `CPP_Programming`, reached by a language that trades
manual memory management and compile-time types for a garbage collector, dynamic
typing, and an enormous standard library ("batteries included," as van
Rossum put it). Every exercise runs cleanly under `ruff` with no warnings and
targets Python 3.11+, the version where exception groups, `tomllib`, and
faster CPython (PEP 659, the adaptive specializing interpreter) all landed.

The 22 topic reference sheets alongside the exercises exist because Python's
readability is a trap for the unwary: code that looks simple often hides a
subtlety — mutable default arguments, late-binding closures, `is` vs `==` —
that only becomes visible when it breaks in production. The pitfall tables in
each topic document those subtleties before they cost you a debugging
session.

> *"Explicit is better than implicit. Simple is better than complex.
> Readability counts."*
> — Tim Peters, *The Zen of Python*

Type `import this` into any Python interpreter. The whole philosophy is
nineteen lines long, and it still holds.
