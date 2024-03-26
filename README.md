# DM_Assignement1
Assignement 1 of DH-401 EPFL course

# Installation 

## Cloning

git clone --recursive https://github.com/JorisMonnet/DM_Assignement1.git

## Requirements

pip install -r requirements.txt

## Architecture

| task_a \
         | task_a_plotter.py -> Plotting the results from task_a
         | timing_for_one_piece.py -> Implementation of the timing function for one piece
         | timing_function.py -> Implementation of the timing function for multiple pieces
| task_b \
         | constants.py -> Constants used in the task_b
         | q1.py -> Analysis of the distribution of note onsets on metrical locations
         | q1b.py -> Analysis of the expressive timing
         | q2.py -> Analysis of the Pitches
| empirical_findings.ipynb -> Global notebook with all results and analysis

# Instructions:



<!-- # Group Project 1-3: Expressive performance 

In these three assignments, we apply the concepts learned in the class to generate expressive musical performance (in MIDI format) from symbolic score. 


- (The artistic approach) Students that has an artistic interest might spend more time on exploring how to create performance based on intuition and music theory/analysis and then subjectively reflect on the musical result.  

- (The scientific/engineering approach) Students with math/engineering background might spend more time on rigorous definitions, machine learning/exploratory data analysis, and quantitative evaluation.

Considering that the students are comming from a wide range of background, we welcome both approaches. 
 -->

# Assignment 1: Expressive Timing in Performance
###### (Due in two weeks)


In this assignment we explore the distortion of the metrical grid in human performance. Your task is to find a interesting mapping from symbolic time to real time. 
<!-- Your model should output a MIDI file with performance atributes (timing and dynamics). -->

<!-- Each group will use their model to ouput MIDI performance of Cello Suite No. 1 (BWV 1007) – Prelude. This piece is not in the dataset, but we will provide the symbolic score as well as the "unperformed" MIDI. To make things more fun, we will do an anonymous vote on moodle on which MIDI rendering is the most beautiful (voting result is not part of the assignment evaluation).
 -->

**Dataset**
https://github.com/fosfrancesco/asap-dataset.
- For each piece, the dataset contains two versions of MIDI files: 
    - unperformed MIDI corresponds to strict timing as shown in the score. 
    - performed MIDI corresponds to MIDI recording from human musicians performing the piece. In these files you will find the timing of the notes does not corresponds strictly to the symbolic metrical grid (i.e. the metrical grid is distorted).
- The dataset contains pieces from different styles, you can decide which subcollection to use.
- ~~The dataset does not contain information about loudness/dynamics in the MIDI files (in a MIDI file this is called the "velocity" attribute).~~ For this assignment, any attempts to model velocity will be considered a plus and you can do it freely according to your musical intuition. 

<!-- For this assignment we will only focus on Bach Preludes that have at least one MIDI performance. -->

## Objectives

### Task A (The timing function)

- [ ] Implement a function `timing` that maps symbolic time to performance attributes (tempo,velocity), so that one can use it to transform the "unperformed" MIDI to the "performed" MIDI. 
    - [ ] Plot this function as a tempo curve that happens in time.
    - [ ] (Optional) Plot this function as a velocity curve that happens in time.
<!-- You may model symbolic time as (Bar=2, quarterbeat=4, eighth_beat=1, ... ). Essentially you need to find a way to encode location of "leafs" on a metrical grid (which is a "tree"). -->
    
<!-- - [ ] Implement a function `performed_midi` from MIDI to MIDI where the user can input a function (like `timing`) from symbolic time to performance attributes.  -->



### Task B (Empirical findings)
- Choose one subcorpus (for example Bach Preludes) and do the following analyses:
    - [ ] What is the distribution of note onsets on metrical locations? Answer this question separately for different time signatures. At least do 4/4 and 3/4 time signatures. Illustrate your finding with figures.
    - [ ] Where in the metrical grid are expressive timing likely to happen? Support it with quantitative evidence. Illustrate your finding with figures.
- Think about another empirical question that you can verify from this data, and present your findings.
    - [ ] (Easy example) which style has the most variability in timing.
    - [ ] (Difficult example) How well can your model generalize across different styles?

<!-- 
### Task C (Main Objective)

Generate a MIDI file with expressive performance for the piece Cello Suite No. 1 (BWV 1007) – Prelude.

For this task you can choose any approaches:
- machine learning.
- musically-informed rules.
- freestyle (intuition).
 -->

## Deliverables

- A 3-4 page report (using the [ISMIR template](https://www.overleaf.com/latex/templates/paper-template-for-ismir/qctvwjqfmyzk)) containing:  
    - [ ] Abstract: A high level summary of your report.
    - [ ] Introduction: Introducing the problem of generating performance. 
    - [ ] The Model: A detailed description of your model (what are the parameters? How are the timing performance aspects determined?)
    - [ ] Results:
        - [ ] Present your findings from Task A.
        - [ ] Present your findings from Task B.
        
    - [ ] Discussion/Conclusion:
        - [ ] Relate your modeling decisions and findings to concepts mentioned in the class. 
        - [ ] What worked well and what did not (why)? 
        - [ ] What other things have you learned from this assignment?
        - [ ] What is the main take home message?
    - [ ] References (does not count towards the page limit).
    - [ ] An author contribution statement agreed among all members of the group (does not count towards the page limit).
    
<!-- - The MIDI file from Task C (with link in the footnote of the report). -->
- The code repository for this assignment (with link in the footnote of the report).

## Grading
- We will evaluate based on the quality of the report and the code.
<!-- - We will not grade based on the midi performance in task C.  -->

<!-- 
**Creative tasks:**

- [ ] **Baseline 0**: Performance with fixed velocity and timing.

- [ ] **Baseline 1**: Setting note velocity based on metrical weight.

- [ ] **Listen to the performance, pick one aspect that you want your algorthm to have. How does that translate to the mapping from symbolic score to timing and note velocity?

- [ ] **Read more about Zuckerkandl's "wave" interpretation of meter (Lecture 2). How may one design a function that output timing and dynamics based on the geometry of the wave? For example, experiment with allowing more timing flexibility on the position where the wave has less "momentum".
 
![Screenshot 2024-03-08 at 13.52.37](https://hackmd.io/_uploads/rkJ8qFdpa.png)

**Empirical questions:**

Use Music21 to load the midi file and think about the following:

- [ ] Which metrical position are accented the most? Does the distribution matches with traditional music theoretical claims. 
- [ ] Where in the metricial grid do expressive timing likely to happen? Support it with quantitative evidence.
- [ ] Think about another emperical question that you can verify from this data, and present your findings.
- [ ] Think about one way to define a MIDI performance model that can be trained from the data, and express it in mathematical forms. 


 -->
